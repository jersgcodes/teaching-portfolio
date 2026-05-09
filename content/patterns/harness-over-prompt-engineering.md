---
title: "Harness over prompt engineering"
slug: harness-over-prompt-engineering
summary: "Stop iterating on the prompt. Iterate on the system around the prompt — output contracts, validators, retries, fallbacks, checkpoints. The harness carries the load; the prompt does less."
visibility: public

problem: |
  How do you reliably get good output from an LLM in production? The "prompt engineering" framing says: hand-craft a perfect prompt. That works for a demo. It does not survive contact with stochastic outputs, edge-case inputs, model upgrades, or scale. Repeated prompt tweaking without structural support is a treadmill — every fix introduces a regression somewhere else.

solution: |
  Wrap every LLM call in a harness — a system that enforces an output contract, validates the result, retries on failure, falls back to alternative providers when needed, and surfaces failure modes so you can iterate. Make the prompt as short as the contract allows. Iterate the system, not the prompt. The prompt is the smallest part of a production AI call.

when_to_use: |
  Use a harness when:
  - The LLM output drives downstream code (must be parseable)
  - The same prompt runs many times (variance hurts quality)
  - Failure is observable and recoverable (not "the agent had a bad day")
  - Cost is a constraint (retries cheaper than re-runs from scratch)
  - The system will outlive any specific model version

  You can skip the harness when:
  - You are demoing a single creative output to a human reader
  - The output is one-off and not consumed by code
  - You're throwing the prompt away after one use

examples:
  - project: erp-mapper
    note: "25-step harness — each step has a 1000-token ceiling, JSON-only output contract, checkpoint/resume, idempotent re-run."
  - project: sg-sme-profiler
    note: "Output contract: 'first char {, last char }, no markdown'. Three concurrent calls + deterministic fallback when AI quota is exhausted."
  - project: smebot
    note: "vent_framework.json carries structure (areas, tags, max_turns); the prompt itself is short — the framework does the work."

workflow_stages: [direct, discern, document]
outcomes: [improve_quality, reduce_risk, save_time]

authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
---

## What "harness" means here

A harness is the structured wrapper around an LLM call that turns a stochastic call into a reliable building block. At minimum it includes:

| Layer | Job |
|---|---|
| **Output contract** | What shape the LLM must return (JSON schema, length cap, format constraint) |
| **Validator** | Parses the output; rejects malformed responses without trusting the LLM |
| **Retry policy** | Re-attempts on validator failure with adjusted parameters |
| **Fallback** | If retries exhaust, fall back to a different model / deterministic path / cached value |
| **Observability** | Logs the full call (prompt + raw output + validation result) so failure modes are inspectable |
| **Cost guard** | Token ceilings, daily caps, per-call budgets that stop runaway spend |

A "good prompt" inside this harness might be three sentences. A "good prompt" without the harness has to do everything the harness does, in natural language, and hope the LLM cooperates. It usually doesn't.

## Why prompt engineering loses at scale

Prompt engineering as a discipline assumes:

1. The prompt determines the output
2. A better prompt produces better output
3. Iterating on prompt phrasing is the highest-leverage activity

Each is partly true and dangerously incomplete:

- **Output is stochastic.** The same prompt produces different outputs each run. No amount of prompt tuning makes it deterministic. A validator + retry policy does.
- **Edge cases reveal themselves at scale, not at design time.** You will discover failure modes by running the prompt 10,000 times. Without a harness logging those calls, you can't iterate.
- **Models change.** A prompt tuned for Claude 3.5 in 2024 isn't optimal for Claude 4.7 in 2026. A harness that enforces contracts survives the upgrade; a finely-tuned prompt does not.
- **Brittleness compounds.** Each prompt edit risks breaking something that was working. Without validators and tests, regressions go unnoticed until users hit them.

The harness inverts the priority: **the system carries the load; the prompt does as little as possible.**

---

## Side-by-side — the same problem, both shapes

