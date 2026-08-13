---
name: llm-wiki-query
description: >-
  Answers questions from an LLM Wiki by reading index.md and relevant pages,
  synthesizing with wikilink citations, and optionally filing insights as
  synthesis pages (Express layer). Use when the user asks a question against
  their wiki, wants analysis from accumulated knowledge, or asks to file an answer.
type: Skill
title: LLM Wiki — Query
tags: [wiki, query, knowledge-base, synthesis, express, okf]
status: stable
version: 2.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# LLM Wiki — Query

## Workflow

1. Read `wiki/index.md` to locate relevant pages
2. Optionally run search: `python scripts/wiki-search.py "terms" --wiki wiki`
3. Read the identified pages (not raw sources alone)
4. Synthesize the answer with `[[wikilink]]` citations
5. Offer to file durable insights as synthesis pages

## Answer rules

- **Closed-World RAG** — search and answer strictly from indexed information in `wiki/` guided by `AGENTS.md`. Never run web/external searches unless explicitly requested by the user.
- **Wiki first** — reflect the synthesized wiki state, not raw re-derivation
- **Cite** — every non-trivial claim links to a wiki page
- **Gaps** — if the wiki lacks coverage, state the gap clearly; ask the user before searching externally or ingesting new sources
- **Contradictions** — surface any flagged on the pages you read; do not hide them
- **Provenance** — for sensitive claims, note the `status` (unverified /
  machine-confirmed / human-reviewed) from the page frontmatter

## Output formats

| Question type | Format |
|---------------|--------|
| General | Markdown prose with wikilinks |
| X vs Y | Comparison table |
| Presentation | Marp slides (`<!-- marp: true -->`) |
| Model / ERD | Mermaid `erDiagram` |
| Architecture | Mermaid `C4Context` or `graph TD` |
| Quantitative | Canvas or chart (if a charting tool is available) |

## Filing insights (Express layer)

When the answer is durable (comparison, analysis, connection) it becomes an
**Intermediate Packet** and should not vanish into chat history:

1. Ask the user to confirm filing
2. Create a page in `wiki/synthesis/` with frontmatter including
   `format: table | slides | diagram | prose` and full OKF fields
   (`generated`, `status`, `sources`, `okf_version`)
3. Correlate it: outbound `[[wikilinks]]` to the pages it draws on, shared tags
4. Update `wiki/index.md` under Synthesis
5. Append log:

```markdown
## [YYYY-MM-DD] query | <short question>
Answered; synthesis page [[page-name]] filed (or declined).
```

## Search tip

```bash
python scripts/wiki-search.py "your topic" -n 10 --wiki wiki
```

## Do not

- Perform web/external searches unless explicitly requested by the user
- Answer from `raw/` without checking wiki pages first
- Let one-off insights vanish — offer to file synthesis pages
- Ignore contradictions flagged on wiki pages — surface them in the answer
