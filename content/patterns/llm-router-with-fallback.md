---
title: "LLM router with provider fallback"
slug: llm-router-with-fallback
summary: "A single LLM provider is a single point of failure: rate limits, free-tier exhaustion, transient outages. A small routing layer that fans calls across providers — Gemini, Claude, Groq, or whatever you have — buys resilience for almost no cost."
visibility: public

problem: |
  When an AI feature depends on a single LLM provider, every provider hiccup becomes your hiccup. Free tiers exhaust unpredictably. Rate limits trigger at the worst times. A provider outage takes the whole system down. Building a fallback chain after the first incident is too late — by then, calling code is scattered across the project.

solution: |
  Wrap LLM calls in a router that fans across N providers in priority order, tracks daily caps per provider, falls back gracefully on rate-limit or quota errors, and exposes a single interface to the rest of the application. The router lives in one place; the application code never knows which provider answered.

when_to_use: |
  Use a router when:
  - You depend on free tiers (which exhaust without warning)
  - You have multiple providers available (Gemini, Claude, Groq, OpenAI, local models)
  - Quality across providers is "close enough" for your use case
  - The cost of an outage exceeds the cost of building the router

  Skip the router when:
  - You need a specific model's specific behaviour (e.g. only Claude Opus's reasoning quality)
  - You require provider-specific features (tool use formats, structured output guarantees)
  - Compliance requires a specific provider or region
  - Latency budget rules out fallback chains (each retry adds RTT)

examples:
  - project: shared
    note: "Workspace-shared LLMRouter (Gemini -> Claude -> Groq) with daily caps and per-provider tracking. The reference implementation."
  - project: news-digest
    note: "Uses the router for digest summarisation; if Gemini's quota is gone, Claude takes over without a code change in news-digest itself."
  - project: compare-agent
    note: "Free-tier rotation across providers is the architectural premise — the bot wouldn't be cost-viable without it."

workflow_stages: [delegate, discern, document]
outcomes: [reduce_risk, save_time, improve_quality]

authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
---

## What the router does

A single function — `callAI(system, user, model_hint=None)` — that:

