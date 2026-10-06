#!/usr/bin/env python3
"""Time tracking for the course repository.

Students record time on an issue in one of two ways (they may use both, but
each work session is recorded only once):

  * manually, in the "Time spent (h)" field of the issue on the project board,
  * with comments on the issue, one entry per line:  /spent 1h30m implemented FSM
    (accepted durations: 2h, 1.5h, 1,5h, 1h30m, 90m, 45min; at most 24h per entry).

The script writes the sum of the comment entries to "Time logged (h)" and the
sum of both sources to "Time total (h)". In report mode it also builds a report
(pinned issue, job summary and CSV files).

Usage:
  time_tracking.py issue <number>                        update one issue and mark its /spent comments
  time_tracking.py report --out <dir>                    update all issues and build the report

Environment:
  GITHUB_TOKEN        token with access to the organization project (Projects: read/write)
                      and the repository (Issues: read/write)
  GITHUB_REPOSITORY   owner/name
  PROJECT_NUMBER      optional; project number when more than one project is linked to the repository
  REPORT_LANG         sr or en (default en)
  RUN_URL             optional; link to the workflow run, shown in the report
"""
import csv
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
# "Estimate" is the number field that GitHub's project templates already contain (hours in this course);
# boards set up by earlier versions of this script have "Estimate (h)" instead, which is still used
FIELD_ESTIMATE = "Estimate"
FIELD_ESTIMATE_LEGACY = "Estimate (h)"
FIELD_SPENT = "Time spent (h)"
FIELD_LOGGED = "Time logged (h)"
FIELD_TOTAL = "Time total (h)"
estimate_field = FIELD_ESTIMATE  # name of the estimate field of the board, set by ensure_fields()
REPORT_LABEL = "time-report"
MAX_ENTRY_HOURS = 24
# In a public repository anyone can comment; only comments of the issue assignees and of
# repository collaborators / organization members are counted
TRUSTED_ASSOCIATIONS = ("OWNER", "MEMBER", "COLLABORATOR")

TEXT = {
    "en": {
        "title": "Time report",
        "intro": "Time spent on the issues of the project board, updated automatically every week "
                 "(and whenever the workflow is run manually). Manually entered time of an issue with "
                 "several assignees is split equally among them; time logged with `/spent` comments "
                 "is credited to the author of the comment.",
        "generated": "Generated",
        "run": "Workflow run (CSV files are attached as the `time-report` artifact)",
        "per_student": "Per student",
        "per_issue": "Per issue",
        "student": "Student", "issue": "Issue", "assignees": "Assignees", "state": "State",
        "estimate": "Estimate (h)", "manual": "Entered (h)", "logged": "Logged (h)", "total": "Total (h)",
        "unassigned": "(unassigned)", "sum": "Sum",
        "truncated": "The issue table is truncated; the complete data is in the CSV files.",
    },
    "sr": {
        "title": "Izvještaj o utrošenom vremenu",
        "intro": "Vrijeme utrošeno na zadatke sa radne ploče, automatski ažurirano svake sedmice "
                 "(i pri svakom ručnom pokretanju workflow-a). Ručno unijeto vrijeme zadatka sa više "
                 "dodijeljenih studenata dijeli se na jednake dijelove; vrijeme evidentirano komentarima "
                 "`/spent` pripisuje se autoru komentara.",
        "generated": "Generisano",
        "run": "Pokretanje workflow-a (CSV fajlovi su priloženi kao artifakt `time-report`)",
        "per_student": "Po studentu",
        "per_issue": "Po zadatku",
        "student": "Student", "issue": "Zadatak", "assignees": "Dodijeljeno", "state": "Status",
        "estimate": "Procjena (h)", "manual": "Unijeto (h)", "logged": "Komentari (h)", "total": "Ukupno (h)",
        "unassigned": "(nedodijeljeno)", "sum": "Zbir",
        "truncated": "Tabela zadataka je skraćena; kompletni podaci nalaze se u CSV fajlovima.",
    },
}

