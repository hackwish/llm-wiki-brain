# Company Brain prompts — governed business knowledge

> Skill: `company-brain` · Four jobs: Capture, Govern, Serve, Trace.
> Entries: `definition | rule | decision | process | tribal` in the OKF bundle,
> with `status: canonical | draft | retired`, `verified: human:<owner>`,
> `last_validated`, and `sources`.

## Capture a definition

```
Captura la definición de "cliente activo" en el company brain. Pregúntame hasta
cerrarla sin ambigüedad (incluye ejemplos válidos e inválidos), asígnale owner y
márcala como draft. Correlaciona con tags y wikilinks a métricas relacionadas.
```

## Capture tribal knowledge

```
Entrevístame sobre cómo se aprueban realmente las renovaciones (lo que no está
escrito en ningún lado). Documenta eso como tipo `tribal` con ejemplos concretos y
edge cases, y márcalo draft con owner y fecha de validación.
```

## Govern (canonical vs draft vs retired)

```
Revisa el estado de governance del brain: lista entradas sin `status`, sin `verified`
o sin `last_validated`, y muéstrame una propuesta de canonical/draft/retired para
cada una antes de aplicarla. Nada se vuelve canonical sin tu aprobación.
```

## Resolve a contradiction

```
Encontré dos definiciones de "margen" contradictorias en wiki/definitions/. Revisa
sus fuentes, propón la definición correcta y déjala en "Contradictions & Open
Questions" hasta que la confirme el owner. No sobrescribas nada silenciosamente.
```

## Generate an SOP (Express)

```
Genera un SOP de "aprobación de reembolsos > $100" desde las reglas y procesos del
brain: pasos numerados, responsables, manejo de errores, y citas a las entradas
fuente. Fílelo en wiki/synthesis/ y registra qué entradas usó en lineage.md.
```

## Onboarding doc

```
Crea una guía de onboarding para ventas (role-specific) compilando definiciones,
reglas, decisiones y conocimiento tribal relevantes del brain. Debe ser progresiva
(semana 1, 2, 3) y citar sus fuentes.
```

## Trace a wrong AI answer

```
Un agente dio un número de "clientes activos" incorrecto. Usa lineage.md para
encontrar qué definición usó, corrige la fuente (no la respuesta), y dime qué
herramienta/agente estaba citando la versión vieja.
```

## Anti-staleness pass

```
Ejecuta el pase anti-staleness: flag entradas con last_validated de más de 90 días
o status retired, sugiere revisar/renovar cada una, y apunta los hallazgos en
log.md. Un brain stale es peor que ninguno — no dejes que algo envejezca en silencio.
```