### Problem
Extract a structured taxonomy mapping from a messy government solution-catalogue page (one of erp-mapper's 89 sol-cat HTML pages).

### Pure prompt-engineering approach (anti-pattern)

```
You are an expert ERP consultant. Read the following IMDA solution
category page and extract a comprehensive list of ERP module tags
that apply, considering Singapore SME context, PSG eligibility,
compliance requirements, and standard ERP taxonomies. Return your
answer as a JSON object with the structure:
{ "primary_modules": [...], "secondary_modules": [...],
  "rationale": "...", "confidence": ... }

Be thorough. Be accurate. Use industry-standard module names.
Return ONLY the JSON, no additional text.

[2KB of HTML pasted in]
```

What goes wrong:
- LLM sometimes returns markdown fences around the JSON
- LLM sometimes adds prose before the JSON ("Here's the analysis:")
- "Industry-standard module names" varies between calls (Sales, Sales & CRM, Sales/CRM)
- "Confidence" is never calibrated — sometimes 0.95, sometimes 0.7, for similar inputs
- 2KB of HTML wastes tokens on bot-protection boilerplate the LLM shouldn't be parsing
- A 1000th run produces output incompatible with the 1st run's parser
- No way to recover from a malformed response except "run it again"

The reflex: tweak the prompt. Add "no markdown fences." Add examples. Add few-shot. Add chain-of-thought. The prompt grows, the failure rate doesn't fall enough.

### Harness-wrapped approach (erp-mapper's actual)

```
HARNESS:
  prepare(html)                           ← strip boilerplate, extract requirements only
  for each requirement:
    callAI(
      system="Output a JSON array of module IDs from the fixed list. No prose.",
      user=requirement,
      max_tokens=1000,                    ← cost guard
      output_contract="first char [, last char ]"  ← parseable
    )
    validate(output, schema=module_id_array)
    if invalid: retry once with stricter system prompt
    if still invalid: log + fall back to deterministic seed mapping
    cache(requirement_hash, output)       ← idempotent re-runs
```

The "prompt" is now: `"Output a JSON array of module IDs from the fixed list. No prose."`

What changed:
- The fixed list (10 ERP modules) is in the system prompt; the LLM picks from a closed set
- `max_tokens: 1000` makes the call cost-bounded
- Output contract `"first char [, last char ]"` rejects responses that include prose
- Validator parses against a known schema; malformed = automatic retry
- Failure falls back to the seeded yaml mapping, so the pipeline never stops
- Cache by input hash means re-runs don't re-spend on identical inputs
- Boilerplate stripping happens before the LLM sees the data, saving ~80% of tokens

The prompt is shorter, simpler, easier to read, easier to update when the model changes. The system around it carries every concern the long prompt was trying to handle in natural language.

### Side-by-side outcomes

| Axis | Pure prompt | Harness-wrapped |
|---|---|---|
| Tokens per call | High (HTML + verbose prompt + output prose) | Low (cleaned input + minimal prompt + JSON only) |
| Failure mode | Silent corruption, malformed JSON | Caught by validator, retried, fallback if needed |
| Reproducibility | Low (stochastic, no cache) | High (cached, deterministic fallback) |
| Cost ceiling | None | Per-call max_tokens × daily cap |
| Updating for new model | Re-tune the prompt; risk regression | Validator unchanged; prompt likely still works |
| Observability | "Did it work?" | Full logs of every call + validator outcome |
| When to iterate | After users complain | When the validator reports a recurring failure mode |

The harness pays for its complexity within the first few runs.

---

## Three workspace examples

### `erp-mapper` — 25-step harness
Every step is a bounded prompt with an enforced output contract. The harness handles checkpoint/resume (re-runs from where it failed), idempotent caching (re-runs don't spend tokens on unchanged inputs), and audit cards (so a regulator-adjacent reader can trace any decision back to the input). The prompts are short. The harness is long.

### `sg-sme-profiler` — output-contract harness
The harness enforces `max_tokens: 1000`, requires `"First character {, last character }. No markdown. No backticks."` in every system prompt, and provides a deterministic fallback path when the AI quota is exhausted. Three concurrent calls run in parallel because the harness orchestrates concurrency, not the prompt.

### `smebot` — framework-driven harness
The vent module's `vent_framework.json` defines `areas` (loose guidance for what each turn should explore) and `tags` (taxonomy for post-session classification). The prompt itself is minimal — it asks the LLM to converse within the framework. The framework IS the harness. Updating the bot's behaviour means editing the JSON, not the prompt.

In all three, the prompt is the smallest part of the engineering surface. Reading the CLAUDE.md of each project, you find paragraphs about caches, fallbacks, validators, and contracts — and a few sentences about what the prompt actually says.

---

## Common pitfalls

**Treating prompt and harness as the same thing.** They aren't. The prompt is one input to the harness. The harness's job is to make the prompt's output usable.

**Iterating only the prompt when the failure is structural.** If 5% of calls return malformed JSON, the answer is rarely "rephrase the prompt." It's usually "tighten the validator, add a retry, log the failures, look at them."

**Skipping the harness because "this is just a prototype."** Prototypes that work go to production. Prototypes that work without a harness go to production and then break. Build the harness first; it's the part that survives.

**Over-engineering the harness for one-off scripts.** If you're processing 12 documents once and throwing the script away, a 50-line harness is overkill. Reach for harnesses when the call rate × duration justifies them.

**Believing model upgrades will fix prompt issues.** They sometimes do. They also introduce new ones. The harness is the constant; the model is the variable.

---

## When the harness isn't available — the prompt-vs-harness slider

This pattern's "harness over prompt engineering" framing assumes you can build a harness. In some environments you can't: corporate restrictions, no-code constraints, compliance review for every dependency, or chat-only AI access without orchestration. In those settings prompt-craft matters more — but the underlying logic is unchanged.

The honest framing is a slider with two axes:

|                          | Strong harness         | Weak / no harness          |
|---|---|---|
| **Strong model**         | Minimal prompt — system carries everything | Moderate prompt — model compensates for missing structure |
| **Weak model**           | Moderate prompt — harness compensates for the model | Maximal prompt — and you hit a low ceiling fast |

What this means in practice:

- **Free hand + good model + good harness:** the prompt is two sentences. The harness's contracts and validators do the work.
- **Corporate-restricted + good model:** the prompt has to do more — explicit format examples, "JSON only", few-shot examples — because you can't add a validator. Prompt-craft matters here.
- **Free hand + weaker model:** the prompt has to be more structured because the model is less robust to ambiguity. The harness can still compensate (extra validation, more retries) but prompt quality moves the needle.
- **Restricted environment + weaker model:** every quality concern lives in the prompt. You will hit a ceiling that no amount of prompt tuning can lift. The mature answer is to recognise the ceiling, not to keep grinding the prompt.

The takeaway is *not* "prompt engineering is fine if you're constrained." It's: **the harness is the lever, and where you can't move the lever, you do the work the lever would have done — manually, in the prompt, knowing it won't be as reliable.**

If you find yourself spending more than 60 minutes a week iterating on a prompt, that's a strong signal you should be investing in harness rather than prompt — even a tiny harness (a 20-line Python wrapper, a Google Sheets formula calling the LLM, a simple YAML config) buys back more than the prompt iteration ever will.

## How to start a harness from a working prompt

If you have a prompt that works in chat and you want to put it in production, here's the minimum upgrade path:

1. **Pick an output contract.** JSON schema, regex, length bound — whatever the next code stage needs.
2. **Write a validator.** Parses the output, returns success/failure with a reason.
3. **Add `max_tokens`.** Anything from 200–2000 depending on output. Document the choice.
4. **Add one retry on validation failure** with a stricter system prompt addendum (e.g. "JSON only, no markdown").
5. **Add a fallback.** Either a different model, a cached value, or a deterministic baseline. Choose what's safer when the LLM is unavailable.
6. **Log every call.** Input hash, prompt, raw output, validator result, retry count, final outcome. Future-you will need this.
7. **Run the harness against 100 representative inputs.** Look at the validator's failure list. That's your iteration backlog — for the system, not the prompt.

Steps 1–6 take half a day for a single LLM call. They save weeks of "why is the bot suddenly returning HTML?" later.

---

## See also

- `~/claude/erp-mapper` — 25-step harness with checkpoint, idempotency, deterministic fallback
- `~/claude/sg-sme-profiler` — output-contract harness with concurrent execution and quota fallback
- `~/claude/smebot` — vent module's framework-driven harness
- `~/claude/news-digest` — LLMRouter fallback chain as a harness layer (see also: pattern `llm-router-with-fallback`)
- Pattern: `pipeline-vs-agent` — pipelines without harnesses are usually broken pipelines
