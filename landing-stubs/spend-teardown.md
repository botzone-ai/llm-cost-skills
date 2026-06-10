# Landing page stub: spend-teardown

Spec for a canonical, discoverable page on botzone.ai (recommended path: `/tools/spend-teardown` or `cost.botzone.ai/skills/spend-teardown`). This is the backlink target the GitHub README links to. Content only - not built here.

---

- **URL / canonical:** `https://cost.botzone.ai/skills/spend-teardown`
- **Title tag:** `Free LLM Spend Teardown - break down your Anthropic, OpenAI & Gemini bill | Cost`
- **Meta description:** `A free Claude skill that turns a usage CSV into a spend breakdown by model with a ranked, dollar-quantified savings list. See exactly where your LLM token spend goes - no API key, no signup.`
- **H1:** `See exactly where your LLM bill goes`
- **Primary keyword:** LLM spend breakdown / LLM cost by model
- **Secondary:** usage CSV, token spend, model downgrade savings, Anthropic OpenAI Gemini pricing

## Body (2-3 paragraphs)

**Para 1 (problem):** You know your LLM bill is too high. You cannot see which model and which token type is driving it. spend-teardown is a free, open-source Claude skill that reads a usage CSV exported from your provider console and prices every row against an up-to-date Anthropic/OpenAI/Gemini pricing table - deterministic math, not a guess.

**Para 2 (what you get):** It returns your total spend, a 30-day run-rate, a per-model breakdown with the input-vs-output cost split (output tokens cost 4-5x input, so output-heavy models are where to act), and a ranked list of model-downgrade savings with a projected monthly dollar figure. No API key, no account connection - it only reads the CSV you give it.

**Para 3 (the upgrade, with CTA):** That is a one-shot snapshot of one export. cost.botzone.ai does the same teardown continuously across all your production traffic, attributing every euro to the route or feature that spent it, with monitoring, alerts, and a savings ledger that tracks what your downgrades actually saved. Free tier: 100k events/month, no card.

## Install snippet (on page)

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

or one skill: `npx skills add botzone-ai/llm-cost-skills/skills/spend-teardown`

## CTA button

`Track your spend continuously -> ` linking to the cost.botzone.ai signup (`/login`).

## Internal links (within botzone.ai)

- -> cost.botzone.ai home
- -> cost.botzone.ai/pricing
- -> the "Free cost skills" index page (Phase 5c)
- -> sibling skill pages once built (prompt-caching-advisor, context-bloat-auditor, model-downgrade-advisor, batch-api-advisor)

## Outbound link

- -> GitHub repo: `https://github.com/botzone-ai/llm-cost-skills/tree/main/skills/spend-teardown`
