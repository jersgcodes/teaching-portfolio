# ADR 0004 — Tool-agnostic discussion-space ingestion

- Status: Accepted
- Date: 2026-05-07

## Context

`labs` (the work team surface) needs a "common discussion space" for ideation, references, and meeting prep. The team has not yet picked a tool — the lead raised it but no decision exists. Likely candidates given a corporate M365 environment: Microsoft Loop, OneNote, Word with comments, PowerPoint, Teams.

We need a content pipeline that:

1. Doesn't depend on a specific tool the team hasn't chosen yet
2. Works on a corporate work laptop (M365 ecosystem)
3. Can ingest mixed media (text, links, images)
4. Feeds the mood-board summariser before each meeting
5. Survives a future tool switch without re-architecting

## Options considered

### A. Pick a tool now (Discord / Slack / Notion / Loop)
Wire an API connector; bake the choice into the pipeline.

- **Pros:** highest-fidelity ingestion when the API is good
- **Cons:** team's lead drives this decision; we'd be guessing; if wrong, throwaway integration cost; many candidate tools have weak or paid APIs.

### B. Black-box paste-into-inbox (chosen)
Ingestion is a known markdown format. Whatever tool the team uses, content gets pasted into `labs/inbox/<date>-<topic>.md` in a structured shape. The pipeline reads the markdown.

- **Pros:** zero tool dependency; works with any tool the team picks; survives tool switches; trivial to build now.
- **Cons:** human paste step; loses image fidelity (images become URLs or attached files in the inbox folder).

### C. Build a generic "M365 connector" upfront
Use Microsoft Graph to read from whatever M365 surface ends up chosen.

- **Pros:** no manual paste
- **Cons:** premature; M365 Graph permissions on a corporate tenant likely require IT approval; spec moves fast; lock-in to Microsoft.

## Decision

**Black-box paste-into-inbox in a known markdown format.**

The format:

```markdown
---
date: 2026-05-12
source: <Loop/Word/Teams/etc.>
participants: <names or anon>
---

## Raw
<paste here — text, image references, links, anything>

## Already decided
<anything the discussion already concluded>

## Open questions
<anything still being debated>
```

The mood-board summariser (`content-core/tools/moodboard-prep/`) reads this markdown and produces meeting artifacts.

## Consequences

- Discussion-space tool can be Loop, OneNote, Word, Teams, Slack, Notion — all work the same.
- Migration to a different tool later: no pipeline changes.
- If volume justifies it later, an automated connector for the *chosen* tool can be added — pipeline still consumes the same inbox markdown shape.
- Image handling: contributors save images to the meeting folder alongside the markdown and reference by relative path. Acceptable friction for v1.
