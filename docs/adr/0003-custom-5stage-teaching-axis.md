# ADR 0003 — Custom 5-stage workflow as primary teaching axis

- Status: Accepted
- Date: 2026-05-07

## Context

The portfolio teaches AI fluency across two audiences (corporate non-tech and aspiring vibe coders). Content needs an organising scheme that:

1. Maps to how AI-assisted work actually happens
2. Speaks to both audiences
3. Drives navigation, filtering, and a dedicated `/ai-fluency` page
4. Tags every content item meaningfully

Several established frameworks exist. We considered:

- **4D AI Fluency** (Dakan/Feller via Anthropic): Delegation, Description, Discernment, Diligence — process-oriented, citable, academically rigorous
- **Outcome-only categories**: Save time / Improve quality / Enable new / Reduce risk — corporate-friendly, ROI-shaped
- **Custom 5-stage workflow**: Define / Delegate / Direct / Discern / Document — a build-cycle framing
- **Bloom's revised taxonomy** applied to AI: Remember / Understand / Apply / Analyse / Evaluate / Create — academic
- **Single-axis vs multi-axis** combinations of the above

## Decision

**Two-axis tagging on every content item:**

**Primary axis — Custom 5-stage workflow** (drives navigation spine, the `/ai-fluency` page):

1. **Define** — frame the problem; what good looks like
2. **Delegate** — decide what AI does, what stays human
3. **Direct** — communicate intent (prompts, constraints, examples)
4. **Discern** — evaluate output; quality, accuracy, fit
5. **Document** — capture decisions, lessons, attribution

**Secondary axis — Outcome categories** (drives `/use-cases` page, corporate-lens entry point):

- Save time
- Improve quality
- Enable new capability
- Reduce risk

## Why this over 4D alone

- **Maps to actual build cycles.** "Define" front-loads problem framing; "Document" tail-loads the lessons capture step that the portfolio's own workflow (`/wrap-up`, ADRs, LEARNINGS.md) demonstrates. This matches how Jerome's projects actually run, making the framework credible by example.
- **Coherent with the portfolio's own meta-narrative.** The site describes a workflow; the workflow shapes the site. Self-similar teaching artifact.
- **Compatible with 4D conceptually.** Delegate/Direct/Discern overlap heavily with Delegation/Description/Discernment. The 5-stage version adds Define and Document — the bookends that academic 4D treats as background. Means future content can reference 4D when academic citation is useful, without restructuring.
- **Outcome axis brings the corporate audience.** Workflow appeals to vibe coders; outcomes appeal to decision-makers. Two doors, one body of content.

## Why not Bloom

Schoolroom-coded; doesn't differentiate AI work from other learning.

## Why not outcome-only

Doesn't teach the *how* — risks becoming consultant-speak. Pairs well *with* a process axis.

## Consequences

- Every content item carries a `workflow_stages: [...]` and `outcomes: [...]` tag in frontmatter.
- `/ai-fluency` aggregated page sorts by workflow stage with examples from real Tier-1 projects.
- `/use-cases` page sorts by outcome.
- Schema validators enforce both fields are present on `project` and `lesson` content types.
- If 4D framing becomes useful for an academic audience later, content can be re-tagged via a build-time mapping — no source changes required.
