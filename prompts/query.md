# Query prompts — ask, analyze, and file insights

> Skill: `llm-wiki-query` · Always read `wiki/index.md` first; searches operate as
> a closed-world RAG strictly based on indexed `wiki/` content guided by `AGENTS.md`.
> Web searches require explicit user request. Cite with `[[wikilinks]]`; surface
> contradictions; file durable answers to `wiki/synthesis/`.

## Simple question

```
Según lo que hemos acumulado en la wiki, ¿qué sabemos sobre las limitaciones de
los RAG frente a un wiki persistente? Cita las páginas que uses con wikilinks y
señala cualquier contradicción que encuentres.
```

## Comparison (table)

```
Compare RAG and persistent wiki approaches for knowledge bases: build me a
comparison table drawing only from wiki pages, with wikilink citations.
```

## Presentation from the wiki

```
Create a Marp slide deck (10 slides) from the wiki summarizing our synthesis on
<topic>. Pull from synthesis and concepts pages, cite each slide.
```

## Analysis + file the insight

```
Answer: what patterns do our synthesis pages reveal about how the wiki compounds
over time? Then file the answer as a synthesis page in wiki/synthesis/ with full
frontmatter, correlated via wikilinks and tags, and update index.md + log.md.
```

## Gap honesty

```
What does the wiki cover about <topic>? If coverage is thin, say so explicitly and
suggest 2-3 sources to ingest or searches to run, instead of inventing.
```

## Search first

```
Search the wiki for a topic: run python scripts/wiki-search.py "<topic>" -n 10
--wiki wiki, read the top pages, and answer with citations.
```
