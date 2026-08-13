---
name: company-brain
description: >-
  Builds and manages a company brain: a single, governed, current source of how a
  business actually works — definitions, rules, decisions, and tribal knowledge —
  captured once and readable by both people and AI agents. Applies the four jobs
  (Capture, Govern, Serve, Trace) on top of the LLM Wiki OKF bundle. Use when the
  user wants to capture business knowledge, define metrics/rules, record decisions,
  generate SOPs or onboarding docs, or stop AI tools from guessing at company context.
type: Skill
title: Company Brain — Operations
tags: [company-brain, context-layer, knowledge-management, governance, okf, wiki]
status: stable
version: 1.0.0
generated:
  by: human:hackwish
  at: 2026-08-12
---

# Company Brain — Operations

A company brain is a single, current source of how a business actually works: its
definitions, rules, decisions, and institutional knowledge, captured once and made
readable by both people and AI tools. It is the place a company's meaning lives so
every tool and every new hire works from the same source instead of piecing it
together from a dozen scattered places — and so no AI tool has to guess.

This skill is a **specialization of the LLM Wiki pattern applied to an
organization**. It runs on the same OKF bundle (`raw/` + `wiki/`) as the rest of
this toolkit; the difference is the page types and the governance rules.

## When to use

- User wants to centralize how the business works (definitions, rules, policies)
- AI tools are giving confidently wrong answers because they don't know the company
- Capture tribal knowledge that lives in people's heads
- Record decisions with context and rationale
- Generate SOPs, decision records, onboarding guides from the brain
- Audit what context an answer was built from (traceability)

## The four jobs

1. **Capture** — definitions, rules, decisions, and the *unwritten* kind (tribal
   knowledge). Capture is a byproduct of work, not a documentation chore.
2. **Govern** — someone decides what is canonical vs draft vs retired. If every
   note is treated as truth, the brain becomes a dumping ground and the AI cites
   contradictions with equal confidence.
3. **Serve** — the knowledge reaches the AI tool at the moment it answers, filtered
   by who is asking and what they may see. *Note: this toolkit is markdown-based;
   expose the bundle to agents via MCP (e.g. a search/MCP server) or direct file
   access — the repository itself does not ship a server.*
4. **Trace** — every answer can be traced back to the exact rule and definition it
   used, so a wrong answer points to the source that needs correcting.

**The failure mode:** a stale company brain is worse than none, because it is wrong
with authority — a person shrugs at an outdated wiki page and asks a colleague, but
an agent quotes it to a customer. Seed from the tools you already run and keep it
current; never let pages silently rot.

## The unified structure

```text
<wiki-root>/
  raw/                 # CAPTURE — immutable sources (docs, Slack exports, transcripts, interviews)
  wiki/                # the governed brain — OKF bundle
    index.md           # catalog of all entries
    lineage.md         # traceability: which entries fed each answer/doc
    log.md             # chronological activity (optional, append-only)
    definitions/       # type: definition  — what X means
    rules/             # type: rule       — what triggers an action
    decisions/         # type: decision   — what was decided and why
    processes/         # type: process    — workflows, SOP source material
    tribal/            # type: tribal     — tacit knowledge from team members
    synthesis/         # generated docs: SOPs, decision records, onboarding guides
```

## Governance (OKF-compatible)

Every entry carries OKF v0.2 frontmatter plus company-brain governance:

```yaml
---
type: definition | rule | decision | tribal | process | synthesis
title: "Active Customer"
description: "One-line definition"
domain: definitions
tags: [metrics, sales]
created: YYYY-MM-DD
updated: YYYY-MM-DD
okf_version: "0.2"
sources:
  - id: raw/<file>
    title: "Source"
    author: "<author>"
generated:
  by: <agent>/<version>
  at: YYYY-MM-DD
verified:                  # trust: owner + date (OKF human review)
  - by: human:<owner-id>
    at: YYYY-MM-DD
last_validated: YYYY-MM-DD   # anti-staleness: flagged when aging
status: canonical | draft | retired
---

## Definition
{clear, unambiguous definition}

## Examples
- Valid: {example}
- Invalid: {example}

## Related
[[wikilinks]] to related entries
```

