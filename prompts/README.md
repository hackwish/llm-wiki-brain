# Agent Prompts

Copy-paste prompts for **agent-assisted** use of this toolkit. Each file maps to a
workflow (skill). Prompts assume the agent has this repo available (skills +
scripts + templates). Adjust paths and details to your situation.

| File | Workflow | Skill |
|------|----------|-------|
| [scaffold.md](scaffold.md) | Create / bootstrap a new wiki + second brain | `llm-wiki-scaffold` |
| [ingest.md](ingest.md) | Process a source into the wiki | `llm-wiki-ingest` |
| [query.md](query.md) | Ask questions, analyze, file insights | `llm-wiki-query` |
| [lint.md](lint.md) | Health-check and repair the wiki | `llm-wiki-lint` |
| [second-brain.md](second-brain.md) | CODE + PARA capture/organize/distill/express | `second-brain-ops` |
| [company-brain.md](company-brain.md) | Governed business knowledge | `company-brain` |
| [project-sdd.md](project-sdd.md) | Specify and plan a significant change in an existing repository | `spec-driven-development` |

## Tips

- The agent loads the matching skill automatically from phrases like "ingesta
  este", "health-check the wiki", "create a wiki".
- Tell the agent which **preset** (`general | llm-wiki | second-brain | company-brain | research | book | business`) or custom config to use when scaffolding.
- Use the SDD prompt only for an existing code repository; preserve its specification system and approve each phase before proceeding.
- After a wiki ingest or synthesis operation, the agent must update
  `wiki/index.md` and append `wiki/log.md`; verify it did. SDD and portfolio
  operations do not require wiki log updates unless they also modify the wiki.
- Use `scripts/wiki-lint.py` before/after big changes and offer to fix findings.
