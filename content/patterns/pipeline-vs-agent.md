---
title: "Pipeline vs agent — when to choose each"
slug: pipeline-vs-agent
summary: "A practical decision framework for choosing between a deterministic AI pipeline and an autonomous agentic system, with three side-by-side examples from real projects."
visibility: public

problem: |
  AI work can be structured as a fixed pipeline of bounded steps OR as autonomous agents that decide what to do. Choosing wrong is expensive: pipelines applied to open-ended problems are brittle; agents applied to known problems are wasteful and unauditable. How do you decide which shape fits?

solution: |
  Apply the decision rubric: pipelines win when the steps are knowable, the input space is bounded, and reproducibility matters. Agents win when the steps are not knowable in advance, the decision tree is input-dependent, or editorial judgment is the work itself. Most production AI is pipeline-shaped, not agentic — calling a 25-step deterministic sequence "agentic" because it sounds modern erodes the meaning of the word.

when_to_use: |
  Reach for a PIPELINE when:
  - The steps are knowable and stable
  - Inputs share a common structure
  - Reproducibility matters (audit, compliance, regulatory)
  - Cost matters (agents spend tokens reasoning, then more tokens working)
  - Failure modes need to be constrained
  - The output is a structured artifact

  Reach for an AGENT when:
  - The next step depends on the current step's output in unpredictable ways
  - Tool composition is dynamic — you don't know in advance which tools solve it
  - Editorial judgment, synthesis, or opinion is the work
  - The interaction is genuinely multi-turn with stateful context
  - The problem space is open-ended

examples:
  - project: erp-mapper
    note: "Deterministic pipeline is correct. 25 known steps, bounded inputs, regulatory artifact."
  - project: policy-lens
    note: "Multi-agent flow is correct. Open-ended policy comparison; sources and depth vary per question."
  - project: news-digest
    note: "Pipeline chosen for cost and consistency, even though agentic could work. Worked example of trade-off resolution."

workflow_stages: [define, delegate, document]
outcomes: [improve_quality, reduce_risk]

authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
---

## The decision in one sentence

A pipeline is the right shape when you know the steps. An agent is the right shape when you don't.

Most builders default-assume "agentic = modern = better." It isn't. A pipeline is older, simpler, cheaper, and more defensible. The cost of choosing agent when pipeline fits is paid every run forever — in tokens, latency, and unexplainable outputs. The cost of choosing pipeline when agent fits is paid once, when you discover the system can't handle inputs it wasn't designed for.

This page walks three real projects from the workspace through the same decision, showing where each verdict lands and why.

---

## Decision rubric

| Question | If yes, lean pipeline | If yes, lean agent |
|---|---|---|
| Are the steps knowable up front? | YES → pipeline | NO → agent |
| Do all inputs share a common structure? | YES → pipeline | NO → agent |
| Is reproducibility a hard requirement? | YES → pipeline | (agents are hard to reproduce) |
| Is cost-per-run a constraint? | YES → pipeline | (agents reason out loud, paying for the reasoning) |
| Is editorial / opinion the work itself? | (pipelines do mechanical) | YES → agent |
| Does the next step depend on the previous in unpredictable ways? | (pipelines are predictable) | YES → agent |
| Will an auditor / regulator review the output? | YES → pipeline | (agent traces are not enough) |
| Is the input space genuinely open-ended? | (pipelines need a shape) | YES → agent |

If most of your "yes" answers fall in the left column, build a pipeline. If most fall right, build an agent. Mixed signals usually mean **a deterministic core with an agentic edge** — the most common production shape.

---

## Example 1 — `erp-mapper` (pipeline-correct)

**The problem.** Map IMDA's pre-approval catalogue (89 software-vendor categories) into 10 generic ERP modules so vendors can find which categories their product fits and SMEs can find which products fit their needs. Output: structured JSON + a public dashboard. Audience expects defensibility — vendors will rely on this for grant eligibility decisions.

### Pipeline approach (chosen)

```
scrape (89 pages)
  → parse (HTML to structured JSON)
  → dedup (lexical + semantic via Haiku)
  → tag (each requirement -> ERP module(s) via Haiku)
  → cluster (three views: solution-based, requirement-based, union)
  → re-rank criticality (Haiku)
  → audit (deterministic validators)
  → publish JSON + Excel + Observable viewer
```

