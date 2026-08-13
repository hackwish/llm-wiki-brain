---
name: llm-wiki-lint
description: >-
  Health-checks an LLM Wiki for contradictions, stale claims, orphan pages,
  missing cross-references, index gaps, and OKF trust/freshness issues. Use when
  the user asks to lint, health-check, audit, or maintain wiki quality, or runs a
  weekly/monthly Second Brain review.
type: Skill
title: LLM Wiki — Lint
tags: [wiki, lint, health-check, quality, audit, okf, review]
status: stable
version: 2.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# LLM Wiki — Lint

## Workflow

1. Run the automated scan:

```bash
python scripts/wiki-lint.py --wiki wiki -v
```

2. Manual review for issues automation misses:
   - **Contradictions** — conflicting claims across pages
   - **Stale** — claims superseded by newer sources or pages older than a threshold
   - **Orphans** — pages with no inbound links
   - **Gaps** — concepts mentioned but lacking pages; missing cross-refs; isolated pages
   - **OKF trust/freshness** — pages missing `verified`/`status`, or marked `stale`

3. Report findings by severity:

```
contradiction > stale > orphan > gap
```

4. Suggest: new sources, web searches, pages to create
5. Offer to fix issues directly

## Automated checks (wiki-lint.py)

| Check | Severity |
|-------|----------|
| Missing frontmatter | gap |
| Missing required frontmatter (`title`, `type`, `domain`, `created`, `updated`) | gap |
| Missing OKF recommended fields (`generated`, `status`, `sources`) | gap |
| `wiki/index.md` missing `okf_version` declaration | gap |
| No outbound wikilinks | gap |
| Unresolved wikilink targets | gap |
| No inbound links (non-overview) | orphan |
| Page not in index.md | gap |
| `updated` older than `created`, or stale by max age | stale |
| Page marked `status: stale` | stale |

## Manual checks

- Read `## Contradictions & Open Questions` sections — are any unresolved?
- Compare source dates vs page `updated` fields
- Review graph hubs vs isolated clusters (Obsidian graph view)
- Scan index for domains with only `_overview.md`
- Confirm the **correlation rule** held on recent ingests: no page left isolated

## After lint

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | Health check
<N> issues found (X contradiction, Y stale, Z orphan, W gap). <resolved or pending>.
```

## Fix patterns

| Issue | Fix |
|-------|-----|
| Orphan page | Add wikilinks from related pages and an index entry |
| Missing page | Create stub with frontmatter and links |
| Contradiction | Update both pages; keep the contradiction section until resolved |
| Stale claim | Update page; note what changed and which source superseded it |
| Index gap | Add a one-line entry under the correct section |
| Unverified / stale status | Set `status` and add `verified` per OKF trust tiers |

## Periodic cadence

Suggest lint after every 5–10 ingests, when the user feels answers getting noisy,
or as part of the weekly/monthly Second Brain review (`second-brain-ops`).
