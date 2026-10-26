---
name: second-brain-ops
description: >-
  Builds and manages a Second Brain using the CODE methodology (Capture, Organize,
  Distill, Express) and the complete PARA organization system (Projects, Areas,
  Resources, Archive), unified with the LLM Wiki OKF bundle. Use when the user
  wants to capture, organize, distill, or express knowledge; run weekly/monthly
  reviews; or manage projects, areas, and resources alongside their wiki.
type: Skill
title: Second Brain — Operations
tags: [second-brain, code, para, knowledge-management, progressive-summarization, okf]
status: stable
version: 2.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# Second Brain — Operations

An external, centralized digital repository that expands memory and intellect.
Based on CODE (Capture, Organize, Distill, Express) and PARA, **unified with the
LLM Wiki OKF bundle**: the wiki is the knowledge graph; PARA folders are the
actionability layer; `raw/` is the capture inbox. Primary front-end: **Obsidian**
or similar markdown tools.

## The unified structure

```text
<wiki-root>/
  raw/                 # CAPTURE — immutable inbox (PDFs, transcripts, notes)
  Clippings/           # CAPTURE — Obsidian Web Clipper output (optional, potential ingest)
  Agent Client/        # CAPTURE — agent client output (optional, potential ingest)
  wiki/                # ORGANIZE + DISTILL — OKF bundle (knowledge graph)
    index.md, log.md
    sources/           # one page per captured source
    entities/          # people, places, products, events
    concepts/          # topics and ideas
    synthesis/         # EXPRESS — filed answers and Intermediate Packets
    <domain>/          # domain folders
  projects/            # PARA — project registry and short-term efforts
    <project-id>/
      PROJECT.md       # project context, repository link, status, and initiatives
  areas/               # PARA — long-term responsibilities
  resources/           # PARA — topics that may be useful later
  archive/             # PARA — inactive items
```

## Project Registry And Delivery

For an existing code repository, keep one tracking note at
`projects/<project-id>/PROJECT.md`, starting from
[`templates/projects/PROJECT.md.template`](../../../templates/projects/PROJECT.md.template).
Record its objective, current status, repository path or URL, useful context,
next action, and links to related wiki pages. This is a private PARA tracking
note, not a portfolio case.

Specification work is optional. Keep initiative specifications, plans, tasks,
and verification evidence in the code repository. Respect an existing
specification system and its artifact locations; otherwise use
`docs/specs/<initiative-id>/`. The project note should link to those artifacts,
not copy their contents. Follow the human approval gates in
`spec-driven-development` before advancing to implementation.

Update the project status and next action during weekly reviews. Archive a
completed or inactive project using the existing PARA review process.

## CODE methodology

### C — Capture
Save what **resonates**, not everything.

- Curate, don't hoard: decide strategically what you consume.
- Use capture tools (read-later apps, web clippers, ebook exporters, voice
  transcription); in Obsidian, the Web Clipper lands articles into `Clippings/`
  at the wiki root, and agent outputs into `Agent Client/`.
- Anything in `raw/` is a **potential ingest source**: run `llm-wiki-ingest` to
  integrate it into the wiki.
- Ask: recurring themes, high-value accessible info, what to interconnect?

### O — Organize (PARA)
Organize by **actionability**, not by subject. Ask in order:
1. What **project** would this be useful for?
2. If none: which **area**?
3. If none: which **resource**?
4. If none: **archive** or don't save.

- Start from a clean slate: move legacy files to `archive/` with today's date.
- Batch process the inbox ~weekly (10–20 items in minutes).
- Don't overthink placement — search will find things again.
- Keep PARA **folders** for working material; keep the durable knowledge in the
  wiki bundle where it cross-links and compounds.

### D — Distill (Progressive Summarization)
Design notes for your future self; add value every time you touch them.

- **Layer 1** Original highlights / excerpts
- **Layer 2** Key excerpts (best quotes)
- **Layer 3** Summary (bullet points of main ideas)
- **Layer 4** Executive summary (2–3 sentence core insight)

Distill opportunistically, a little at a time — never perfect upfront.

### E — Express
Turn knowledge into tangible results; a factory, not a warehouse.

- Build **Intermediate Packets**: discrete, reusable units of work (a comparison,
  an analysis, a slide deck, a decision brief).
- End each session by completing one Intermediate Packet.
- File durable packets into `wiki/synthesis/` (see `llm-wiki-query`).
- Share early; nothing is ever truly "finished".

## Reviews

### Weekly
1. Process the capture inbox (batch).
2. Review active projects; update status.
3. Move completed projects to `archive/`.
4. Distill: add Progressive Summarization layers to touched notes.
5. Create one new Intermediate Packet.

### Monthly
1. Review all active projects and areas.
2. Archive completed or paused projects.
3. Clean resources; verify wiki freshness/status (see `llm-wiki-lint`).
4. Back up the vault (it is a git repo of markdown — commit or sync).

## Conventions

- All wiki pages use OKF v0.2 frontmatter: required `type`, `title`, `description`,
  `domain`, `tags`, `created`, `updated`, `okf_version`; provenance `sources`,
  `generated`, `verified`, `status`.
- **Correlation rule**: content is never isolated — link related pages via
  `[[wikilinks]]` and shared `tags` every time you touch a note.
- PARA folders keep lightweight `README.md`-style working notes that link into the
  wiki concepts they touch.

## Key principles

- Your brain is for having ideas, not storing them.
- Start with a clean slate; simple systems win.
- Add value incrementally; focus on actionability.
- Think in Intermediate Packets.
- The wiki compounds because the agent does the bookkeeping.

## Output expectations

The agent should provide:
- A capture workflow for new information (→ `raw/`)
- An actionability decision using the four PARA questions
- Progressive Summarization layers on wiki pages
- Intermediate Packets / synthesis pages
- Weekly/monthly review checklists
