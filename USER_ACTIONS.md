# User Actions

After each build session, Claude adds an entry here. Most recent at the top.

---

## 2026-05-07 — Source material: AI Fluency for Educators

### Built
- `sources/` directory created (new convention for committed-in reference material that informs portfolio writing but is not itself published)
- `sources/ai-fluency-educators.md` — notes from an Anthropic course on AI Fluency for Educators, preserved verbatim with a thin frame:
  - Source attribution and intended-use header
  - 4D ↔ 5-stage workflow crosswalk explaining how the educator framing maps to our locked taxonomy
  - Inline portfolio notes flagging where specific concepts could become content (e.g. "AI as perspective-taker" pattern; Teaching Context Document parallel to our project-overview.yaml)
- Updated `CLAUDE.md` to introduce the `sources/` convention

### Why this matters
The 4D framework is widely taught (Anthropic's own educator course is a major surface). Our 5-stage workflow uses different vocabulary but maps cleanly. Capturing the crosswalk explicitly means a 4D-trained reader can navigate our portfolio without friction — and we can write educator content that honours both framings.

### Test on your device
- [ ] Read `sources/ai-fluency-educators.md` — verify the crosswalk feels honest and the inline portfolio notes match your intent
- [ ] Confirm the 4D ↔ 5-stage mapping (especially Diligence's "split between Document and cross-cutting" framing)
- [ ] Decide whether the future `/educators` content should be its own collection on growth, or absorbed into existing pages

### Decisions surfaced
- The Teaching Context Document concept (Lesson 1) is the same shape as our project-overview.yaml — worth name-checking the parallel when we write educator content
- "Ask AI to act as one of my students" generalises to "act as a sceptical reader / junior dev / regulator" — pattern candidate

---

## 2026-05-07 — Remaining Tier-2 migrations complete (8 of 8)

### Built
- `~/claude/claude-orchestrator/project-overview.yaml` — `ai_role: none`. Read-only Telegram dashboard aggregating workspace state.
- `~/claude/event-radar/project-overview.yaml` — `ai_role: core`. SG event scraper + LLM scoring with one-way module dependency rules.
- `~/claude/sme-radar/project-overview.yaml` — `ai_role: core`. Two-axis scoring (relevance × signal) with HIGH/MID/LOW tiers.
- `~/claude/sg-sme-maturity/project-overview.yaml` — `ai_role: none`. Pure data engineering reference layer; layered build (L0 -> L4).
- `~/claude/sme-outreach/project-overview.yaml` — `ai_role: helper`. 4-dimension scoring + ACRA classifier with QA smell detectors.
- `~/claude/shared/project-overview.yaml` — `ai_role: helper`. The LLMRouter library itself; small intentional surface.

### Final agentic distribution across the workspace

| `agentic` | Count | Projects |
|---|---|---|
| `yes` | 1 | policy-lens (multi-agent: Discovery -> [Analyst | Economist] -> Synthesizer) |
| `partial` | 1 | smebot (vent module is multi-turn AI within a mostly-single-call system) |
| `no` | 12 | erp-mapper, sg-sme-profiler, news-digest, playo, claude-orchestrator, event-radar, sme-radar, sg-sme-maturity, sme-outreach, shared, compare-agent, miles-optimizer |

Genuine agentic content in this workspace is thin, as predicted. The portfolio's stance — "most production AI work is bounded prompts + pipelines, not agents" — is now substantiated by the data.

### Test on your device
- [ ] Spot-check each of the 6 new yamls — particularly `audience` and `lessons`
- [ ] `sg-sme-maturity` is in active build (L1 in flight per its own CLAUDE.md); confirm `status: building` is correct
- [ ] `claude-orchestrator`'s "Personal — me" audience is honest but might be worth softening if you want it more shareable
- [ ] `shared` is positioned as the LLMRouter library — if you want it framed differently (e.g. as the LLMRouter pattern's reference implementation), say so

### Migration progress

| Tier | Done | Remaining |
|---|---|---|
| Tier-1 (full lens) | 6 | 0 |
| Tier-2 (mention-only) | 8 | 0 |
| Tier-3 (skipped) | 0 | (intentionally not migrated: spending-monitor, investment-analyst, market-intel, nutrilens, wip-next, moonshot-sme-governance) |

### What's now possible
- Aggregator (Task 7) has 14 fixtures across both tiers — TDD-friendly
- Pattern pages have all referenced projects backed by real metadata
- Freshness checker can run meaningfully now that yamls exist

---

## 2026-05-07 — Two more patterns + first Tier-2 migrations

### Built
- **Extended `harness-over-prompt-engineering.md`** with the prompt-vs-harness slider — names the trade-off explicitly: prompt importance scales inversely with both harness strength AND model strength. 2x2 matrix included. Addresses corporate-restricted environments where the harness isn't available.
- **`content/patterns/privacy-first-design.md`** — pattern on architectural privacy (vs marketing privacy). Three honest postures for AI on sensitive data: none / derived features only / local models. Examples from miles-optimizer, spending-monitor, investment-analyst.
- **`content/patterns/idempotent-checkpoint-processing.md`** — pattern on cost-bounded re-runs. Side-by-side: naive vs idempotent on erp-mapper's pipeline. Examples from erp-mapper, news-digest, miles-optimizer.
- **`~/claude/compare-agent/project-overview.yaml`** — Tier-2 mention-only filling. Strong concrete example for the LLM-router pattern (uses LLMRouter as architectural premise).
- **`~/claude/policy-lens/project-overview.yaml`** — Tier-2 fill, `agentic: yes` (the genuine multi-agent reference). Status `building` since the project itself flags Phase 2 work pending.

### On the prompt-vs-harness slider question
The user asked whether prompt becomes more important in constrained environments (no harness, weaker models). Answer: yes — it's a slider, not a binary. Both axes (harness strength + model strength) push prompt importance up when weakened. The harness pattern now captures this honestly — including the harder truth that constrained-env + weak-model has a low ceiling no amount of prompt tuning fixes.

### Patterns now form a teaching arc
The five published patterns compose:
1. `pipeline-vs-agent` — what shape
2. `harness-over-prompt-engineering` — how to make the shape reliable
3. `llm-router-with-fallback` — provider resilience as one harness layer
4. `privacy-first-design` — when sensitive data constrains the architecture (rules out cloud LLMs in many cases)
5. `idempotent-checkpoint-processing` — cost discipline for any pipeline-shaped system

Each cross-references the others. A reader landing on any of them can find the others via the See Also section.

### Test on your device
- [ ] Read both new patterns — push back on opinions / framings
- [ ] Verify policy-lens's `agentic: yes` characterisation matches your design intent
- [ ] Confirm compare-agent's `agentic: no` (the clarifier asks follow-ups but it's a single decision point)
- [ ] Check the prompt-vs-harness slider section feels right — particularly the "low ceiling" claim for constrained-env + weak-model

### Remaining Tier-2 migrations
6 left: claude-orchestrator, event-radar, sme-radar, sg-sme-maturity, sme-outreach, shared. These are quicker since the pattern is established and the schema fields are well-understood.

---

## 2026-05-07 — Two more cross-project patterns: harness + LLM router

### Built
- `content/patterns/harness-over-prompt-engineering.md` — pattern page inverting the "prompt engineering" framing. The harness (output contract, validator, retry, fallback, observability, cost guard) carries the load; the prompt does less. Side-by-side: pure-prompt vs harness-wrapped on the same problem (erp-mapper's IMDA category mapping). Three workspace examples and a 7-step "how to start a harness" checklist.
- `content/patterns/llm-router-with-fallback.md` — pattern page on the multi-provider router. Side-by-side: single-provider vs router on the same problem (news-digest summarisation). The workspace `LLMRouter` (Gemini -> Claude -> Groq) is the reference implementation; 4+ projects consume it.

### Why these two together
Both patterns answer different parts of the same production-AI question: how do you make LLM calls reliable? The router handles "which provider answered" (resilience to outages, quota, rate limits). The harness handles "is the answer usable" (contracts, validators, retries, fallbacks). They compose: the router is one layer of the harness.

### On the user's stance: harness > prompt engineering
The user expressed uncertainty about whether their preference for "prompt iteration via harness" rather than "prompt engineering" was best practice. The pattern page explicitly affirms it IS best practice, with workspace evidence (erp-mapper, sg-sme-profiler, smebot) showing that the prompts in production-quality projects are short and the harnesses around them carry the structural load. Industry consensus has shifted in this direction over the last 18 months — the user's instincts are well-aligned.

### Test on your device
- [ ] Read both pattern pages — push back on any framing that overstates or understates
- [ ] Particularly the "free-tier rotation as primary architecture is fragile for revenue-bearing systems" line in the LLM router page — confirm that matches your view
- [ ] Confirm the side-by-side examples use realistic-enough versions of the actual code (the snippets are pseudocode; verify they don't misrepresent how erp-mapper or news-digest actually work)

### Decisions surfaced this session
- The portfolio's strongest cross-cutting teaching themes are now captured as three patterns (pipeline-vs-agent, harness-over-prompt, llm-router-with-fallback)
- Each pattern uses parallel worked examples to make the point concrete rather than abstract
- The user's "harness > prompt engineering" stance is well-founded and now publishable

---

## 2026-05-07 — Pattern page: pipeline vs agent

### Built
- `content/patterns/pipeline-vs-agent.md` — full pattern page with frontmatter conforming to schema/v1/pattern.json
- Three side-by-side worked examples grounded in real workspace projects:
  - **erp-mapper** as pipeline-correct (steps known, inputs bounded, regulatory artifact)
  - **policy-lens** as agent-correct (open-ended question space, synthesis is the work)
  - **news-digest** as either-but-pipeline-chosen-for-cost (acknowledged trade-off)
- Decision rubric (8 questions, lean-left vs lean-right answers)
- Common pitfalls section (calling long pipelines "agentic", single LLM calls "agentic", resume-driven agent adoption, refusing to mix shapes)
- Decision worksheet (5 questions to answer before picking a shape)

### Why this matters
The "pipeline vs agent" decision is the single most-confused architectural call in production AI today. Most builders default-assume agentic = modern = better. The portfolio's contribution is teaching the inverse: most production AI is pipeline-shaped, and that's correct. Three real examples (one per verdict) make the rubric concrete rather than hand-wavy.

### Test on your device
- [ ] Read `content/patterns/pipeline-vs-agent.md` — push back on any of the three example verdicts
- [ ] Particularly check the **policy-lens** example — it's projected (the project is in build phase per its overview); confirm the agentic framing matches your design intent
- [ ] Confirm the **news-digest** trade-off framing — "agentic would be better but cost says pipeline" is a strong claim; verify it matches your view

### Deploy / setup steps
- [ ] Once content-core / growth split is built, this file moves to `growth/content/patterns/pipeline-vs-agent.md`
- [ ] When the lessons aggregator runs, this pattern's `examples[]` references should resolve cleanly to project pages

### Decisions worth remembering
- "Length isn't autonomy" — a 25-step pipeline is not agentic
- "Sometimes agentic would be better but the budget says pipeline" is an honest call, not a failure
- Mixed shapes (deterministic core + agentic edge) are the most common production answer

---

## 2026-05-07 — All six Tier-1 project-overview files filled

### Built
- `~/claude/miles-optimizer/project-overview.yaml` — `ai_role.role: none` (deliberately AI-free runtime; privacy-first stance is incompatible with sending transactions to LLMs). Earlier survey claim of "Haiku for MCC inference" was incorrect; corrected.
- `~/claude/news-digest/project-overview.yaml` — `ai_role.role: core`, agentic: no. Cost/cadence pattern (free embeddings frequent, paid LLM rare) is teaching-grade content.
- `~/claude/playo/project-overview.yaml` — `ai_role.role: helper`, agentic: no. AI used only at the content edge (trivia question generation), never in the live game loop.
- Added a new lesson to `~/claude/erp-mapper/project-overview.yaml` capturing the "pipeline beats agent when steps are known" reasoning — directly answers the user's question about whether erp-mapper could/should be agentic.

### All six Tier-1 projects now have filled project-overview.yaml

| Project | role | agentic | Why agentic call holds |
|---|---|---|---|
| erp-mapper | core | no | 25 known steps; reproducibility/auditability outweigh agent flexibility |
| smebot | core | partial | Vent module multi-turn AI is mildly agentic; rest is single-call |
| sg-sme-profiler | core | no | Bounded concurrent + sequential prompts |
| miles-optimizer | none | no | Deliberately no AI in runtime — privacy stance |
| news-digest | core | no | Single-call summarisation per cluster |
| playo | helper | no | AI for content gen only, not in live game loop |

### Test on your device
- [ ] Read each filled yaml — focus on lessons (these are publishable) and audience (these frame the project)
- [ ] Verify `ai_role.role: none` for miles-optimizer — confirm there really is no AI in the runtime
- [ ] Confirm playo's GitHub/live-site link (https://playo.jersgcodes.com) is current
- [ ] Confirm miles-optimizer's GitHub link (https://github.com/jersgcodes/miles-optimiser) is correct

### Deploy / setup steps
- [ ] After review per project: add `{ role: reviewed, by: Jerome, when: <date> }` and commit in each project repo
- [ ] Decide whether to start Task 6.9 (Tier-2 migrations) or jump to Task 7 (aggregator) since 6 fixtures are enough to TDD against

### Decisions made / surfaced this session
- erp-mapper is correctly NOT agentic — added as an explicit lesson
- "Pipeline vs agent" is teaching-grade content worth lifting to a cross-project pattern (Task 6.10)
- The genuine agentic content in this workspace is thin — only policy-lens (Tier-2) plus smebot's vent module qualify. The portfolio can teach what agentic IS by showing what it ISN'T

---

## 2026-05-07 — First three Tier-1 project-overview migrations + agentic field

### Built
- Migrated and filled `project-overview.yaml` for three Tier-1 projects:
  - `~/claude/erp-mapper/project-overview.yaml` (agentic: no)
  - `~/claude/smebot/project-overview.yaml` (agentic: partial — vent module)
  - `~/claude/sg-sme-profiler/project-overview.yaml` (agentic: no)
- Added `ai_role.agentic` field (required, enum: yes/no/partial) to both schemas (workspace + this repo) — distinguishes single-call AI / pipelines of bounded prompts (no) from multi-step autonomous reasoning (yes/partial)
- Updated migration script's stub template to include the new field
- Updated AGENTS.md with explicit "be honest about agentic" guidance — a deterministic 25-step pipeline is NOT agentic

### Why the agentic distinction matters
Agentic AI is a frequently-used buzzword. The portfolio is a teaching artifact — it should make the distinction sharp, not blurry. Among the workspace projects to date, only the eventual `policy-lens` migration (multi-agent flow: discovery -> analyst -> economist -> synthesizer) and `smebot`'s vent module qualify as agentic. Most projects are pipelines of bounded prompts, not agents.

### Test on your device
- [ ] Read each filled yaml — push back on lessons, capabilities, or audience that feel off
- [ ] Confirm the `agentic: no/partial` calls — particularly smebot's "partial" (justifiable but borderline)
- [ ] Decide whether to add a deployment link to sg-sme-profiler when the URL is finalised

### Deploy / setup steps
- [ ] Per project, after review: add `{ role: reviewed, by: Jerome, when: <date> }` to `authors[]` and commit in the project repo
- [ ] Continue with miles-optimizer / news-digest / playo for the remaining Tier-1 migrations

### Decisions made this session
- `ai_role.agentic` is now required across all project-overview.yaml — explicit honest tracking, not buried in description
- `visibility` field clarified as portfolio rendering ceiling only — deployment access state goes in link labels
- Link convention documented (Option C — label-suffix carries `(login required)` etc.)

---

## 2026-05-07 — Workspace standardisation (project-overview.yaml)

### Naming note
Mid-session discovery: `project-status.yaml` is **already in use** as an orchestrator-generated, gitignored file tracking APIs and dependencies per project. The new hand-written file was renamed to `project-overview.yaml` to avoid collision. The two coexist with different lifecycles. Future v1.5 work could consolidate them by modifying the orchestrator wrap-up skill — out of scope today.

### Built (workspace-level — touches `~/claude/`)
- `~/claude/scripts/templates/project-overview-schema.json` — JSON Schema for the new workspace standard
- `~/claude/scripts/migrate-project-overview.py` — generates stub `project-overview.yaml` for each existing project; never overwrites
- `~/claude/scripts/check-overview-freshness.py` — flags drift between yaml `last_updated` and git activity (manual CLI; no hook yet)
- `~/claude/CLAUDE.md` — added `project-overview.yaml` to "Project structure standards" + "Automatic systems" table, with explicit note that it is distinct from `project-status.yaml`

### Built (in this repo)
- `docs/adr/0006-workspace-standardised-project-status.md` — captures the decision and trade-offs
- `projects.yaml` — slimmed dramatically: now a portfolio registry (slug + tier + optional overrides) rather than a data store
- `CLAUDE.md` — updated "Where data lives" and visibility model sections
- `AGENTS.md` — updated file locations table; added "Contributing project metadata" + "Contributing lens content" sections
- `TASKS.md` — Task 6.7 (workspace standardisation) marked DONE; Task 6.8 (run migration) added; Task 7 (aggregator) re-scoped to read project-overview.yaml directly

### Why this changes the aggregator
The aggregator (Task 7) becomes trivial: read each listed project's `~/claude/<slug>/project-overview.yaml`, validate, apply override rules from `projects.yaml`, output JSON. No heuristics, no LLM, no special cases. The cost was moved upstream: each project now owns its own metadata file.

### Test on your device
- [ ] Read `docs/adr/0006-workspace-standardised-project-status.md` — confirm the workspace-level decision sits well with you
- [ ] Run `python3 ~/claude/scripts/migrate-project-overview.py --list` to see which projects need migration
- [ ] Run `python3 ~/claude/scripts/migrate-project-overview.py --project erp-mapper --dry-run` to preview a single migration before writing
- [ ] Spot-check the schema at `~/claude/scripts/templates/project-overview-schema.json` — push back on any field

### Deploy / setup steps
- [ ] When ready: run the migration **one project at a time** (`--project <slug>`), fill TODO markers, commit per project
- [ ] Add `python3 ~/claude/scripts/check-overview-freshness.py` to your monthly maintenance ritual
- [ ] Defer: pre-commit hook for staleness (calibrate first)
- [ ] Defer: updating `~/claude/scripts/new-project.sh` until standard is proven on existing projects

### Decisions made this session
- Workspace standardisation YES (over per-aggregator workarounds)
- Lens content lives portfolio-side (separate from project facts)
- Visibility = max permitted exposure on project; portfolio overrides DOWN only
- Default visibility for new projects = `hidden` (explicit opt-in to share)
- Freshness checker = manual CLI tool for v1; pre-commit hook deferred to v1.5

---

## 2026-05-07 — Python scaffold + aggregator spike

### Built
- `pyproject.toml` (Python 3.11+, ruff/mypy/pytest/bandit/radon/vulture configured)
- `.pre-commit-config.yaml` from workspace Python template (ruff, bandit, mypy, vulture, radon, pip-audit, detect-secrets, no-commit-to-main)
- `.gitignore` extended with Python tooling caches and `data/` (aggregator output)
- `aggregator/__init__.py` + `tests/__init__.py` package skeletons
- `docs/spikes/aggregator-extraction.md` — spike report on auto-extraction viability
- TASKS.md updated: Task 6.5 (spike) + Task 6.6 (scaffold) marked DONE; Task 7 (aggregator) scope reduced (no LLM); Task 8.5 (hand-write lens content) added

### Key spike finding
`LEARNINGS.md` and `docs/adr/` are NOT reliably present across Tier-1 projects. CLAUDE.md heading structure also varies. Decision: aggregator becomes "merge yaml + light auto-decoration" rather than "auto-extract everything." Lens content is hand-written per Tier-1 project (~30 min each).

### Test on your device
- [ ] Read `docs/spikes/aggregator-extraction.md` — push back on the design call (auto-extract vs hand-curate)
- [ ] Spot-check the open questions at the bottom of the spike — particularly whether `WORKSPACE_STACKS.md` reuse is OK
- [ ] Confirm: `~30 min per project` to hand-write 3 lenses each is acceptable

### Deploy / setup steps
- [ ] When ready to begin aggregator implementation: install Python deps with `pip install -e ".[dev]"`, then `pre-commit install`
- [ ] Create `.secrets.baseline` for detect-secrets: `detect-secrets scan > .secrets.baseline`

### Decisions still needed
- [ ] Auto-extraction tier for Tier-2 (mention-only) projects: yaml-only, or also auto-decorate?
- [ ] Lens content storage: inline in `projects.yaml`, or separate markdown files per project?

---

## 2026-05-07 — foundation files (Phase 0 + start of Phase 1)

### Built
- `docs/restructure-plan.md` — execution playbook for renaming `teaching-portfolio/` -> `content-core/` and creating `growth/` + `labs/` sibling repos with submodule wiring (Task 2)
- `schema/v1/{project,lesson,concept,pattern}.json` — JSON Schema draft-07 definitions for all four content types, with attribution required (Task 3)
- `taxonomy/{workflow-5stage,outcomes,lenses}.json` — controlled vocabularies for the two teaching axes and three reader lenses (Task 4)
- `projects.yaml` — 6 Tier-1 projects + 8 Tier-2 mention-only entries; Tier-3 deliberately omitted (Task 5)
- `AGENTS.md` — contribution guide for AI agents and humans, per-surface voice, attribution rules, file locations, inbox format (Task 6)
- TASKS.md updated: Tasks 2-6 marked DONE

### Test on your device
- [ ] Read `docs/restructure-plan.md` — validate the migration steps before running them in a future session
- [ ] Skim `AGENTS.md` — does the voice guidance match your intent for growth vs labs?
- [ ] Spot-check `projects.yaml` — the lessons / one-liners / ai_role descriptions are AI-drafted from the workspace survey; review before publishing
- [ ] Glance at the four schema files — are any fields missing for your use case, or is anything over-specified?
- [ ] Glance at the three taxonomy files — push back on stage names, outcome wording, or lens descriptions

### Deploy / setup steps
- [ ] None yet — still no commit, no repos, no scaffolding
- [ ] When ready: commit `feat/design-lock` -> create GitHub repo for content-core -> begin restructure per `docs/restructure-plan.md`

### Decisions still needed
- [ ] Confirm `content-core` is public (default) or flip private
- [ ] Final pass on `projects.yaml` — promote / demote / drop any entries before first publish

---

## 2026-05-07 — design lock via /feature-design

### Built
- Long `/feature-design` session that locked the architecture end-to-end
- Surveyed all 20 workspace projects via Explore subagent; tiered into Share / Mention-only / Skip
- Switched from single-purpose teaching portfolio to two-surface content engine:
  - `growth` (personal/public) at `growth.jersgcodes.com`
  - `labs` (work team/private) at `labs.jersgcodes.com` (Cloudflare Access gated)
  - `content-core` (this repo) as shared infra (public)
- Rewrote `CLAUDE.md` to reflect locked architecture
- Rewrote `TASKS.md` with phased backlog (5 phases, 25 tasks)
- Created `docs/adr/` with 5 ADRs documenting load-bearing decisions
- Moved off main onto `feat/design-lock` branch (prior dirty files carried with)

### Test on your device
- [ ] Review `CLAUDE.md` — confirm locked architecture matches your intent
- [ ] Review `TASKS.md` — push back on priorities or scope
- [ ] Review the 5 ADRs in `docs/adr/` — push back on the WHY of any decision
- [ ] Decide whether `content-core` should be public (default) or private

### Deploy / setup steps
- [ ] None yet — design-lock checkpoint, no code or scaffolding written
- [ ] When ready to execute: start a build session for Phase 0 (repo restructure prep)

### Decisions needed
- [ ] Confirm or override `content-core` public visibility
- [ ] Repo rename strategy: rename `teaching-portfolio/` -> `content-core/` in place, or migrate to a fresh directory?
- [ ] When to begin execution? (Phase 0 will take ~1 session of focused work)

### Locked decisions reference
- See full block in `CLAUDE.md`
- ADRs in `docs/adr/0001-*.md` through `0005-*.md`

### Notable scope decisions
- Labs is **fully private** (no public face, no SEO needed); public publishing is corporate's responsibility via separate channels — labs produces export-ready assets
- External contribution paths (Discord, public form, GPT Action) **deferred** to v1.5+
- Build-time/runtime AI generation (Patterns X2/X3) **deferred**
- MCP server **deferred** (free protocol, but not v1 critical)
- Search, RSS, comments, multi-language **deferred**
- Discussion-space tool TBD by work lead (Loop / OneNote / Word) — pipeline ingests via paste-into-inbox

---

## 2026-05-05 — project skeleton + scoping

### Built
- Created `~/claude/teaching-portfolio/` with `git init`
- `CLAUDE.md` with proposed architecture, data sources, site structure, open questions
- `TASKS.md` with 12 tasks across 3 phases (Foundation, MVP, Teaching content)
- `USER_ACTIONS.md` (this file)

### Test on your device
- [ ] Review `CLAUDE.md` — confirm site structure and audience match your intent
- [ ] Review `TASKS.md` — adjust priorities, add/remove tasks

### Deploy / setup steps
- [ ] None (project is just scoping at this point)

### Decisions needed
- Open questions in `CLAUDE.md`:
  1. SSG choice (Astro / Next.js / 11ty / Hugo)
  2. Auto-pull vs hand-curated content
  3. Privacy filter rules — which projects are public
  4. Friendly translation approach
  5. Update cadence
  6. Comments / engagement
- These should be locked in the next session via `/feature-design` (Task 1)

---
