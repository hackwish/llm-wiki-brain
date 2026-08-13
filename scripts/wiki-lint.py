#!/usr/bin/env python3
"""wiki-lint.py — Health-check an LLM Wiki (OKF bundle).

Checks the wiki/ bundle for:
  - missing frontmatter and missing required/recommended OKF fields
  - missing outbound wikilinks and unresolved wikilink targets
  - orphan pages (no inbound links, excluding overview/index/log)
  - pages missing from index.md
  - freshness (updated older than created or older than a threshold)

Usage:
  python3 scripts/wiki-lint.py [-v] [--wiki path/to/wiki]

Exit code: 0 = no issues, 1 = issues found, 2 = usage/IO error.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["title", "type", "domain", "created", "updated"]
OKF_RECOMMENDED = ["generated", "status", "sources"]
INDEX_LOG_FIELDS = ["title", "created", "updated"]
NON_OVERVIEW_TYPES = {"index", "log", "overview"}
WIKILINK_RE = re.compile(r"\[\[([^#|\]]+)")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fm = text[4:end]
    data = {}
    key = None
    for line in fm.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if key:
                data[key] = (data.get(key) or "") + " " + line.strip()
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") or val.startswith("{") or val.startswith(">"):
                data[key] = val
            elif val.startswith('"'):
                data[key] = val.strip('"')
            elif val.startswith("'"):
                data[key] = val.strip("'")
            else:
                data[key] = val
    return data, text


def wikilink_targets(text):
    targets = set()
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).strip()
        if target:
            targets.add(target)
    return targets


def slugify(name):
    return name.strip().replace(" ", "-").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="wiki", help="path to wiki bundle (default: wiki)")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--max-age-days", type=int, default=180, help="stale threshold in days")
    args = ap.parse_args()

    wiki = Path(args.wiki)
    if not wiki.is_dir():
        print(f"error: wiki bundle not found: {wiki}", file=sys.stderr)
        return 2

    md_files = sorted(p for p in wiki.rglob("*.md") if p.name != "README.md")
    pages = {}
    for p in md_files:
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        pages[p] = {"fm": fm, "body": body}

    issues = {"contradiction": [], "stale": [], "orphan": [], "gap": []}
    today = dt.date.today()

    # --- frontmatter / OKF checks ---
    index_page = wiki / "index.md"
    index_okf_declared = False
    for p, info in pages.items():
        rel = p.relative_to(wiki).as_posix()
        fm = info["fm"]
        if fm is None:
            issues["gap"].append(f"missing frontmatter: {rel}")
            continue
        if p.name in {"index.md", "log.md"}:
            required = INDEX_LOG_FIELDS
        else:
            required = REQUIRED_FIELDS
        for field in required:
            if not fm.get(field):
                issues["gap"].append(f"missing required frontmatter '{field}': {rel}")
        for field in OKF_RECOMMENDED:
            if not fm.get(field):
                if args.verbose:
                    issues["gap"].append(f"missing OKF recommended '{field}': {rel}")
        if "okf_version" not in fm and rel != "index.md":
            if args.verbose:
                issues["gap"].append(f"missing 'okf_version' declaration: {rel}")
        if p.name == "index.md" and fm.get("okf_version"):
            index_okf_declared = True

    if not index_okf_declared:
        issues["gap"].append("index.md missing 'okf_version' declaration")

    # --- freshness ---
    for p, info in pages.items():
        rel = p.relative_to(wiki).as_posix()
        fm = info["fm"]
        if not fm:
            continue
        try:
            created = dt.date.fromisoformat(fm.get("created", ""))
            updated = dt.date.fromisoformat(fm.get("updated", fm.get("created", "")))
        except ValueError:
            issues["gap"].append(f"invalid date fields (created/updated): {rel}")
            continue
        if fm.get("status") == "stale":
            issues["stale"].append(f"marked stale: {rel}")
        elif created and updated and updated < created:
            issues["stale"].append(f"updated ({updated}) older than created ({created}): {rel}")
        elif today - updated > dt.timedelta(days=args.max_age_days):
            if args.verbose:
                issues["stale"].append(f"not updated in {args.max_age_days}+ days: {rel}")

    # --- wikilinks ---
    canonical = {}
    for p in pages:
        stem = slugify(p.stem)
        canonical.setdefault(stem, p)
    for p, info in pages.items():
        rel = p.relative_to(wiki).as_posix()
        targets = wikilink_targets(info["body"])
        if not targets and p.name not in {"index.md", "log.md"}:
            issues["gap"].append(f"no outbound wikilinks: {rel}")
        for t in targets:
            slug = slugify(Path(t).stem)
            if slug not in canonical:
                issues["gap"].append(f"unresolved wikilink '[[{t}]]' from {rel}")

    # --- orphans (no inbound links) ---
    inlinks = {p: 0 for p in pages}
    for info in pages.values():
        for t in wikilink_targets(info["body"]):
            slug = slugify(Path(t).stem)
            if slug in canonical:
                inlinks[canonical[slug]] += 1
    for p, count in inlinks.items():
        rel = p.relative_to(wiki).as_posix()
        if count == 0 and p.name not in {"index.md", "log.md"}:
            issues["orphan"].append(f"no inbound links: {rel}")

    # --- index gaps ---
    if index_page in pages:
        index_text = pages[index_page]["body"] + pages[index_page]["fm"].get("title", "")
        for p in pages:
            if p == index_page or p.name in {"log.md"}:
                continue
            rel = p.relative_to(wiki).as_posix()
            slug = p.stem.lower()
            if slug not in index_text.lower():
                issues["gap"].append(f"page not in index.md: {rel}")

    severity_order = ["contradiction", "stale", "orphan", "gap"]
    total = 0
    for sev in severity_order:
        lst = issues[sev]
        total += len(lst)
        for item in lst:
            print(f"[{sev}] {item}")

    summary = ", ".join(f"{len(issues[s])} {s}" for s in severity_order)
    print(f"\n{total} issue(s) found ({summary}).")
    if total:
        print("Fix patterns: orphans -> add inbound wikilinks + index entry; missing pages -> create stub; stale -> update claim and note source; gaps -> add index entry / frontmatter / links.")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
