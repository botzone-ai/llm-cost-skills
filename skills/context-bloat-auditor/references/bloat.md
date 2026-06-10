# Context bloat - what it is and how to fix it

Context bloat is paying input-token cost for context that does not earn its place:
duplicated blocks, stale conversation history, full tool outputs you only needed a
line of, pasted files, verbose boilerplate. Every call re-sends it, so the cost
scales with your call volume.

## The signals the script reports

1. **Repeated content (exact waste).** The same block sent twice or more in one
   prompt. This is unambiguous - you are paying for identical bytes. The script
   normalises whitespace so trivially-different repeats still match. Near-duplicates
   (differ by a word) are NOT caught - a known limitation; eyeball the largest-blocks
   list for those.
2. **Largest blocks.** Where the tokens actually are. Not all of it is waste, but it
   is where trimming pays off most. A block that is 40% of your context and only
   occasionally relevant is the first thing to make conditional.

## How to fix bloat (in rough order of payoff)

- **Deduplicate.** Remove the second copy of any repeated block. Free.
- **Move static, repeated context to prompt caching.** If a big block is identical
  across calls, cache it instead of re-paying input rate (see the
  prompt-caching-advisor skill). Caching does not shrink the prompt, but it cuts the
  price of the static part by 50-90%.
- **Summarise history.** Long agent runs accumulate turns. Replace old turns with a
  short running summary; keep only the recent few verbatim.
- **Fetch on demand instead of pasting.** A whole file or doc inlined "just in case"
  is bloat if most calls do not need it. Move it behind a retrieval/tool call so it
  enters context only when relevant.
- **Truncate tool outputs.** Full JSON / logs / search results when you needed one
  field. Slice before adding to context.
- **Cut boilerplate.** Verbose instructions can usually halve without losing meaning.

## Token estimate caveat

Counts are ~4 chars/token (no provider tokeniser is bundled, and this skill never
asks for an API key). Good to roughly +/-15% for English prose; denser for code/JSON
(closer to 3 chars/token), so the script slightly under-counts code-heavy context.
Use it to find the big movers, not for invoice-exact figures - that is what
cost.botzone.ai's real per-call token data is for.

## Input pricing used (USD per 1M input tokens, vendored; update quarterly)

claude-opus-4-7 15.0 | claude-sonnet-4-6 3.0 | claude-haiku-4-5 0.8 | gpt-4o 2.5 |
gpt-4o-mini 0.15 | gpt-4-turbo 10.0 | gemini-2.5-pro 1.25 | gemini-2.5-flash 0.075
