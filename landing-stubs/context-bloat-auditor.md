# Landing page stub: context-bloat-auditor

- **URL / canonical:** `https://cost.botzone.ai/skills/context-bloat-auditor`
- **Title tag:** `Free Context Bloat Auditor - find the tokens inflating your LLM cost | Cost`
- **Meta description:** `A free Claude skill that reads a prompt or agent run, flags duplicated and oversized context, and prices the wasted tokens in dollars per call and per month. No API key.`
- **H1:** `Find the context that is padding your token bill`
- **Primary keyword:** context bloat / reduce prompt tokens
- **Secondary:** wasted tokens, agent run cost, conversation history cost, duplicated context

## Body (2-3 paragraphs)

**Para 1 (problem):** Prompts and agent loops grow heavy without anyone noticing - re-injected instructions, accumulated history, full tool outputs, pasted files - and you pay input rate to re-send all of it on every call. This free Claude skill reads the prompt or run and shows exactly what is inflating it.

**Para 2 (what you get):** Total context size and cost, a ranked list of repeated blocks with their dollar waste per call and per month (exact, quantifiable duplication), and the largest blocks by share of context. Then concrete fixes: dedupe, cache the static parts, summarise history, fetch large content on demand. Deterministic analysis, no API key, no account connection.

**Para 3 (the upgrade, with CTA):** That is one prompt or run. cost.botzone.ai watches context growth continuously across all your routes, flags bloat as it creeps in, and ties it to the feature paying for it. Free tier: 100k events/month, no card.

## Install snippet

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

or: `npx skills add botzone-ai/llm-cost-skills/skills/context-bloat-auditor`

## CTA button

`Catch bloat across all your prompts -> ` to cost.botzone.ai/login.

## Internal links

- -> cost.botzone.ai home, /pricing, the Free cost skills index
- -> sibling skills: spend-teardown, prompt-caching-advisor, model-downgrade-advisor

## Outbound link

- -> `https://github.com/botzone-ai/llm-cost-skills/tree/main/skills/context-bloat-auditor`
