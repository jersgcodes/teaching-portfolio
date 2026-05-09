# Teaching Portfolio — Task Backlog

A two-surface content engine: `growth` (personal/public) + `labs` (work/private team). Shared infra in `content-core` (this repo).

See `CLAUDE.md` for locked architecture and `docs/adr/` for the WHY behind major decisions.

---

## Phase 0 — Foundation

### Task 1 — Lock architecture via /feature-design
- Status: DONE
- Description: Architecture locked. CLAUDE.md updated with locked decisions; 5 ADRs in docs/adr/.
- Done: 2026-05-07

### Task 2 — Repo restructure prep
- Status: DONE (2026-05-07)
- Description: Migration plan for renaming `teaching-portfolio/` -> `content-core/` and creating sibling `growth/` and `labs/` repos.
- Files: `docs/restructure-plan.md`

### Task 3 — Schema design (content-core/schema/v1/)
- Status: DONE (2026-05-07)
- Description: JSON Schema for project, lesson, concept, pattern with attribution and lens fields.
- Files: `schema/v1/{project,lesson,concept,pattern}.json`
- Examples: TODO — add a real example per type for the validators to run against

### Task 4 — Taxonomy definitions
- Status: DONE (2026-05-07)
- Description: 5-stage workflow stages, outcome categories, and lenses as data files.
- Files: `taxonomy/{workflow-5stage,outcomes,lenses}.json`

### Task 5 — projects.yaml
- Status: DONE (2026-05-07)
- Description: 6 Tier-1 projects + 8 Tier-2 mention-only entries; Tier-3 omitted.
- Files: `projects.yaml`
- Note: human review needed on lessons / one-liners / ai_role descriptions before publishing

### Task 6 — AGENTS.md
- Status: DONE (2026-05-07)
- Description: Contribution guide for AI agents and humans.
- Files: `AGENTS.md`

---

## Phase 1 — Aggregator + validators

### Task 6.5 — Spike: aggregator extraction viability
- Status: DONE (2026-05-07)
- Description: Read CLAUDE.md / README.md across 3 Tier-1 projects to assess auto-extraction quality. Found `LEARNINGS.md` and `docs/adr/` are NOT reliably available; CLAUDE.md heading structure varies project-to-project. Decision: aggregator merges `projects.yaml` (canonical) with light auto-decoration only — no LLM extraction in v1.
- Files: `docs/spikes/aggregator-extraction.md`

### Task 6.6 — Python project scaffold
- Status: DONE (2026-05-07)
- Description: `pyproject.toml` (deps, dev deps, ruff/mypy/pytest config). `.pre-commit-config.yaml` from workspace template. `.gitignore` extended for Python tooling. `aggregator/` and `tests/` package skeletons.
- Files: `pyproject.toml`, `.pre-commit-config.yaml`, `.gitignore`, `aggregator/__init__.py`, `tests/__init__.py`

### Task 6.7 — Workspace standardisation (project-overview.yaml)
- Status: DONE (2026-05-07)
- Description: Decided to standardise project metadata at workspace level rather than work around inconsistency in the aggregator. Each project under ~/claude/ owns its own project-overview.yaml. Lens content stays portfolio-side. See ADR 0006.
- Files (workspace): `~/claude/scripts/templates/project-status-schema.json`, `~/claude/scripts/migrate-project-overview.py`, `~/claude/scripts/check-status-freshness.py`, `~/claude/CLAUDE.md` (appended)
- Files (this repo): `docs/adr/0006-workspace-standardised-project-status.md`, slimmed `projects.yaml`, updated `CLAUDE.md` and `AGENTS.md`

### Task 6.8 — Run migration across Tier-1 projects
- Status: DONE (2026-05-07)
- Description: All 6 Tier-1 projects migrated and filled with hand-curated content (no TODO markers remaining): erp-mapper, smebot, sg-sme-profiler, miles-optimizer, news-digest, playo. Each yaml is uncommitted in its respective project repo, awaiting human review and reviewer attribution.
- Files: `~/claude/<slug>/project-overview.yaml` for each Tier-1 slug

