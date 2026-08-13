#!/usr/bin/env bash
# create-wiki.sh — Scaffold a new LLM Wiki / Second Brain / Company Brain toolkit.
#
# Creates a wiki at --output with:
#   raw/            immutable ingest sources (PDFs, transcripts, notes, assets)
#   wiki/           OKF bundle: index.md, log.md, sources/, entities/, concepts/, synthesis/, <domains>/
#   projects/areas/resources/archive/   (when kit includes PARA actionability structure)
#   AGENTS.md       schema (copied from templates/schema/AGENTS.md.template)
#
# Usage:
#   ./scripts/create-wiki.sh --output /path/to/new-wiki --preset research --title "Quantum ML"
#   ./scripts/create-wiki.sh -o ../japan-trip --topic "Japan spring 2026 trip planning"
#   ./scripts/create-wiki.sh -o ../pure-wiki --preset llm-wiki
#   ./scripts/create-wiki.sh -o ../my-brain --preset second-brain
#   ./scripts/create-wiki.sh --list-presets
#
# Exit codes: 0 ok, 1 error, 2 bad usage.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_SCHEMA="${ROOT_DIR}/templates/schema/AGENTS.md.template"
PRESETS_DIR="${ROOT_DIR}/templates/presets"

usage() {
  sed -n '2,14p' "$0"
  echo
  echo "Options:"
  echo "  -o, --output <dir>       Destination directory (required)"
  echo "  -p, --preset <name>      Preset: $(ls "${PRESETS_DIR}" | sed 's/\.json//g' | tr '\n' ' ')"
  echo "  -t, --title <title>      Wiki title (overrides preset)"
  echo "  -T, --topic <topic>      Purpose statement (overrides preset)"
  echo "  -c, --config <file>      Custom JSON config (overrides preset)"
  echo "      --list-presets       List available presets and exit"
  echo "  -h, --help               Show this help"
}

