#!/usr/bin/env python3
"""One-time initialization of a course repository created from the course template.

Run by .github/workflows/init-course.yml (on the main branch) right after the
repository is created with "Use this template". It replaces the template
placeholders with the values of the new repository and removes the
template-only content (instructor setup guide, template notice in README).

Usage:
    init_course.py --branch main|assignments --path <checkout> \
                   --org <org> --repo <repo> --year <year> --course <course> [--instructor <user>]
"""
import argparse
import pathlib
import re
import shutil
import sys

# Placeholders used in the student documentation (Serbian and English templates)
ORG_PLACEHOLDERS = ("<organizacija>", "<org>")
REPO_PLACEHOLDERS = ("<repozitorijum>", "<repo>")
# README title placeholders
COURSE_PLACEHOLDERS = ("<Naziv kursa>", "<Course name>")

TEMPLATE_BLOCK = re.compile(r"<!-- template:begin -->.*?<!-- template:end -->\n*", re.S)
TITLE_TODO = re.compile(r"^<!-- TODO \((nastavnik|instructor)\): (naziv kursa i godina izvođenja|course name and year) -->\n", re.M)
# Rows of the placeholder table in getting-started.md that no longer apply
PLACEHOLDER_ROW = re.compile(r"^\| `(" + "|".join(re.escape(p) for p in ORG_PLACEHOLDERS + REPO_PLACEHOLDERS) + r")` \|.*\n", re.M)


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


def set_license_year(root, year):
    lic = root / "LICENSE"
    if lic.exists():
        write(lic, read(lic).replace("<year>", year))


def init_main(root, args):
    shutil.rmtree(root / "docs" / "instructor", ignore_errors=True)
    set_license_year(root, args.year)
    for md in [root / "README.md", *sorted((root / "docs").rglob("*.md"))]:
        if not md.exists():
            continue
        text = read(md)
        new = PLACEHOLDER_ROW.sub("", text)
        for p in ORG_PLACEHOLDERS:
            new = new.replace(p, args.org)
        for p in REPO_PLACEHOLDERS:
            new = new.replace(p, args.repo)
        if md.name == "README.md" and md.parent == root:
            new = TEMPLATE_BLOCK.sub("", new)
            new = TITLE_TODO.sub("", new)
            for p in COURSE_PLACEHOLDERS:
                new = new.replace(p, args.course)
        if new != text:
            write(md, new)
            print(f"updated {md.relative_to(root)}")
    # the initialization script is not needed any more (this also turns the workflow into a no-op)
    shutil.rmtree(root / ".github" / "template", ignore_errors=True)


def init_assignments(root, args):
    set_license_year(root, args.year)
    doxyfile = root / "assignments" / "Doxyfile"
    if doxyfile.exists():
        text = read(doxyfile)
        write(doxyfile, re.sub(r"^PROJECT_NAME\s*=.*$", f'PROJECT_NAME           = "{args.course}"', text, flags=re.M))
        print("updated assignments/Doxyfile")
    codeowners = root / ".github" / "CODEOWNERS"
    if codeowners.exists() and args.instructor:
        write(codeowners, read(codeowners).replace("<instructor>", args.instructor))
        print(f"updated .github/CODEOWNERS (@{args.instructor})")


def leftovers(root):
    found = []
    patterns = ORG_PLACEHOLDERS + REPO_PLACEHOLDERS + COURSE_PLACEHOLDERS + ("<year>", "@<instructor>")
    for f in root.rglob("*"):
        if f.is_file() and ".git" not in f.parts and f.suffix in (".md", "", ".txt"):
            text = read(f)
            found += [f"{f.relative_to(root)}: {p}" for p in patterns if p in text]
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", choices=["main", "assignments"], required=True)
    ap.add_argument("--path", required=True)
    ap.add_argument("--org", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--year", required=True)
    ap.add_argument("--course", required=True)
    ap.add_argument("--instructor", default="", help="GitHub username for CODEOWNERS (assignments branch)")
    args = ap.parse_args()
    root = pathlib.Path(args.path)
    (init_main if args.branch == "main" else init_assignments)(root, args)
    rest = leftovers(root)
    for item in rest:
        print(f"::warning::placeholder left: {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
