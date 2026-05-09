---
title: "Privacy-first design for personal AI tools"
slug: privacy-first-design
summary: "When a project handles sensitive personal data — finances, communications, health, location — privacy is an architectural choice, not a feature toggle. Once you commit to 'data never leaves the device', many decisions (especially about AI usage) collapse cleanly."
visibility: public

problem: |
  Personal AI tools are some of the most useful applications of LLMs — analyse my spending, optimise my schedule, surface what I missed in my inbox. They are also some of the riskiest, because the data they handle is the data a user least wants exposed. Most apps lazily ship "we use industry-standard encryption" and call it done. The architectural question — does the data ever leave the user's device? — gets ducked.

solution: |
  Treat privacy as a constraint at architecture time, not as a feature added later. Decide at design time: "this data never leaves the device" OR "this data leaves the device, here's exactly when, here's exactly to whom." The first stance forces specific architectural choices: no cloud LLM calls on raw data, encrypted local storage, sanitisation boundaries between modules, scoped OS permissions. The second stance demands documented data flows. Lazy "encryption in transit" is neither.

when_to_use: |
  Use privacy-first architecture when:
  - The data is personally identifying (names, addresses, contacts)
  - The data reveals financial position (transactions, balances, holdings)
  - The data reveals communication content (messages, emails)
  - The data reveals patterns of life (location, schedule, behaviour)
  - The user has explicit privacy expectations (e.g. they chose your tool over a SaaS alternative for this reason)

  You can take a lighter posture when:
  - Data is already public (research scrapers on public APIs)
  - Data is fully synthetic (generated for testing)
  - The user has explicitly opted in to cloud processing with informed consent

examples:
  - project: miles-optimizer
    note: "Most disciplined example. Encrypted local DB (Fernet); a compiled Swift binary scopes Full Disk Access to the smallest possible surface; no AI in the runtime because privacy stance rules out LLM calls on transactions."
  - project: spending-monitor
    note: "PDF statement processor with PII scrubbing before persistence. Local-only by design. Tier-3 in the portfolio (skip rendering) but the privacy pattern is publishable."
  - project: investment-analyst
    note: "Two-layer security boundary (research layer / account layer). Intentionally non-shareable as a deployed service — pattern-level reference only."

workflow_stages: [define, document]
outcomes: [reduce_risk]

authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
---

## What "privacy-first" actually means

Most products that claim privacy are operating one of three implicit models:

1. **"We encrypt in transit and at rest"** — table stakes, says nothing about who has access on the other end. The cloud provider, the company, and any subpoena reader all see the data plain.
2. **"We don't sell your data"** — a policy commitment, not an architectural one. Reversible by a future board decision, an acquisition, or a leak.
3. **"Your data stays on your device"** — an architectural commitment. The data physically can't leave because there's no code path that sends it.

Privacy-first design is the third. It's a higher bar to clear, but once cleared, an entire class of risks (cloud breaches, insider access, policy reversal, jurisdiction changes, government data requests) simply doesn't apply.

## What it forces in the architecture

Once you commit to "data stays on the device," several decisions collapse cleanly:

