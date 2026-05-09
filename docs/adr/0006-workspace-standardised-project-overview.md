# ADR 0006 — Workspace-standardised `project-overview.yaml`

- Status: Accepted
- Date: 2026-05-07

## Naming note

This file (`project-overview.yaml`) is **distinct** from the existing `project-status.yaml` that the orchestrator wrap-up skill auto-generates per project (and which is workspace-gitignored). Different lifecycles, different purposes:

| File | Source | Lifecycle | Tracks |
|---|---|---|---|
| `project-status.yaml` | Orchestrator (auto) | Regenerated on wrap-up | APIs, dependencies, triggers, last-scan time |
| `project-overview.yaml` | Human (hand-written) | Updated when capabilities change | Title, audience, capabilities, lessons, visibility, lens taxonomy |

Both files coexist in `~/claude/<slug>/`. A future consolidation (modify orchestrator to preserve hand-written fields in a single file) is a candidate for v1.5 but not in scope today — see "Open question (deferred)" below.

## Context

The aggregator spike (`docs/spikes/aggregator-extraction.md`) found that metadata files across the 20 workspace projects are inconsistent: `LEARNINGS.md` is rarely present, `docs/adr/` is often empty, and `CLAUDE.md` heading structure varies project to project. Heuristic auto-extraction would be fragile and quality-variable.

A second issue surfaced when discussing storage of lens content (corporate / builder / deep narratives per project): mixing source-of-truth with editorial framing in the same file conflates "what is this project" (project's concern) with "how shall we present it" (portfolio's concern). Updating the portfolio narrative shouldn't require touching every project repo.

## Options considered

### A. Live with inconsistency; aggregator works around it
Heuristics + LLM fallback per project; per-project special cases.

- **Pros:** no upstream changes
- **Cons:** quality variable; aggregator complex; LLM dependency for fields that are simple facts; failure mode is silent (a missing field becomes an empty page section).

### B. Standardise at workspace level; portfolio reads structured data (chosen)
Every project under `~/claude/` declares its own metadata in a standard `project-overview.yaml`. Portfolio aggregator reads each project's yaml directly. Lens content stays portfolio-side as a separate authoring step.

- **Pros:** single source of truth per project; no heuristics; aggregator becomes trivial; project owners maintain their own metadata; portfolio voice stays decoupled from project facts.
- **Cons:** 20 projects need migration; ongoing maintenance burden per project (mitigated by freshness checker).

### C. Standardise just the portfolio's `projects.yaml`; project files unchanged
All metadata centralised in this repo.

- **Pros:** zero project-level changes
- **Cons:** project owner (you) is also portfolio owner — centralising means you maintain everything in one file as projects grow. Rejected: doesn't scale, doesn't model good practice for distributed authorship if/when others contribute.

## Decision

**Workspace-standardised `project-overview.yaml` per project; lens content lives portfolio-side.**

### What lives where

| Concern | File | Layer | Updated when |
|---|---|---|---|
| Project facts (title, status, capabilities, ai_role, tech_category, lessons) | `~/claude/<slug>/project-overview.yaml` | Project | Project evolves |
| Workflow / outcome tags (which 5-stage axes apply, what value the project produces) | `~/claude/<slug>/project-overview.yaml` | Project | Project evolves |
| Visibility ceiling (max permitted public exposure) | `~/claude/<slug>/project-overview.yaml` | Project | Sensitivity changes |
| Portfolio inclusion / tier / overrides | `projects.yaml` (in this repo) | Portfolio | Editorial decision |
| Lens narrative content (corporate / builder / deep) | `content/projects/<slug>/lenses/{corporate,builder,deep}.md` (in this repo) | Portfolio | Tier-1 promotion |

### Schema location

`~/claude/scripts/templates/project-overview-schema.json` (JSON Schema draft-07). The portfolio's project schema (`schema/v1/project.json`) is a superset — includes the project-side fields plus portfolio-only fields like `lenses`.

### Visibility semantics

- Project's `visibility` field = **maximum permitted exposure**. Default `hidden`. Explicit opt-in to `mentioned` or `public`.
- Portfolio's `projects.yaml` may **override DOWN** (more restrictive) but never up. Validator enforces.
- Result: a project is the floor on its own exposure; the portfolio can choose to under-expose for editorial reasons.

### Tooling

- `~/claude/scripts/migrate-project-overview.py` — generates stub `project-overview.yaml` for projects without one. Inserts TODO markers; never overwrites.
- `~/claude/scripts/check-overview-freshness.py` — flags projects where yaml `last_updated` is more than 30 days behind the latest git commit.
- `~/claude/scripts/sync-workspace-stacks.py` (existing) — produces `WORKSPACE_STACKS.md`. Migration script reads it for `tech_category` defaults.

## Consequences

- The portfolio aggregator (Task 7) reduces to: read each project's `project-overview.yaml`, validate against schema, merge with portfolio registry overrides, output JSON. No heuristics, no LLM, no special cases.
- Each existing project must be migrated. Migration is run manually per project so the human can review and fill TODO markers before commit.
- New projects must include `project-overview.yaml` from day one. The workspace `new-project.sh` will be updated **only after the standard is proven** on the existing 20 projects.
- Freshness checker runs as a manual CLI tool for now. A pre-commit warning hook is a candidate for v1.5 once we have a sense of how often files actually drift.
- The portfolio's `projects.yaml` shrinks dramatically — becomes a registry of slugs + visibility overrides + tier overrides + ordering hints, not a data store.
- AGENTS.md is updated to reflect the new contribution paths: AI agents contributing project metadata write `project-overview.yaml`; AI agents contributing lens content write `content/projects/<slug>/lenses/*.md`.
- Workspace `CLAUDE.md` is updated to add `project-overview.yaml` to the "Project structure standards" requirement.

## Open question (deferred)

Whether to make freshness a pre-commit blocker (current: manual CLI). Decide after first quarter of usage.
