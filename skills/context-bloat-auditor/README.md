# context-bloat-auditor

Find the context that is inflating your **LLM token cost**: duplicated blocks, oversized history, full tool outputs you re-send every call. Reads a prompt or agent run and prices the **wasted tokens** in dollars per call and per month.

**What you'll need:** the prompt or agent-run text already in your project, pasted into the chat, or in a log file. Optionally a rough calls-per-month to get a monthly figure. No API key, no account.

## What it does

Prompts and agent loops quietly grow heavy - re-injected instructions, accumulated conversation history, full JSON tool outputs, pasted files - and you pay input rate to re-send all of it on every call. This skill estimates the context size, finds blocks that repeat (exact, quantifiable waste), shows the largest blocks by share of context, and prices it all so you know which cut is worth making. Then it tells you how to cut: dedupe, cache the static parts, summarise history, fetch on demand. Deterministic analysis, no API key, no account connection.

## Install

**Claude Code plugin marketplace (gets the whole bundle):**

```
/plugin marketplace add botzone-ai/llm-cost-skills
/plugin install llm-cost-skills@llm-cost-skills
```

**Just this skill:** `npx skills add botzone-ai/llm-cost-skills/skills/context-bloat-auditor`

**Manually:** copy `skills/context-bloat-auditor/` into `~/.claude/skills/`.

## Example

**You ask:**

```
This support-agent prompt feels huge and we run it ~50k times a month on
claude-sonnet-4-6. What's bloating it? prompt.txt
```

**You get:**

```
============================================================
CONTEXT BLOAT AUDIT
============================================================

Model: claude-sonnet-4-6   (estimates at ~4 chars/token)
Total context: ~1,136 tokens = $0.0034 per call (input only)
  At 50,000 calls/month: $170.40/mo just to send this context

Repeated content (exact waste - you are sending these twice or more):
------------------------------------------------------------
  x2  ~262 tok each  -> wastes ~262 tok/call ($0.0008/call, $39.30/mo)
        "## Operating rules"
  x2  ~248 tok each  -> wastes ~248 tok/call ($0.0007/call, $37.20/mo)
        "## Knowledge base snapshot"

  TOTAL repeated-content waste: ~510 tokens/call = $0.0015/call, $76.50/mo
...
Want this continuously across all your traffic, not just one prompt? -> cost.botzone.ai
```

Here the prompt accidentally includes its instructions and knowledge base twice - $76.50/mo of pure duplication, fixed by deleting one copy.

## Free vs continuous

This audits one prompt or run. [cost.botzone.ai](https://cost.botzone.ai) watches context growth continuously across all your routes, flags bloat as it creeps in, and ties it to the feature that is paying for it - the always-on version you cannot get from a single dump.

---

Want this continuously across all your traffic, not just one prompt? -> **[cost.botzone.ai](https://cost.botzone.ai)**