- `status` is the **governance** state (canonical / draft / retired).
- `verified: human:<owner>` records the **owner** (OKF trust tier: human-reviewed).
- `last_validated` drives **staleness detection**; anything aging gets flagged for
  review instead of silently rotting.
- `sources` keeps provenance; `lineage.md` records which entries fed each answer/doc.

## Workflow

### 1) Initialize
- Scaffold with the preset: `./scripts/create-wiki.sh -o ../company --preset company-brain`
- Confirm or create `wiki/` subfolders (definitions, rules, decisions, processes, tribal)
- Create or refresh `wiki/index.md` and `wiki/lineage.md`

### 2) Capture
For each piece of knowledge, classify it and capture it (see templates below):

| Source type | Page type | Example |
|-------------|-----------|---------|
| Definition | `definition` | "active customer" = paid an invoice in the last 90 days |
| Rule | `rule` | refunds > $100 require manager approval |
| Decision | `decision` | chose vendor A over B because … |
| Process | `process` | how renewals get approved |
| Tribal | `tribal` | why this account is politically sensitive |

For **tribal knowledge**: interview team members or review Slack/email threads;
document the unwritten rules with concrete examples and edge cases; tag it clearly
and treat it as draft until governed.

Correlate: link every new entry to related entries via `[[wikilinks]]` and shared
`tags` — nothing is isolated. Update `index.md` and `log.md`.

### 3) Govern
- Mark every entry `canonical`, `draft`, or `retired`.
- Only canonical context carries authority; drafts are explicit.
- Resolve contradictions by updating both sides and keeping a
  `## Contradictions & Open Questions` section until resolved — never silently overwrite.
- Set `verified`/`last_validated` with the responsible owner.

### 4) Serve
- Keep the bundle current and canonical so agents read one version of the truth.
- Expose via MCP or direct file access (note above). Filter by who is asking;
  do not leak confidential entries to the wrong audience.

### 5) Trace
- `lineage.md` — record which entries fed each answer or generated document.
- When an AI answer is wrong: check `lineage.md`, find the stale or wrong entry,
  correct the source (not the answer), and mark the fix.

### 6) Maintain (anti-staleness)
Run periodically (mirrors `llm-wiki-lint`):
- Flag entries with `last_validated` older than a threshold (e.g. 90 days)
- Surface contradictions and gaps (topics with no coverage)
- Promote drafts to canonical after review; retire superseded entries
- Append results to `wiki/log.md`

## Capture templates

### Definition
```markdown
---
type: definition
title: "{Term}"
domain: definitions
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft
---

## Definition
{clear, unambiguous definition}

## Examples
- Valid: {example}
- Invalid: {example}

## Related
- [[related entry]]
```

### Rule
```markdown
---
type: rule
title: "{Rule name}"
domain: rules
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft
---

## Condition
{when this rule applies}

## Action
{what happens}

## Exceptions
{when it doesn't apply}

## Rationale
{why this rule exists}

## Related
- [[related entry]]
```

### Decision record
```markdown
---
type: decision
title: "{Decision Title}"
domain: decisions
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft
---

## Context
{what problem this addresses}

## Options considered
- {option 1}: {pros / cons}
- {option 2}: {pros / cons}

## Decision
{what was decided}

## Rationale
{why this was right}

## Implications
{what happens next}

## Review date
{when to revisit}
```

## Generated documentation

- **SOPs** — actionable: numbered steps, clear responsibilities, error handling; filed in `wiki/synthesis/`.
- **Decision records** — enough context for future maintainers.
- **Onboarding guides** — role-specific, progressive; compiled from definitions, rules, and tribal entries.
- **All docs** cite their sources (`sources` + `lineage.md`).

## Output expectations

The agent should provide:
- A capture plan and classified entries for new knowledge
- Governance state (canonical/draft/retired) with owner and last-validated dates
- Generated docs with traceability
- Updated `index.md`, `log.md`, and `lineage.md`
- Staleness/contradiction findings from maintenance passes

## Reference

- Concept: `Context/What Is a Company Brain.md`
- Sibling flows: `llm-wiki` (coordinator), `llm-wiki-ingest`, `llm-wiki-lint`, `second-brain-ops`
- Schema template: `templates/schema/AGENTS.md.template`
- Preset: `templates/presets/company-brain.json`
