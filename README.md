# LLM Wiki Toolkit

A core toolkit for building and maintaining persistent **LLM Wikis, Second Brains, and Company Brains**: cross-linked markdown knowledge bases that **compound over time** instead of re-deriving answers from raw documents on every query.

The core pattern: an LLM reads raw sources, integrates them into a structured, interlinked wiki, keeps it current, and answers queries as a closed-world RAG system. Every page carries provenance and trust metadata (OKF).

Four toolkit modes:

| Toolkit Mode (`kit`) | Presets | Created Folders | Focus & Schema |
|----------------------|---------|-----------------|----------------|
| **`llm-wiki`** (pure) | `llm-wiki` | `raw/` + `wiki/` | Pure Karpathy pattern: raw sources + compounding knowledge graph (no PARA) |
| **`second-brain`** (pure PKM) | `second-brain` | `raw/` + `wiki/` + PARA | PKM methodology: CODE + PARA actionability (`projects/`, `areas/`, `resources/`, `archive/`) + reviews |
| **`company-brain`** (pure org) | `company-brain` | `raw/` + `wiki/` + `wiki/lineage.md` | Governed organizational knowledge: definitions, rules, decisions, processes, tribal knowledge |
| **`blended`** (default) | `general`, `research`, `book`, `business` | `raw/` + `wiki/` + PARA | Combined OKF knowledge bundle + PARA actionability folders |

## Key concepts

- **Closed-World RAG** — regardless of the preset chosen, agent searches and queries within the wiki/vault are strictly grounded in indexed information in `wiki/` guided by `AGENTS.md`. External/web searches are performed ONLY if explicitly requested by the user.
- **Three layers** — `raw/` (immutable source of truth) → `wiki/` (agent-owned OKF bundle) → schema (`AGENTS.md`, co-evolved).
- **Capture inbox** — sources land in `raw/`; optional folders like `Clippings/` (Obsidian Web Clipper) and `Agent Client/` may appear at the wiki root as **potential ingest sources** when used.
- **Correlation rule** — every ingest correlates every touched page via `[[wikilinks]]` and shared `tags`. Nothing is left isolated.
- **Obsidian-first** — the primary front-end is **Obsidian** (or similar: Logseq, Anytype, VS Code). Obsidian is the IDE for browsing the graph; the agent is the writer; the wiki is the codebase.
- **Trust tiers** — no `verified` ⇒ unverified; non-human ⇒ machine-confirmed; `human:<id>` ⇒ human-reviewed.
- **Compounding** — durable answers and insights are filed back into `wiki/synthesis/` as Intermediate Packets.

## Quickstart

Scaffold a knowledge base using any preset:

```bash
# Pure LLM Wiki (no PARA)
./scripts/create-wiki.sh -o ../my-pure-wiki --preset llm-wiki --title "AI Safety Survey"

# Second Brain (CODE + PARA)
./scripts/create-wiki.sh -o ../my-brain --preset second-brain

# Company Brain (Governed business knowledge)
./scripts/create-wiki.sh -o ../my-company --preset company-brain

# Blended general purpose (default)
./scripts/create-wiki.sh -o ../my-wiki --preset general

# List all available presets
./scripts/create-wiki.sh --list-presets
```

Scaffolded output structure (e.g. `blended` kit):

```text
my-wiki/
  AGENTS.md                 schema (rendered from templates/schema/AGENTS.md.template)
  raw/                      immutable sources
  wiki/                     OKF bundle
    index.md, log.md
    sources/ entities/ concepts/ synthesis/ <domains>/
  projects/ areas/ resources/ archive/     PARA structure (for blended and second-brain kits)
```

Then:

```bash
# Drop sources into raw/ (or root Clippings/ or Agent Client/ if used) and run the ingest workflow
# Health-check the wiki
python3 scripts/wiki-lint.py --wiki ../my-wiki/wiki -v

# Search it
python3 scripts/wiki-search.py "your topic" --wiki ../my-wiki/wiki
```

## Presets (`blended` kit)

Los presets `general`, `research`, `book` y `business` comparten el modo combinado (`blended` kit: OKF `raw/` + `wiki/` más carpetas PARA). Se diferencian en su enfoque y en los dominios (`wiki/<domain>/`) que estructuran:

| Preset | Foco de Ingesta | Dominios (`wiki/<domain>/`) |
| :--- | :--- | :--- |
| **`general`** | Aprendizaje general, personas y proyectos cotidianos | `topics`, `people`, `projects`, `learnings` |
| **`research`** | Análisis de literatura académica, teoría y experimentos | `literature`, `theory`, `applications` |
| **`book`** | Acompañante de lectura, ficción, análisis narrativo y lore | `characters`, `world`, `themes` |
| **`business`** | Información de clientes, mercado, entregables y equipo | `customers`, `market`, `projects`, `team` |