Each Haiku call is a bounded prompt with a 1000-token ceiling and JSON-only output. Steps are checkpointed; re-runs produce identical output. Total ~25 steps, cost-bounded per run.

### Agentic alternative (rejected)

```
agent loop:
  - read an IMDA page
  - decide which existing modules it fits OR propose a new module
  - decide whether to re-categorise existing pages given new info
  - decide whether the result is consistent enough to publish
  - if not, re-run with adjusted reasoning
```

The agent would have access to: IMDA page fetcher, ERP module taxonomy reader/writer, classifier, validator. Decisions emerge from the agent's reasoning rather than from a fixed sequence.

### Side-by-side

| Axis | Pipeline | Agent |
|---|---|---|
| Reproducibility | Identical output across runs | Different decisions per run |
| Cost | ~25 bounded prompts × known size | Variable; reasoning tokens dominate working tokens |
| Auditability | Cached JSON at each step is the audit trail | Agent traces are necessary but not sufficient |
| Defensibility | "Here's the rule, here's the data" | "Here's what the agent decided, on this run" |
| Failure mode | Steps can fail loudly; re-run from checkpoint | Agent can hallucinate decisions silently |
| New IMDA category | Re-run pipeline, get incremental output | Agent re-decides existing categorisations too |

**Verdict: pipeline wins decisively.** The steps are knowable, the inputs share a common structure (HTML pages with a parsed schema), and the output is regulatory-adjacent — vendors making real money decisions read this. Agentic non-determinism is a liability, not a feature.

**The teaching point.** A pipeline of 25 LLM calls is impressive but it is *not* agentic. A deterministic sequence is not agentic, even if every step uses an LLM. Confusing length with autonomy is the most common error.

---

## Example 2 — `policy-lens` (agent-correct)

**The problem.** Compare SME policies across countries (Finland, Denmark, Korea, Singapore). Surface what works, what doesn't, why. Inputs are unstructured (academic papers, government reports, news, regulatory filings, interviews). Questions from users are open-ended ("how does Denmark's apprenticeship subsidy compare to Singapore's PSG, and what would adopting their approach require?").

### Pipeline approach (rejected)

```
scrape sources -> classify topic -> extract claims -> cluster by country -> summarise per cluster
```

This works for "give me a summary of Danish SME policies" but breaks the moment a user asks a comparative question. A pipeline can't pre-compute every possible cross-country pairing × every possible policy dimension. Either the pipeline becomes a Cartesian product (too large) or it becomes a search engine (which is what we're trying to avoid).

### Agentic approach (chosen)

```
multi-agent flow:
  discovery agent  - find relevant sources for the user's question
  policy_analyst   - read sources, extract policy mechanisms
  economist        - reason about incentive structures and outcomes
  synthesiser      - integrate the analyst + economist into an answer
```

Each agent has a specific role and tool access (search, read, summarise, compare). The number of sources, the depth of analysis, and the structure of the answer all depend on the question. The synthesiser decides when the answer is good enough.

### Side-by-side

