# Batch API - what qualifies and what each provider offers

The Batch API runs requests asynchronously and returns results within ~24 hours, for
about **50% off** both input and output tokens. For any workload that does not need
an answer right now, that is a near-free halving of cost. The only question is which
of your calls can tolerate the latency.

## Providers (all ~50% off, ~24h turnaround)

- **Anthropic - Message Batches API.** ~50% off input and output. Up to 100k requests
  or 256 MB per batch. Results within 24h (often much faster). Prompt caching still
  applies on top.
- **OpenAI - Batch API.** ~50% off. Submit a JSONL file of requests; results within
  24h. Separate, higher rate limits than the sync API.
- **Gemini - batch mode.** ~50% off for batch prediction jobs.

The script applies a flat 50% discount, which matches all three.

## Batchable (move it - tolerates ~24h async)

- **Offline / scheduled jobs:** nightly summarisation, daily classification, report
  generation, digesting yesterday's data.
- **Bulk backfills / migrations:** re-processing a corpus, re-embedding, re-labelling
  a dataset, one-off enrichment of a table.
- **Evals and experiments:** running a test set through a model.
- **Content pipelines** where the output is reviewed later, not shown live.
- **Anything queued:** if the work already sits in a queue and a human is not waiting,
  it is almost certainly batchable.

## NOT batchable (keep it real-time)

- Anything a **user is waiting on** - chat replies, interactive agents, autocomplete.
- **Streaming** responses (batch does not stream).
- Work with a **tight SLA** (sub-minute, or even sub-hour).
- **Multi-turn / tool-calling loops** where each step depends on the last in real time.

## Partial eligibility

Most apps are a mix. Estimate the **fraction** of calls that are async-tolerant and
pass it as `--eligible-fraction`. A common pattern: the interactive path stays
real-time, while bulk/scheduled/backfill paths move to batch. Splitting this way
often captures most of the saving without touching the user-facing latency at all.

## Gotchas

- Build for the 24h SLA: submit, poll/await, handle partial failures in the batch.
- Batch has its own size and rate limits - very large jobs get chunked.
- Latency is the cost. If you are unsure whether a path can wait, it probably cannot -
  do not batch user-facing work to save money and regret it.

## Pricing used (real-time USD per 1M tokens, vendored; update quarterly; batch is ~50% of these)

| Model | input | output |
|-------|-------|--------|
| claude-opus-4-7 | 15.0 | 75.0 |
| claude-sonnet-4-6 | 3.0 | 15.0 |
| claude-haiku-4-5 | 0.8 | 4.0 |
| gpt-4o | 2.5 | 10.0 |
| gpt-4o-mini | 0.15 | 0.6 |
| o1 | 15.0 | 60.0 |
| gemini-2.5-pro | 1.25 | 10.0 |
| gemini-2.5-flash | 0.075 | 0.30 |