### Task 6.9 — Run migration across Tier-2 projects
- Status: PENDING
- Priority: Medium
- Description: For Tier-2 (mention-only) projects, generate stubs and fill the minimum set: title, one_liner, audience, ai_role, lessons. Capabilities/workflow_stages/outcomes can be lighter since lens content isn't authored for Tier-2.
- Slugs: claude-orchestrator, compare-agent, event-radar, sme-radar, sg-sme-maturity, sme-outreach, shared, policy-lens
- Done when: each Tier-2 project has a minimum-fields project-overview.yaml

### Task 6.10 — Cross-project pattern: pipeline vs agent
- Status: DONE (2026-05-07)
- Description: Pattern page written with decision rubric + three side-by-side worked examples (erp-mapper as pipeline-correct, policy-lens as agent-correct, news-digest as either-but-pipeline-chosen-for-cost). Includes common pitfalls and a decision worksheet.
- Files: `content/patterns/pipeline-vs-agent.md`

### Task 6.11 — Cross-project pattern: harness over prompt engineering
- Status: DONE (2026-05-07)
- Description: Pattern page that inverts the "prompt engineering" framing. The harness (output contract, validator, retry policy, fallback, observability, cost guard) carries the load; the prompt does as little as possible. Side-by-side example: same problem solved with pure prompt vs harness-wrapped, showing what fails and why. Three workspace examples: erp-mapper, sg-sme-profiler, smebot.
- Files: `content/patterns/harness-over-prompt-engineering.md`

### Task 6.12 — Cross-project pattern: LLM router with provider fallback
- Status: DONE (2026-05-07)
- Description: Pattern page on the multi-provider router (Gemini -> Claude -> Groq) that 4+ workspace projects depend on. Side-by-side single-provider vs router showing what breaks. Reference implementation lives in `shared/`. Examples: news-digest, compare-agent, event-radar.
- Files: `content/patterns/llm-router-with-fallback.md`

### Task 6.13 — Pattern: privacy-first design
- Status: DONE (2026-05-07)
- Description: Pattern page on architectural privacy (vs marketing privacy). Three honest postures for AI on sensitive data (none, derived features only, local models only). Examples from miles-optimizer (disciplined), spending-monitor (pre-LLM), investment-analyst (two-layer boundary).
- Files: `content/patterns/privacy-first-design.md`

### Task 6.14 — Pattern: idempotent processing with checkpointing
- Status: DONE (2026-05-07)
- Description: Pattern page on cost-bounded re-runs. Side-by-side: naive pipeline vs idempotent + checkpointed on erp-mapper's 7-step subset. Examples: erp-mapper (canonical), news-digest (multi-cadence), miles-optimizer (incremental).
- Files: `content/patterns/idempotent-checkpoint-processing.md`

### Task 6.15 — Harness pattern: prompt-vs-harness slider
- Status: DONE (2026-05-07)
- Description: Added section to existing harness pattern that names the trade-off explicitly: prompt importance scales inversely with both harness strength AND model strength. 2x2 matrix. Affirms the user's "prompt iteration via harness" stance is correct AND addresses constrained environments where harness isn't available.
- Files: `content/patterns/harness-over-prompt-engineering.md` (extended)

### Task 6.16 — Tier-2 migrations
- Status: DONE (2026-05-07)
- Description: All 8 Tier-2 projects have project-overview.yaml filled. Each: minimum required schema fields, 4-6 capabilities, 3-4 lessons. All set to `visibility: mentioned`. Each yaml is uncommitted in its respective project repo.
- Projects done: compare-agent, policy-lens, claude-orchestrator, event-radar, sme-radar, sg-sme-maturity, sme-outreach, shared

