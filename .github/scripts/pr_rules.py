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
  7. the description follows the pull request template: the sections marked with
     <!-- section:summary --> and <!-- section:changes --> are filled in and every line
     marked with <!-- check:... --> is ticked ([x]).

All broken rules are reported, each as a separate error. The script only reads data through the
GitHub API; it never runs code of the pull request.

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
unsigned, bad_format = [], []
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
    if not any(ITEM.match(l) for l in lines[2:] if not TRAILER.match(l)):
        problems.append("no list of changes ('- ' lines)")
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

# 7. Description
body = (pr["body"] or "").replace("\r\n", "\n")
sections = dict(re.findall(r"<!--\s*section:(\w+)\s*-->(.*?)<!--\s*/section:\1\s*-->", body, re.S))
checks = re.findall(r"^\s*[-*]\s*\[( |x|X)\].*?<!--\s*check:(\w+)\s*-->", body, re.M)
description = []
for name in ("summary", "changes"):
    if name not in sections:
        description.append(f"section '{name}' is missing")
    elif not re.sub(r"<!--.*?-->", "", sections[name], flags=re.S).strip(" \n-"):
        description.append(f"section '{name}' is empty")
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
