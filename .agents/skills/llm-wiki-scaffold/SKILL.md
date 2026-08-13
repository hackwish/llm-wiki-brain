---
name: llm-wiki-scaffold
description: >-
  Scaffolds a new LLM Wiki, Second Brain, or Company Brain with schema, folder structure, and bootstrap pages
  from a topic, preset, or custom domain config. Creates the OKF bundle (raw/,
  wiki/) and optional PARA actionability folders (projects, areas, resources, archive) depending on the selected kit.
  Use when the user wants to create, start, instantiate, or bootstrap a knowledge base, research wiki, second brain, or company brain.
type: Skill
title: LLM Wiki — Scaffold
tags: [wiki, knowledge-base, scaffolding, bootstrap, second-brain, company-brain, para]
status: stable
version: 2.1.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# LLM Wiki — Scaffold

## When to use

- User wants a **new** knowledge base / LLM Wiki / Second Brain / Company Brain (not ingest/query/lint on an existing one)
- User gives a topic, preset name, or custom domains
- User references this toolkit or the `llm-wiki` pattern

## Toolkits & Presets

The toolkit supports four distinct toolkit modes (`kit`):

| Toolkit (`kit`) | Presets | Created Structure | Schema Focus |
|-----------------|---------|-------------------|--------------|
| **`blended`** (default) | `general`, `research`, `book`, `business` | `raw/` + `wiki/` + PARA (`projects/`, `areas/`, `resources/`, `archive/`) | Full combo: OKF + Second Brain (CODE+PARA) |
| **`llm-wiki`** (pure) | `llm-wiki` | `raw/` + `wiki/` | Pure Karpathy pattern: raw sources + compounding wiki (no PARA) |
| **`second-brain`** (pure PKM) | `second-brain` | `raw/` + `wiki/` + PARA | PKM methodology: CODE + PARA + reviews |
| **`company-brain`** (pure org) | `company-brain` | `raw/` + `wiki/` + `wiki/lineage.md` | Governed business knowledge: definitions, rules, decisions, processes, tribal knowledge |

## Quick start

1. **Clarify intent** (skip if already clear):
   - Topic or title
   - Preset: `general` | `llm-wiki` | `second-brain` | `company-brain` | `research` | `book` | `business`
   - Output path

2. **Scaffold with the script** (preferred):

```bash
# Pure LLM Wiki (no PARA folders)
./scripts/create-wiki.sh --output /path/to/pure-wiki --preset llm-wiki --title "Quantum ML Survey"

# Pure Second Brain (with CODE + PARA)
./scripts/create-wiki.sh -o ../my-brain --preset second-brain

# Company Brain (governed organizational knowledge)
./scripts/create-wiki.sh -o ../company-brain --preset company-brain

# Blended general purpose (default)
./scripts/create-wiki.sh -o ../my-wiki -p general

# List available presets
./scripts/create-wiki.sh --list-presets
```

3. **Custom domains** — when presets don't fit, design domains with the user, then
   write JSON from `templates/config/custom-config.example.json` and run:

```bash
./scripts/create-wiki.sh -o ../my-wiki --config /path/to/config.json
```

The script creates: `raw/` (immutable), `wiki/` (OKF bundle with `index.md`,
`log.md`, `sources/`, `entities/`, `concepts/`, `synthesis/`, one folder per domain),
and PARA folders (`projects/`, `areas/`, `resources/`, `archive/`) if the kit uses PARA.
Optional folders like `Clippings/` and `Agent Client/` may appear during use as potential ingest sources.

## Agent-assisted domain design

If the user gives only a free-text topic, propose 2–4 domains before scaffolding:

| Topic flavor | Preset / Kit | Suggested domains |
|--------------|--------------|-------------------|
| Pure research wiki | `llm-wiki` | topics, people, learnings |
| Deep research | `research` (blended) | literature, theory, applications |
| Book reading | `book` (blended) | characters, world, themes |
| Business / team | `business` (blended) | customers, market, projects, team |
| Company brain | `company-brain` | definitions, rules, decisions, processes |
| Second brain / PKM | `second-brain` | notes, summaries |
| General purpose | `general` (blended) | topics, people, projects, learnings |

Confirm domains with the user, then use a close preset or a custom config.

## After scaffolding

Tell the user:

1. Open the wiki folder in **Obsidian** (browse) and in their agent IDE (maintain).
2. Drop sources into `raw/` (or root `Clippings/` / `Agent Client/` if used) — the primary front-end is Obsidian or a similar markdown tool.
3. Use the **ingest**, **query**, **lint**, **second brain**, or **company brain** workflows (sibling skills).
4. Co-evolve the wiki's `AGENTS.md` as conventions mature.

## Customization pass (optional)

After script scaffolding, refine the generated `AGENTS.md`:

- Sharpen domain ontologies with domain-specific entity types
- Add output formats the user cares about (Marp slides, Mermaid, canvas)
- Document ingest style (supervised vs batch)
- Configure Obsidian settings (attachment folder → `raw/assets/`, wikilink style)

## Reference

- Schema template: `templates/schema/AGENTS.md.template`
- Presets: `templates/presets/`
- Custom config example: `templates/config/custom-config.example.json`
- Concept: `Context/llm-wiki.md`

## Do not

- Modify files in an existing wiki's `raw/` during creation
- Skip `wiki/index.md` and `wiki/log.md` — the script creates them
- Invent a different directory layout unless the user explicitly requests it
