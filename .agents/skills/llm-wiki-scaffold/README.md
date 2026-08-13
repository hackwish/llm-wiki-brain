# LLM Wiki Scaffold Skill

Scaffolds a new LLM Wiki, Second Brain, or Company Brain with four distinct toolkit modes (`blended`, `llm-wiki`, `second-brain`, `company-brain`).

## Usage

```bash
# Pure LLM Wiki (no PARA folders)
./scripts/create-wiki.sh --output ../my-wiki --preset llm-wiki --title "My Topic"

# Second Brain (with CODE + PARA)
./scripts/create-wiki.sh -o ../my-brain --preset second-brain

# Company Brain (governed organizational knowledge)
./scripts/create-wiki.sh -o ../company-brain --preset company-brain

# Blended general purpose (default)
./scripts/create-wiki.sh -o ../my-wiki --preset general

./scripts/create-wiki.sh --list-presets
```

## What it creates

- `raw/` — immutable ingest sources (PDFs, transcripts, notes)
- `wiki/` — OKF bundle: `index.md`, `log.md`, `sources/`, `entities/`, `concepts/`, `synthesis/`, domain folders
- `projects/` `areas/` `resources/` `archive/` — PARA actionability structure (when using `blended` or `second-brain` kits)
- `AGENTS.md` — schema rendered from `templates/schema/AGENTS.md.template`

Optional folders like `Clippings/` and `Agent Client/` may appear at the root during use as potential ingest sources.

See [SKILL.md](./SKILL.md) for the full workflow.
