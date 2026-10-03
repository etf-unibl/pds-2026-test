#!/usr/bin/env python3
"""Checks the submission rules of a pull request (pr-checks job of verif-tests.yml).

The rules (see docs/assignment-submission.md):
  1. the title is "Issue #<N> : <issue title>" (whitespace differences are ignored),
  2. the branch name starts with "<N>-",
  3. the author of the pull request is an assignee of issue <N>,
  4. only files in assignments/<N>/ are added, modified, deleted or renamed,
  5. every commit except merge commits is signed off by its author ("Signed-off-by: <name> <e-mail>"),
  6. every commit message has the format
         Issue #<N> : <issue title>
         <empty line>
         - change
         ...
  7. the description follows the pull request template: the section marked with
     <!-- section:summary --> is filled in and every line marked with <!-- check:... --> is
     ticked ([x]).

Before checking, the script fills the section marked with <!-- section:changes --> with the
"- " items of all commit messages (and adds the section if it is missing), so students do not
have to repeat them, removes copies of these items that GitHub puts above the template for
a single-commit pull request, and replaces <N> in the template with the issue number; these are
the only changes it makes. All broken rules are reported, each as
a separate error. The script never runs code of the pull request.

Environment: GITHUB_TOKEN, GITHUB_REPOSITORY, ISSUE, PR (pull request number)
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"
REPO = os.environ["GITHUB_REPOSITORY"]
ISSUE = os.environ["ISSUE"]
PR = os.environ["PR"]
errors = []


def get(path):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        req = urllib.request.Request(f"{API}{path}{sep}per_page=100&page={page}", headers={
            "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
            "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
        if not isinstance(data, list):
            return data
        out += data
        if len(data) < 100:
            return out
        page += 1


def patch(path, data):
    req = urllib.request.Request(f"{API}{path}", data=json.dumps(data).encode(), method="PATCH", headers={
        "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
        "Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def norm(text):
    return " ".join((text or "").split())


def ok(text):
    print(f"OK   {text}")


def fail(text):
    errors.append(text)


issue = get(f"/repos/{REPO}/issues/{ISSUE}")
pr = get(f"/repos/{REPO}/pulls/{PR}")
expected_title = f"Issue #{ISSUE} : {issue['title']}"

# 1. Title
if norm(pr["title"]) == norm(expected_title):
    ok("title")
else:
    fail(f"The pull request title must be '{expected_title}'.")

# 2. Branch name
branch = pr["head"]["ref"]
if branch.startswith(f"{ISSUE}-"):
    ok(f"branch {branch}")
else:
    fail(f"The branch name '{branch}' must start with '{ISSUE}-' (create the branch from issue #{ISSUE}).")

# 3. Assignee
author = pr["user"]["login"]
if author in [a["login"] for a in issue["assignees"]]:
    ok(f"{author} is assigned to issue #{ISSUE}")
else:
    fail(f"Issue #{ISSUE} is not assigned to {author}. Check the issue number in the title.")

# 4. Changed files
outside = []
for f in get(f"/repos/{REPO}/pulls/{PR}/files"):
    for path in (f["filename"], f.get("previous_filename")):
        if path and not path.startswith(f"assignments/{ISSUE}/"):
            outside.append(path)
if outside:
    fail(f"Only files in assignments/{ISSUE}/ may be changed. Changed outside: {', '.join(sorted(set(outside)))}")
else:
    ok(f"all changes are in assignments/{ISSUE}/")

# 5. and 6. Commits
SUBJECT = re.compile(r"^Issue #(\d+) : (.+)$")
ITEM = re.compile(r"^\s*-\s+\S")
TRAILER = re.compile(r"^[A-Za-z-]+: ")
unsigned, bad_format, items = [], [], []
for c in get(f"/repos/{REPO}/pulls/{PR}/commits"):
    if len(c["parents"]) > 1:
        continue
    sha = c["sha"][:7]
    message = c["commit"]["message"].replace("\r\n", "\n")
    a = c["commit"]["author"]
    if f"signed-off-by: {a['name']} <{a['email']}>".lower() not in message.lower():
        unsigned.append(sha)
    lines = message.split("\n")
    problems = []
    m = SUBJECT.match(lines[0])
    if not m:
        problems.append("first line is not 'Issue #<N> : <issue title>'")
    elif m.group(1) != ISSUE or norm(m.group(2)) != norm(issue["title"]):
        problems.append(f"first line must be '{expected_title}'")
    if len(lines) > 1 and lines[1].strip():
        problems.append("second line is not empty")
    commit_items = [l.strip() for l in lines[2:] if ITEM.match(l) and not TRAILER.match(l)]
    if not commit_items:
        problems.append("no list of changes ('- ' lines)")
    items += [i for i in commit_items if i not in items]
    if problems:
        bad_format.append(f"{sha} ({'; '.join(problems)})")
if unsigned:
    fail(f"Commits without 'Signed-off-by: <author name> <author email>': {', '.join(unsigned)} (use git commit -s).")
else:
    ok("all commits are signed off")
if bad_format:
    fail("Commit messages that do not follow the format: " + ", ".join(bad_format)
         + ". See docs/assignment-submission.md and docs/troubleshooting.md.")
else:
    ok("all commit messages follow the format")

# 7. Description; the changes section is filled from the commits first
body = (pr["body"] or "").replace("\r\n", "\n")
CHANGES = re.compile(r"(<!--\s*section:changes\s*-->)(.*?)(<!--\s*/section:changes\s*-->)", re.S)
generated = "\n" + "\n".join(items) + "\n" if items else "\n"
if CHANGES.search(body):
    new_body = CHANGES.sub(lambda m: m.group(1) + generated + m.group(3), body, count=1)
else:
    # A marker was deleted: remove the remaining one and put the section back under its heading
    # ("## Izmjene" / "## Changes"), or add the heading if it was deleted as well
    rest = re.sub(r"<!--\s*/?section:changes\s*-->[ \t]*\n?", "", body)
    block = "<!-- section:changes -->" + generated + "<!-- /section:changes -->"
    heading = re.search(r"^##[ \t]*(Izmjene|Changes)[ \t]*$", rest, re.M)
    if heading:
        new_body = rest[:heading.end()] + "\n" + block + rest[heading.end():]
    else:
        title = "## Izmjene" if re.search(r"^##[ \t]*Opis[ \t]*$", rest, re.M) else "## Changes"
        new_body = rest.rstrip("\n") + "\n\n" + title + "\n" + block + "\n"
# For a single commit, GitHub puts the commit description above the template; the change items
# there are copies of the generated list, so they are removed (moved into the changes section)
first = new_body.find("<!-- section:")
if first > 0 and items:
    head = [l for l in new_body[:first].split("\n") if l.strip() not in items]
    new_body = "\n".join(head).lstrip("\n") + new_body[first:]
# The template refers to the issue number as <N> (e.g. "vhdl-style <N>"); fill in the actual number
new_body = new_body.replace("<N>", ISSUE)
if new_body != body:
    patch(f"/repos/{REPO}/pulls/{PR}", {"body": new_body})
    print("OK   changes section filled from the commit messages")
    body = new_body

sections = dict(re.findall(r"<!--\s*section:(\w+)\s*-->(.*?)<!--\s*/section:\1\s*-->", body, re.S))
checks = re.findall(r"^\s*[-*]\s*\[( |x|X)\].*?<!--\s*check:(\w+)\s*-->", body, re.M)
description = []
if "summary" not in sections:
    description.append("section 'summary' (description of the solution) is missing")
elif not re.sub(r"<!--.*?-->", "", sections["summary"], flags=re.S).strip():
    description.append("section 'summary' (description of the solution) is empty")
if not checks:
    description.append("the check list is missing")
unticked = [name for state, name in checks if state == " "]
if unticked:
    description.append("not ticked: " + ", ".join(unticked))
if description:
    fail("The description must follow the pull request template (" + "; ".join(description)
         + "). Edit the description of the pull request; the checks run again automatically.")
else:
    ok("description follows the template")

for e in errors:
    print(f"::error::{e}")
sys.exit(1 if errors else 0)
