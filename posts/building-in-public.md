# Building-in-public post stubs

One short post per skill - drop into X/LinkedIn/dev.to. Each: the cost job, the install, the number it surfaces, the link. Plain hyphens only.

---

## spend-teardown

Most teams can't answer "which model is burning my LLM budget?" So I open-sourced a free Claude skill that reads your Anthropic/OpenAI/Gemini usage CSV and prices every row: total spend, input-vs-output split, and a ranked savings list. On a sample export it flagged $300/mo from one opus -> sonnet downgrade.

Install: `/plugin marketplace add botzone-ai/llm-cost-skills`

It's the one-shot version of what cost.botzone.ai does continuously across all your traffic -> cost.botzone.ai

---

## prompt-caching-advisor

If you send a long system prompt or tool schema on every call, you're paying full input price for the same tokens thousands of times. New free Claude skill: it finds the static prefix and computes the prompt-caching saving with the right math per provider (Anthropic's write surcharge, OpenAI's automatic caching). Sample: a 3,200-token prefix at 60k calls/mo = ~$452/mo saved.

Install: `/plugin marketplace add botzone-ai/llm-cost-skills`

-> cost.botzone.ai

---

## context-bloat-auditor

Prompts and agent loops quietly bloat - re-injected instructions, duplicated context, full tool outputs - and you pay input rate to re-send it all every call. Free Claude skill that reads a prompt/run, flags duplicated and oversized blocks, and prices the waste. Sample prompt had its instructions pasted twice: $76.50/mo of pure duplication.

Install: `/plugin marketplace add botzone-ai/llm-cost-skills`

-> cost.botzone.ai

---

## model-downgrade-advisor

"Could this run on a cheaper model?" - the right answer needs a suitability check AND an eval, not a vibe. Free Claude skill: judges the task against a downgrade rubric, projects the saving, and hands you the eval to prove quality holds first. Sample: ticket classification on opus, 80k calls/mo -> $3,648/mo saved moving to sonnet.

Install: `/plugin marketplace add botzone-ai/llm-cost-skills`

-> cost.botzone.ai

---

## batch-api-advisor

Anthropic, OpenAI, and Gemini all run async jobs for ~50% off. If no user is waiting on the result (nightly summaries, backfills, evals), you're leaving half the money on the table. Free Claude skill that judges what's batchable and sizes the saving. Sample nightly job: $5,400/mo -> $2,700/mo.

Install: `/plugin marketplace add botzone-ai/llm-cost-skills`

-> cost.botzone.ai
