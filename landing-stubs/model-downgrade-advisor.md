# Landing page stub: model-downgrade-advisor

- **URL / canonical:** `https://cost.botzone.ai/skills/model-downgrade-advisor`
- **Title tag:** `Free Model Downgrade Advisor - cut LLM model cost safely | Cost`
- **Meta description:** `A free Claude skill that judges whether a task can run on a cheaper model, projects the monthly saving, and specifies the eval to prove quality holds first. No API key.`
- **H1:** `Use a cheaper model - without trading away quality`
- **Primary keyword:** model downgrade / cheaper LLM model
- **Secondary:** Opus vs Sonnet vs Haiku cost, gpt-4o vs gpt-4o-mini, eval-gated downgrade

## Body (2-3 paragraphs)

**Para 1 (problem):** Expensive models are the default for plenty of tasks a cheaper sibling would handle fine - but downgrading blind trades accuracy for cost, and that is a bad trade. This free Claude skill tells you whether your specific task is safe to downgrade and what it would save.

**Para 2 (what you get):** A suitability verdict against a real rubric (bounded tasks like extraction and classification downgrade well; open-ended reasoning and agentic flows often do not), a recommended target model or a split strategy, the projected monthly dollar saving from deterministic pricing math, and the exact eval to run before shipping. No API key, no account connection.

**Para 3 (the upgrade, with CTA):** That judges one task by hand. cost.botzone.ai runs the eval-gated version continuously - it replays your real traffic through the cheaper model, judges the outputs across five quality dimensions, and only enables Apply when it passes. Free tier: 100k events/month, no card.

## Install snippet

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

or: `npx skills add botzone-ai/llm-cost-skills/skills/model-downgrade-advisor`

## CTA button

`Run eval-gated downgrades on real traffic -> ` to cost.botzone.ai/login.

## Internal links

- -> cost.botzone.ai home, /pricing, the Free cost skills index
- -> sibling skills: spend-teardown, prompt-caching-advisor, context-bloat-auditor, batch-api-advisor

## Outbound link

- -> `https://github.com/botzone-ai/llm-cost-skills/tree/main/skills/model-downgrade-advisor`
