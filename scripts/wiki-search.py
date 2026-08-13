#!/usr/bin/env python3
"""wiki-search.py — Simple full-text search over an LLM Wiki (OKF bundle).

Searches the wiki/ bundle (bodies + frontmatter) and ranks results by a simple
term-frequency score. Designed for small-to-medium wikis where the index file is
not enough and embedding-based RAG is overkill.

Usage:
  python3 scripts/wiki-search.py "terms to find" [-n 10] [--wiki path/to/wiki]

Exit code: 0 ok, 1 no results, 2 usage/IO error.
"""

import argparse
import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9\-_']*")


def tokenize(text):
    return [t for t in TOKEN_RE.findall(text.lower()) if len(t) > 1]


def score(text, terms, fields_boost):
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    total = len(tokens)
    s = 0.0
    for term in terms:
        s += counts.get(term, 0)
    # normalize by size so short pages aren't buried by long ones
    return (s / total) * (1000 * fields_boost)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="search terms")
    ap.add_argument("-n", type=int, default=10, help="max results (default 10)")
    ap.add_argument("--wiki", default="wiki", help="path to wiki bundle (default: wiki)")
    args = ap.parse_args()

    terms = tokenize(args.query)
    if not terms:
        print("error: empty query", file=sys.stderr)
        return 2

    wiki = Path(args.wiki)
    if not wiki.is_dir():
        print(f"error: wiki bundle not found: {wiki}", file=sys.stderr)
        return 2

    files = sorted(p for p in wiki.rglob("*.md") if p.name != "README.md")
    results = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = p.relative_to(wiki).as_posix()
        # title/headings carry more weight
        headings = " ".join(re.findall(r"^#{1,3} .*$", text, flags=re.M))
        title_boost = 3.0 if re.match(r"^# ", text, flags=re.M) else 1.5
        s = (
            score(text, terms, 1.0)
            + score(headings, terms, 4.0)
            + score(rel, terms, 5.0 * title_boost)
        )
        if s > 0:
            results.append((s, rel))

    results.sort(key=lambda r: -r[0])
    if not results:
        print(f"No matches for '{args.query}'.")
        return 1

    print(f"Top {min(len(results), args.n)} of {len(results)} result(s) for '{args.query}':")
    for s, rel in results[: args.n]:
        print(f"  {s:6.1f}  wiki/{rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