1. **Picks a provider** based on priority order, current daily cap usage, and any model hint
2. **Calls that provider** with the prompt
3. **Catches provider-specific errors** (rate limit, quota, transient 5xx)
4. **Falls back to the next provider** in the chain on retryable failure
5. **Tracks usage** per provider per day (so the next call knows what's available)
6. **Returns the answer** with metadata (which provider answered, latency, cost estimate)

The application code calls `callAI(...)`. It does not know whether Gemini, Claude, or Groq answered. That decoupling is the point.

---

## Side-by-side — single-provider vs router

### Problem
Summarise 30 news clusters at digest time, twice a day. Cost-sensitive personal project; free tiers must be respected.

### Single-provider approach

```
def summarise(cluster):
    return anthropic.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        system="...",
        messages=[{"role": "user", "content": cluster.text}]
    )
```

What goes wrong:
- Anthropic free tier hits its daily cap mid-digest at the worst time (third digest of the week, 2 AM)
- The bot crashes loudly or — worse — silently returns errors as content
- A transient 5xx from the provider takes down the whole digest run
- When you decide to add Gemini later, every call site needs editing
- Cost tracking lives in Anthropic's dashboard, not in your code

Workaround attempts:
- Try/except with hard-coded retries → still single-provider
- Wait for cap reset → digest is hours late
- Pay for a higher tier → defeats the purpose

### Router approach

```
def summarise(cluster):
    return llm_router.call(
        system="...",
        user=cluster.text,
        max_tokens=400,
        # router picks provider based on priority + caps:
        # 1. Gemini (free tier, used until cap)
        # 2. Claude  (free tier, used until cap)
        # 3. Groq    (free tier, used until cap)
    )
```

What changes:
- Daily cap on Gemini hit at noon → router silently switches to Claude for the next call
- Anthropic outage at 2 AM → router fans to Groq, digest still ships
- Adding a new provider tomorrow → one config edit, zero changes to `summarise()`
- Cost tracking lives in the router, queryable from anywhere
- Per-provider failure modes (timeouts, malformed responses) handled in one place

The application gets simpler. The infrastructure gets one new module. The total system is more resilient.

### Side-by-side outcomes

| Axis | Single-provider | Router |
|---|---|---|
| Resilience to quota | None | Falls through chain |
| Resilience to outages | None | Falls through chain |
| Cost transparency | Provider dashboards | One unified log |
| Adding a provider | Edit every call site | One config change |
| Provider-specific features | Available | Lost (or behind opt-in) |
| Latency on first call | One RTT | One RTT (fallback only on failure) |
| Quality variance | Zero (one provider) | Some (acceptable for many tasks) |
| Cost | Whatever the chosen provider charges | Lowest available across chain (free tiers used first) |

For most production tasks where "any modern LLM is fine," the router pays for itself the first time a provider blips. For tasks where the model's specific behaviour matters, prefer a single provider — but log the provider explicitly so you know what you're depending on.

---

## Workspace example — `shared.LLMRouter`

The workspace ships a single `LLMRouter` module under `~/claude/shared/` consumed by 4+ projects. Roughly:

```python
class LLMRouter:
    PROVIDERS = ["gemini", "claude", "groq"]   # priority order
    DAILY_CAPS = {"gemini": 1500, "claude": 50, "groq": 14400}

    def call(self, system, user, max_tokens=1000):
        for provider in self.PROVIDERS:
            if self.usage_today(provider) >= self.DAILY_CAPS[provider]:
                continue
            try:
                response = self._dispatch(provider, system, user, max_tokens)
                self._record_usage(provider, response.tokens_used)
                return response
            except (RateLimitError, QuotaError, TransientError):
                continue
        raise AllProvidersFailedError()
```

Real implementation has more — exponential backoff, per-provider transformations of the prompt format, response normalisation across providers, daily reset logic. But the shape is exactly that: try in order, skip on cap, fall through on retryable error, raise only when all providers fail.

The 4+ consumer projects (`compare-agent`, `news-digest`, `event-radar`, plus others) call `router.call(...)` and never know which provider answered. When `claude-orchestrator` or smebot want to use the same pattern, they import the same module — no duplication.

---

## Common pitfalls

**Falling back silently with no observability.** If the router quietly switches from Claude to Groq, the calling code may not notice that output quality changed. Log every call with the provider that answered. Surface failure rate per provider in a dashboard or weekly digest.

**Treating providers as interchangeable when they aren't.** Quality differences between providers are real. For some tasks (creative writing, complex reasoning, instruction-following on long context), the gap is large enough that fallback degrades the user experience. Test each provider against your actual prompts before adding it to the chain.

**Hard-coding the priority order.** Today's "Gemini first" might be next year's "Groq first" as pricing and tiers shift. Make the priority order config-driven so changes don't require code edits.

**Not normalising output shapes.** Different providers return different JSON, different message formats, different error types. The router should normalise everything to one shape so the calling code is provider-agnostic. Otherwise, the abstraction leaks and you're back to provider-specific branches in application code.

**Conflating routing with retrying.** Retrying within a provider (transient failure) and falling back to a different provider (persistent failure) are different policies. A good router does both, but the rules are separate: retry-with-backoff inside one provider, fall-through across providers.

**Using free-tier rotation as primary architecture.** It works for personal projects and prototypes. It's fragile for revenue-bearing systems where a provider can change terms unilaterally. For paid usage, route for resilience but pay for the priority provider.

---

## How to start a router

Minimum viable router for a 1-person project:

1. **Wrap one provider.** A function `call(system, user)` that hits Anthropic. Get this clean and tested.
2. **Add a second provider behind a feature flag.** Same signature, different SDK. Same response shape (the router normalises).
3. **Add a try/except fallback.** If the first provider raises a retryable error, call the second.
4. **Add daily-cap tracking.** A simple dict in memory (or sqlite for persistence) that increments on each call.
5. **Make priority order config-driven.** A list in a yaml file, not hard-coded.
6. **Log every call.** Provider, latency, tokens, success/failure. Inspect weekly.
7. **Add a third provider when you hit caps regularly.** Same shape; the router doesn't care about the count.

Total time: ~1 day for steps 1–4, another half-day for 5–7. The cost amortises over every project that uses it.

---

## See also

- `~/claude/shared` — workspace LLMRouter (Gemini -> Claude -> Groq). The reference implementation.
- `~/claude/news-digest` — consumer: digest summarisation
- `~/claude/compare-agent` — consumer: free-tier rotation as architectural premise
- `~/claude/event-radar` — consumer: event scoring with fallback
- Pattern: `harness-over-prompt-engineering` — the router is a harness layer; the rest of the harness (validators, contracts, retries) sits on top of it
- Pattern: `pipeline-vs-agent` — both shapes benefit from a router; the router is independent of pipeline-vs-agent choice
