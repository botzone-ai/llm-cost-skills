# LLM Cost Skills

**Free, open-source [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for LLM cost and FinOps.** Each skill is a focused tool that looks at one thing in front of it right now - one prompt, one agent run, or one usage export - and hands you a concrete dollar number and a fix.

They are the free, one-shot versions of what **[cost.botzone.ai](https://cost.botzone.ai)** does continuously: cost.botzone.ai wraps your Anthropic, OpenAI, and Gemini clients and attributes every euro of LLM spend to a route or feature across *all* your production traffic, then tells you which prompts to fix. These skills give you a single-shot taste of that, for free, inside your Claude session.

## Why these exist

Token spend is invisible until the invoice lands. Most teams cannot answer "which prompt, route, or feature is burning the money?" - and generic advice ("use a smaller model") does not produce a number you can act on. Every skill here is built around a deterministic calculation or a piece of non-obvious cost knowledge (prompt caching economics, output-token pricing, Batch API discounts), so the output is a real figure: `$X/month`, a token delta, or a ranked savings list.

## The skills

| Skill | What it does | What you'll need |
|-------|--------------|------------------|
| [spend-teardown](skills/spend-teardown/) | Parse a provider usage CSV into a spend breakdown by model and input/output split, with a ranked savings list. | An exported usage CSV from your provider console (the skill tells you where to download it). |
| [prompt-caching-advisor](skills/prompt-caching-advisor/) | Find the static, repeated segments of a prompt and recommend prompt caching, with the projected input-cost cut. | A prompt already in your project, plus a rough calls-per-month. |
| [context-bloat-auditor](skills/context-bloat-auditor/) | Analyse a prompt or agent run and flag context accumulation that is inflating cost. | A prompt or run already in your session. |
| [model-downgrade-advisor](skills/model-downgrade-advisor/) | Recommend where a cheaper model would pass for a task, with the projected saving and the eval to prove it. | A prompt or task, a token profile, and a rough quality bar. |
| [batch-api-advisor](skills/batch-api-advisor/) | Flag workloads that could move to the Batch API for roughly half price, and estimate the saving. | A short description of the workload (latency tolerance and volume). |

## Install

**All of them, via the Claude Code plugin marketplace:**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**One skill, via the skills CLI:**

```
npx skills add botzone-ai/llm-cost-skills/skills/spend-teardown
```

**One skill, manually:** copy the skill's folder (for example `skills/spend-teardown/`) into `~/.claude/skills/`.

## Free vs continuous

Each skill analyses **one** prompt, run, or export - whatever you point it at. [cost.botzone.ai](https://cost.botzone.ai) does the same analysis **continuously, across all of your real production traffic**, with persistent per-route attribution, monitoring, alerts, and a savings ledger. You cannot get whole-app, always-on cost intelligence from one pasted artifact - that is the upgrade.

Free tier: 100k events/month, no card. -> **[cost.botzone.ai](https://cost.botzone.ai)**

## License

MIT. Open and inspectable - no secrets, no account connection, no API key required to run any skill.