## Uso diario: Generador vs Carpeta Core

Este repositorio puede ser utilizado de dos formas principales según tu flujo de trabajo:

1. **Como Generador / Fábrica (Uso Recomendado):**
   Mantiene este repo independiente para instanciar, auditar y actualizar otras LLM-Wikis/Second-Brains en directorios o repositorios separados según tus proyectos:
   ```bash
   ./scripts/create-wiki.sh -o ~/mis-wikis/mi-proyecto --preset llm-wiki
   ```
   *Cada carpeta generada cuenta con sus propias reglas y contexto en su `AGENTS.md` local.*

2. **Como Carpeta Core / Monorepo:**
   Si prefieres no crear carpetas externas, puedes instanciar la wiki (`raw/`, `wiki/`) dentro de este mismo repositorio y trabajar directamente utilizando las reglas y skills locales (`.agents/skills/`).

## Operations

| Operation | What happens | Skill |
|-----------|--------------|-------|
| **Scaffold** | New wiki, second brain, or company brain + schema + index/log | `llm-wiki-scaffold` |
| **Capture** | Sources land in `raw/` (or root `Clippings/`, `Agent Client/` if used) | `second-brain-ops` |
| **Ingest** | Source page, entity/concept updates, correlation, index, log | `llm-wiki-ingest` |
| **Query** | Closed-world RAG synthesis from wiki with `[[wikilink]]` citations | `llm-wiki-query` |
| **Express** | File durable answers into `wiki/synthesis/` | `llm-wiki-query` / `second-brain-ops` |
| **Lint** | Contradictions, stale, orphans, gaps, OKF tiers | `llm-wiki-lint` |
| **Review** | Weekly / monthly Second Brain reviews | `second-brain-ops` |
| **Company brain** | Governed definitions/rules/decisions/tribal; capture → govern → serve → trace | `company-brain` |

## OKF ↔ LLM Wiki ↔ CODE/PARA mapping

| OKF v0.2 | LLM Wiki | CODE / PARA |
|----------|----------|-------------|
| Bundle (`index.md`, `log.md`, concepts) | `wiki/` | Organize + Distill |
| Sources / provenance | `raw/` + `sources:` frontmatter | Capture |
| `generated` / `verified` / `status` | page frontmatter | — |
| Attested computations | synthesis / intermediate packets | Express |
| Cross-linked concepts | `[[wikilinks]]` | Distill |
| — | PARA folders | Organize for actionability |

## Repo layout

```text
.
├── AGENTS.md                 master schema for this toolkit
├── README.md                 this file
├── LICENSE                   MIT
├── .gitignore
├── Context/                  founding documents (read-only reference)
├── .agents/
│   ├── README.md             skill library index
│   └── skills/               standardized agent workflows
├── prompts/                  copy-paste agent prompts (one file per workflow)
├── scripts/
│   ├── create-wiki.sh        scaffold a wiki / second brain / company brain
│   ├── wiki-lint.py          OKF health-check
│   └── wiki-search.py        full-text search over wiki/
└── templates/
    ├── schema/AGENTS.md.template
    ├── config/custom-config.example.json
    └── presets/              general, llm-wiki, second-brain, company-brain, research, book, business
```

## Skills

See [`.agents/README.md`](.agents/README.md) for the skill library index. The skills are the agent-facing workflows: `llm-wiki` (coordinator), `llm-wiki-scaffold`, `llm-wiki-ingest`, `llm-wiki-query`, `llm-wiki-lint`, `second-brain-ops`, `company-brain`.

## Agent prompts

Ready-to-use copy-paste prompts for agent-assisted creation and operation of wikis live in [`prompts/`](prompts/README.md) — one file per workflow (scaffold, ingest, query, lint, second brain, company brain), in English and Spanish.

## Context

The `Context/` folder holds the founding documents this toolkit is built on — read them, never edit them:

- [`Context/llm-wiki.md`](Context/llm-wiki.md) — the original llm-wiki pattern
- [`Context/Open Knowledge Format (OKF).md`](Context/Open%20Knowledge%20Format%20(OKF).md) — the OKF v0.2 spec
- [`Context/Building a Second Brain The Definitive Introductory Guide.md`](Context/Building%20a%20Second%20Brain%20The%20Definitive%20Introductory%20Guide.md) — CODE + PARA
- [`Context/What Is a Company Brain.md`](Context/What%20Is%20a%20Company%20Brain.md) — Company Brain pattern & governance

## License

MIT — see [LICENSE](LICENSE).
