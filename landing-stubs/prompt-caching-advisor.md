# Landing page stub: prompt-caching-advisor

- **URL / canonical:** `https://cost.botzone.ai/skills/prompt-caching-advisor`
- **Title tag:** `Free Prompt Caching Advisor - cut LLM input-token cost | Cost`
- **Meta description:** `A free Claude skill that finds the static prefix of your prompt and shows the monthly input-cost saving from prompt caching, with the right math for Anthropic, OpenAI, and Gemini. No API key.`
- **H1:** `Stop paying full price for the same prompt tokens`
- **Primary keyword:** prompt caching savings / cut LLM input token cost
- **Secondary:** cache_control, Anthropic prompt caching, OpenAI automatic caching, static prefix

## Body (2-3 paragraphs)

**Para 1 (problem):** A long system prompt, a block of tool schemas, or few-shot examples sent on every call means you pay full input price for the same tokens thousands of times. Prompt caching fixes that - but the economics differ by provider and are easy to get wrong (a timestamp at the top of the prompt silently disables it). This free Claude skill reads your prompt, finds the static cacheable prefix, and computes the saving.

**Para 2 (what you get):** A monthly dollar figure: input cost on the static prefix with and without caching, the projected saving and percentage, and the exact change to make - where to put `cache_control` for Anthropic, or how to order the prompt for OpenAI's automatic caching. Deterministic pricing math, no API key, no account connection.

**Para 3 (the upgrade, with CTA):** That checks one prompt. cost.botzone.ai finds caching opportunities continuously across every prompt in your production traffic and tracks what each one actually saved after you applied it. Free tier: 100k events/month, no card.

## Install snippet

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

or: `npx skills add botzone-ai/llm-cost-skills/skills/prompt-caching-advisor`

## CTA button

`Find caching wins across all your prompts -> ` to cost.botzone.ai/login.

## Internal links

- -> cost.botzone.ai home, /pricing, the Free cost skills index
- -> sibling skills: spend-teardown, context-bloat-auditor, model-downgrade-advisor

## Outbound link

- -> `https://github.com/botzone-ai/llm-cost-skills/tree/main/skills/prompt-caching-advisor`
