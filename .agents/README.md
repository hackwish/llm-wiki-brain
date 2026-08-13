# Skill Library

Standardized skills for building and maintaining a persistent **LLM Wiki +
Second Brain**, built on **OKF v0.2** frontmatter/provenance and the **CODE +
PARA** methodology. All skills share the same frontmatter and conventions; use
the coordinator to decide which operational skill applies.

| Skill | Purpose |
|-------|---------|
| [`llm-wiki`](skills/llm-wiki/SKILL.md) | Umbrella coordinator — workflow map + shared conventions |
| [`llm-wiki-scaffold`](skills/llm-wiki-scaffold/SKILL.md) | Bootstrap a new wiki, second brain, or company brain |
| [`llm-wiki-ingest`](skills/llm-wiki-ingest/SKILL.md) | Ingest a source into the wiki (Capture + Distill) |
| [`llm-wiki-query`](skills/llm-wiki-query/SKILL.md) | Answer questions, file synthesis pages (Express) |
| [`llm-wiki-lint`](skills/llm-wiki-lint/SKILL.md) | Health-check: contradictions, stale, orphans, gaps, OKF tiers |
| [`second-brain-ops`](skills/second-brain-ops/SKILL.md) | CODE + PARA operations, weekly/monthly reviews |
| [`company-brain`](skills/company-brain/SKILL.md) | Governed business knowledge: definitions, rules, decisions, tribal (4 jobs) |

## Conventions

- Each skill: `SKILL.md` (frontmatter `name/description/type/title/tags/status/version/generated` + instructions) + `README.md`.
- Skills reference shared tooling in [`scripts/`](../scripts/) and
  [`templates/`](../templates/).
- Non-negotiable: never edit `raw/`, `Clippings/`, or `Agent Client/`; correlate touched pages via `[[wikilinks]]`
  and tags; flag contradictions; file durable answers back into the wiki.

## Workflow map

```
scaffold → capture(raw/, Clippings/, Agent Client/) → ingest → query → express(synthesis/)
                              └── lint / review ──┘
company-brain: definition/rule/decision/tribal → govern → serve → trace
```

Context documents that ground these skills live in [`Context/`](../Context/).
