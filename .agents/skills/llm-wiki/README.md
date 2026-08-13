# LLM Wiki Skill

Umbrella coordinator for building and maintaining a persistent LLM Wiki +
Second Brain: a cross-linked markdown knowledge base that compounds over time.

## Workflow map

| Operation | Sub-skill |
|-----------|-----------|
| Bootstrap | `llm-wiki-scaffold` |
| Capture | `second-brain-ops` |
| Ingest | `llm-wiki-ingest` |
| Query | `llm-wiki-query` |
| Express | `llm-wiki-query` / `second-brain-ops` |
| Lint / Review | `llm-wiki-lint` |

## Key principles

- Raw sources are immutable; the wiki owns synthesis and cross-references.
- Every ingest correlates its touched pages via `[[wikilinks]]` and tags.
- Durable answers are filed back into `wiki/synthesis/`.
- Built on OKF v0.2 frontmatter and the Second Brain CODE + PARA methodology.

## See also

- [SKILL.md](./SKILL.md) for the full coordinator workflow.
- `Context/` in the repo root for the founding documents.
