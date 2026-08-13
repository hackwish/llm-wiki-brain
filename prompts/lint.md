# Lint prompts — health-check and repair the wiki

> Skill: `llm-wiki-lint` · Tool: `scripts/wiki-lint.py`
> Severity order: `contradiction > stale > orphan > gap`.

## Routine health check

```
Haz un health-check de la wiki: corre scripts/wiki-lint.py --wiki wiki -v, revisa
manualmente contradicciones, claims stale, orphans y gaps, y reporta por severidad.
No corrijas nada todavía — primero muéstrame el reporte y propón un plan.
```

## Fix after report

```
Aplica los fixes del reporte de lint: añade wikilinks a los orphans, crea stubs
para conceptos faltantes, corrige contradicciones manteniendo la sección "Open
Questions" hasta que las resolvamos, y actualiza index.md. Termina con un lint
limpio.
```

## Staleness pass (OKF freshness)

```
Revisa la frescura OKF: páginas sin `verified`, sin `status`, con `updated` más
antiguo que 90 días, o marcadas stale. Propón actualizarlas o archivarlas y
muéstrame el plan antes de tocar nada.
```

## After an AI gave a wrong answer

```
Un agente respondió mal a un cliente. Revisa lineage.md y la página del concepto
que usó: ¿estaba stale o mal definida? Corrige la fuente, no la respuesta, y
documenta el fix en log.md.
```

## Periodic cadence

```
Programa mental: he hecho 8 ingests desde el último lint. Ejecuta el health-check
completo y apunta en log.md cuántos issues de cada tipo había y cuáles resolviste.
```
