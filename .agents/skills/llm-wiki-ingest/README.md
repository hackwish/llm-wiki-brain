# LLM Wiki Ingest Skill

Processes a source dropped into `raw/`, `Clippings/`, or `Agent Client/` (the
wiki-root ingest sources) into the wiki: source page, entity/concept updates,
correlation via wikilinks and tags, index and log updates. Applies OKF provenance
fields and progressive summarization (Distill layer of CODE).

## Flow

1. Read source fully
2. Align takeaways with the user
3. Create `wiki/sources/YYYY-MM-DD-<slug>.md`
4. Update/create entity + concept pages
5. **Correlate** touched pages (wikilinks + tags)
6. Update `wiki/index.md` and append `wiki/log.md`

See [SKILL.md](./SKILL.md) for templates and rules.
