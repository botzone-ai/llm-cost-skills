# model-downgrade-advisor

Find out whether a task could run on a cheaper model, how much it would **save per month**, and the eval to prove quality holds first. The responsible way to cut **LLM model cost** without trading away accuracy.

**What you'll need:** the prompt or task already in your project, a rough token profile (input/output tokens per call) and calls-per-month, and your quality bar. The skill estimates tokens and asks for volume if you have not said. No API key, no account.

## What it does

Expensive models (Opus, GPT-4o, Gemini Pro) are the default for a lot of tasks that a cheaper sibling would handle fine - but downgrading blind trades quality for cost. This skill judges your task against a downgrade-suitability rubric (bounded tasks like extraction and classification downgrade well; open-ended reasoning and agentic flows often do not), recommends a target model or a split, projects the monthly dollar saving with deterministic pricing math, and specifies the eval to run before you ship. No API key, no account connection.

## Install

**Claude Code plugin marketplace (gets the whole bundle):**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**Just this skill:** `npx skills add botzone-ai/llm-cost-skills/skills/model-downgrade-advisor`

**Manually:** copy `skills/model-downgrade-advisor/` into `~/.claude/skills/`.

## Example

**You ask:**

```
We classify support tickets on claude-opus-4-7, about 1,800 in / 400 out tokens a
call, ~80k calls a month. Could we drop to a cheaper model, and what would it save?
```

**You get:** the verdict that ticket classification is a bounded task that downgrades well, a recommended target (sonnet, or haiku with an eval), and:

```
============================================================
MODEL DOWNGRADE - PROJECTED SAVING
============================================================

Task profile: ~1,800 input + 400 output tokens/call, 80,000 calls/month

  claude-opus-4-7             $0.06/call      $4,560.00/mo
  claude-sonnet-4-6           $0.01/call        $912.00/mo

  -> Projected saving: $3,648.00/mo (80% cheaper)
...
Want this continuously across all your traffic, not just one task? -> cost.botzone.ai
```

Plus the eval to run first: 20-50 real tickets through both models, compare on label accuracy, downgrade only where the cheaper model matches.

## Free vs continuous

This judges one task by hand. [cost.botzone.ai](https://cost.botzone.ai) runs the eval-gated version continuously - it replays your real production traffic through the cheaper model, judges the outputs across five quality dimensions, and only enables Apply when it passes, then tracks what the downgrade actually saved. This skill is the manual taste of that.

---

Want this continuously across all your traffic, not just one prompt? -> **[cost.botzone.ai](https://cost.botzone.ai)**
