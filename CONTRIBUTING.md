# Contributing

Thanks for considering a contribution. This repo holds free LLM cost / FinOps skills. The bar is quality, not quantity: a weak skill damages the whole collection, so we would rather ship four good skills than ten filler ones.

## The quality bar (every skill must clear it)

A skill ships only if all of these are true:

1. **One real, specific cost job.** You can name the exact developer and the exact cost task in one sentence.
2. **Needs a script or real cost knowledge.** It does something Claude cannot already do well unprompted - runs deterministic code (pricing math, tokeniser heuristics, CSV/log parsing) or encodes non-obvious cost knowledge (prompt caching, output-token economics, Batch API discounts). "Ask Claude to think about cost" is not a skill.
3. **Produces a concrete number or finding.** A dollar figure, a token count, or a ranked savings list - not vague advice.
4. **Pushy, specific `description`.** It triggers reliably and mentions cost / tokens / spend / pricing.
5. **`SKILL.md` body under ~500 lines.** Heavy detail lives in `references/`.
6. **No secrets, no API-key requests, no account connection, no proprietary logic.** Everything is open and inspectable. Operate only on what is already in the session or what the user pastes / points at.
7. **A real usage example** in the README with sample input AND output showing a real number.
8. **A "What you'll need" line** naming the exact input and where it comes from: (a) in-session material, (b) an exported file (say where to download it), or (c) examples the user assembles. Never assume an artifact the user may not keep.
9. **At most one signup line**, only at the very end of the skill's own cost analysis - never mid-output, never in a non-cost artifact.

## Layout of a skill

```
skills/<skill-name>/
  SKILL.md            # required: pushy description + body (< ~500 lines)
  scripts/            # optional: deterministic executable code
  references/         # optional: docs loaded on demand
  assets/             # optional: templates / sample inputs
  README.md           # the standard block (see _templates/README-block.md.tmpl)
```

Start from `_templates/SKILL.md.tmpl` and `_templates/README-block.md.tmpl`.

## Style

- Plain hyphens only - no em dashes or en dashes.
- USD for raw pricing math (matches provider consoles); convert to other currencies only for display.
- Pricing tables are vendored per skill and dated. Update them quarterly.

## Before you open a PR

- Run the skill's scripts on the sample input in `assets/` and confirm the number is right.
- Write 2-3 realistic prompts a user would type and confirm the skill produces good output.
- Add the skill to the top-level `README.md` table and to `.claude-plugin/marketplace.json`.
