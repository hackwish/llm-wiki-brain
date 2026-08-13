---
name: llm-wiki-ingest
description: >-
  Ingests a source document into an LLM Wiki: reads raw/, Clippings/ and Agent
  Client/ at the wiki root, writes a source summary, updates entity and concept pages with
  cross-links and tags, and updates index and log. Applies OKF provenance and
  progressive summarization (Distill). Use when the user says ingest, add source,
  process document, or drops a file into raw/.
type: Skill
title: LLM Wiki — Ingest
tags: [wiki, ingest, knowledge-base, source-processing, distillation, okf]
status: stable
version: 2.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# LLM Wiki — Ingest

## Prerequisites

- The wiki has `AGENTS.md` (or `CLAUDE.md`) and `wiki/index.md`
- Source file is in `raw/`, `Clippings/`, or `Agent Client/` (all immutable —
  never edit source files). Those folders are **potential ingest sources**.

## Workflow

Copy this checklist and track progress:

```
Ingest Progress:
- [ ] Read source fully (images noted for separate viewing)
- [ ] Discuss key takeaways with user — confirm emphasis
- [ ] Create wiki/sources/YYYY-MM-DD-slug.md
- [ ] Update or create entity/concept pages (5–15 pages typical)
- [ ] Correlate touched pages: add [[wikilinks]] + shared tags
- [ ] Update wiki/index.md
- [ ] Append wiki/log.md
```

### Step 1 — Read

Read `<source-path>` (`raw/`, `Clippings/`, or `Agent Client/`) completely. For
images: read the text first, then view referenced images in `raw/assets/` (or the
source's asset folder) for extra context.

### Step 2 — Align with user

Summarize 3–5 key takeaways. Ask what to emphasize before writing. For batch
ingests, note reduced discussion.

### Step 3 — Source page

Create `wiki/sources/YYYY-MM-DD-<slug>.md`:

```yaml
---
title: "Source Title"
type: source
domain: <primary-domain> | cross-domain
tags: [source, <topic-tags>]
sources:
  - id: <source-path>
    title: "Source Title"
    author: "<author if known>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
generated:
  by: agent
  at: YYYY-MM-DD
status: draft
okf_version: "0.2"
---
```

Include: a progressive summary (see below), key claims, entities/concepts
introduced, and links to updated pages.

**Progressive Summarization (Distill layer):** keep the source page layered so a
future self can read it at any depth:

```markdown
## Layer 1: Original
{key highlights or excerpts}

## Layer 2: Key excerpts
> {best quotes}

## Layer 3: Summary
- {main point 1}
- {main point 2}
- {main point 3}

## Layer 4: Executive summary
{2–3 sentences: what this is about and why it matters}
```

### Step 4 — Entity & concept pages

For each significant entity or concept:

- **Exists** → update; add `[[wikilinks]]`; note contradictions under
  `## Contradictions & Open Questions`
- **New** → create in the correct domain subfolder with full frontmatter

Prefer updating existing pages over creating duplicates.

### Step 5 — Correlate (non-negotiable)

Every page touched by this ingest must be correlated with the rest of the
repository-managed content:

- Add outbound `[[wikilinks]]` from each touched page to related pages (source,
  entities, concepts, synthesis).
- Add shared `tags` so pages surface together.
- Nothing may be left isolated.

### Step 6 — Index & log

**index.md** — add a one-line entry per new/updated page under the right section.

**log.md** — append:

```markdown
## [YYYY-MM-DD] ingest | Source Title
Summary of what was ingested and which pages were created or updated.
```

## Rules

- Never modify `raw/`, `Clippings/`, or `Agent Client/`
- Every new page needs full YAML frontmatter (OKF v0.2)
- Every page needs outbound `[[wikilinks]]` (except `log.md`)
- Flag contradictions explicitly — do not silently overwrite
- Correlate all touched pages via wikilinks and tags

## Optional validation

```bash
python scripts/wiki-lint.py --wiki wiki
```

## Reference

Follow the wiki's own `AGENTS.md` for domain names, page types, and ontology
specifics. OKF field guidance: `Context/Open Knowledge Format (OKF).md`.