SPENT_LINE = re.compile(r"^\s*/spent\b(.*)$", re.IGNORECASE)
DURATION = re.compile(
    r"^\s*(?:(?P<h>\d+(?:[.,]\d+)?)\s*h(?:ours?|rs?)?)?\s*(?:(?P<m>\d+)\s*m(?:in(?:utes?)?)?)?(?=\s|$)(?P<rest>.*)$",
    re.IGNORECASE)


# ---------------------------------------------------------------- GitHub API

def _request(method, url, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as err:
        sys.exit(f"::error::{method} {url} failed: {err.code} {err.read().decode(errors='replace')[:500]}")


def rest(method, path, body=None):
    return _request(method, API + path, body)


def rest_pages(path):
    page, out = 1, []
    sep = "&" if "?" in path else "?"
    while True:
        chunk = rest("GET", f"{path}{sep}per_page=100&page={page}")
        out += chunk
        if len(chunk) < 100:
            return out
        page += 1


def gql(query, **variables):
    res = _request("POST", API + "/graphql", {"query": query, "variables": variables})
    if res.get("errors"):
        sys.exit("::error::GraphQL error: " + "; ".join(e.get("message", "") for e in res["errors"]))
    return res["data"]


# ---------------------------------------------------------------- project

FIELD_VALUES = """fieldValues(first: 50) { nodes { ... on ProjectV2ItemFieldNumberValue {
  number field { ... on ProjectV2FieldCommon { name } } } } }"""


def find_project(owner, name):
    number = os.environ.get("PROJECT_NUMBER", "").strip()
    if number:
        data = gql("""query($o: String!, $n: Int!) { repositoryOwner(login: $o) {
            ... on Organization { projectV2(number: $n) { id title } }
            ... on User { projectV2(number: $n) { id title } } } }""", o=owner, n=int(number))
        project = (data["repositoryOwner"] or {}).get("projectV2")
        if not project:
            sys.exit(f"::error::Project number {number} of {owner} not found (check PDS_PROJECT_NUMBER and the token).")
        return project
    data = gql("""query($o: String!, $r: String!) { repository(owner: $o, name: $r) {
        projectsV2(first: 20) { nodes { id title closed } } } }""", o=owner, r=name)
    projects = [p for p in data["repository"]["projectsV2"]["nodes"] if not p["closed"]]
    if len(projects) != 1:
        sys.exit(f"::error::Found {len(projects)} open projects linked to the repository; link exactly one "
                 "or set the repository variable PDS_PROJECT_NUMBER.")
    return projects[0]


def ensure_fields(project_id):
    global estimate_field
    data = gql("""query($p: ID!) { node(id: $p) { ... on ProjectV2 { fields(first: 50) {
        nodes { ... on ProjectV2FieldCommon { id name dataType } } } } } }""", p=project_id)
    fields = {f["name"]: f for f in data["node"]["fields"]["nodes"] if f}
    # use the board's own estimate field; create one only if the board has neither name
    estimate_field = FIELD_ESTIMATE_LEGACY if FIELD_ESTIMATE not in fields and FIELD_ESTIMATE_LEGACY in fields else FIELD_ESTIMATE
    for name in (estimate_field, FIELD_SPENT, FIELD_LOGGED, FIELD_TOTAL):
        if name not in fields:
            created = gql("""mutation($p: ID!, $n: String!) { createProjectV2Field(input: {
                projectId: $p, dataType: NUMBER, name: $n }) { projectV2Field {
                ... on ProjectV2FieldCommon { id name dataType } } } }""", p=project_id, n=name)
            fields[name] = created["createProjectV2Field"]["projectV2Field"]
            print(f"created project field '{name}'")
        elif fields[name]["dataType"] != "NUMBER":
            sys.exit(f"::error::Project field '{name}' exists but is not a Number field.")
    return {name: fields[name]["id"] for name in (estimate_field, FIELD_SPENT, FIELD_LOGGED, FIELD_TOTAL)}


def numbers(item):
    return {v["field"]["name"]: v["number"] for v in item["fieldValues"]["nodes"] if v and "field" in v}


def set_number(project_id, item_id, field_id, value):
    gql("""mutation($p: ID!, $i: ID!, $f: ID!, $v: Float!) { updateProjectV2ItemFieldValue(input: {
        projectId: $p, itemId: $i, fieldId: $f, value: { number: $v } }) { projectV2Item { id } } }""",
        p=project_id, i=item_id, f=field_id, v=float(value))


# ---------------------------------------------------------------- /spent entries

def parse_hours(text):
    """Return (hours, note) for the text after /spent, or None if the duration is invalid."""
    m = DURATION.match(text)
    if not m or (m["h"] is None and m["m"] is None):
        return None
    hours = float((m["h"] or "0").replace(",", ".")) + int(m["m"] or 0) / 60
    if not 0 < hours <= MAX_ENTRY_HOURS:
        return None
    return round(hours, 2), m["rest"].strip()


def comment_entries(comment):
    """All /spent entries of a comment: (entries, number of invalid /spent lines)."""
    entries, invalid = [], 0
    for line in (comment.get("body") or "").splitlines():
        m = SPENT_LINE.match(line)
        if not m:
            continue
        parsed = parse_hours(m.group(1))
        if parsed is None:
            invalid += 1
            continue
        entries.append({"author": comment["user"]["login"], "hours": parsed[0], "note": parsed[1],
                        "date": comment["created_at"][:10], "comment": comment["html_url"]})
    return entries, invalid


def counted(comment, assignees):
    """True if the comment comes from an assignee of the issue or from a collaborator / member."""
    if comment["user"]["type"] == "Bot":
        return False
    return comment["user"]["login"] in assignees or comment.get("author_association") in TRUSTED_ASSOCIATIONS


def issue_entries(repo, number, assignees, mark=False):
    """All /spent entries of an issue; with mark=True also sets the reactions of its /spent comments."""
    entries, me = [], (rest("GET", "/user")["login"] if mark else None)
    for comment in rest_pages(f"/repos/{repo}/issues/{number}/comments"):
        if not counted(comment, assignees):
            continue
        found, invalid = comment_entries(comment)
        entries += found
        if mark and (found or invalid):
            react(repo, me, comment["id"], invalid == 0)
    return entries


def react(repo, me, comment_id, ok):
    """Mark a comment: +1 when all its /spent lines are valid, confused otherwise (idempotent)."""
    wanted, other = ("+1", "confused") if ok else ("confused", "+1")
    mine = [r for r in rest_pages(f"/repos/{repo}/issues/comments/{comment_id}/reactions") if r["user"]["login"] == me]
    for r in mine:
        if r["content"] == other:
            rest("DELETE", f"/repos/{repo}/issues/comments/{comment_id}/reactions/{r['id']}")
    if not any(r["content"] == wanted for r in mine):
        rest("POST", f"/repos/{repo}/issues/comments/{comment_id}/reactions", {"content": wanted})


# ---------------------------------------------------------------- modes

def update_item(project_id, field_ids, item_id, values, logged):
    spent = values.get(FIELD_SPENT) or 0
    total = round(spent + logged, 2)
    if values.get(FIELD_LOGGED) != logged:
        set_number(project_id, item_id, field_ids[FIELD_LOGGED], logged)
    if values.get(FIELD_TOTAL) != total:
        set_number(project_id, item_id, field_ids[FIELD_TOTAL], total)
    return spent, total


def mode_issue(number):
    repo = os.environ["GITHUB_REPOSITORY"]
    owner, name = repo.split("/")
    data = gql("""query($o: String!, $r: String!, $n: Int!) { repository(owner: $o, name: $r) {
        issue(number: $n) { id labels(first: 20) { nodes { name } } assignees(first: 20) { nodes { login } }
        projectItems(first: 20) { nodes { id project { id } %s } } } } }""" % FIELD_VALUES,
               o=owner, r=name, n=number)
    issue = data["repository"]["issue"]
    if issue is None:
        print(f"#{number} is not an issue, nothing to do.")
        return
    if REPORT_LABEL in [l["name"] for l in issue["labels"]["nodes"]]:
        return
    project = find_project(owner, name)
    field_ids = ensure_fields(project["id"])
    item = next((i for i in issue["projectItems"]["nodes"] if i["project"]["id"] == project["id"]), None)
    if item is None:
        added = gql("""mutation($p: ID!, $c: ID!) { addProjectV2ItemById(input: { projectId: $p, contentId: $c }) {
            item { id %s } } }""" % FIELD_VALUES, p=project["id"], c=issue["id"])
        item = added["addProjectV2ItemById"]["item"]
        print(f"added issue #{number} to project '{project['title']}'")
    assignees = [a["login"] for a in issue["assignees"]["nodes"]]
    logged = round(sum(e["hours"] for e in issue_entries(repo, number, assignees, mark=True)), 2)
    spent, total = update_item(project["id"], field_ids, item["id"], numbers(item), logged)
    print(f"issue #{number}: entered {spent} h, logged {logged} h, total {total} h")


def fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".") if x else "0"


