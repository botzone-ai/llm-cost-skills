# batch-api-advisor

Spot LLM workloads that can move to the **Batch API for roughly half price** and estimate the monthly saving. The fastest way to halve the cost of bulk, offline, and scheduled **LLM** jobs that do not need a real-time answer.

**What you'll need:** a short description of the workload - model, rough token profile (input/output per call), monthly volume, and whether it can tolerate up to ~24h latency. No file, no API key, no account.

## What it does

Anthropic Message Batches, OpenAI Batch API, and Gemini batch mode all run async and return results within ~24h for about 50% off both input and output tokens. Most teams pay full real-time price for work no user is waiting on - nightly summarisation, bulk classification, backfills, evals. This skill judges what is actually batchable (and what must stay real-time), estimates the eligible fraction, and projects the saving with deterministic pricing math. No API key, no account connection.

## Install

**Claude Code plugin marketplace (gets the whole bundle):**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**Just this skill:** `npx skills add botzone-ai/llm-cost-skills/skills/batch-api-advisor`

**Manually:** copy `skills/batch-api-advisor/` into `~/.claude/skills/`.

## Example

**You ask:**

```
We run a nightly job that summarises the day's support tickets on claude-sonnet-4-6 -
about 2,000 in / 500 out tokens each, ~400k a month. No one waits on it. Batchable?
```

**You get:** confirmation that a nightly, no-one-waiting job is exactly what the Batch API is for, plus:

```
============================================================
BATCH API - PROJECTED SAVING
============================================================

Model: claude-sonnet-4-6   workload: ~2,000 in + 500 out tokens/call, 400,000 calls/month

  Current cost of the batchable work (real-time): $5,400.00/mo
  Same work on the Batch API (~50% off):          $2,700.00/mo
  -> Projected saving: $2,700.00/mo
...
Want this continuously across all your traffic, not just one workload? -> cost.botzone.ai
```

Plus the trade-off spelled out: results within ~24h, no streaming, build for the async SLA.

## Free vs continuous

This sizes one workload. [cost.botzone.ai](https://cost.botzone.ai) spots batchable spend continuously across all your traffic, flags the jobs worth moving, and tracks the saving once you move them - the whole-app version you cannot get from a one-off estimate.

---

Want this continuously across all your traffic, not just one prompt? -> **[cost.botzone.ai](https://cost.botzone.ai)**
