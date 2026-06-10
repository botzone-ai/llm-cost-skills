# Model downgrade - is this task safe to downgrade?

A downgrade saves money only if the cheaper model still does the job. The script
gives you the dollar prize; this rubric helps you judge whether the prize is worth
chasing - and the eval at the end is how you actually confirm it.

## Tasks that usually downgrade well (try it)

- **Extraction / parsing** - pull fields, classify, tag, route. Structured and checkable.
- **Format conversion** - JSON <-> text, reshaping, templating.
- **Short factual transforms** on provided context (the answer is in the prompt).
- **Classification / routing / moderation** with a fixed label set.
- **Simple summarisation** of short, self-contained text.
- **Boilerplate generation** from a tight spec.

These are bounded: the output space is small or verifiable, so a smaller model rarely
surprises you. Haiku / gpt-4o-mini / gemini-flash are built for exactly this.

## Tasks that often need the bigger model (downgrade with care, eval hard)

- **Multi-step reasoning / planning** where one wrong step compounds.
- **Long-context synthesis** across many documents.
- **Nuanced writing** where tone and judgement matter (sales, exec comms).
- **Agentic tool use** with many tools and tricky tool-choice decisions.
- **Code generation** beyond small, well-specified snippets.
- **Ambiguous instructions** needing the model to infer intent.

A downgrade here can pass 90% of the time and fail expensively on the 10% that
matters. That is what the eval is for.

## How to pick the target

- Move one rung, not three: opus -> sonnet before opus -> haiku; gpt-4o -> gpt-4o-mini.
- Consider a **split**: route the easy majority to the cheap model and keep the hard
  cases on the expensive one. Often beats a blanket downgrade.
- Output-heavy tasks save more from a downgrade (output is priced 4-5x input), so
  the dollar prize is biggest where the model writes a lot.

## The eval (do this before shipping)

1. Pull 20-50 real inputs for this task (more for higher-stakes tasks).
2. Run them through both the current and the candidate model.
3. Compare on what actually matters for the task: factual equivalence, instruction
   compliance, format validity, completeness, and tool-use parity if relevant.
4. Downgrade only where the cheaper model passes. Where it fails, keep the expensive
   model or route just those cases to it.

cost.botzone.ai runs this eval-gated check automatically (replays real traffic
through the cheaper model and judges it) before it lets you apply a downgrade. This
skill is the manual, one-task version of that.

## Pricing used (USD per 1M tokens, vendored; update quarterly)

| Model | input | output |
|-------|-------|--------|
| claude-opus-4-7 | 15.0 | 75.0 |
| claude-sonnet-4-6 | 3.0 | 15.0 |
| claude-haiku-4-5 | 0.8 | 4.0 |
| gpt-4o | 2.5 | 10.0 |
| gpt-4o-mini | 0.15 | 0.6 |
| gpt-4-turbo | 10.0 | 30.0 |
| o1 | 15.0 | 60.0 |
| o1-mini | 1.1 | 4.4 |
| gemini-2.5-pro | 1.25 | 10.0 |
| gemini-2.5-flash | 0.075 | 0.30 |
| gemini-2.5-flash-lite | 0.04 | 0.15 |
