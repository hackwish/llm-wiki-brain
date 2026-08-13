# Ingest prompts — process a source into the wiki

> Skill: `llm-wiki-ingest` · Sources land in `raw/`, `Clippings/`, or `Agent
> Client/` at the wiki root. All are immutable.

## Single source (supervised — recommended)

```
Ingesta Clippings/2026-08-12-el-patron-llm-wiki.md en la wiki.
Lee la fuente completa, proponme 3-5 takeaways y confirma conmigo qué enfatizar
antes de escribir. Luego crea la página de fuente, actualiza entidades/conceptos,
correlaciona todo con wikilinks y tags, y actualiza index.md y log.md.
```

## Process a Clippings dump

```
Process everything under Clippings/ (batch ingest, reduced discussion).
For each article: source page, update/create entity+concept pages, correlate via
wikilinks and shared tags, and keep index.md and log.md current.
```

## Agent Client drop

```
Ingesta el documento que dejó el agent client en Agent Client/ y destíla con
capas de progressive summarization (original → excerpts → summary → executive).
Si contradice algo ya documentado, márcalo en "Contradictions & Open Questions",
no lo sobrescribas silenciosamente.
```

## Distill only (Second Brain angle)

```
No escribas páginas nuevas: solo destila mi nota wiki/concepts/ideas-creativas.md
en 4 capas (progressive summarization) y deja el resto de la wiki intacta.
```

## Verify

```
After ingesting, run scripts/wiki-lint.py --wiki wiki -v and fix any orphans or
missing cross-links the ingest introduced.
```
