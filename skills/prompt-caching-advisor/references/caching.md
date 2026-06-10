# Prompt caching - how the economics work

Prompt caching cuts the cost of the **repeated, static** part of a prompt (system
prompt, tool/function schemas, few-shot examples, retrieved boilerplate, long
instructions). The variable part (the user's actual input) is never cached. So the
whole game is: how many tokens are static, how often is the prompt called, and what
does your provider charge for a cache read vs a normal input token.

## Per-provider rules (this is the non-obvious bit)

### Anthropic (explicit)
- You mark cacheable spans with `cache_control: {type: "ephemeral"}`.
- A **cache write** costs **1.25x** the input rate (you pay a premium to populate it).
- A **cache read** costs about **0.1x** the input rate (sonnet: $3 -> $0.30).
- TTL is ~5 minutes (refreshed on each hit). If calls are spaced >5 min apart, each one re-writes.
- Win condition: a large static prefix called frequently enough that reads dominate writes.
- The script models this with `--write-fraction` (default 0.10 = 10% of calls pay the write surcharge). Lower it for high-frequency steady traffic, raise it for bursty/sparse traffic.

### OpenAI (automatic)
- No API change needed. Prompts **>1024 tokens** with a stable prefix are cached automatically.
- **No write surcharge**; cached input is billed at about **0.5x** (gpt-4o: $2.50 -> $1.25).
- The only action item: put the static content **first** so the prefix matches byte-for-byte across calls. Anything that changes early (a timestamp, a per-call id at the top) breaks the prefix and kills the cache.

### Gemini (explicit, with storage)
- Explicit context caching gives a cached-read discount (2.5-pro: $1.25 -> $0.31)...
- ...but also charges **per-hour storage** for the cached content, which this script does NOT model. Treat the script's number as a ceiling; subtract storage.

## How to find the static prefix (the agent's job)

Read the prompt and separate:
- **Static / cacheable:** system prompt, role instructions, tool/function definitions, few-shot examples, fixed retrieved context, style guides. The same on every call.
- **Variable / not cacheable:** the user message, per-request data, retrieved chunks that change, anything with a timestamp or id.

Count the static tokens (or pass the static text as `--static-file`) and feed it to the script with the call volume.

## Common mistakes that silently disable caching

- Putting a per-call timestamp, request id, or user name at the very top of the prompt - breaks the prefix match.
- Reordering tool definitions between calls.
- A static prefix under the minimum cacheable size (Anthropic ~1024 tokens for most models; OpenAI 1024).
- Assuming output tokens get cheaper - they do not. Caching only touches input.

## Pricing (USD per 1M tokens, vendored; update quarterly)

| Model | input | cached read | cache write |
|-------|-------|-------------|-------------|
| claude-opus-4-7 | 15.0 | 1.5 | 18.75 |
| claude-sonnet-4-6 | 3.0 | 0.3 | 3.75 |
| claude-haiku-4-5 | 0.8 | 0.08 | 1.0 |
| gpt-4o | 2.5 | 1.25 | (automatic) |
| gpt-4o-mini | 0.15 | 0.075 | (automatic) |
| gemini-2.5-pro | 1.25 | 0.31 | (+ storage) |
| gemini-2.5-flash | 0.075 | 0.019 | (+ storage) |
