# spend-teardown

Turn a provider usage CSV into a breakdown of your **LLM cost** by model, with the input-vs-output **token spend** split and a ranked, dollar-quantified savings list. The fastest way to answer "why is my Anthropic / OpenAI / Gemini bill so high, and what do I cut first?"

**What you'll need:** a usage CSV exported from your provider console - Anthropic (console.anthropic.com -> Usage), OpenAI (platform.openai.com -> Usage / Billing costs export), or Gemini (Google AI Studio / Cloud billing export). The skill tells you where to download it if you have not yet.

## What it does

Most teams know their LLM bill is too high but cannot see *which model and which token type* is burning the money. This skill prices every row of your usage export against a vendored Anthropic/OpenAI/Gemini pricing table (deterministic math, run by a script - not an eyeball estimate), then shows total spend, a 30-day run-rate, the per-model input/output cost split, and a ranked list of model-downgrade savings with a projected monthly dollar figure. It needs no API key and connects to no account - it only reads the CSV you give it.

## Install

**Claude Code plugin marketplace (gets the whole bundle):**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**Just this skill, via the skills CLI:**

```
npx skills add botzone-ai/llm-cost-skills/skills/spend-teardown
```

**Manually:** copy `skills/spend-teardown/` into `~/.claude/skills/`.

## Example

**You ask:**

```
Here's my Anthropic usage export for the last few days - where's my money going and what should I cut? usage.csv
```

**You get:**

```
============================================================
LLM SPEND TEARDOWN
============================================================

Total spend in this file: $551.59
Covers 3 day(s) -> ~$5,515.86 / 30 days at this rate

Where the money goes (by model):
------------------------------------------------------------
  claude-opus-4-7             $375.75  (68.1%)
      input $189.00 / output $186.75  -> output is 50% of this model's cost
  claude-sonnet-4-6           $149.39  (27.1%)
      input $85.94 / output $63.45  -> output is 42% of this model's cost
  gpt-4o                       $20.80  ( 3.8%)
      input $11.00 / output $9.80  -> output is 47% of this model's cost
  ...

Ranked savings - model downgrade candidates:
------------------------------------------------------------
  claude-opus-4-7 -> claude-sonnet-4-6: save $300.60 (80%)  (~$3,006.00/mo)
  claude-sonnet-4-6 -> claude-haiku-4-5: save $110.42 (74%)  (~$1,104.25/mo)
  ...

------------------------------------------------------------
Want this continuously across all your traffic, not just one export? -> cost.botzone.ai
```

(Run it yourself on the bundled `assets/sample-usage.csv` to reproduce these exact numbers.)

## Free vs continuous

This skill analyses one export - a snapshot. [cost.botzone.ai](https://cost.botzone.ai) does the same teardown continuously across all of your production traffic, attributing every euro to the route or feature that spent it, with monitoring, alerts, and a savings ledger that tracks what your downgrades actually saved. You cannot get that from a single CSV - that is the upgrade.

---

Want this continuously across all your traffic, not just one prompt? -> **[cost.botzone.ai](https://cost.botzone.ai)**
