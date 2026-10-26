# Scaffold prompts — create a new wiki, second brain, or company brain

> Skill: `llm-wiki-scaffold` · Tool: `scripts/create-wiki.sh`

## Pure LLM Wiki (no PARA folders)

```
Crea un wiki puro sobre inteligencia artificial en ../ai-wiki con el preset llm-wiki.
Asegúrate de que use el patrón llm-wiki (raw/ + wiki/) sin la estructura PARA.
```

## From a topic (let the agent design the domains)

```
Crea un nuevo wiki de investigación sobre computación cuántica aplicada a ML.
Úsalo para planear el tema, proponer 2-4 dominios y scaffoldearlo en ../quantum-ml
con el preset research. Después abre el wiki en Obsidian y cuéntame la estructura.
```

## From a preset with explicit title

```
./scripts/create-wiki.sh -o ../quantum-ml --preset research --title "Quantum ML" --topic "Quantum machine learning survey"
Explain what the script created and what the next steps are.
```

## Custom domains (no preset fits)

```
I'm starting a wiki for planning a 2026 trip to Japan. Design the domains with me
(destinations, logistics, culture, budget), write a config JSON from
templates/config/custom-config.example.json, and scaffold it with
./scripts/create-wiki.sh -o ../japan-trip --config <file>.
```

## As a company brain

```
Scaffold a company brain for our ~90-person software company at ../company with the
company-brain preset. Confirm the domains, then create it. What's the first
knowledge I should capture (definitions, rules, decisions)?
```

## Second brain focus (CODE + PARA)

```
Crea mi segundo cerebro en ../my-brain: usa el preset second-brain, y asegúrate de que
las 4 carpetas PARA (projects, areas, resources, archive) queden listas. Explica
cómo capture, organice, destile y exprese usando esta estructura.
```

## Portfolio with selective publication

```bash
./scripts/create-wiki.sh -o ../mi-portfolio --preset portfolio --title "Mi portfolio"
python3 scripts/portfolio-export.py --root ../mi-portfolio --output public
```

Registra cada caso en `projects/` desde `PROJECT-TEMPLATE.md`. Manténlo privado
hasta revisar texto, enlaces y evidencias; solo se exportan notas con
`portfolio: true`, `visibility: public` y `status: published`. El resultado es
un `public/index.html` estático que puedes alojar con cualquier hosting estático.

## After scaffolding (verify)

```
The wiki in ../my-wiki was scaffolded. Run scripts/wiki-lint.py against it, check
AGENTS.md has no leftover placeholders, and summarize the structure.
```
