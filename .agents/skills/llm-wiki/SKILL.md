---
name: llm-wiki
description: >-
  Umbrella coordinator for a persistent, compounding LLM Wiki + Second Brain.
  Maps the full workflow (scaffold, capture, ingest, query, lint, express),
  applies shared OKF + CODE/PARA conventions, and delegates to the operational
  sub-skills. Use when the user references this toolkit, wants a knowledge base,
  or asks to start, ingest, query, lint, or maintain an LLM Wiki.
type: Skill
title: LLM Wiki — Coordinator
tags: [wiki, knowledge-base, llm-wiki, second-brain, okf, coordinator]
status: stable
version: 2.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# LLM Wiki — Coordinator

Build and maintain a **persistent, compounding knowledge base** instead of
re-deriving answers from raw documents on every query. The wiki is a directory of
cross-linked markdown pages (an OKF bundle) that the agent owns and keeps current;
raw sources are immutable. This is a **Second Brain**: knowledge accumulates,
compounds, and gets expressed as Intermediate Packets.

## When to use

Use this skill (or the sub-skill it points to) when the user wants to:

- create / bootstrap a knowledge base (→ `llm-wiki-scaffold`)
- ingest a source, add notes, process a document (→ `llm-wiki-ingest`)
- ask a question, get analysis, or save an insight (→ `llm-wiki-query`)
- health-check, audit, or maintain quality (→ `llm-wiki-lint`)
- run Second Brain workflows: capture, organize (PARA), distill, express (→ `second-brain-ops`)
- manage a company brain: definitions, rules, decisions, tribal knowledge (→ `company-brain`)
- register and track an existing codebase as a Second Brain project (→ `second-brain-ops`)
- specify or plan a significant change in an existing codebase (→ opt-in `spec-driven-development`)
- prepare approved project cases for a portfolio export (→ `scripts/portfolio-export.py`)

Trigger phrases: "llm wiki", "knowledge base", "persistent wiki", "second brain",
"ingest this", "health-check the wiki", "guardar este insight en la wiki".
For project workflows, phrases include "track this repository", "write a spec",
"plan this change", and "publish this project to my portfolio".

## Three layers

1. **`raw/`** — immutable source of truth. `Clippings/` and `Agent Client/` may
   appear at the wiki root as **potential ingest sources**. The agent never edits
   them.
2. **`wiki/`** — the agent-owned OKF bundle: `index.md`, `log.md`, `sources/`,
   `entities/`, `concepts/`, `synthesis/`, domain folders.
3. **Schema** — the wiki's `AGENTS.md` (or `CLAUDE.md`), copied from the template
   in this toolkit. Co-evolve it with the user.

The primary front-end is **Obsidian** (or similar: Logseq, Anytype, VS Code).
Obsidian is the IDE; the agent is the writer; the wiki is the codebase.

## Workflow map

| Operation | Sub-skill | Output |
|-----------|-----------|--------|
| Bootstrap | `llm-wiki-scaffold` | new wiki / second brain / company brain + schema + index/log |
| Capture | `second-brain-ops` | sources in `raw/`, inbox-style working notes |
| Ingest | `llm-wiki-ingest` | source page, entity/concept updates, index, log |
| Query | `llm-wiki-query` | synthesized answer with `[[wikilink]]` citations |
| Express | `llm-wiki-query` / `second-brain-ops` | synthesis pages, Intermediate Packets |
| Lint / Review | `llm-wiki-lint` | contradiction/stale/orphan/gap report, weekly review |
| Company Brain | `company-brain` | governed definitions/rules/decisions/tribal, serve + trace |
| Project registry | `second-brain-ops` | project note at `projects/<project-id>/PROJECT.md` |
| Project specification | `spec-driven-development` | opt-in, approved specification and plan for an existing codebase |
| Portfolio export | `scripts/portfolio-export.py` | static page from explicitly approved project notes |

Project SDD is optional and does not scaffold applications or choose frameworks.
Keep initiative artifacts with the codebase, use its existing specification
system when present, and retain human approval gates. Portfolio publication is a
separate, explicit opt-in; never treat a project registry entry as public by
default.

## Shared OKF conventions

Every page uses YAML frontmatter (OKF v0.2):

- Required: `type`, `title`, `description`, `domain`, `tags`, `created`, `updated`, `okf_version`
- Provenance: `sources`, `generated: {by, at}`, `verified: [{by, at}]`, `status`,
  `usage_window`
- Trust tiers: no `verified` ⇒ **unverified**; non-human only ⇒ **machine-confirmed**;
  `human:<id>` ⇒ **human-reviewed**

## Non-negotiable rules

- **Closed-World RAG rule**: regardless of the preset chosen, all agent searches and answers within the LLM Wiki/vault are strictly based on indexed information in `wiki/` guided by `AGENTS.md`. External/web searches are performed ONLY if explicitly requested by the user.
- Never modify anything in `raw/`, `Clippings/`, or `Agent Client/`.
- **Correlation rule**: every ingest correlates every touched page via `[[wikilinks]]`
  and shared `tags` — nothing is left isolated.
- Flag contradictions explicitly; never silently overwrite.
- Answers compound: file durable insights back into `wiki/synthesis/`.
- Always read `wiki/index.md` first when locating pages.

## Delegation

When the task matches an operational sub-skill, load that skill and follow it.
Use this coordinator to decide *which* sub-skill applies when ambiguous.

## Reference

- Concept paper: `Context/llm-wiki.md`
- OKF spec: `Context/Open Knowledge Format (OKF).md`
- Second Brain / CODE / PARA: `Context/Building a Second Brain The Definitive Introductory Guide.md`
- Schema template: `templates/schema/AGENTS.md.template`
- Scaffold tool: `scripts/create-wiki.sh`
- Helpers: `scripts/wiki-lint.py`, `scripts/wiki-search.py`
