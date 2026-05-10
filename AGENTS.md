# AGENTS.md — Contribution guide for AI agents (and humans)

This repository (`content-core`) is the shared infrastructure of a two-surface content engine. Two consumer sites (`growth`, `labs`) consume it. This file tells AI agents — and the humans driving them — how to contribute content that the system will accept.

If you are an AI agent reading this: follow it literally. If you are a human asking an AI agent to contribute: paste this file (or a link) into your chat.

---

## What this repo contains

- `schema/v1/` — JSON Schemas for the four content types: `project`, `lesson`, `concept`, `pattern`
- `taxonomy/` — controlled vocabularies for workflow stages, outcomes, and lenses
- `projects.yaml` — the single source of truth for which projects appear in the portfolio
- `components/` — shared React components (lens toggle, attribution display, badges) — to be added in Phase 2
- `aggregator/` — Python scripts that scan the workspace and produce structured JSON — to be added in Phase 1
- `validators/` — schema and integrity checks — to be added in Phase 1
- `tools/moodboard-prep/` — meeting prep tooling — to be added in Phase 4
- `docs/adr/` — Architecture Decision Records explaining the WHY of major decisions

The two consumer repos (`growth`, `labs`) live separately and consume this repo as a git submodule. Content that is specific to one surface lives in that surface's repo, not here.

---

## Decide first: which content type?

| Type | Use when |
|---|---|
| `project` | A specific build under `~/claude/<project>/`. One per project. |
| `lesson` | A concrete, often cross-cutting takeaway. Specific enough to be actionable. |
| `concept` | A teaching primitive someone needs to understand to follow other content. |
| `pattern` | A recurring architecture motif visible across multiple projects. |

If your contribution doesn't fit one of these, push back to a human — the system intentionally constrains shape.

---

## Decide first: which surface?

| Surface | Voice | Visibility |
|---|---|---|
| `growth` | Candid, in-progress, mistakes-out-loud, plain English | Public |
| `labs` | Polished, credible, outcome-led, corporate-friendly | Auth-gated |

`projects` and `patterns` typically live in `growth`. `lessons` and `concepts` may live in either depending on whether they are personal-journey or work-output. Meeting artifacts always live in `labs`. When in doubt: `growth`.

---

## Required fields

For every content item, the schema (`schema/v1/<type>.json`) defines required fields. Run your output through schema validation before submitting. Schemas are JSON Schema draft-07.

Common required fields across types:

- `title` — display title
- `slug` — URL-safe identifier
- `summary` (or `one_liner` for projects)
- `visibility` — `public` / `mentioned` / `hidden`
- `authors` — array of `{role, by, when}`. **Mandatory on every item.**

For `project`, `lesson`, `pattern`: `workflow_stages` and `outcomes` are required.

---

## Link label convention

When listing links in a project's `project-overview.yaml`, the **label** carries any access caveat. The schema has no separate field for "is the deployment public" — labels are the source of truth. Convention:

- No suffix: publicly accessible (e.g. `"Live dashboard"`)
- `(login required)`: any auth gate (e.g. `"Live dashboard (login required)"`)
- `(team only)`: restricted group access
- `(reference)` or `(data source)`: third-party link, not our deployment
- `(internal)`: listed for record-keeping; portfolio readers can't access it

Do not put deployment access state in the project's `visibility` field — that controls portfolio rendering only. A project with `visibility: public` plus a link labelled `"Live dashboard (login required)"` is internally consistent.

## Voice rules per surface

### `growth`

- Speak in the first person where it serves the story.
- Mistakes are content. Don't sand them off.
- Plain English first. Technical depth only behind the Builder or Deep lens.
- One useful sentence beats three vague ones.

### `labs`

- Outcome-first. What changes for the user / business?
- Avoid claims you cannot stand behind in a meeting with corporate.
- Names of clients, internal tools, and infrastructure: **never**.
- Categorical descriptions only: "uses an LLM API", "uses a chat platform", "uses a managed database".

---

## Lens content (for projects)

If your content is a `project`, populate the `lenses` field with three blocks:

```yaml
lenses:
  corporate: |
    Plain-English explanation of what it does for users / the business.
    No tool names. No code. No architecture diagrams.
  builder: |
    Light-technical: how it's wired, key choices, and why.
    Names tools by category, not SKU.
  deep: |
    Full technical: code references, architecture decisions, alternatives considered, tradeoffs.
    Assume the reader wants the engineering substance.
```

A reader picks which lens to view; all three should be coherent on their own.

---

## Attribution

Every content item must declare its authors. Be honest:

```yaml
authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
  - role: reviewed
    by: "Jerome"
    when: 2026-05-07
```

`role` is one of: `drafted`, `reviewed`, `edited`. `by` should be a specific identifier — for AI, model name + version (e.g. `Claude Opus 4.7`); for humans, prefer a non-PII handle (e.g. `@jersgcodes`) over a real name, since project-overview.yaml lives in committed source and some projects' PII guards block real names. `when` is ISO date.

This is rendered visibly on every page. Misattribution is a worse failure than no attribution.

---

## Workflow stages and outcomes

These are not optional flair. The site organises content by them.

**`ai_role.agentic`** — required. Tracked separately because agentic AI is a teaching-relevant distinction worth surfacing in the portfolio:

- `yes` — multi-step autonomous reasoning is a primary mode (agent loops, tool use, multi-agent collaboration)
- `partial` — bounded agentic patterns coexist with single-call AI (e.g. one multi-turn module within a mostly single-call system)
- `no` — single-call AI only, OR pipelines of bounded prompts. **A deterministic sequence is not agentic** — even if it's 25 steps long.

Be honest. Calling a non-agentic system "agentic" because it sounds modern erodes the value of the field.

**Workflow stages** (pick the ones that actually apply, not all):

- `define` — frame the problem
- `delegate` — decide what AI does vs human
- `direct` — communicate intent (prompts, examples, constraints)
- `discern` — evaluate output
- `document` — capture decisions, lessons, attribution

**Outcomes** (pick what value this produces):

- `save_time` — reduces human hours
- `improve_quality` — catches errors, raises consistency
- `enable_new` — unlocks something previously impossible
- `reduce_risk` — lowers exposure to mistakes / compliance / privacy issues

Most projects span multiple of each. Be honest, not exhaustive.

---

## Forbidden content

Do not include:

- Real client names, project codes, or internal hostnames in any surface
- Code snippets that contain secrets, credentials, or API keys
- Hallucinated URLs or citations
- Tool names / versions / paths in `mentioned`-tier project entries
- Personal data of identifiable third parties
- Marketing language ("revolutionary", "cutting-edge", "transform your business")

---

## How to submit

### If you are a human contributor

1. Fork or branch the appropriate repo (`content-core` for shared schema/components, `growth` or `labs` for content)
2. Add your file in the correct location (see below)
3. Run validators locally (instructions in each repo's README, once Phase 1 lands)
4. Open a PR

### If you are an AI agent

1. Read the relevant schema in `schema/v1/`
2. Produce content that validates against it
3. Format as markdown with YAML frontmatter (frontmatter holds the schema fields; body is the content)
4. Save to the correct path
5. Open a PR via the GitHub API or hand to a human to commit

### File locations

| Type | Lives in | Path |
|---|---|---|
| Project facts | the project itself | `~/claude/<slug>/project-overview.yaml` (workspace standard, see ADR 0006) |
| Portfolio registry | this repo | `projects.yaml` (slug + tier + optional overrides only) |
| Project lens content | this repo (Tier-1 only) | `content/projects/<slug>/lenses/{corporate,builder,deep}.md` |
| `lesson` | growth or labs | `content/lessons/<slug>.md` |
| `concept` | growth or labs | `content/concepts/<slug>.md` |
| `pattern` | growth | `content/patterns/<slug>.md` |
| Meeting artifact | labs | `meetings/<YYYY-MM-DD>-<topic>/` |

### Contributing project metadata

If you (the AI agent) are updating facts about a project — its capabilities, status, lessons learned, what AI role it plays:

1. Find the project under `~/claude/<slug>/`
2. Open `project-overview.yaml` (validate against `~/claude/scripts/templates/project-overview-schema.json`)
3. Update the relevant fields (capabilities is most often the one that goes stale)
4. Update `last_updated` to today's ISO date
5. Open a PR in that project's repo

Do **not** put project facts in this repo's `projects.yaml`. That file is a registry of which projects appear in the portfolio, with editorial overrides only.

### Contributing lens content

Lens content (corporate / builder / deep narrative for a Tier-1 project) is editorial. It lives in this repo at `content/projects/<slug>/lenses/{corporate,builder,deep}.md`. Each is hand-authored for a specific audience depth (see `taxonomy/lenses.json`).

Voice rules for lens content:

- **corporate.md** — non-technical decision-maker. What the project does for users / business. No tool names. ~3-5 sentences.
- **builder.md** — light-technical peer. How it's wired, key choices. Tools by category. ~5-8 sentences.
- **deep.md** — technical practitioner. Code references, architecture decisions, alternatives, tradeoffs. As long as it needs to be (cap at ~600 words).

---

## Inbox: ideas not yet ready for canonical content

If you have raw material that isn't shaped into a final content item, drop it into the inbox of the appropriate surface:

- `growth/inbox/<YYYY-MM-DD>-<topic>.md`
- `labs/inbox/<YYYY-MM-DD>-<topic>.md`

Inbox files do not need to validate against any schema. They are pre-canonical. A human (or a follow-up AI session) will curate them into proper content items later.

For `labs/inbox/`, follow this format if the source is a discussion-space paste:

```markdown
---
date: 2026-05-12
source: <Loop / OneNote / Word / Teams / etc.>
participants: <names or anon>
---

## Raw
<paste here — text, image references, links, anything>

## Already decided
<anything the discussion already concluded>

## Open questions
<anything still being debated>
```

The mood-board summariser tool (Phase 4) reads this format.

---

## Meta-principle

This system is intentionally a teaching artifact about how AI-assisted work should be done. Treat your own contribution to it as an example of the 5-stage workflow:

- **Define** — what content type, which surface, what's the takeaway
- **Delegate** — which parts you (the AI) draft vs. which need human judgement
- **Direct** — write to the schema and voice, not in your default mode
- **Discern** — validate before submitting; flag anything you're uncertain about
- **Document** — attribute honestly; record what was AI-drafted vs. human-edited

The integrity of the teaching depends on it.
