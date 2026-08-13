# Company Brain Skill

A governed, current source of how a business actually works — definitions, rules,
decisions, and tribal knowledge — readable by both people and AI agents. A
specialization of the LLM Wiki pattern for organizations.

## The four jobs

| Job | What it does |
|-----|--------------|
| Capture | Definitions, rules, decisions, and tribal knowledge (incl. the unwritten kind) |
| Govern | Canonical vs draft vs retired; owner + last-validated on every entry |
| Serve | Context reaches AI at the moment it answers (MCP or file access — note in SKILL.md) |
| Trace | Every answer traces back to the exact rule/definition it used |

**Anti-staleness:** a stale brain is worse than none — it is wrong with authority.
Entries carry `last_validated` and get flagged for review as they age.

## Usage

```bash
./scripts/create-wiki.sh -o ../company --preset company-brain
```

Page types: `definition`, `rule`, `decision`, `process`, `tribal` in the OKF bundle.

See [SKILL.md](./SKILL.md) for governance, templates, and the full workflow.
