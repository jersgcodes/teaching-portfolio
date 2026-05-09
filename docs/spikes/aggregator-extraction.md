# Spike: Aggregator extraction viability

- Date: 2026-05-07
- Question: Can the aggregator auto-extract enough quality content from existing project files to feed the schema, or do we need significant hand curation?
- Status: Done — recommendation locked.

## Method

Inspected the metadata files actually present in three Tier-1 projects representative of the workspace:

- `erp-mapper` — most polished Python project, complex pipeline
- `smebot` — Telegram bot system with extensive `docs/` folder
- `playo` — TypeScript multiplayer platform, different stack

For each: ran `ls` to enumerate metadata files, then read the head of `CLAUDE.md` and `README.md` where present.

## Findings

### What is reliably available across projects

| File | Across all 3? | Notes |
|---|---|---|
| `CLAUDE.md` | YES | Present in all three; structure varies project to project |
| `TASKS.md` | YES | Standard workspace pattern |
| `USER_ACTIONS.md` | YES | Standard workspace pattern |
| `README.md` | NO (2 of 3) | Present in erp-mapper, smebot; absent in playo |

### What is NOT reliably available

| File | Across all 3? | Notes |
|---|---|---|
| `LEARNINGS.md` | NONE | The original aggregator design assumed this; it does not exist in this sample |
| `docs/adr/` | NONE | Either empty or missing |
| `project-status.yaml` | UNKNOWN | Gitignored across workspace per `.gitignore`; not visible to git but may exist locally |
| `docs/postmortems/` | NONE | Original design source not present |

### Structural variability of CLAUDE.md

Each project's CLAUDE.md uses different headings:

- erp-mapper: `## What this project does`, `## Stack`, `## Architecture principles`, gotchas as freeform `##` sections
- smebot: `## What this is`, `### Module map`, `## Deployment`
- playo: `## Stack`, `## Branching`, `## End-of-build-session checklist`

There is no consistent heading taxonomy. Heuristic extraction by heading text will hit ~50% of cases at best.

### Stack info IS extractable with heuristics

All three CLAUDE.md files mention the stack in plain language near the top. Regex on common keywords (`Python`, `Node.js`, `React`, `FastAPI`, `Telegram`, `Anthropic`, `tRPC`, etc.) reliably surfaces tech_category-level info — which is what the schema actually wants for `mentioned`-tier projects. **Workspace `WORKSPACE_STACKS.md` already does this** via `~/claude/scripts/sync-workspace-stacks.py` — we can reuse its output.

## Decision

**Aggregator = `projects.yaml` + light auto-decoration. NOT auto-extract-everything.**

The aggregator's job in v1:

1. Read `projects.yaml` (canonical source)
2. For each project with a `corpus_path`:
   - Read `CLAUDE.md` (if present) — extract first paragraph below the H1 (likely the "what it does" sentence)
   - Read `README.md` (if present) — alternative source if CLAUDE.md is sparse
   - Run `git log` — first commit date, last commit date, total commit count
   - Count `Status: DONE` lines in `TASKS.md`
   - Cross-reference `WORKSPACE_STACKS.md` for stack info (already maintained)
3. Merge auto-extracted facts with the yaml entry; **yaml fields always win** on conflict
4. Write `data/projects.json`

What the aggregator will NOT do in v1:

- Auto-extract lens content (corporate/builder/deep). Hand-write these in yaml or as separate markdown files per project. ~30 min per project.
- Call any LLM. Pattern X2 (build-time AI generation) is explicitly deferred.
- Synthesise `lessons` from project files. Yaml is the source of truth.

### Why this beats full auto-extraction

- **Quality control.** AI-generated lens content from messy CLAUDE.md is consistently mediocre. Hand-written lens content for 6 Tier-1 projects is ~3 hours of work, once.
- **Privacy enforcement.** `mentioned`-tier rules (no tool names, no infra detail) are easy to enforce when content is hand-written; hard to enforce when an LLM is extracting freely.
- **Schema simplicity.** Aggregator has one job: merge yaml + light decoration. No LLM dependency, no rate limits, no flaky tests.
- **Reversibility.** If we want to add LLM extraction later, the aggregator is already structured to merge it as additional decoration. The yaml stays the source of truth either way.

## Implications for downstream tasks

- **Task 7 (Aggregator MVP):** scope reduced — no LLM dependency in v1. Pure file-system-and-yaml work. Faster TDD cycle.
- **Task 8 (Validators):** unchanged scope — schema check, dedupe, links, attribution, exposure.
- **Lens content authoring:** add as a new task ("Hand-write lens content for 6 Tier-1 projects"). Not blocking aggregator.
- **`WORKSPACE_STACKS.md` reuse:** confirm with workspace owner that aggregator can read this file and trust its output. Otherwise reimplement the stack detection.
- **`LEARNINGS.md` and `docs/adr/`:** deprecated as required inputs. Optional; aggregator reads if present, ignores if not.

## Open questions for human review

1. Confirm: hand-write lens content per Tier-1 project (~30 min each), or accept lower-quality auto-extraction in v1?
2. Confirm: aggregator may consume `WORKSPACE_STACKS.md` directly?
3. For Tier-2 (mention-only) projects: is the projects.yaml content sufficient, or do we want any auto-decoration there too?

## Files referenced

- `~/claude/erp-mapper/CLAUDE.md`, `README.md`
- `~/claude/smebot/CLAUDE.md`
- `~/claude/playo/CLAUDE.md`
- `~/claude/WORKSPACE_STACKS.md`
- `~/claude/scripts/sync-workspace-stacks.py`
