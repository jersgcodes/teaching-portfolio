# Session notes — Talk prep conversation (2026-05-12 to 2026-05-13)

> **What this is.** Captured thinking from an extended conversation on (a) preparing a 15-min internal sharing on AI for SG SME digitalisation, (b) finding experts / building a content engine, (c) positioning as an AI practitioner from a non-coder background, (d) skill-building roadmap, (e) the "naive SME prompt" insight, and (f) two crux teaching tensions.
>
> **Why kept.** Most of these insights aren't ready to be content yet, but they're the raw material that several future content artifacts (patterns, handouts, talk segments) will be built from. Storing them so they don't evaporate between sessions.
>
> **Status.** Internal planning material — not for publication. Distil into `content/patterns/`, `content/lessons/`, or `content/handouts/` over time.

---

## Table of contents

1. [The 6 surfaces taxonomy (everyday language)](#1-the-6-surfaces-taxonomy)
2. [The architecture spectrum (6 layers)](#2-the-architecture-spectrum)
3. [Decision rubric — which surface and which architecture](#3-decision-rubric)
4. [Cost differences across architectures](#4-cost-differences)
5. [The corporate AI reality](#5-the-corporate-ai-reality)
6. [Three-track prep plan (sharing / experts / media)](#6-three-track-plan)
7. [Practitioner positioning](#7-practitioner-positioning)
8. [Non-coder background — defensible or weak?](#8-non-coder-positioning)
9. [Mode-1 gaps + 6-project skill ladder](#9-mode-1-gaps-and-skill-ladder)
10. [Production-readiness checklist](#10-production-readiness)
11. [The "naive SME prompt" teaching device](#11-naive-sme-prompt)
12. [Cold-vs-context comparison demo](#12-cold-vs-context-demo)
13. [Two crux teaching tensions](#13-crux-tensions)
14. [Open items + next steps](#14-open-items)

---

## 1. The 6 surfaces taxonomy

Where you interact with AI, vendor-agnostic, in plain language:

| Surface | Metaphor | What it is | Vendors |
|---|---|---|---|
| **Casual asking** | "Calling a knowledgeable friend who forgets you after the call" | Ephemeral chat | claude.ai chat, ChatGPT, Gemini, Perplexity |
| **Trained assistant** | "Hiring a new staff member and briefing them once" | Persistent project with knowledge | Claude Projects, ChatGPT Projects + GPTs, Gemini Gems, NotebookLM |
| **AI sitting beside you** | "Colleague looking over your shoulder while you work" | In-tool, in-context AI | Cursor, GitHub Copilot, Windsurf, Notion AI, Google Workspace AI, Microsoft 365 Copilot |
| **Errand-runner / agent** | "Junior staff member working multi-step tasks autonomously" | Goal-given, multi-step autonomy | Claude Code, ChatGPT Agent / Operator, Devin, Manus |
| **Baked into a tool** | "AI invisible behind a button in a system you already use" | API integration, custom builds | Custom apps, MS Copilot in Salesforce, etc. |
| **Specialised tools** | "Dedicated specialist for one job" | Domain-tuned applications | NotebookLM, Perplexity, v0, Lovable, Harvey, Khanmigo |

Most production AI workflows blend 2-3 surfaces.

---

## 2. The architecture spectrum

What's happening under the hood, from simplest to most autonomous:

| Layer | Pattern | Example |
|---|---|---|
| **1. Single call** | One prompt → one response | Translation, summarisation |
| **2. Pipeline** | Fixed sequence of LLM calls | erp-mapper's 25-step canonicalisation |
| **3. Workflow w/ routing** | Sequence with conditional branches | Customer support triage |
| **4. Parallel + reduce** | Fan out → aggregate | Multi-perspective analysis (parts of policy-lens) |
| **5. Orchestrator-workers** | Planner LLM directs other LLMs | Deep research; complex refactoring |
| **6. Autonomous agent** | LLM in a loop: think → act → observe → repeat | Claude Code; computer-use agents |

Anthropic's distinction: layers 1-4 are **workflows** (predefined paths); layers 5-6 are **agentic** (LLM dynamically directs its own path).

**Workflows** = LLMs follow code you wrote. **Agents** = LLMs write the structure as they go.

---

## 3. Decision rubric

Which architecture, in order:

| Question | Lean towards |
|---|---|
| Can you describe the steps a human expert would take? | Pipeline |
| Steps known but path depends on input? | Workflow with routing |
| Subtasks independent and parallelisable? | Parallel + reduce |
| Novel each time, but subtasks knowable? | Orchestrator-workers |
| Path genuinely unknown until execution? | Autonomous agent |
| Just one ask? | Single call |

**Three sharper heuristics:**
1. *"Can you write the spec?"* — Yes → workflow. No → agent.
2. *"Would a regulator accept this?"* — Needs explainability → workflow.
3. *"What's the cost ceiling per task?"* — Hard ceiling → workflow.

---

## 4. Cost differences

Same task, rough order of magnitude per query:

| Architecture | Haiku | Sonnet |
|---|---|---|
| Single call | $0.001 | $0.02 |
| Pipeline | $0.01 | $0.10 |
| Workflow w/ routing | $0.02 | $0.20 |
| Parallel + reduce | $0.05 | $1.00 |
| Orchestrator-workers | $0.10 | $5.00 |
| Autonomous agent | $0.50–$20 | $5–$50 |

Roughly 100–1000× cost difference top to bottom. Most teams default to the most capable shape they can build, then hit budget ceilings. The discipline is dropping a layer unless the problem demands the higher one.

---

## 5. The corporate AI reality

Most corp environments have a constrained set of approved AI tools. The mapping:

| Rung | Usually approved? |
|---|---|
| Cowork (Copilot in Word/Outlook, Workspace AI) | ✓ when IT licenses it |
| Approved chat (corp ChatGPT / Claude enterprise) | ✓ often |
| Trained assistants in approved tier | ✓ sometimes |
| Specialist tools (NotebookLM, etc.) | ⚠ requires approval |
| Agents (Claude Code, Operator, agentic Copilot) | ⚠ rarely yet |
| Vibe-coded internal tools | ⚠ needs IT partnership |

**Practical SG civil service moves:**
1. Use cowork wherever approved
2. Get good at corp-approved chat
3. Consumer AI for non-sensitive personal/learning tasks only
4. Specialist tools via partnership with IT, not rogue
5. Vibe coding stays personal/sandbox until proven, then approached via demo not request

---

## 6. Three-track plan

For the next 4 weeks:

| Track | Goal | Audience |
|---|---|---|
| **1. Sharing** | 15-min talk for internal mixed-level audience | Officers helping SG digitalise |
| **2. Experts bench** | Identify 5-10 named individuals across 4 categories (case-study SMEs, AI experts, government practitioners, adjacent disciplines) | Cross-leveraging with Track 3 |
| **3. Media formats** | Build Tier-1 content (LinkedIn posts, WhatsApp-shareable cards, short videos, one-pagers) for SME audience | SG SME owners, officers |

**The three reinforce each other.** Track 1 surfaces candidates for Track 2; Track 2 provides content for Track 3; Track 3 audience eventually attends Track 1.

---

## 7. Practitioner positioning

**Practitioner vs expert distinction:**

| Practitioner | Expert |
|---|---|
| Shipped systems | Research / theory |
| 12-36 months to recognised status | 5-10+ years |
| High market demand right now | Saturated at top |

Aim for practitioner — most "AI experts" in industry are practitioners with better communication.

**What's already strong:** 14 shipped projects, cross-project patterns, honest critical voice, defined niche (SG SME digitalisation).

**What's weak / to build:**
- Consistent public presence (need a channel + cadence — LinkedIn 1-2/wk)
- Named institutional affiliations (NUS-ISS, AI Singapore, etc.)
- Recognised credentials (one stackable cert that signals in SG context)
- Network of peer practitioners (the Track 2 bench)
- Surfaced signature POV (you have multiple — make them visible)

**Three signature POVs already in your work:**
- "Most production AI is bounded pipelines, not autonomous agents — and that's a feature"
- "Harness over prompt engineering — the system carries the load, not the prompt"
- "Match the AI surface to the task, not the trend"

These are publishable, defensible, contrarian.

---

## 8. Non-coder positioning

**Is "non-coder building with AI" defensible?** Yes, but the label is doing you a disservice now.

You currently:
- Manage git branches, pre-commit hooks, merge conflicts
- Read and debug failed tests
- Understand YAML, JSON Schema, Python project structure
- Architect pipelines with conditional logic and fallbacks
- Reason about technical trade-offs

That's coder-equivalent, just learned through AI. The "non-coder" label was true 6-12 months ago, false-modesty now.

**Better labels to consider:**
- "Vibe coder" — on-trend but young term
- "AI-native builder" — forward-looking, sounds like a category
- "Practitioner who ships AI tools without an engineering background" — formal, anti-fraud
- "Officer who builds — through AI partnership" — context-anchored

**Frame "non-coder" as ORIGIN, not identity:** *"I started as a non-coder. AI let me build. Now I ship things engineers respect."*

**Your real differentiation is the intersection:** SG civil service domain + 14 shipped systems + cross-project patterns + critical voice + teaching instinct. Each is uncommon; together they're rare.

**Erosion timeline:** "Non-coder building with AI" is rare and valuable today; in 12-24 months as tools democratise, the label becomes commodity. Either deepen technically (toward coder-equivalent) or rely on broader intersection — preferably both.

---

## 9. Mode-1 gaps and skill ladder

Mode 1 = the technical complexity ceiling where "AI made me write code" stops working. Six progressive projects (full spec in `docs/learning-roadmap.md`):

1. **Harden sg-sme-profiler** — production-readiness scaffolding (1 wkd)
2. **Security audit on own project** — threat modelling (1 wkd)
3. **Multi-user SME tracker** — concurrency / state (2 wkd)
4. **Self-hosted with monitoring** — ops / observability (2 wkd)
5. **Performance optimisation of erp-mapper** — profiling / db (2 wkd)
6. **Full public deployment** — end-to-end (multi-week)

Each project produces a learning artifact (LinkedIn post + long-form + pattern + talk segment). By project 4 you have ~16 pieces of differentiated content.

---

## 10. Production-readiness

**Risk-tiered "is this ready?" framework:**

| Audience | Bar |
|---|---|
| Personal use | Works for you, has readable logs |
| Small trusted team | + Env vars, basic auth, no PII in logs, daily cost cap |
| Free public tool | + Rate limiting, input validation, friendly errors, monitoring, reachable when broken |
| Paying customers | + Tests for critical paths, deploy pipeline with rollback, dep security scan, incident playbook |
| Regulated / gov-facing | + Threat model, PDPA compliance, audit trail, pen-test, sign-off |

**Five concrete checks AI tools won't volunteer:**
1. Run `bandit` / `npm audit` for security
2. Run `pip-audit` for dep vulnerabilities
3. Trace sensitive data paths manually
4. Adversarial testing (paste bombs, SQL, prompt injection)
5. Have another AI critique your code for production-readiness

**The line for teaching SMEs:** *"Vibe coding gets you a working prototype in a weekend. Getting that prototype to safely face real users is another month of work — and it's mostly NOT the code, it's the scaffolding around the code."*

---

## 11. Naive SME prompt

**The teaching insight.** When SMEs ask *"can I just build an AI agent ready for business use?"* they encode four hidden assumptions:

| Assumption | Reality |
|---|---|
| AI can do anything if described well | AI prototypes anything; productionising is 70% of work |
| Vibe coding eliminates engineering | Lowers bar, doesn't eliminate ops/security/scale |
| Agent = smart assistant | Agents are most expensive surface (10-50× cost) |
| "Ready" is a checkbox | 5-tier concept; each ~2× effort of previous |

**The reframe — three stacked questions:**
1. *Can I get value from AI?* — Yes, almost certainly
2. *Is the answer an agent?* — Almost certainly no
3. *Is it ready for business use?* — Depends which "ready"

**Five questions SMEs should ask BEFORE "build me an agent":**
1. What ONE recurring task am I trying to remove?
2. How much time / money does this task cost today?
3. Could a generic AI tool do this task?
4. What would it cost if AI got this wrong?
5. Who maintains it 3 months from now?

If 2+ are shaky → not ready for an agent → start with trained assistant.

---

## 12. Cold-vs-context demo

**Teaching device.** Same prompt, two Claude Code sessions:
- **Cold:** fresh directory, no CLAUDE.md, no projects.yaml, no schemas. (Or claude.ai web with no project.)
- **Full-context:** workspace with all the harness.

**Setup options:**
1. claude.ai web (no project) vs Claude Code in workspace — easiest, two screens
2. `/tmp/cold-claude` fresh dir vs workspace — same model, only context differs
3. `CLAUDE_CONFIG_DIR=/tmp/cold-config claude` — truly fresh, no global CLAUDE.md leakage

**Prompts that maximise visible difference** (context-dependent):
- "Help me add a new project to my portfolio"
- "I want to build an AI tool that profiles SMEs"
- "Write a pattern doc about something I've built"
- "Set up a new project called sme-finder"

**Prompts that DON'T differentiate** (avoid):
- "Write me a Python script to sort a list"
- "Explain what an LLM is"

**Teaching line:** *"AI is a function of what you feed it, not just what you ask it. The leverage isn't being better at asking — it's building the context that makes asking work. That's the real vibe coding skill, and it's the part most demos hide."*

---

## 13. Crux tensions

### A. Teaching vs copying

**Risk:** showing examples enables surface mimicry without understanding. SMEs replicate your patterns without recognising the principles.

**Detection test:** *"Could the audience apply this to a different problem than the one I showed?"*

**Techniques to flip copying into learning:**
1. Show the decision, not just the output (3 alternatives + why you chose this one)
2. One concept, multiple examples (forces pattern recognition)
3. Adversarial framing ("which one of these are YOU?")

**Six-month signal:** the SME applies the lesson to a problem you never discussed → they learned. They only apply it to your exact case → they copied.

### B. Vendor displacement

**Risk:** "vibe coding for SMEs" content reads as "replace your vendors with AI." That's wrong (often), reputationally risky, and strategically narrow.

**The honest decision frame — build vs buy for SMEs:**

| Factor | Lean BUILD | Lean BUY |
|---|---|---|
| Specificity | Unique to your biz | Common across many |
| Complexity | Single-purpose, narrow | Multi-feature, integrated |
| Maintenance capacity | Someone reliable will own it | No in-house owner |
| Security stakes | Low, low blast radius | High, regulatory |
| Scale | Single/small team | Many users, growth |
| Time horizon | Experimental, short | Operational, long-term |
| Compliance | Self-managed | Cert required (SOC2, PDPA) |
| Learning value | Build teaches you | Buy lets you focus |
| 3-year TCO | Build < buy | Build > buy |
| Continuity risk | OK if broken for a week | Business-critical |

**Rule of thumb:** 6+ on either side → that's the answer. Mixed → buy first, build only after feeling friction.

**What vendors still genuinely offer:** maintenance forever, security expertise, compliance certs, ongoing improvements, insurance / SLA, multi-tenant learnings, specialised UX.

**The honest pitch to SMEs:** *"Vibe coding lets you build what was unbuildable a year ago. But it doesn't make vendors obsolete — it changes WHICH vendors you need. Build the parts unique to your business; buy where vendors do it better than you ever will. The skill isn't 'replace vendors' — it's knowing which is which."*

**For your positioning:** be the **build-vs-buy literacy** voice, not the "AI replaces everything" voice. More durable niche.

---

## 14. Open items + next steps

### Talk-prep deliverables (Phase 7, Tasks 32-34)
- [ ] Cold-vs-context demo recipe + captured comparison (Task 32)
- [ ] Build-vs-buy pattern doc (Task 33)
- [ ] 5-questions-before-AI-agent handout (Task 34)

### Skill-building (Phase 6, Tasks 26-31)
- [ ] Project 1: Harden sg-sme-profiler — start when ready
- [ ] Projects 2-6 sequential

### Open decisions
- Lock the positioning sentence: "AI-native builder in [niche]"
- Decide on first LinkedIn cadence (start week of talk)
- Pick first credential / cert track (NUS-ISS, AI Singapore apprenticeship, Anthropic AI Fluency)

### Open from earlier in workspace work
- Track 2 bench: identify 5-10 named candidates via LinkedIn after this session's institutional map
- Track 3 first content piece: distil one of the patterns or this conversation into a LinkedIn post

---

## Notes about this file

- Created 2026-05-13 as a checkpoint capture of ~3 days of thinking
- Will be referenced when drafting:
  - Talk slides (sections 1, 2, 3, 11, 12 are most talk-ready)
  - Pattern docs (sections 13a → teaching framework pattern; 13b → build-vs-buy pattern)
  - Handouts (section 11 → 5 questions handout)
  - LinkedIn posts (any single section can become a 400-word piece)
- Not for publication — internal source material only