def mode_report(out_dir):
    repo = os.environ["GITHUB_REPOSITORY"]
    owner, name = repo.split("/")
    t = TEXT.get(os.environ.get("REPORT_LANG", "en"), TEXT["en"])
    project = find_project(owner, name)
    field_ids = ensure_fields(project["id"])

    items, cursor = [], None
    while True:
        data = gql("""query($p: ID!, $c: String) { node(id: $p) { ... on ProjectV2 {
            items(first: 100, after: $c) { pageInfo { hasNextPage endCursor } nodes { id
            content { __typename ... on Issue { number title state url repository { nameWithOwner }
            labels(first: 20) { nodes { name } } assignees(first: 20) { nodes { login } } } }
            %s } } } } }""" % FIELD_VALUES, p=project["id"], c=cursor)
        page = data["node"]["items"]
        items += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    issues, entries, students = [], [], {}

    def student(login):
        return students.setdefault(login, {"estimate": 0.0, "manual": 0.0, "logged": 0.0})

    for item in items:
        c = item["content"] or {}
        if c.get("__typename") != "Issue" or c["repository"]["nameWithOwner"].lower() != repo.lower():
            continue
        if REPORT_LABEL in [l["name"] for l in c["labels"]["nodes"]]:
            continue
        values = numbers(item)
        found = issue_entries(repo, c["number"], [a["login"] for a in c["assignees"]["nodes"]])
        for e in found:
            e["issue"] = c["number"]
        entries += found
        logged = round(sum(e["hours"] for e in found), 2)
        spent, total = update_item(project["id"], field_ids, item["id"], values, logged)
        estimate = values.get(estimate_field) or 0
        assignees = [a["login"] for a in c["assignees"]["nodes"]] or [t["unassigned"]]
        for login in assignees:
            student(login)["estimate"] += estimate / len(assignees)
            student(login)["manual"] += spent / len(assignees)
        for e in found:
            student(e["author"])["logged"] += e["hours"]
        issues.append({"number": c["number"], "title": c["title"], "url": c["url"], "state": c["state"].lower(),
                       "assignees": assignees, "estimate": estimate, "manual": spent, "logged": logged,
                       "total": total})

    issues.sort(key=lambda i: i["number"])
    rows = sorted(students.items())
    for _, s in rows:
        s["total"] = s["manual"] + s["logged"]

    # CSV files
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "time-per-student.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student", "estimate_h", "entered_h", "logged_h", "total_h"])
        for login, s in rows:
            w.writerow([login] + [round(s[k], 2) for k in ("estimate", "manual", "logged", "total")])
    with open(os.path.join(out_dir, "time-per-issue.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["issue", "title", "state", "assignees", "estimate_h", "entered_h", "logged_h", "total_h"])
        for i in issues:
            w.writerow([i["number"], i["title"], i["state"], " ".join(i["assignees"]),
                        i["estimate"], i["manual"], i["logged"], i["total"]])
    with open(os.path.join(out_dir, "time-entries.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "issue", "author", "hours", "note", "comment"])
        for e in sorted(entries, key=lambda e: (e["date"], e["issue"])):
            w.writerow([e["date"], e["issue"], e["author"], e["hours"], e["note"], e["comment"]])

    # Markdown report
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    head = [f"## {t['title']}", "", t["intro"], "", f"{t['generated']}: {now}"]
    if os.environ.get("RUN_URL"):
        head.append(f"{t['run']}: {os.environ['RUN_URL']}")
    sums = {k: sum(s[k] for _, s in rows) for k in ("estimate", "manual", "logged", "total")}
    student_table = ["", f"### {t['per_student']}", "",
                     f"| {t['student']} | {t['estimate']} | {t['manual']} | {t['logged']} | {t['total']} |",
                     "| :------ | ------: | ------: | ------: | ------: |"]
    student_table += [f"| {login} | {fmt(s['estimate'])} | {fmt(s['manual'])} | {fmt(s['logged'])} | **{fmt(s['total'])}** |"
                      for login, s in rows]
    student_table.append(f"| **{t['sum']}** | {fmt(sums['estimate'])} | {fmt(sums['manual'])} | "
                         f"{fmt(sums['logged'])} | **{fmt(sums['total'])}** |")
    issue_head = ["", f"### {t['per_issue']}", "",
                  f"| {t['issue']} | {t['assignees']} | {t['state']} | {t['estimate']} | {t['manual']} | {t['logged']} | {t['total']} |",
                  "| :------ | :------ | :------: | ------: | ------: | ------: | ------: |"]
    issue_rows = [f"| #{i['number']} {i['title'].replace('|', '/')} | {', '.join(i['assignees'])} | {i['state']} | "
                  f"{fmt(i['estimate'])} | {fmt(i['manual'])} | {fmt(i['logged'])} | {fmt(i['total'])} |"
                  for i in issues]
    report = "\n".join(head + student_table + issue_head + issue_rows) + "\n"
    while len(report) > 60000 and issue_rows:   # issue body limit is 65536 characters
        issue_rows = issue_rows[:-50]
        report = "\n".join(head + student_table + issue_head + issue_rows + ["", t["truncated"]]) + "\n"
    with open(os.path.join(out_dir, "time-report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(report)

    # Pinned report issue
    labels = [l["name"] for l in rest_pages(f"/repos/{repo}/labels")]
    if REPORT_LABEL not in labels:
        rest("POST", f"/repos/{repo}/labels", {"name": REPORT_LABEL, "color": "5319E7",
                                                "description": "Automatically generated time report"})
    existing = rest("GET", f"/repos/{repo}/issues?labels={REPORT_LABEL}&state=open&per_page=1")
    if existing:
        number = existing[0]["number"]
        rest("PATCH", f"/repos/{repo}/issues/{number}", {"body": report})
    else:
        created = rest("POST", f"/repos/{repo}/issues", {"title": t["title"], "body": report,
                                                        "labels": [REPORT_LABEL]})
        number = created["number"]
        gql("mutation($i: ID!) { pinIssue(input: { issueId: $i }) { issue { id } } }", i=created["node_id"])
    print(f"report: {len(issues)} issues, {len(rows)} students, {len(entries)} /spent entries -> issue #{number}")


def main(argv):
    if len(argv) == 2 and argv[0] == "issue":
        mode_issue(int(argv[1]))
    elif len(argv) == 3 and argv[0] == "report" and argv[1] == "--out":
        mode_report(argv[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