list_presets() {
  printf "  %-14s %-14s %s\n" "PRESET" "KIT" "PURPOSE"
  printf "  %-14s %-14s %s\n" "------" "---" "-------"
  for f in "${PRESETS_DIR}"/*.json; do
    name="$(basename "$f" .json)"
    kit="$(python3 -c "import json,sys; print(json.load(open('$f')).get('kit','blended'))" 2>/dev/null || echo 'blended')"
    purpose="$(python3 -c "import json,sys; print(json.load(open('$f')).get('purpose',''))" 2>/dev/null || echo '')"
    printf "  %-14s %-14s %s\n" "$name" "$kit" "$purpose"
  done
}

die() { echo "error: $1" >&2; exit 1; }

OUTPUT=""
PRESET=""
TITLE=""
TOPIC=""
CONFIG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output) OUTPUT="$2"; shift 2 ;;
    -p|--preset) PRESET="$2"; shift 2 ;;
    -t|--title) TITLE="$2"; shift 2 ;;
    -T|--topic) TOPIC="$2"; shift 2 ;;
    -c|--config) CONFIG="$2"; shift 2 ;;
    --list-presets) list_presets; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

[[ -n "$OUTPUT" ]] || die "--output is required (try --help)"

# Build effective config: config file > preset > defaults
CONFIG_DATA="{}"
if [[ -n "$CONFIG" ]]; then
  [[ -f "$CONFIG" ]] || die "config file not found: $CONFIG"
  CONFIG_DATA="$(cat "$CONFIG")"
elif [[ -n "$PRESET" ]]; then
  [[ -f "${PRESETS_DIR}/${PRESET}.json" ]] || die "unknown preset: ${PRESET} (see --list-presets)"
  CONFIG_DATA="$(cat "${PRESETS_DIR}/${PRESET}.json")"
fi

resolve() { # resolve <key> <default>
  local key="$1" default="$2"
  local val
  val="$(python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('$key','$default'))" <<<"$CONFIG_DATA")"
  printf '%s' "$val"
}
resolve_json() { # resolve_json <key> <fallback-json-string>
  local key="$1" fallback="$2"
  python3 -c "import json,sys; d=json.loads(sys.stdin.read()); v=d.get('$key'); print(json.dumps(v) if v is not None else json.dumps($fallback))" <<<"$CONFIG_DATA"
}

WIKI_TITLE="${TITLE:-$(resolve title 'Untitled Wiki')}"
WIKI_TOPIC="${TOPIC:-$(resolve topic '')}"
WIKI_PURPOSE="$(resolve purpose 'A persistent, compounding knowledge base maintained by an LLM.')"
WIKI_OWNER="$(resolve owner '')"
WIKI_LANG="$(resolve lang 'en')"
WIKI_PRESET="${PRESET:-$(resolve preset 'general')}"
WIKI_KIT="$(resolve kit 'blended')"
DOMAINS_JSON="$(resolve_json domains '[]')"

[[ -e "$OUTPUT" ]] && die "output already exists: $OUTPUT"
mkdir -p "$OUTPUT"

# ---- Core wiki folders ----
mkdir -p "$OUTPUT/raw/assets"
mkdir -p "$OUTPUT/wiki/sources"
mkdir -p "$OUTPUT/wiki/entities"
mkdir -p "$OUTPUT/wiki/concepts"
mkdir -p "$OUTPUT/wiki/synthesis"

# Create PARA folders if kit is blended or second-brain
if [[ "$WIKI_KIT" == "blended" || "$WIKI_KIT" == "second-brain" ]]; then
  mkdir -p "$OUTPUT/projects"
  mkdir -p "$OUTPUT/areas"
  mkdir -p "$OUTPUT/resources"
  mkdir -p "$OUTPUT/archive"
fi

TODAY="$(date +%F)"

LINEAGE_INDEX_LINE=""
# Company brain specific file
if [[ "$WIKI_KIT" == "company-brain" ]]; then
  LINEAGE_INDEX_LINE="- [[lineage]] — Artifact traceability and source attributions"
  cat > "$OUTPUT/wiki/lineage.md" <<EOF
---
type: log
title: "${WIKI_TITLE} — Lineage"
description: "Chronological tracking of generated artifacts and source attributions"
domain: cross-domain
tags: [lineage, traceability, governance]
created: ${TODAY}
updated: ${TODAY}
okf_version: "0.2"
---

# Lineage Record

Chronological tracking of generated artifacts and source attributions.
Back to [[index]].
EOF
fi

# ---- Schema ----
[[ -f "$TEMPLATE_SCHEMA" ]] || die "schema template not found: $TEMPLATE_SCHEMA"
DOMAINS_LINES=""
python3 - "$DOMAINS_JSON" <<'PY' > /tmp/domains_lines.txt
import json, sys
domains = json.loads(sys.argv[1])
for d in domains:
    print(f"- `{d}` — see `wiki/{d}/`")
PY
DOMAINS_LINES="$(cat /tmp/domains_lines.txt)"
rm -f /tmp/domains_lines.txt

# Create domain folders
python3 - "$DOMAINS_JSON" "$OUTPUT" <<'PY'
import json, sys, os
domains = json.loads(sys.argv[1])
root = sys.argv[2]
for d in domains:
    slug = d.lower().replace(" ", "-")
    os.makedirs(os.path.join(root, "wiki", slug), exist_ok=True)
PY

python3 - "$TEMPLATE_SCHEMA" "$OUTPUT/AGENTS.md" "$WIKI_TITLE" "$WIKI_PURPOSE" "$WIKI_TOPIC" "$WIKI_OWNER" "$WIKI_LANG" "$WIKI_PRESET" "$WIKI_KIT" "$DOMAINS_LINES" <<'PY'
import sys

template, out, title, purpose, topic, owner, lang, preset, kit, domains = sys.argv[1:11]
text = open(template, encoding="utf-8").read()

kit_intro = {
    "blended": "It follows the **Open Knowledge Format (OKF)** v0.2 for frontmatter and provenance, and integrates the **Second Brain** methodology (CODE + PARA) for capture, distillation, and expression.",
    "llm-wiki": "It follows the **Open Knowledge Format (OKF)** v0.2 for frontmatter and provenance, focusing purely on a compounding, persistent knowledge base.",
    "second-brain": "It follows the **Open Knowledge Format (OKF)** v0.2 for frontmatter and provenance, and implements the **Second Brain** methodology (CODE + PARA) for personal knowledge management.",
    "company-brain": "It follows the **Open Knowledge Format (OKF)** v0.2 for frontmatter and provenance, and implements a governed **Company Brain** for business definitions, rules, decisions, processes, and tribal knowledge."
}

kit_layers = {
    "blended": """1. **`raw/`** — immutable source of truth. Files here are **never modified**.
   `Clippings/` and `Agent Client/` may appear at the wiki root as **potential
   ingest sources**. The agent reads from these, writes to `wiki/`.
2. **`wiki/`** — the OKF bundle the agent owns. Cross-linked markdown pages,
   `index.md` (catalog) and `log.md` (chronological record).
3. **This file** — the schema that makes the agent a disciplined maintainer.""",
    "llm-wiki": """1. **`raw/`** — immutable source of truth. Files here are **never modified**.
   `Clippings/` and `Agent Client/` may appear at the wiki root as **potential
   ingest sources**. The agent reads from these, writes to `wiki/`.
2. **`wiki/`** — the OKF bundle the agent owns. Cross-linked markdown pages,
   `index.md` (catalog) and `log.md` (chronological record).
3. **This file** — the schema that makes the agent a disciplined maintainer.""",
    "second-brain": """1. **`raw/`** — immutable source of truth for captured sources (read-only).
   `Clippings/` and `Agent Client/` may appear at the wiki root as **potential
   ingest sources**.
2. **`wiki/`** — the OKF knowledge bundle organized and distilled by the agent.
3. **This file** — the schema guiding CODE capture and PARA actionability.""",
    "company-brain": """1. **`raw/`** — immutable source of truth for company documents, transcripts, and policies.
2. **`wiki/`** — governed knowledge entries (definitions, rules, decisions, processes, tribal knowledge) + `lineage.md`.
3. **This file** — the schema enforcing governance, authority, validation, and lineage."""
}

kit_structure = {
    "blended": """raw/                       # immutable ingest sources (never edit)
  assets/                  # downloaded images referenced by sources
wiki/                      # OKF bundle — agent-owned
  index.md                 # catalog of all pages, by category
  log.md                   # chronological append-only history
  lineage.md               # optional traceability
  sources/                 # one page per ingested source (YYYY-MM-DD-<slug>.md)
  entities/                # named things: people, places, products, events
  concepts/                # abstract ideas and topics
  synthesis/               # filed answers, comparisons, analyses (Express)
  <domain>/                # one folder per domain (see Domains below)
projects/                  # PARA — short-term efforts with goals
areas/                     # PARA — long-term responsibilities
resources/                 # PARA — topics that may be useful later
archive/                   # PARA — inactive items""",
    "llm-wiki": """raw/                       # immutable ingest sources (never edit)
  assets/                  # downloaded images referenced by sources
wiki/                      # OKF bundle — agent-owned
  index.md                 # catalog of all pages, by category
  log.md                   # chronological append-only history
  sources/                 # one page per ingested source (YYYY-MM-DD-<slug>.md)
  entities/                # named things: people, places, products, events
  concepts/                # abstract ideas and topics
  synthesis/               # filed answers, comparisons, analyses
  <domain>/                # one folder per domain (see Domains below)""",
    "second-brain": """raw/                       # immutable capture inbox (PDFs, transcripts, notes)
  assets/                  # downloaded images
wiki/                      # OKF knowledge bundle — agent-owned
  index.md                 # catalog of knowledge pages
  log.md                   # chronological history
  sources/ entities/ concepts/ synthesis/ <domain>/
projects/                  # PARA — short-term efforts with goals
areas/                     # PARA — long-term responsibilities
resources/                 # PARA — topics that may be useful later
archive/                   # PARA — inactive items""",
    "company-brain": """raw/                       # immutable source documents (policies, transcripts, docs)
  assets/                  # referenced assets
wiki/                      # governed company knowledge bundle
  index.md                 # catalog of definitions, rules, decisions
  log.md                   # chronological audit log
  lineage.md               # answer traceability and source mapping
  sources/                 # source documents
  entities/                # team, products, systems, partners
  concepts/                # key domain concepts
  synthesis/               # compiled guides and briefs
  <domain>/                # definitions, rules, decisions, processes"""
}

cb_mode_text = """## Company Brain mode (business/organization wikis)

If this wiki operates as a **company brain**, generic types map to governed knowledge entries:

| Business knowledge | Page type | Example |
|--------------------|-----------|---------|
| What X means | `definition` | "active customer" = paid in last 90 days |
| What triggers an action | `rule` | refunds > $100 require manager approval |
| What was decided and why | `decision` | chose vendor A over B because … |
| How a workflow runs | `process` | how renewals get approved |
| Unwritten knowledge | `tribal` | why this account is sensitive |

Governance:
- `status: canonical | draft | retired` — only canonical carries authority
- `verified: [{by: human:<owner>, at: date}]` — owner + review date
- `last_validated: YYYY-MM-DD` — anti-staleness
- `sources` keeps provenance; `wiki/lineage.md` records lineage"""

sb_ops_text = """### Second Brain (PARA)
- Capture → `raw/` (immutable) or `projects/areas/resources/` working notes.
- Organize → file by actionability using PARA; weekly batch (10–20 items).
- Distill → Progressive Summarization layers on wiki pages over time.
- Express → Intermediate Packets in `projects/` or `wiki/synthesis/`."""

kit_extra_mode = {
    "blended": cb_mode_text,
    "llm-wiki": "",
    "second-brain": "",
    "company-brain": cb_mode_text
}

kit_sb_ops = {
    "blended": sb_ops_text,
    "llm-wiki": "",
    "second-brain": sb_ops_text,
    "company-brain": ""
}

k = kit if kit in kit_intro else "blended"

text = text.replace("{{TITLE}}", title)
text = text.replace("{{PURPOSE}}", purpose)
text = text.replace("{{TOPIC}}", topic)
text = text.replace("{{OWNER}}", owner)
text = text.replace("{{LANG}}", lang)
text = text.replace("{{PRESET}}", preset)
text = text.replace("{{KIT}}", k)
text = text.replace("{{DOMAINS}}", domains)
text = text.replace("{{KIT_INTRO}}", kit_intro[k])
text = text.replace("{{KIT_LAYERS}}", kit_layers[k])
text = text.replace("{{KIT_STRUCTURE}}", kit_structure[k])
text = text.replace("{{KIT_EXTRA_MODE}}", kit_extra_mode[k])
text = text.replace("{{KIT_SB_OPS}}", kit_sb_ops[k])

open(out, "w", encoding="utf-8").write(text)
PY

# ---- index.md ----
TODAY="$(date +%F)"
cat > "$OUTPUT/wiki/index.md" <<EOF
---
type: index
title: "${WIKI_TITLE} — Index"
okf_version: "0.2"
created: ${TODAY}
updated: ${TODAY}
generated:
  by: script:create-wiki.sh
  at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

# ${WIKI_TITLE}

${WIKI_PURPOSE}

## Domains
${DOMAINS_LINES}
## Sources
- (none yet — drop files into \`raw/\` and run the ingest workflow)

## Entities
- (none yet)

## Concepts
- (none yet)

## Synthesis
- (none yet)
${LINEAGE_INDEX_LINE}
EOF

# ---- log.md ----
cat > "$OUTPUT/wiki/log.md" <<EOF
---
type: log
title: "${WIKI_TITLE} — Log"
okf_version: "0.2"
created: ${TODAY}
updated: ${TODAY}
---

# Log

## [${TODAY}] scaffold | Initialized wiki
Created the wiki with preset \`${WIKI_PRESET}\` (kit \`${WIKI_KIT}\`).
EOF

# ---- Section READMEs ----

# raw/
cat > "$OUTPUT/raw/README.md" <<'EOF'
# raw/

**Immutable ingest sources.** This is the layer the LLM *reads from and never
writes to*: the "source of truth" of the wiki (llm-wiki pattern). Drop files here —
articles, PDFs, transcripts, meeting notes — and run the **ingest** workflow to
integrate them into `wiki/`.

> Context: *"Raw sources — your curated collection of source documents. These are
> immutable — the LLM reads from them but never modifies them."* — `llm-wiki.md`

**Rules:**
- Never edit files inside `raw/` — they are the source of truth.
- The agent reads from `raw/`, writes to `wiki/`.
- `assets/` holds downloaded images referenced by sources (Obsidian attachment
  folder; e.g. bind "Download attachments" to a hotkey after clipping).
EOF

# wiki/
cat > "$OUTPUT/wiki/README.md" <<'EOF'
# wiki/

**The OKF bundle — agent-owned.** The wiki is the layer the LLM writes and
maintains: cross-linked markdown pages that keep getting richer with every source
you add and every question you ask. This is where knowledge *compounds*.

> Context: *"The wiki is a persistent, compounding artifact. The cross-references
> are already there. The contradictions have already been flagged. The synthesis
> already reflects everything you've read."* — `llm-wiki.md`

Structure: `index.md` (catalog, content-oriented) · `log.md` (chronological,
append-only) · `sources/` · `entities/` · `concepts/` · `synthesis/` · domain
folders. Every page carries OKF v0.2 frontmatter (provenance, trust, freshness).
EOF

# ---- PARA READMEs (if kit has PARA) ----
if [[ "$WIKI_KIT" == "blended" || "$WIKI_KIT" == "second-brain" ]]; then
cat > "$OUTPUT/projects/README.md" <<'EOF'
# projects/

**PARA — Projects.** *"Short-term efforts (in your work or personal life) that you
take on with a certain goal in mind."* Each project has a beginning and an end.

> Context: — *PARA, Building a Second Brain*

Keep intermediate packets, deliverables, and working notes here; link into the
wiki concepts they touch. Move completed projects to `archive/` in the monthly
review.

_See [wiki/index.md](wiki/index.md) for the knowledge bundle._
EOF

cat > "$OUTPUT/areas/README.md" <<'EOF'
# areas/

**PARA — Areas.** *"Long-term responsibilities you want to manage over time"* —
things you maintain without a fixed deadline (health, team, finances).

> Context: — *PARA, Building a Second Brain*

Keep working material here and link into the wiki concepts it touches. Areas
change rarely; review them in the monthly review.

_See [wiki/index.md](wiki/index.md) for the knowledge bundle._
EOF

cat > "$OUTPUT/resources/README.md" <<'EOF'
# resources/

**PARA — Resources.** *"Topics or interests that may be useful in the future"* —
reference material and interests with no active project attached.

> Context: — *PARA, Building a Second Brain*

Keep research, clippings, and reference notes here; link into the wiki concepts
they touch. Clean stale items in the monthly review.

_See [wiki/index.md](wiki/index.md) for the knowledge bundle._
EOF

cat > "$OUTPUT/archive/README.md" <<'EOF'
# archive/

**PARA — Archive.** *"Inactive items from the other 3 categories"* — a "time
capsule" that preserves what you had going on until this moment, nothing deleted.

> Context: *"Move all existing files to a folder titled Archive with today's
> date... you're not deleting anything."* — *PARA, Building a Second Brain*

Move completed or paused projects and superseded material here. Keep the digital
workspace clean so you can start over.

_See [wiki/index.md](wiki/index.md) for the knowledge bundle._
EOF
fi

echo "✔ Wiki scaffolded at: ${OUTPUT} (preset: ${WIKI_PRESET}, kit: ${WIKI_KIT})"
echo "  Open it in Obsidian to browse, and in your agent IDE to maintain."
echo "  Next: drop sources into ${OUTPUT}/raw/ and run the ingest workflow."
