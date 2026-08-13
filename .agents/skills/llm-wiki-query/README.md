# LLM Wiki Query Skill

Answers questions from the wiki with `[[wikilink]]` citations and files durable
insights into `wiki/synthesis/` (Express layer of CODE).

## Flow

1. Read `wiki/index.md`
2. Search if needed: `python scripts/wiki-search.py "terms" --wiki wiki`
3. Read relevant pages
4. Synthesize with citations
5. Offer to file the answer as a synthesis page

See [SKILL.md](./SKILL.md) for output formats and filing rules.
