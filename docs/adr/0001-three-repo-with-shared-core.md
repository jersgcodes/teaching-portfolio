# ADR 0001 — Three-repo architecture with shared `content-core`

- Status: Accepted
- Date: 2026-05-07
- Supersedes: original "single repo" plan in initial CLAUDE.md

## Context

The teaching portfolio originally scoped as a single static site grew into two distinct surfaces during `/feature-design`:

1. `growth` — personal AI fluency journey, public-facing, shareable with friends/family/peers/aspiring vibe coders
2. `labs` — work team's content factory, private to the team, produces export-ready assets handed off to corporate

The two surfaces share:
- Schema for content units (project, lesson, concept, pattern)
- Taxonomy (5-stage workflow + outcome categories + lenses)
- Components (lens toggle, attribution, badges)
- Aggregator (scans `~/claude/<project>/`)
- Validators

The two surfaces differ in:
- Audience (public vs internal team)
- Tone (candid vs polished)
- Risk (none vs corporate IP exposure)
- Repo visibility (private repo with public site vs private repo with auth-gated site)
- Contribution paths (controlled vs team-only)

## Options considered

### A. Mono-repo with two SSG outputs
One repo containing both surfaces' content + shared infra. SSG produces two sites.

- **Pros:** atomic refactors, single CI, simplest local dev
- **Cons:** GitHub access control is repo-level only — can't expose `labs/` privately while making `growth/` open. Mixing personal + work in one place creates real privacy risk.

### B. Two repos (one per surface), no shared core
Each site duplicates schema, components, aggregator.

- **Pros:** maximum isolation
- **Cons:** drift between sites; every shared change applied twice; aggregator divergence inevitable.

### C. Three repos: `content-core` + `growth` + `labs`, sharing via git submodule (chosen)
Shared infra extracted into a third repo. Both consumer sites embed it as a submodule.

- **Pros:** clean privacy boundaries (each consumer can be its own repo with its own visibility); single source of truth for schema/components; submodule pin gives reproducible builds.
- **Cons:** submodule update DX (manual bumps); slight learning curve; three deployments.

### D. Three repos with NPM-published `content-core`
Same as C but `content-core` published to npm and consumed as a package.

- **Pros:** cleaner DX than submodules; semver-able
- **Cons:** publish step on every change; needs registry setup; overkill for solo work where all consumers are co-located.

## Decision

**Three repos with `content-core` consumed by `growth` and `labs` via git submodule.**

`content-core` is **public** by default — itself a teaching artifact (transparency about how the system thinks). May flip private if team objects.

`growth` is a private repo that deploys a public site.

`labs` is a private repo that deploys a private (Cloudflare Access gated) site.

## Consequences

- Updates to shared infra: change `content-core` -> bump submodule pointer in each consumer -> rebuild both sites. Manual for v1.
- If submodule friction emerges, escalate to NPM publish (Option D) — non-destructive transition.
- `AGENTS.md` and `CONTRIBUTING.md` live in `content-core` because they describe the shared schema and process.
- This ADR is referenced in `CLAUDE.md` under Architecture.
