---
title: "Idempotent processing with checkpointing"
slug: idempotent-checkpoint-processing
summary: "Long-running pipelines fail. Re-running from scratch is expensive. Idempotent steps with cached intermediate output let you re-run only what's changed and resume from where you crashed — without paying for the work you've already done."
visibility: public

problem: |
  Multi-step data pipelines — especially those that call paid APIs — fail in the middle. A network blip, a rate limit, a malformed input on item 47 of 89, a model upgrade that changes output shape. Re-running from scratch wastes time and money. Re-running selectively requires the pipeline to be designed for it; bolting selective re-run on later is painful.

solution: |
  Make every step idempotent (same input -> same output) and cache its output keyed by input hash. A re-run reads the cache for unchanged inputs and only does new work for changed or missing ones. Add a checkpoint file that records progress so a crash mid-step resumes from the right place. Together they turn a multi-hour, expensive run into something you can iterate on cheaply.

when_to_use: |
  Use idempotency + checkpointing when:
  - The pipeline has more than ~5 steps
  - Any step calls a paid API (LLM, external service)
  - Any step takes more than ~30 seconds
  - Inputs grow over time (you'll want to reprocess only the new ones)
  - Failures are common enough that re-running from zero is annoying
  - You'll iterate on later-stage logic without wanting to re-run early stages

  You can skip when:
  - The pipeline is short (1-2 steps), fast, and free
  - Inputs are tiny and never grow
  - You only run the pipeline once

examples:
  - project: erp-mapper
    note: "25-step canonicalisation pipeline. Each step writes structured JSON to data/. Re-running with --resume picks up where the last run failed; unchanged inputs hit the cache. Critical because individual steps cost real money via Haiku API calls."
  - project: news-digest
    note: "RSS poll every 15min uses dedup-by-fingerprint to avoid re-processing the same article. LLM summarisation runs only at digest time on new clusters. The 'don't re-do work you've already done' principle, applied at multiple cadences."
  - project: miles-optimizer
    note: "MCC mapper writes to optimizer_transactions.db; re-runs only process new statement imports. dedup.py uses 5-min amount+card fingerprint to handle multi-source ingestion (SMS + email + manual)."

workflow_stages: [define, discern, document]
outcomes: [save_time, improve_quality, reduce_risk]

authors:
  - role: drafted
    by: "Claude Opus 4.7"
    when: 2026-05-07
---

## The two ideas

### Idempotency
A step is idempotent if running it twice with the same input produces the same output (and doesn't have side effects beyond writing that output). The simplest test: can you delete the output file and re-run the step, and get the same result?

The classic violations:
- Steps that depend on wall-clock time (timestamp gets baked in)
- Steps that depend on random seeds (output varies per run)
- Steps that call non-deterministic APIs (LLMs without temperature=0; or even with, sometimes)
- Steps that mutate shared state (write to a DB row, increment a counter)

You don't always need true idempotency — sometimes "approximately idempotent" is enough (the output is functionally equivalent, even if textually different). But the closer you can get to bit-identical, the easier debugging becomes.

### Checkpointing
A checkpoint is a record of progress: "I have completed steps 1-7; if you re-run me, start at step 8." It can be:
- A file in the output directory (existence = "this step finished")
- A field in a JSON state file (`{"last_completed_step": 7}`)
- A row in a SQLite table tracking per-input progress
- A `--resume` flag that scans output directories to figure out where to start

Checkpoints work hand-in-glove with idempotency. Without idempotency, restarting from a checkpoint may produce inconsistent state. With it, restart is just "carry on from where you stopped."

---

## Side-by-side — naive pipeline vs idempotent + checkpointed

### Problem
Process 89 IMDA HTML pages through a 7-step canonicalisation: scrape, parse, dedup, tag (Haiku), cluster, rank (Haiku), validate. Each Haiku call costs ~$0.02 (so ~$3.50 per full pipeline pass).

### Naive approach

```
def run_pipeline():
    for page in pages:
        html = scrape(page)
        parsed = parse(html)
        deduped = dedup(parsed)
        tagged = tag_with_haiku(deduped)        # API call, ~$0.02
        clustered = cluster(tagged)
        ranked = rank_with_haiku(clustered)     # API call, ~$0.02
        validated = validate(ranked)
        save_to_db(validated)
```

What goes wrong:
- The script crashes on page 47 (parse error)
- Re-running starts from page 1, re-spending ~$1.84 on Haiku calls for pages already done
- Fixing a bug in the `rank` step requires re-running everything, including unchanged scrape + parse + tag work
- No way to inspect what tag step produced for page 23 — it's transient
- No way to re-run only the rank step on a subset of pages

You end up either:
- Adding ad-hoc print statements + commenting out completed steps (anti-pattern)
- Loading data into memory and writing throwaway scripts to "patch up" output (anti-pattern)
- Running the pipeline at 3 AM and hoping (anti-pattern)

### Idempotent + checkpointed approach (erp-mapper's actual)

```
data/
  raw/<page_slug>.html
  parsed/<page_slug>.json
  deduped/<page_slug>.json
  tagged/<page_slug>.json
  clustered/<page_slug>.json
  ranked/<page_slug>.json
  validated/<page_slug>.json

def run_step(step_name, input_dir, output_dir, fn):
    for page_slug in list_inputs(input_dir):
        out_path = output_dir / f"{page_slug}.json"
        if out_path.exists() and not args.force:
            continue                     # idempotent: skip work already done
        result = fn(read(input_dir / f"{page_slug}.json"))
        write(out_path, result)

def run_pipeline(args):
    if args.from_step <= 1: run_step("scrape", ...)
    if args.from_step <= 2: run_step("parse", ...)
    ...
    if args.from_step <= 6: run_step("rank", ...)
    if args.from_step <= 7: run_step("validate", ...)
```

What changes:
- Crash on page 47 in parse step → re-run starts from page 47 (everything before is on disk)
- Fixing rank step → re-run with `--from-step rank`, only rank + validate re-execute; scrape/parse/tag stays cached
- Inspecting page 23's tag output → it's a JSON file at `data/tagged/page-23.json`, just open it
- Re-running only rank for a subset → delete the relevant `data/ranked/*.json` files, re-run with `--from-step rank`
- Cost of fixing a bug in step 6 dropped from ~$3.50 to ~$0.20

### Side-by-side outcomes

| Axis | Naive | Idempotent + checkpointed |
|---|---|---|
| Crash recovery | Restart from step 1 | Restart from where it failed |
| Cost of bug fix in step N | Re-run all N steps | Re-run from step N only |
| Inspection / debugging | Print statements | Open the JSON file |
| Selective re-run | Edit the script | Delete output files, re-run |
| Iteration speed | Slow (full pipeline per change) | Fast (only changed steps re-run) |
| Memory profile | Everything in RAM | Streaming through disk |
| Code complexity | Lower at first | Higher upfront, lower over time |

The idempotent version pays for its complexity within ~3 iterations of the pipeline. By iteration 30, the gap is huge.

---

## Three workspace examples

### `erp-mapper` — the canonical example
- 25 steps, each producing a directory of JSON files keyed by input slug
- `--resume` flag scans for missing outputs and runs only the missing ones
- `--from-step N` re-runs from a specific step downward
- Per-input idempotency means re-runs are essentially free for unchanged inputs
- Critical for cost control: 89 pages × ~25 Haiku calls × ~$0.02 = ~$45 per full pipeline; selective re-runs are usually <$1

### `news-digest` — checkpointing at multiple cadences
- RSS polled every 15 minutes; dedup-by-fingerprint avoids re-processing seen articles
- Embeddings computed once per article (local, free) and cached in SQLite
- LLM summarisation runs at digest time only on new clusters since the last digest
- The "checkpoint" is implicit: the database row's existence is the cache; new articles are the only ones that need work

### `miles-optimizer` — incremental statement processing
- `mcc_mapper.py` reads the latest `transactions.db` and writes to `optimizer_transactions.db`
- Already-processed transactions are detected via primary key (transaction ID); re-runs only handle new rows
- `dedup.py` uses 5-minute amount+card fingerprint windows to deduplicate across SMS, email, and manual sources
- Cap counters reset based on statement-cycle dates, also detected at startup — idempotent in that re-running the bot doesn't double-reset

---

## Common pitfalls

**Storing intermediate outputs in memory only.** Then a crash loses everything. Write to disk after each step.

**Putting timestamps in the cache key.** Then nothing ever hits the cache. Hash the actual input content; if you must include time, round to a coarse granularity (e.g. day, not second).

**Using mutable cache keys.** A cache keyed by a list that gets sorted differently per run will miss. Hash a canonical representation.

**Forgetting that LLM calls aren't fully idempotent.** Even with `temperature=0`, models can return slightly different outputs across runs (especially after an API-side update). Cache the output, not the call. If output shape matters, validate after caching.

**Mixing idempotency levels.** If step 3 is idempotent but step 4 isn't, re-running from step 3 leaves you in a weird state. Either make every step idempotent or document explicitly which steps need to be redone together.

**Treating the cache as authoritative when the input has changed.** If `data/parsed/page-23.json` exists from yesterday but the underlying `data/raw/page-23.html` was re-scraped today, you may serve stale data. Either compare timestamps (cheap, sometimes wrong) or hash the input (robust, slightly more code).

**Not making the cache discardable.** A `--clean` or `rm -rf data/` option is essential — you'll need it. If your pipeline can't recover from "delete everything and re-run", you've coupled too tightly to the cache.

---

## How to add idempotency + checkpointing to an existing pipeline

If you have a single-pass pipeline that's getting painful to iterate on:

1. **List the steps.** Write them down in order. Each step has an input shape and an output shape.
2. **Pick a cache directory layout.** One per step, keyed by some stable input identifier (slug, hash, primary key).
3. **Convert each step to "skip if output exists, else run."** Add a `--force` flag for when you genuinely want to re-do work.
4. **Add a `--from-step N` flag.** It just gates which steps run.
5. **Migrate one step at a time.** Don't try to refactor the whole pipeline at once. Each step migration is small and independent.
6. **Test by deleting output files and re-running.** If the pipeline doesn't recover, you have a hidden non-idempotency.
7. **Add a `--clean` for "start from scratch" cases.** Deletes the cache directory; you'll need it more than you'd expect.

Total time: a few hours for a 5-step pipeline. Pays back the first time you fix a step-7 bug without re-running steps 1-6.

---

## See also

- `~/claude/erp-mapper` — the most thorough example; 25 steps, multiple resume modes
- `~/claude/news-digest` — checkpointing at multiple cadences, dedup-as-cache
- `~/claude/miles-optimizer` — incremental processing of growing input streams
- Pattern: `pipeline-vs-agent` — pipelines benefit hugely from this; agents less so (their work is non-repeating by design)
- Pattern: `harness-over-prompt-engineering` — caching + retry are core harness components
