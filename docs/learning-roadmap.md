# Personal skill-building roadmap

Six projects that progressively close the gaps between "vibe coder who ships prototypes" and "AI practitioner ready to take systems to public-business-grade use." Designed so each project both teaches one specific skill AND produces a content artifact that strengthens the portfolio.

See `TASKS.md` Phase 6 for the task list version.

## The Mode-1 gaps these projects target

When a vibe-coded MVP needs to go from "works for me" to "real users depending on it":

1. **Production-readiness scaffolding** — error handling, rate limiting, secrets management, basic ops
2. **Security thinking** — threat modelling, common vulnerabilities, AI-specific risks
3. **Concurrency** — multiple users, race conditions, database locking
4. **Operations / observability** — logs, metrics, alerts, incident response
5. **Performance / database** — profiling, indexing, caching, optimization
6. **End-to-end production** — domain, deploy pipeline, support, real users

Most "experts" learn these by encountering them painfully in production. Doing them deliberately, in small projects, is faster and produces teaching content along the way.

## The ladder (do in this order)

| # | Project | Gap closed | Time | Output |
|---|---|---|---|---|
| 1 | Harden sg-sme-profiler for team-use bar | Production-readiness scaffolding | 1 weekend | Feature branch + before/after writeup |
| 2 | Security audit on own project | Threat modelling | 1 weekend | Self-audit report + applied fixes |
| 3 | Multi-user SME tracker | Concurrency / state | 2 weekends | Working tool + concurrency lessons writeup |
| 4 | Self-hosted service with monitoring | Ops / observability | 2 weekends | Monitored service + ops writeup |
| 5 | Performance optimization of erp-mapper | Performance / db | 2 weekends | Benchmark report + performance pattern |
| 6 | Full public deployment (capstone) | End-to-end production | Multi-week | Live tool + full production writeup |

Total: ~10-12 weeks of weekend work for the first five. Project 6 is ongoing.

## How each connects to content output

Each project becomes:
- **A LinkedIn post** — the single lesson (~400 words)
- **A long-form article** — the full journey (~1500 words)
- **A pattern in `content/patterns/`** — the abstracted teaching (~2000 words)
- **A talk segment** — 5-7 min demo + lesson

By project 4 you have ~16 pieces of differentiated content. That's serious public output for a 4-6 month investment.

## Project specs

### Project 1 — Harden sg-sme-profiler for team-use bar