### Task 7 — Aggregator MVP
- Status: PENDING
- Priority: High
- Description: Python module: reads `projects.yaml` (registry — slug + tier + overrides) and walks each listed project's `~/claude/<slug>/project-overview.yaml` for canonical facts. Validates against schema. Applies override rules (visibility may only ratchet down). For Tier-1 projects, additionally reads `content/projects/<slug>/lenses/*.md`. Outputs `data/projects.json`. No heuristics, no LLM, no special cases.
- Files: `aggregator/scan.py`, `merge.py`, `output.py`, tests
- Skill: `/tdd` (pure function, filesystem in -> JSON out)
- Done when: produces valid JSON for all registry projects; tests cover override-rule violations and missing-yaml errors

### Task 8 — Validators
- Status: PENDING
- Priority: High
- Description: Schema check (against JSON Schema), dedupe (no clone of existing lesson), link check (no fabricated URLs), attribution-required, infra-exposure check (mentioned-tier projects don't leak tool names).
- Files: `content-core/validators/{schema,dedupe,links,attribution,exposure}.py`, tests
- Skill: `/tdd`
- Done when: each validator catches its target issue with a test

### Task 8.5 — Hand-write lens content for Tier-1 projects
- Status: PENDING
- Priority: High
- Description: For each of the 6 Tier-1 projects, hand-write the corporate / builder / deep lens content in projects.yaml `lenses:` field (or as separate markdown files referenced from yaml). ~30 min per project. Aggregator merges yaml + auto-decoration; lenses are the only fields the LLM can't draft well.
- Files: `projects.yaml` (lenses field), or `content/projects/<slug>/lenses/{corporate,builder,deep}.md` per project
- Done when: all 6 Tier-1 projects have all three lenses populated

### Task 9 — Spike: PDF export approach
- Status: PENDING
- Priority: Medium
- Description: Pick PDF export approach (Puppeteer, weasyprint, Marp, others). Spike before committing.
- Files: `docs/spikes/pdf-export.md` (write-up)
- Skill: `/spike`
- Done when: chosen approach with rationale

### Task 10 — Spike: moodboard summariser shape
- Status: PENDING
- Priority: Medium
- Description: Given a `labs/inbox/<file>.md`, what does the summariser actually produce? Try Claude API on real-ish input. Produce a sample Excalidraw + agenda + decisions-needed file. Refine output shape before TDD'ing the tool.
- Files: `docs/spikes/moodboard-prep.md`
- Skill: `/spike`
- Done when: sample output exists and reads well in a meeting context

---

## Phase 2 — Sites scaffold

### Task 11 — growth site scaffold
- Status: PENDING
- Priority: High
- Description: Next.js (static export). App router. Submodule pointer to content-core. Layout, navigation, project page template, lesson page template, ai-fluency page template, about page template.
- Files: `growth/` repo
- Skill: direct + `/style-check`
- Done when: builds locally; one Tier-1 project page renders

### Task 12 — labs site scaffold
- Status: PENDING
- Priority: High
- Description: Next.js (static export). Same scaffold as growth. Adds meeting page template (`/meetings/<date>`), inbox view, export button (PDF).
- Files: `labs/` repo
- Skill: direct + `/style-check`
- Done when: builds locally; placeholder labs landing renders

### Task 13 — Shared components in content-core
- Status: PENDING
- Priority: High
- Description: Lens toggle, 5-stage workflow badge, outcome tag, attribution display, Excalidraw embed, mood-board renderer, last-updated date pulled from git.
- Files: `content-core/components/`
- Skill: direct + `/style-check`
- Done when: each component renders in both sites

### Task 14 — Cloudflare Pages deployment
- Status: PENDING
- Priority: Medium
- Description: Two Cloudflare Pages projects (growth + labs). Custom domains. Cloudflare Web Analytics on growth.
- Files: deployment notes in `docs/deployment.md`
- Done when: both sites live at their domains

### Task 15 — Cloudflare Access on labs
- Status: PENDING
- Priority: Medium
- Description: Cloudflare Access app gating `labs.jersgcodes.com`. M365 SSO if available; else email-OTP. Allowlist team members.
- Files: deployment notes
- Done when: unauthenticated requests to labs hit the Access challenge; team members log in successfully

---

## Phase 3 — MVP content

### Task 16 — Tier-1 project pages (growth)
- Status: PENDING
- Priority: High
- Description: Aggregator produces all 6 Tier-1 project pages on growth. Hand-fill any missing fields in projects.yaml.
- Files: `projects.yaml`, generated pages
- Done when: erp-mapper, smebot, sg-sme-profiler, miles-optimizer, news-digest, playo all have pages with all three lenses populated

### Task 17 — /ai-fluency page (growth)
- Status: PENDING
- Priority: High
- Description: Aggregated page explaining the 5-stage workflow + outcome categories with examples drawn from the Tier-1 projects.
- Files: `growth/content/ai-fluency.md`, generated page
- Done when: page reads cleanly, links to relevant project examples

### Task 18 — /use-cases page (growth)
- Status: PENDING
- Priority: Medium
- Description: Sorted by outcome category. Corporate-lens entry point.
- Files: generated page from outcome-tagged content
- Done when: each outcome category has at least one project example

### Task 19 — About page (growth)
- Status: PENDING
- Priority: Medium
- Description: Brief, honest, links to projects. Avoids overclaiming.
- Files: `growth/content/about.md`
- Done when: page is published

### Task 20 — Tier-2 mention cards (growth)
- Status: PENDING
- Priority: Low
- Description: Mention-only entries for the 8 Tier-2 projects. No infra, no architecture; just title + use case + lessons.
- Files: projects.yaml updates, aggregator coverage
- Done when: mention cards render on the projects index

---

## Phase 4 — Mood-board + export

### Task 21 — moodboard-prep tool
- Status: PENDING
- Priority: High
- Description: CLI in `content-core/tools/moodboard-prep/`. Reads inbox markdown, calls Claude API, produces Excalidraw + agenda + decisions-needed in a meeting folder.
- Files: `content-core/tools/moodboard-prep/{pull.py,summarise.py,render.py}`, tests, README
- Skill: `/spike` (Task 10) -> `/tdd`
- Done when: produces a usable meeting kit from a real inbox file

### Task 22 — Meeting template + first labs meeting
- Status: PENDING
- Priority: Medium
- Description: Set up the `labs/meetings/<date>/` convention. Run the moodboard-prep tool ahead of one real meeting to validate the workflow.
- Files: `labs/meetings/<date>/`
- Done when: one real meeting used the artifact

### Task 23 — PDF greenlight export
- Status: PENDING
- Priority: Medium
- Description: From any labs page, produce a PDF deck suitable for boss greenlight. Approach picked in Task 9 spike.
- Files: `content-core/tools/pdf-export/`, `labs/` integration
- Skill: `/spike` -> direct
- Done when: a labs page exports to a presentation-quality PDF

---

## Phase 5 — Cross-cutting patterns

### Task 24 — Pattern: LLM router with provider fallback
- Status: PENDING
- Priority: Low
- Description: Lifted from compare-agent + news-digest + others. Cross-project pattern page on growth.
- Files: `growth/content/patterns/llm-router-fallback.md`
- Done when: pattern page links to the projects that use it

### Task 25 — Pattern: privacy-first design
- Status: PENDING
- Priority: Low
- Description: Lifted from spending-monitor, miles-optimizer, investment-analyst. Even though those projects are Tier-3, the pattern is publishable.
- Files: `growth/content/patterns/privacy-first.md`
- Done when: pattern page exists

---

## Cross-cutting deferred (post-v1)

- Build-time AI generation (Pattern X2)
- Runtime AI explainer (Pattern X3)
- External contribution paths beyond team PRs (Discord, public form, GPT Action)
- Asset-handoff pipeline for corporate
- MCP server
- Side-by-side model comparison pages (Pattern delta)
- Search (Pagefind), RSS, comments, newsletter
- Multi-language

---

## Skill routing summary

| Step | Skill |
|---|---|
| Schema design | direct |
| Aggregator | `/tdd` |
| Validators | `/tdd` |
| moodboard-prep | `/spike` -> `/tdd` |
| PDF export | `/spike` -> direct |
| Site chrome | direct + `/style-check` |
| Components | direct + `/style-check` |
| Repo restructure | direct (manual file ops) |
