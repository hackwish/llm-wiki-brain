---
name: spec-driven-development
description: Use when a significant change in an existing codebase lacks an approved specification, requirements are unclear, or one initiative bundles independently testable capabilities that need a capability map.
---

# Spec-Driven Development

## Overview

For significant changes in an existing codebase, write or update an approved specification before implementation. The spec records the objective, boundaries, and evidence of success without replacing the repository's existing architecture or delivery conventions.

This workflow manages specifications and implementation planning. It does not scaffold applications, select frameworks, or require a repository to adopt SDD.

## When to Use

- Starting a significant feature or change in an existing codebase when no approved specification exists
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

**When NOT to use:** Scaffolding a new application, single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained. Do not create a duplicate spec when the repository already has an applicable specification system.

## Repository Conventions

- Inspect the existing repository instructions, architecture, test setup, and specification artifacts before proposing changes.
- Preserve the existing specification format and location, including OpenSpec or another established system. Do not create parallel artifacts.
- An existing specification system remains authoritative for artifact format and storage.
- When the repository has no specification convention, use `docs/specs/<initiative-id>/` for initiative artifacts. Keep artifacts with the code they govern; a Second Brain project note may link to them but should not duplicate the full specification.
- Use evidence from the existing codebase for its stack, structure, and commands. Record unknowns as open questions instead of choosing a framework or inventing project conventions.
- Keep human approval gates: do not advance from capability map, specification, or plan/tasks until the human approves that phase.
- Reusable templates live in `templates/sdd/`; use `CAPABILITY-MAP-TEMPLATE.md` only when the scope check identifies multiple independent capabilities.

## The Gated Workflow

Spec-driven development has four phases, preceded by a scope check (Phase 0) that activates only when one request bundles several independently testable capabilities. Do not advance to the next phase until the current one is validated.

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### Phase 0: Scope Check

Most requests describe one capability. If this one does, skip this phase and go straight to Specify — Phase 0 exists for the exception, not the rule, and it puts no hierarchy on single-capability features.

**Detection.** Decompose before specifying when a single requirement bundles several independently testable capabilities:

- The requirement names distinct capabilities with their own consumers or data (e.g. identity, billing, notifications, reporting)
- Acceptance criteria cluster into groups that could ship and be verified separately
- One capability could be cut or replaced without rewriting the others' requirements

**Propose a capability map before writing any spec.** Small and reviewable — a module table plus a build order, not a project plan:

```markdown
# Capability Map: [Initiative Name]

| Module id | Responsibility | Depends on |
|---|---|---|
| identity | Accounts, sessions, SSO | — |
| billing | Plans, invoices, payments | identity |
| notifications | Email and webhook fan-out | identity |
| reporting | Usage dashboards | billing, notifications |

Build order: identity → billing, notifications → reporting
```

- **Stable module ids.** Kebab-case, chosen once, never renamed mid-initiative. Specs, plans, and downstream commands select work by these ids instead of guessing which spec is active.
- **Dependency direction, no cycles.** Arrows point one way. If two modules each need the other, they are one module.
- **Interfaces live at the boundary.** The map records dependencies; the relevant module specification describes the contract at that boundary.

**The map is gated like every phase.** The human reviews module boundaries, dependency direction, and build order before any module spec is written. Getting the map wrong is expensive; reviewing ten lines is not.

**Then recurse per module.** Run Specify → Plan → Tasks → Implement for each module in dependency order. Each module gets a specification scoped to its objective, boundaries, and success criteria. Save the approved map and module specs in the repository's established specification location; otherwise use `docs/specs/<initiative-id>/` and identify modules by their stable ids.

### Phase 1: Specify

Start from the current codebase and a high-level change objective. Ask the human clarifying questions until requirements are concrete and consistent with existing behavior.

**Surface assumptions immediately.** Before writing any spec content, list what you're assuming:

```
ASSUMPTIONS I'M MAKING:
1. The change belongs in the existing service rather than a new application
2. Existing authentication and persistence behavior must remain compatible
3. The current test suite is the primary regression baseline
4. Any behavior not established by the repository remains an open question
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements. The spec's entire purpose is to surface misunderstandings *before* code gets written — assumptions are the most dangerous form of misunderstanding.

**Write or update a specification covering the applicable areas below:**

1. **Objective** — What are we building and why? Who is the user? What does success look like?

2. **Commands** — Existing executable commands with flags, verified from repository files or instructions; do not invent commands.
   ```
   Build: npm run build
   Test: npm test -- --coverage
   Lint: npm run lint --fix
   Dev: npm run dev
   ```

3. **Project Structure** — Existing source, test, and documentation locations relevant to the change.
   ```
   src/           → Application source code
   src/components → React components
   src/lib        → Shared utilities
   tests/         → Unit and integration tests
   e2e/           → End-to-end tests
   docs/          → Documentation
   ```

4. **Code Style** — Cite relevant local conventions and a representative existing example when useful.

5. **Testing Strategy** — Existing test framework and locations, with checks mapped to the changed behavior.

6. **Boundaries** — Three-tier system:
   - **Always do:** Run tests before commits, follow naming conventions, validate inputs
   - **Ask first:** Database schema changes, adding dependencies, changing CI config
   - **Never do:** Commit secrets, edit vendor directories, remove failing tests without approval

**Spec template:**

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Existing Context
[Relevant architecture, components, current behavior, and verified stack]

## Commands
[Build, test, lint, dev — full commands]

## Project Locations
[Existing source, test, and documentation paths relevant to this change]

## Existing Conventions
[Relevant local patterns and references]

## Testing Strategy
[Existing test commands and locations, mapped to changed behavior]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

**External spec tools:** This workflow is format-agnostic. If the project
already uses OpenSpec or another specification system, keep that system's
artifact format and storage conventions instead of creating a duplicate
`SPEC.md`. This skill owns the clarification, content, and approval gates; the
external tool owns how the approved spec is represented.

**Reframe instructions as success criteria.** When receiving vague requirements, translate them into concrete conditions:

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

This lets you loop, retry, and problem-solve toward a clear goal rather than guessing what "faster" means.

**Stop after writing the spec (CRITICAL).** Once the specification is saved or updated:

1. Summarize it and list any Open Questions.
2. Ask the human to approve it or request changes.
3. **STOP YOUR TURN IMMEDIATELY.** Do not start Phase 2 or write code in this turn. Planning starts only after the human approves the specification in a later turn.

### Phase 2: Plan

With the approved specification, prepare a plan that fits the existing architecture:

1. Identify the major components and their dependencies
2. Determine the implementation order (what must be built first)
3. Note risks and mitigation strategies
4. Identify what can be built in parallel vs. what must be sequential
5. Define verification checkpoints between phases

Use the plan to preserve behavior, order dependent work, and identify verification checkpoints. Prefer small vertical slices and state risks or unresolved interfaces explicitly.

**Output convention:** Update the repository's established planning artifacts. Otherwise save `plan.md` and `tasks.md` next to the specification in `docs/specs/<initiative-id>/`. Use an existing external task tracker when the repository or team already designates one.

The plan should be reviewable: the human should be able to read it and say "yes, that's the right approach" or "no, change X."

### Phase 3: Tasks

Break the approved plan into discrete, implementable tasks:

- Each task should be completable in a single focused session
- Each task has explicit acceptance criteria
- Each task includes a verification step (test, build, manual check)
- Tasks are ordered by dependency, not by perceived importance
- Keep each task focused; identify its expected files and avoid unrelated cleanup.

**Task template:**
```markdown
- [ ] Task: [Description]
   - Requirements: [REQ-IDs]
  - Acceptance: [What must be true when done]
   - Verify: [Existing test or check that proves it]
  - Files: [Which files will be touched]
```

Record requirement identifiers in the specification as `REQ-001`, `REQ-002`, etc. Each task should reference at least one applicable requirement; do not create empty acceptance criteria or orphan tasks.

Stop after presenting the plan and tasks. Ask the human to approve them before implementation.

### Phase 4: Implement

Only implement approved tasks. Follow the repository's development process and use available local guidance where applicable: [test-driven-development](../test-driven-development/SKILL.md), [executing-plans](../executing-plans/SKILL.md), and [verification-before-completion](../verification-before-completion/SKILL.md). These are reusable local workflows, not required external installations. Load only the relevant specification and source context for each task.

Do not scaffold an application, introduce a framework, or expand beyond the approved task list. Keep implementation, tests, and evidence in the existing codebase.

### Optional Traceability Check

When the initiative uses the Markdown structure in `templates/sdd/`, run
`python3 scripts/sdd-lint.py --spec <spec.md> --tasks <tasks.md>` to check for
duplicate requirement definitions, missing acceptance criteria, and tasks
without valid requirement links. This check is opt-in and does not apply to
other specification formats or repositories that do not use SDD.

## Keeping the Spec Alive

The spec is a living document, not a one-time artifact:

- **Update when decisions change** — If you discover the data model needs to change, update the spec first, then implement.
- **Update when scope changes** — Features added or cut should be reflected in the spec.
- **Commit the spec** — The spec belongs in version control alongside the code.
- **Reference the spec in PRs** — Link back to the spec section that each PR implements.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. A two-line spec is fine. |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. Waterfall in 15 minutes beats debugging in 15 hours. |
| "Requirements will change anyway" | That's why the spec is a living document. An outdated spec is still better than no spec. |
| "The user knows what they want" | Even clear requests have implicit assumptions. The spec surfaces those assumptions. |
| "It's one big feature; splitting it is overhead" | If acceptance criteria cluster into independently testable groups, a monolithic spec forces every downstream task to reason over the whole contract. A ten-line capability map is the cheap alternative. |
| "I'll decompose during planning" | Planning slices tasks within a spec. By then the oversized artifact already exists — module boundaries and dependency direction must be decided before the spec is written, not after. |

## Red Flags

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"
- Writing the spec and starting the plan or code in the same turn
- One spec whose requirements span several independently testable capabilities
- Module boundaries or build order decided implicitly during implementation because no capability map was approved up front

## Verification

Before proceeding to implementation, confirm:

- [ ] The spec covers all six core areas
- [ ] The human has reviewed and approved the spec
- [ ] The turn ended after saving the spec; approval came in a later turn
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The spec is saved to a file in the repository
- [ ] If the request bundles several independently testable capabilities, a capability map (module ids, dependency direction, build order) was approved before any module spec was written
- [ ] Every module spec traces to a module id in the approved map
