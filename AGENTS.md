# AGENTS.md — LLM Wiki Toolkit

This repository is the **generator + instruction toolkit** for instantiating and maintaining **LLM Wiki / Second Brain / Company Brain** knowledge bases built on the **Open Knowledge Format (OKF v0.2)**. It does not contain a wiki itself; it contains the scripts, schemas, skills, and prompts to manage them.

> **Master Schema**: This file governs how agents operate *this toolkit repo*. Each generated wiki receives its own customized copy of `templates/schema/AGENTS.md.template`.

---

## Toolkit Architecture & Subdirectories

- `.agents/skills/` — Agent skills (`llm-wiki-scaffold`, `llm-wiki-ingest`, `llm-wiki-query`, `llm-wiki-lint`, `second-brain-ops`, `company-brain`, `llm-wiki`).
- `scripts/` — Executable Python and Bash tooling:
  - `create-wiki.sh` — Scaffolds a new wiki from presets/configs.
  - `wiki-lint.py` — Health-checks OKF compliance, stale claims, orphans, index gaps, and contradictions.
  - `wiki-search.py` — Full-text search over `wiki/` markdown pages.
- `templates/` — `schema/AGENTS.md.template` (schema generator) and `presets/*.json` (`general`, `llm-wiki`, `second-brain`, `company-brain`, `research`, `book`, `business`).
- `prompts/` — Copy-paste prompts mapped 1:1 to agent skills.
- `Context/` — Founding specification documents. **Read-only reference — never edit files here.**

---

## Toolkit Verification & Development Commands

When modifying `create-wiki.sh`, `templates/`, or `scripts/`, verify changes using:

```bash
# 1. Validate Bash syntax
bash -n scripts/create-wiki.sh

# 2. Verify preset list rendering
./scripts/create-wiki.sh --list-presets

# 3. Test scaffold end-to-end across kit variants
./scripts/create-wiki.sh -o /tmp/test_llm_wiki -p llm-wiki
./scripts/create-wiki.sh -o /tmp/test_second_brain -p second-brain
./scripts/create-wiki.sh -o /tmp/test_company_brain -p company-brain

# 4. Verify scaffolded wiki health and placeholder replacement
python3 scripts/wiki-lint.py --wiki /tmp/test_llm_wiki/wiki
grep -E "\{\{[A-Z_]+\}\}" /tmp/test_llm_wiki/AGENTS.md # Should return nothing
```

---

## Skill Selection Matrix

| User Intent | Load Skill |
|-------------|------------|
| Bootstrap or scaffold a new wiki | `llm-wiki-scaffold` |
| Ingest or process a document / raw source | `llm-wiki-ingest` |
| Query, answer, or file a synthesis insight | `llm-wiki-query` |
| Audit, lint, or health-check a wiki | `llm-wiki-lint` |
| Personal knowledge management (CODE + PARA, reviews) | `second-brain-ops` |
| Governed business definitions, rules, decisions, tribal knowledge | `company-brain` |
| Ambiguous or multi-step wiki request | `llm-wiki` (coordinator) |

---

## Key Rules & Operational Constraints

1. **Closed-World RAG Rule**: Searches and answers against any wiki must be grounded **strictly in the indexed content in `wiki/`** guided by `AGENTS.md`. Agents must NEVER perform web or external searches unless the user explicitly requests it.
2. **Immutability of Ingest Sources**: Never edit files in `raw/` or optional root-level `Clippings/` or `Agent Client/`. Agents read from raw sources and write to `wiki/`.
3. **Correlation Rule**: Every ingest or synthesis page creation must correlate all touched pages via `[[wikilinks]]` and shared `tags`. No page may be left isolated.
4. **Explicit Contradictions**: Flag contradictions explicitly under `## Contradictions & Open Questions` on the relevant concept/entity pages. Never silently overwrite conflicting information.
5. **Catalog & Log Invariants**: Update `wiki/index.md` (catalog) and append `wiki/log.md` (format: `## [YYYY-MM-DD] <op> | <Title>`) on every operation.
6. **Template Synchronization**: When modifying `templates/schema/AGENTS.md.template`, ensure all placeholders (`{{KIT_INTRO}}`, `{{KIT_LAYERS}}`, `{{KIT_STRUCTURE}}`, `{{KIT_EXTRA_MODE}}`, `{{KIT_SB_OPS}}`) match the Python substitution logic in `scripts/create-wiki.sh`.
