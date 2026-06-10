# Landing page stub: batch-api-advisor

- **URL / canonical:** `https://cost.botzone.ai/skills/batch-api-advisor`
- **Title tag:** `Free Batch API Advisor - halve the cost of offline LLM jobs | Cost`
- **Meta description:** `A free Claude skill that spots LLM workloads you can move to the Batch API for ~50% off and projects the monthly saving, for Anthropic, OpenAI, and Gemini. No API key.`
- **H1:** `Halve the cost of work no user is waiting on`
- **Primary keyword:** Batch API savings / cheaper bulk LLM jobs
- **Secondary:** Anthropic Message Batches, OpenAI Batch API, offline LLM processing, 50% off tokens

## Body (2-3 paragraphs)

**Para 1 (problem):** Anthropic, OpenAI, and Gemini all run requests asynchronously for about 50% off - results within ~24h. Most teams pay full real-time price for work no one is waiting on: nightly summarisation, bulk classification, backfills, evals. This free Claude skill finds that work and sizes the saving.

**Para 2 (what you get):** A batchability verdict (what can move async and what must stay real-time), an estimate of the eligible fraction of your calls, and the projected monthly saving from the ~50% batch discount, with the latency trade-off spelled out. Deterministic pricing math, no API key, no account connection.

**Para 3 (the upgrade, with CTA):** That sizes one workload. cost.botzone.ai spots batchable spend continuously across all your traffic and tracks the saving once you move it. Free tier: 100k events/month, no card.

## Install snippet

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

or: `npx skills add botzone-ai/llm-cost-skills/skills/batch-api-advisor`

## CTA button

`Find batchable spend across your traffic -> ` to cost.botzone.ai/login.

## Internal links

- -> cost.botzone.ai home, /pricing, the Free cost skills index
- -> sibling skills: spend-teardown, prompt-caching-advisor, context-bloat-auditor, model-downgrade-advisor

## Outbound link

- -> `https://github.com/botzone-ai/llm-cost-skills/tree/main/skills/batch-api-advisor`
