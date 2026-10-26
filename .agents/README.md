# Skill Library

This toolkit's primary purpose is to create and maintain **LLM Wikis, Second
Brains, and Company Brains** using **OKF v0.2** and **CODE + PARA**. Its local
skill library also contains optional workflows from other toolkits. The groups
below describe what this repository supports; they do not imply that every
skill is loaded or required for every project.

## Core: Wiki And Brain

Use [`llm-wiki`](skills/llm-wiki/SKILL.md) to route wiki and brain work to the
appropriate operation.

| Skill | Purpose |
|-------|---------|
| [`llm-wiki-scaffold`](skills/llm-wiki-scaffold/SKILL.md) | Bootstrap a wiki, Second Brain, or Company Brain |
| [`llm-wiki-ingest`](skills/llm-wiki-ingest/SKILL.md) | Ingest sources into the wiki (Capture + Distill) |
| [`llm-wiki-query`](skills/llm-wiki-query/SKILL.md) | Answer questions and file synthesis pages (Express) |
| [`llm-wiki-lint`](skills/llm-wiki-lint/SKILL.md) | Check contradictions, stale claims, orphan pages, gaps, and OKF metadata |
| [`second-brain-ops`](skills/second-brain-ops/SKILL.md) | CODE + PARA operations and reviews |
| [`company-brain`](skills/company-brain/SKILL.md) | Governed business definitions, rules, decisions, and tribal knowledge |

Shared wiki rules: never edit `raw/`, `Clippings/`, or `Agent Client/`; connect
touched pages with `[[wikilinks]]` and tags; flag contradictions; and record
durable answers in the wiki.

```text
scaffold → capture → ingest → query → express
                       └── lint / review ──┘
Company Brain: capture → govern → serve → trace
```

## Project Specs: Opt-In

Use these workflows when managing a significant change in an existing code
repository. They do not scaffold an application or choose its framework. SDD
integration is being normalized; check each skill's instructions and any
project-local specification conventions before use.

| Skill | Use |
|-------|-----|
| [`requirements-clarity`](skills/requirements-clarity/SKILL.md) | Clarify scope and acceptance conditions |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | Draft and maintain a gated specification |
| [`writing-plans`](skills/writing-plans/SKILL.md) | Prepare an implementation plan |
| [`executing-plans`](skills/executing-plans/SKILL.md) | Execute an approved implementation plan |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Implement behavior with a red-green-refactor test cycle |
| [`verification-before-completion`](skills/verification-before-completion/SKILL.md) | Verify evidence before reporting completion |

Keep initiative artifacts with the codebase. The default location is
`docs/specs/<initiative-id>/`, unless the repository already has a specification
system or a different convention. Human approval gates remain in force.

## Portfolio: Existing Operation

Portfolio is provided by the [`portfolio` preset](../templates/presets/portfolio.json)
and [`scripts/portfolio-export.py`](../scripts/portfolio-export.py), not by a
separate skill. Export is opt-in and includes only project notes explicitly
marked `portfolio: true`, `visibility: public`, and `status: published`.

## Optional Skill Library

These skills remain available but are not part of the default wiki/brain
routing. Load them only when their stated task and prerequisites apply.

| Area | Skills |
|------|--------|
| Planning, architecture, and review | `agent-md-refactor`, `architecture-decision-records`, `architecture-patterns`, `before-you-build`, `brainstorming`, `c4-architecture`, `code-review-excellence`, `design-system-patterns`, `skill-judge` |
| Git, delivery, and team workflow | `commit-work`, `dispatching-parallel-agents`, `git-advanced-workflows`, `session-handoff`, `team-communication-protocols`, `using-git-worktrees` |
| Writing and documentation | `avoid-ai-writing`, `changelog-automation`, `crafting-effective-readmes`, `humanizer`, `professional-communication`, `writing-clearly-and-concisely`, `writing-skills` |
| Obsidian and content tools | `defuddle`, `json-canvas`, `knap`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown` |
| Domain and external-service workflows | `command-creator`, `cost-optimization`, `cqrs-implementation`, `daily-meeting-update`, `difficult-workplace-conversations`, `domain-name-brainstormer`, `draw-io`, `excalidraw`, `gitops-workflow`, `grafana-dashboards`, `jira`, `llm-evaluation`, `meme-factory`, `secrets-management`, `ship-learn-next` |

Optional skills may rely on external CLIs, APIs, services, runtimes, or agent
capabilities. Their presence in this repository does not install those
dependencies or make them available in a generated wiki.

`skills-lock.json` records imported skill sources and may contain entries for
skills that are not installed under `.agents/skills/`. A directory with a local
`SKILL.md` is the source of truth for local availability; do not remove a
lockfile-only entry as part of catalog curation.

## Skill Conventions

- Every local skill has a `SKILL.md`; supporting files and metadata vary by
  skill. A `README.md` is optional, and imported skills are not assumed to use
  the wiki toolkit's conventions.
- Wiki-specific invariants apply to wiki operations, not automatically to
  unrelated optional skills.
- Shared toolkit scripts and templates live in [`scripts/`](../scripts/) and
  [`templates/`](../templates/).

Project tracking and SDD templates are optional additions under
[`templates/projects/`](../templates/projects/) and [`templates/sdd/`](../templates/sdd/).
The [`sdd-lint.py`](../scripts/sdd-lint.py) check is opt-in and only validates
the supplied Markdown REQ/TASK format; it is not a wiki or scaffold requirement.

Foundational references live in [`Context/`](../Context/).