| Axis | Pipeline | Agent |
|---|---|---|
| Question coverage | Limited to pre-computed dimensions | Open-ended |
| Source strategy | Pre-decided | Question-dependent |
| Reasoning depth | Fixed | Adapts to complexity |
| Cost | Predictable | Higher and variable |
| Reproducibility | High | Low (and that's okay) |
| Trust model | "Trust the pipeline's design" | "Trust the agents' reasoning, surface their work" |

**Verdict: agentic wins.** The question space is unbounded, sources need question-specific filtering, and synthesis IS the work. A pipeline approach would either over-pre-compute or degrade into a thin search wrapper.

**The teaching point.** When the work is judgment under uncertainty, encoding the steps in advance is the wrong shape. Agents earn their cost by being responsive to inputs the designer didn't anticipate. The right concession to determinism is *agent traces* — make every decision visible, even if you can't make it reproducible.

---

## Example 3 — `news-digest` (either could work; pipeline chosen)

**The problem.** Aggregate news from RSS + NewsAPI, dedup, and deliver two daily digests of what matters. Inputs share a structure (articles with title/body/link), but the world's news is genuinely open-ended — what counts as "matters" varies daily.

### Pipeline approach (chosen)

```
ingest (RSS every 15 min, NewsAPI at digest time)
  -> embed (sentence-transformer, local, free)
  -> cluster (cosine similarity, 72h window, 0.65 threshold)
  -> score (importance, niche, velocity)
  -> summarise per cluster (LLMRouter: Gemini -> Claude -> Groq)
  -> tag sentiment per cluster
  -> deliver as digest
```

Each step is bounded. Embeddings run locally and frequently (free). LLM summarisation runs once per cluster, twice a day (cost-bounded).

### Agentic alternative (rejected for cost reasons)

```
agent loop, twice daily:
  - read all articles since last digest
  - decide which clusters matter to which user
  - decide what to summarise and how long to spend on each
  - decide whether to follow up on developing stories
  - write the digest in a voice tuned to the reader
```

This would produce *better* digests in the editorial sense — more nuanced, more responsive to user preferences, more able to surface "this is connected to that" insights across stories. But it would also cost roughly 10–50× more in tokens, and the variance in output quality and length would frustrate readers expecting a consistent rhythm.

### Side-by-side

| Axis | Pipeline | Agent |
|---|---|---|
| Editorial quality | Good — clusters surface the same story across sources | Better — could find non-obvious connections |
| Cost per digest | Bounded (one LLM call per cluster) | 10–50× higher (agent reasons, then writes) |
| Consistency | Same shape every day | Variable |
| Latency | Predictable | Variable (could be very long) |
| User trust | Reliable rhythm | Editorial surprise (good and bad) |

**Verdict: pipeline chosen, despite agentic having editorial upside.** The deciding factors are cost (free-tier LLM provider rotation only works because each call is bounded) and consistency (users expect a digest, not an essay). The editorial trade-off is real and acknowledged — if cost weren't a constraint, an agentic version would be the more interesting product.

**The teaching point.** Sometimes the right answer is "agentic would be better, but the budget says pipeline." That's an honest engineering call, not a failure of imagination. Document it explicitly so future-you knows what was sacrificed and why.

---

## Common pitfalls

**Calling a long pipeline "agentic" because it uses an LLM.** A 25-step Haiku pipeline is not agentic. Length isn't autonomy.

**Calling a single LLM call "agentic" because it has a system prompt.** A prompt isn't an agent. Agents make decisions across multiple LLM calls, with state.

**Building agentic when pipeline would do, "to demo the modern stack."** This is the most expensive form of resume-driven development. The audit-trail debt compounds.

**Building pipeline when agentic would do, "to keep things deterministic."** Predictability is a feature only when it serves the user. For open-ended problems, locking down the steps locks out the work.

**Refusing to mix shapes.** Real systems often have a deterministic core (data ingestion, validation, structured output) with an agentic edge (synthesis, query, integration). Treat them as separable concerns, not competing paradigms.

---

## Decision worksheet

When you're picking the shape for a new AI system, answer these in writing — your future-self auditor will thank you:

1. **What are the inputs?** If they share a schema, lean pipeline. If they're free-form, lean agent.
2. **What are the steps?** If you can list them now, lean pipeline. If you genuinely can't, lean agent.
3. **Who reads the output?** If a regulator / auditor / lawyer might, lean pipeline. If a human consumer with editorial taste, lean agent.
4. **What's the cost ceiling?** If tight, pipeline. If flexible, either.
5. **What does failure look like?** If it must be observable and recoverable, pipeline. If "the agent didn't do well today" is acceptable, agent.

If you can't answer any of these, you don't yet know enough to pick. Spike a thin version of both and see which the data supports.

---

## See also

- `~/claude/erp-mapper` — the deterministic pipeline reference (25 steps, regulatory artifact)
- `~/claude/policy-lens` — the multi-agent reference (open-ended policy comparison)
- `~/claude/news-digest` — the cost-bounded pipeline reference (where editorial agentic loses to budget)
- `~/claude/smebot` — a pragmatic mix: mostly single-call pipeline, with one bounded agentic module (vent conversation) where multi-turn judgment is the work
