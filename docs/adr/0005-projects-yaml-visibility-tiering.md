# ADR 0005 — `projects.yaml` visibility tiering

- Status: Accepted
- Date: 2026-05-07

## Context

Twenty projects live under `~/claude/<project>/`. They span a wide spectrum:

- Public-shareable (event-radar, playo, news-digest, etc.)
- Personal/sensitive (spending-monitor, investment-analyst, miles-optimizer)
- Client-related / business-sensitive (sme-outreach, sg-sme-maturity, sme-radar)
- Stubs / paused (nutrilens, market-intel, wip-next)

The portfolio needs to:

1. Know which projects appear at all
2. For projects that appear, control how much detail is exposed
3. Skip projects that don't have the minimum metadata to render a useful page
4. Stay easy to maintain as the workspace grows

## Options considered

### A. Whitelist by `projects.yaml` listing only
Projects appear only if listed in `projects.yaml`.

- **Pros:** explicit, safe-by-default, won't accidentally publish a new private project
- **Cons:** one-time per-project setup cost

### B. Blacklist via `project-status.yaml` flag in each project
A `public: true|false` flag in each project's own metadata, aggregator includes by default.

- **Pros:** distributed ownership; each project controls its own exposure
- **Cons:** unsafe-by-default — a new project added to `~/claude/` without the flag would auto-publish; harder to centrally audit.

### C. Hybrid (chosen): whitelist via `projects.yaml` + per-project visibility tier
Projects appear only if listed in `projects.yaml`. Each entry has a `visibility` field:

- `public` — full lens stack, all sections (Tier 1)
- `mentioned` — title + one_liner + audience + ai_role + lessons only; no architecture/infra/repo links (Tier 2)
- `hidden` — skipped entirely (or omit from yaml)

Projects missing required schema fields are also skipped — no stubs.

## Decision

**Whitelist via `projects.yaml` with three-tier `visibility` field.**

`projects.yaml` lives at the root of `content-core` and is the single source of truth.

The required minimum schema:

```yaml
title: <string>
one_liner: <=140 chars
audience: <string>
status: building | live | shelved | archived
visibility: public | mentioned | hidden
ai_role: core | helper | none + one-line description
lessons: [<>=1 item>]
# optional fields enrich rendering when available
```

For `visibility: mentioned` (private/sensitive projects):

- Permitted infra description: categorical only (e.g. "uses a VPS", "uses an LLM API")
- Forbidden: tool names, versions, ports, paths, hostnames, auth mechanisms, repo links

## Consequences

- Adding a new project to `~/claude/` does not auto-publish. Explicit yaml addition required.
- Sensitive projects can still appear and contribute lessons without leaking infrastructure detail.
- The aggregator's logic: read `projects.yaml`; for each entry, scan the project for richer content; render at the visibility tier specified.
- Stubs and paused projects don't pollute the portfolio.
- `projects.yaml` itself is checked into `content-core` — its diff history doubles as a publication record.
