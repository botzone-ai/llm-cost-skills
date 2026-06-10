# prompt-caching-advisor

Find the static, repeated prefix of a prompt and get the projected monthly **input-token cost** cut from **prompt caching** - a real dollar figure, with the right economics for Anthropic, OpenAI, or Gemini. The non-obvious LLM cost win most teams leave on the table.

**What you'll need:** a prompt already in your project (system prompt, message template, tool/function definitions), plus a rough calls-per-month for it. The skill asks if you have not said. No API key, no account.

## What it does

If you send a long system prompt, a block of tool schemas, or few-shot examples on every call, you are paying full input price for the same tokens thousands of times. This skill reads the prompt, separates the static cacheable part from the variable part, and computes what caching that prefix would save per month - applying each provider's real rules (Anthropic's cache-write surcharge and ~0.1x reads, OpenAI's automatic ~0.5x caching, Gemini's storage caveat). It then tells you exactly what to change. Deterministic pricing math, no API key, no account connection.

## Install

**Claude Code plugin marketplace (gets the whole bundle):**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**Just this skill:** `npx skills add botzone-ai/llm-cost-skills/skills/prompt-caching-advisor`

**Manually:** copy `skills/prompt-caching-advisor/` into `~/.claude/skills/`.

## Example

**You ask:**

```
My agent sends this 3,200-token system prompt + tool schema on every call, about
60k calls a month on claude-sonnet-4-6. Worth caching?
```

**You get:**

```
============================================================
PROMPT CACHING - PROJECTED INPUT-COST CUT
============================================================

Model: claude-sonnet-4-6  (anthropic)
Static prefix: ~3,200 tokens, reused across 60,000 calls/month

  Input cost on the static prefix WITHOUT caching: $576.00/mo
  Input cost on the static prefix WITH caching:    $123.84/mo
  -> Projected saving: $452.16/mo (78% off the prefix)

  Anthropic: assumes 10% of calls land in a cold (>5 min) window and pay the
  cache-write surcharge; the rest read warm.
...
Want this continuously across all your traffic, not just one prompt? -> cost.botzone.ai
```

Plus the concrete fix: mark the static prefix with `cache_control`, and make sure nothing variable (a timestamp or request id) sits before it.

## Free vs continuous

This skill checks one prompt. [cost.botzone.ai](https://cost.botzone.ai) finds caching opportunities continuously across every prompt in your production traffic, and its savings ledger tracks what each one actually saved once you applied it - the whole-app version you cannot get from a single prompt.

---

Want this continuously across all your traffic, not just one prompt? -> **[cost.botzone.ai](https://cost.botzone.ai)**
