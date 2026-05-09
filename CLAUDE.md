# CLAUDE.md — Teaching Portfolio (working directory)

> **Note:** this directory will be renamed to `content-core/` during Phase 0 of execution. It is the **shared infrastructure** of a three-repo architecture. Two **consumer sites** (`growth`, `labs`) will be created as separate repos that consume this one as a git submodule.

---

## Purpose

A two-surface content engine that supports:

1. **Personal AI fluency journey + project showcase** (public-facing, surfaces Jerome's growth as a builder and lessons learned)
2. **Work team content factory** (private to team, produces export-ready assets handed off to corporate for official publishing through corporate channels)

The two surfaces share schema, taxonomy, components, and aggregator. They differ only in content, deployment URL, and access control.

---

## Architecture (locked)

### Three repos

| Repo | Visibility | Purpose | Domain |
|---|---|---|---|
| `content-core` (this dir) | **public** | Schema, taxonomy, shared components, aggregator, validators, AGENTS.md | none — library |
| `growth` (to create) | **private repo, public site** | Personal surface; project showcases, AI fluency journey, lessons | `growth.jersgcodes.com` |
| `labs` (to create) | **private repo, private site** | Work team workspace; produces export assets | `labs.jersgcodes.com` (Cloudflare Access gated) |

Sharing: `growth` and `labs` consume `content-core` via **git submodule** (manual bumps).

### Stack

- **SSG:** Next.js (static export)
- **Hosting:** Cloudflare Pages (free tier, push-to-deploy)
- **Auth (labs only):** Cloudflare Access on the whole zone (free up to 50 seats; M365 SSO compatible)
- **Mood-board format:** Excalidraw (text-based JSON, committed)
- **Visual authoring:** Claude design (claude.ai) → export → commit (Pattern X1)

### Content pipeline

```
External discussion space (Loop / OneNote / whatever lead picks)
        | paste into known markdown format
        v
labs/inbox/<date>-<topic>.md
        | summarise (content-core/tools/moodboard-prep/)
        v
labs/meetings/<date>/{agenda.md, moodboard.excalidraw, notes.md, outputs/}
        | curate
        v
labs/content/ (canonical work content)
        | aggregate
        v
labs site (auth-gated)
        | export (PDF for greenlight; assets for corporate handoff)
        v
External corporate channels for any public publishing
```

For `growth/`, the inbox is fed by Jerome alone; the rest of the pipeline is identical.

---

## Content model

### Content units (4 types)

| Type | Purpose | Example |
|---|---|---|
| Project | A specific build under `~/claude/<project>/` | erp-mapper |
| Lesson | A concrete takeaway, often cross-cutting | "Cap-aware AI scoring" |
| Concept | A teaching primitive | "What is an embedding" |
| Pattern | A recurring architecture motif | "LLM router with provider fallback" |

### Lenses (3, audience-depth)

- **Corporate / Outcome** — non-technical decision-makers; what it does for users / business
- **Builder** — light-technical; how it's wired, key choices
- **Deep** — full technical; code, tradeoffs, alternatives

Every content item renders all three lenses where applicable; reader toggles which to read.

### Teaching axes (2, orthogonal to lenses)

**Primary axis — 5-stage workflow (custom):**

1. **Define** — frame the problem; what good looks like
2. **Delegate** — decide what AI does, what stays human
3. **Direct** — communicate intent (prompts, constraints, examples)
4. **Discern** — evaluate output; quality, accuracy, fit
5. **Document** — capture decisions, lessons, attribution

**Secondary axis — Outcome categories:**

- Save time
- Improve quality
- Enable new capability
- Reduce risk

Every content item is tagged on both axes. Drives `/ai-fluency` page (workflow spine) and `/use-cases` page (outcome spine).

### Where data lives (revised per ADR 0006)

| Concern | File | Layer |
|---|---|---|
| Project facts (title, status, capabilities, ai_role, tech_category, lessons, workflow_stages, outcomes) | `~/claude/<slug>/project-overview.yaml` (workspace standard) | Project |
| Portfolio inclusion / tier / overrides | `projects.yaml` (this repo) | Portfolio registry |
| Lens narrative (corporate / builder / deep) per Tier-1 project | `content/projects/<slug>/lenses/{corporate,builder,deep}.md` (this repo) | Portfolio editorial |

This split keeps source quality (project facts) decoupled from editorial framing (lens text).

### Visibility model

`visibility` is a **portfolio rendering ceiling** — how much information about a project the portfolio is permitted to show. It is NOT a statement about whether the project's running deployment is publicly accessible (that goes in link labels — see "Link conventions" below).

- Project's `visibility` in its own `project-overview.yaml` = the ceiling. Default `hidden`. Explicit opt-in to share.
- `projects.yaml` (this repo) may override DOWN (more restrictive) but never UP. Validator enforces.
- `visibility: hidden` projects are skipped entirely by the aggregator.
- `visibility: mentioned` (whether by project declaration or override) renders title + one_liner + audience + ai_role + lessons only — no architecture/infra/repo links.
- `visibility: public` renders the full lens stack (lens content must exist in `content/projects/<slug>/lenses/`).

Projects without `project-overview.yaml` cannot appear in the portfolio at all.

### Link conventions (deployment access state)

Whether a project's deployment is publicly accessible, auth-gated, or internal-only is captured in the **label of the link**, not in the visibility field. Convention:

| Label suffix | Meaning |
|---|---|
| no suffix | Publicly accessible to anyone with the URL |
| `(login required)` | Auth-gated (any form of login) |
| `(team only)` | Restricted to a specific group; stronger signal than 'login required' |
| `(reference)` or `(data source)` | Third-party site we link out to, not our deployment |
| `(internal)` | Listed for record-keeping; not accessible to portfolio readers |

A project's `visibility: public` plus a link labelled `"Live dashboard (login required)"` is internally consistent — the portfolio shows the project openly while signalling that the live deployment is gated.

### Attribution

Every content item carries `authors[]` rendered visibly on the page:

```yaml
authors:
  - role: drafted | reviewed | edited
    by: "Claude Opus 4.7" | "Jerome" | "ChatGPT-5" | etc.
    when: 2026-05-07
```

Default storage: frontmatter. Aggregate "all content by X" indexes generated at build time from frontmatter if needed later.

### Infra exposure rules (private projects)

For `visibility: mentioned` (private projects), permitted infra description is **categorical only**:

- Permitted: "uses a VPS", "uses a chat platform", "uses an LLM API", "uses a managed database"
- Forbidden: tool names, versions, ports, hostnames, paths, auth mechanisms, repo links

---

## Seed projects (Tier 1 — full pages on growth)

Selected after surveying all 20 workspace projects:

1. **erp-mapper** — IMDA solution catalogue scraper + AI canonicalisation pipeline
2. **smebot** — Dual-bot Telegram survey research system
3. **sg-sme-profiler** — React PWA AI diagnostic for SG SMEs
4. **miles-optimizer** — Privacy-first credit card miles engine
5. **news-digest** — Telegram bot with embedding dedup + LLM scoring
6. **playo** — Multiplayer game platform (real-time architecture)

Tier 2 (mention-only): claude-orchestrator, compare-agent, event-radar, sme-radar, sg-sme-maturity, sme-outreach, shared, policy-lens.

Tier 3 (skip in v1): spending-monitor, investment-analyst, market-intel, nutrilens, wip-next.

(`moonshot-sme-governance` not yet assessed; defer to projects.yaml curation step.)

Cross-cutting **patterns** to extract (not per-project, lifted into `/patterns/`):

- LLM router with provider fallback (appears in 4+ projects)
- Privacy-first design (recurring intentional choice across personal-finance projects)

---

## Standards

### Accessibility

WCAG 2.1 AA per workspace `STYLE_GUIDE.md`. Mandatory both surfaces.

### Mobile

Responsive by default; workspace standard.

### Performance

`/perf-audit` baseline applied to growth (public). Labs not gated on perf budgets.

### SEO

- `growth`: yes — semantic HTML, OG metadata, sitemap
- `labs`: not needed (auth-gated); same templates produce semantic HTML so no regression

### Languages

English only.

### Analytics

- `growth`: Cloudflare Web Analytics (free, privacy-friendly, no cookie banner needed)
- `labs`: none

### Versioning

Git is the version history. Pages render `last_updated` from git log. No visible content version labels in v1.

### Backups

Git on GitHub is canonical. Excalidraw files committed. No additional backup infra in v1.

### Branching

Workspace default: `feature/xxx` -> `dev` -> `main`. Build work goes on `feat/<name>`, never directly on main.

---

## v1 scope

### In scope

- Three repos (content-core public; growth and labs private)
- Aggregator scanning `~/claude/<projects>/` per `projects.yaml`
- Schema-validated content units (project, lesson, concept, pattern)
- Two-axis teaching taxonomy + three lenses
- Six Tier-1 projects rendered on growth
- `/ai-fluency` page (5-stage workflow + outcome explainer)
- Mood-board summariser tool (`content-core/tools/moodboard-prep/`)
- Excalidraw meeting artifacts in `labs/meetings/<date>/`
- PDF greenlight export from labs pages
- Cloudflare Access on labs zone
- AGENTS.md as v1 deliverable in content-core

### Deferred

- Build-time AI generation (Pattern X2)
- Runtime AI explainer (Pattern X3)
- External contribution paths beyond team PRs (Discord, public form, GPT Action)
- Asset-handoff pipeline for corporate (waits until corporate states their need)
- MCP server
- Side-by-side model comparison pages (Pattern delta)
- Search, RSS, comments, newsletter
- Multi-language

---

## Standards inheritance

Workspace `~/claude/CLAUDE.md` and this file both apply. Project-specific overrides above; otherwise follow workspace defaults.

Tests required for any code per workspace policy. Pre-commit hooks via `.pre-commit-config.yaml` (to be added during Phase 0).

---

## Source material

`sources/` holds reference material that informs portfolio content but is not itself published. Drop notes / transcripts / external course material here when it's worth keeping for future writing. Each file should carry a short header (what it is, source, date captured, intended use).

Currently:
- `sources/ai-fluency-educators.md` — notes from an Anthropic course on AI Fluency for Educators; informs future `/educators` content and includes a 4D ↔ 5-stage crosswalk

## ADRs

Six ADRs capture the WHY for the load-bearing decisions:

- `docs/adr/0001-three-repo-with-shared-core.md`
- `docs/adr/0002-cloudflare-pages-over-vps.md`
- `docs/adr/0003-custom-5stage-teaching-axis.md`
- `docs/adr/0004-tool-agnostic-discussion-ingest.md`
- `docs/adr/0005-projects-yaml-visibility-tiering.md`
- `docs/adr/0006-workspace-standardised-project-overview.md`