**What to do (concrete punch list):**
- [ ] Move all API keys / secrets to env vars; remove from code
- [ ] Add rate limiting (e.g., 30 requests/IP/hour) — use a simple in-memory counter or Redis
- [ ] Add structured logging with request IDs (use Python's `logging` with JSON formatter)
- [ ] Friendly error pages — no stack traces to users; log full details internally
- [ ] Add `/health` endpoint returning service status + dependencies (AI API reachable, DB up)
- [ ] Add a simple monitoring page or daily email — uptime, error rate, AI cost
- [ ] Document backup strategy (what's backed up, how to restore, when last tested)
- [ ] Write a 1-page `runbook.md` — "what to do when X breaks"

**Skills you'll pick up:** Working with env vars cleanly. Structured logging conventions. Health-check patterns. Basic operational maturity.

**Honesty check:** Most vibe-coded apps fail this list on at least 4 items. That's normal — closing the gap is exactly the exercise.

**Writeup template (~1500 words):**
- The state of the app before (what existed, what didn't)
- The 8-item checklist applied
- 3-5 things that surprised me (rate limiting harder than expected, secret discovery in old code, etc.)
- What "team-use ready" actually means (the difference from "production")
- What I deliberately did NOT do for this bar (the things you'd add for paying-customer ready)

### Project 2 — Security audit on own project

**What to do:**
- [ ] Pick erp-mapper or sme-outreach
- [ ] Run `bandit -ll .` and read every result (don't auto-dismiss)
- [ ] Run `pip-audit` and update vulnerable deps; document why each upgrade was needed
- [ ] On paper / in markdown: document the data flow for every input field (where does it go? logged? stored? sent to third parties?)
- [ ] Adversarial testing: try paste-bomb (1MB string), SQL-injection-style strings, prompt injection ("ignore all previous instructions and..."), empty inputs, unicode edge cases
- [ ] Map findings against OWASP Top 10
- [ ] Write a "security review report" — formal-looking, will be shareable

**Skills you'll pick up:** Reading static analysis output. Thinking like an attacker. Understanding AI-specific vulnerabilities (prompt injection, data exfil through completion).

**Writeup template:**
- Methodology (what I looked for, what tools)
- Findings (severity tiered)
- Fixes applied (with PR-style before/after)
- The OWASP top 10 mapping — which apply to AI apps, which don't
- The AI-specific items not in OWASP (yet)

### Project 3 — Multi-user SME tracker

**What to do:**
- [ ] Define minimal feature set: an SME has a name, status, notes; multiple officers can comment
- [ ] Build with whatever stack — Next.js, FastAPI + React, whatever
- [ ] Pick PostgreSQL (real DB) or SQLite-WAL (cheaper, has limits)
- [ ] Handle the hard cases: two officers editing the same record (conflict resolution UI). One officer deletes while another is editing. Concurrent comments.
- [ ] Real-time updates: WebSockets, Server-Sent Events, or smart polling
- [ ] Test by opening 3 browser tabs and racing yourself

**Skills you'll pick up:** Optimistic vs pessimistic locking. Eventual consistency. Race condition diagnosis. The "but it worked on my machine" lesson at depth.

### Project 4 — Self-hosted service with monitoring

**What to do:**
- [ ] Pick a project that's worth deploying (sme-outreach, erp-mapper, etc.)
- [ ] Deploy to a small VPS (DigitalOcean, Hetzner, Linode — $5-10/mo)
- [ ] Set up structured log aggregation (even just journalctl + log rotation)
- [ ] Add metrics: Prometheus + Grafana, OR simpler alternatives like Better Stack, Axiom
- [ ] Alerts on: error rate above threshold, service unavailable, daily AI cost > $X
- [ ] Write a `runbook.md`: what to do when each alert fires

**Skills you'll pick up:** systemd / docker / supervisord. Metrics design. Alerting (when to alert, what NOT to alert on). The "we don't actually know what's happening" problem.

### Project 5 — Performance optimization of erp-mapper

**What to do:**
- [ ] Baseline: how long does a full pipeline run take today? Profile with cProfile / py-spy
- [ ] Identify hot paths: where is time actually spent?
- [ ] Try optimizations: cache identical inputs, parallelise independent steps, use cheaper models where adequate, optimize file I/O
- [ ] Re-benchmark; document end-to-end speedup
- [ ] Decide what NOT to optimize (premature optimization is real)

**Skills you'll pick up:** Profiling. The 80/20 of optimization. AI-pipeline-specific patterns (cost vs latency vs quality trade-offs).

### Project 6 — Full public deployment (capstone)

**What to do:**
- [ ] Pick a project safe to make public (public-data-only — sme-outreach lite-version maybe)
- [ ] HTTPS + custom subdomain
- [ ] CI/CD deploy pipeline (GitHub Actions → Cloudflare Pages or Fly.io)
- [ ] Status page (Statuspage, BetterUptime, or DIY)
- [ ] User-facing docs (one-pager: what it does, what it doesn't)
- [ ] Privacy policy + ToS (even for free; copy from a similar tool and adapt)
- [ ] Cost monitoring + budget alerts
- [ ] Incident playbook
- [ ] Cycle: real user reports a bug, you fix it without breaking everything else

**Skills you'll pick up:** Everything from projects 1-5, integrated. Plus the user-facing layer most builders skip.

## What this roadmap doesn't include (intentionally)

These are real skills but deferred — they don't justify their effort right now:

- **Deep ML / training your own models** — overkill for the work you do
- **Distributed systems at scale** — you don't have the volume
- **Kubernetes / container orchestration** — your projects are too small to need it
- **Frontend framework deep-dives** — you can get most of what you need from AI-built code
- **Algorithmic interview prep** — useless for practitioner work

## Update cadence

Mark tasks DONE in TASKS.md as projects complete. Each project's writeup becomes a content item in `content/lessons/` or `content/patterns/`. Reassess after Project 3 — by then you'll know if the ladder is working or needs adjustment.
