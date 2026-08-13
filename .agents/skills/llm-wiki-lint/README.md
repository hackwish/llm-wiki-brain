# LLM Wiki Lint Skill

Health-checks the wiki: contradictions, stale claims, orphans, index gaps, and
OKF trust/freshness issues.

## Flow

1. `python scripts/wiki-lint.py --wiki wiki -v`
2. Manual review (contradictions, stale, orphans, gaps, OKF tiers)
3. Report by severity: `contradiction > stale > orphan > gap`
4. Offer to fix; append result to `wiki/log.md`

See [SKILL.md](./SKILL.md) for check tables and fix patterns.