| Concern | Privacy-first answer |
|---|---|
| Where does processing happen? | Local. Always. |
| Where does AI run? | Either nowhere, or via a strictly bounded sanitisation layer (sample only non-identifying features) |
| What data goes to disk? | Encrypted at rest, decrypted only when needed |
| Who can read the local DB? | Only the application. OS permissions enforce this. |
| What about backups? | User controls them. Tool exports unencrypted only if user actively chooses. |
| What's the threat model? | Device theft, family member curiosity, OS-level malware. Not "cloud breach" because there's no cloud. |
| What about updates / sync? | The hard one. Either skip cross-device sync entirely or use end-to-end encryption (e.g. iCloud Drive with Apple's E2EE). |

The trade-offs are real:
- No cloud sync (or expensive E2EE sync)
- No analytics / usage telemetry from the developer's perspective
- No remote troubleshooting
- No "AI features" that rely on cloud LLMs touching raw data

What you get in exchange:
- A threat model you can fully reason about
- No reliance on third-party policy commitments
- No data-breach exposure (because there's no central data to breach)
- Defensibility — when a user asks "where does my data go", the answer is genuinely "nowhere"

## Privacy-first AI is mostly "no AI"

This is where personal AI tools usually fail their own privacy promise. The temptation is overwhelming: "we promise it's private, AND we have an AI feature that summarises your spending." The truth is usually that the AI feature ships your transactions to a cloud LLM, then the privacy promise has a footnote.

Three honest postures:

1. **No cloud AI at all.** What `miles-optimizer` does. Recommendation engine, MCC mapping, cap math, dedup are all deterministic. The lessons of LLM-era development still apply (good interfaces, good tests, good fallbacks) but the LLM never runs on the user's data.

2. **AI on derived non-identifying features only.** Compute aggregates locally (e.g. "total spend per category last month"), send the aggregates to an LLM for summarisation. Never send the raw transactions. This is harder than it sounds — the LLM gets less context, and prompts must be written carefully to not encourage the model to ask for raw data.

3. **AI on local models only.** Run a small model on-device (Ollama, llama.cpp, Apple's on-device foundation models). The model is less capable than cloud Claude/GPT but the data physically can't leave. Useful for summarisation, classification, simple Q&A.

What is NOT a privacy-first posture:
- "We anonymise it before sending" — anonymisation is harder than people think; identifiers leak through patterns
- "We use a privacy-respecting LLM provider" — you've just relocated the trust, not eliminated it
- "We only send the relevant parts" — the relevant parts are usually the most sensitive parts

## Workspace examples

### `miles-optimizer` — the disciplined reference
- Fernet-encrypted local DB; transactions never leave the device
- A compiled Swift binary, not Python, has Full Disk Access — keeps the scope minimal
- Multi-source ingestion (Mac Messages SQLite, Gmail IMAP, manual paste) all stays local
- Recommendation engine, MCC mapping, dedup are deterministic — no LLM calls in the runtime
- iCloud sync is opt-in for a small recommendations.json (no transactions); the sync layer chosen specifically because Apple offers E2EE for iCloud Drive

### `spending-monitor` — pre-LLM privacy stance
- PDF statement processor; PII scrubbing before persistence
- Local SQLite only; export to Excel for the user's own analysis
- Pre-dates the LLM era of the workspace, but the architectural choice (local-only, no cloud) holds up
- Listed as Tier-3 in the portfolio for editorial reasons (personal finance) but the pattern is publishable

### `investment-analyst` — two-layer boundary
- Research layer (publicly available market data) and account layer (user's actual holdings) are physically separated
- Account-layer queries can only be initiated from the device; research-layer queries can hit external APIs
- Intentionally non-shareable as a deployed service — the architectural pattern (boundary between safe and sensitive) is what's publishable

## Common pitfalls

**Treating privacy as a marketing feature.** "Your data is private" sells. It also creates an obligation. Make sure the architecture matches the marketing.

**Letting AI features quietly violate the promise.** The most common breach. Adding "summarise my spending" looks innocent — and ships the user's transactions to a cloud provider. Audit every code path that touches sensitive data; ensure every external call is documented and justified.

**Anonymisation theatre.** Stripping names from transactions doesn't make them anonymous. The pattern of dates, amounts, and merchants identifies a household uniquely. If you need to use cloud AI, use aggregates, not "anonymised" detail.

**Skipping privacy because "it's just for me".** Personal projects become shared projects. They become demoed projects. They become team projects. The architectural choice is much cheaper to make at design time than at "we have users now" time.

**Conflating local-first with privacy-first.** A local-first app that backs up unencrypted to Dropbox is local-only-until-it-isn't. Privacy is about the full data lifecycle, not just where the primary store lives.

**Ignoring scope of OS permissions.** A Python script with Full Disk Access can read everything. A compiled binary with the same access can also read everything but is harder to inspect. Scope permissions to the smallest possible surface; prefer separate processes with narrow permissions over one fat process with broad ones.

## Decision worksheet

Before you ship a tool that handles personal data, answer in writing:

1. **What data does this handle, and how sensitive is each field?** Be specific. "Transactions" means amounts, merchants, dates, accounts.
2. **Where is each field stored?** On disk? Encrypted? Where exactly?
3. **What external services does the data touch?** Every API call, every cloud LLM, every analytics event. List them.
4. **What's the threat model?** Who are you protecting against? Device theft? Cloud breach? Insider access? Be explicit.
5. **What does the user expect?** If they think the tool is local-only and it's not, that's a trust violation regardless of legality.
6. **What happens at update time?** Backups, sync, telemetry, crash reports — each is a potential leak.

If any answer is fuzzy, you don't have a privacy-first design. Tighten it before shipping.

## See also

- `~/claude/miles-optimizer` — the most disciplined privacy-first reference
- `~/claude/spending-monitor` — pre-LLM privacy-first PDF processor
- `~/claude/investment-analyst` — two-layer security boundary
- Pattern: `harness-over-prompt-engineering` — when AI must run on sensitive data, the harness includes a sanitisation layer
- Pattern: `pipeline-vs-agent` — privacy-first systems usually prefer pipelines (auditable data flows) over agents (where data may flow unpredictably)
