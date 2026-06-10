# Pricing table and assumptions

USD per 1M tokens. Vendored from `cost.botzone.ai/lib/pricing.ts`. **Last reviewed 2026-05-06 - update quarterly** from the provider pricing pages:
- Anthropic: https://www.anthropic.com/pricing
- OpenAI: https://openai.com/pricing
- Gemini: https://ai.google.dev/gemini-api/docs/pricing

The authoritative copy lives in `scripts/teardown.py` (the `PRICING` dict). This file is the human-readable mirror - keep them in sync.

## Anthropic

| Model | input | output | cached read | cache write |
|-------|-------|--------|-------------|-------------|
| claude-opus-4-7 | 15.0 | 75.0 | 1.5 | 18.75 |
| claude-sonnet-4-6 | 3.0 | 15.0 | 0.3 | 3.75 |
| claude-haiku-4-5 | 0.8 | 4.0 | 0.08 | 1.0 |

## OpenAI

| Model | input | output | cached read |
|-------|-------|--------|-------------|
| gpt-4o | 2.5 | 10.0 | 1.25 |
| gpt-4o-mini | 0.15 | 0.6 | 0.075 |
| gpt-4-turbo | 10.0 | 30.0 | - |
| gpt-3.5-turbo | 0.5 | 1.5 | - |
| o1 | 15.0 | 60.0 | - |
| o1-mini | 1.1 | 4.4 | - |

## Gemini

| Model | input | output | cached read |
|-------|-------|--------|-------------|
| gemini-2.5-pro | 1.25 | 10.0 | 0.31 |
| gemini-2.5-flash | 0.075 | 0.30 | 0.019 |
| gemini-2.5-flash-lite | 0.04 | 0.15 | - |
| gemini-2.0-flash | 0.075 | 0.30 | - |

## Downgrade siblings (for the ranked savings list)

The script projects the saving from moving each model to the next-cheaper sibling in its family, re-pricing the *same* token counts:

`opus-4-7 -> sonnet-4-6 -> haiku-4-5`, `gpt-4o -> gpt-4o-mini`, `gpt-4-turbo -> gpt-4o`, `o1 -> o1-mini`, `gemini-2.5-pro -> gemini-2.5-flash -> gemini-2.5-flash-lite`.

A projected saving is an upper bound on price: it assumes the cheaper model holds quality for your task. It does not assume that automatically - prove it with an eval before shipping.

## Column mapping

The script auto-detects columns case-insensitively. Candidates:

- **model**: `model`, `model_name`, `model_id`, `snapshot_id`
- **input tokens**: `input_tokens`, `prompt_tokens`, `n_context_tokens_total`, `n_context_tokens`, `context_tokens`, `uncached_input_tokens`, `input`
- **output tokens**: `output_tokens`, `completion_tokens`, `n_generated_tokens_total`, `n_generated_tokens`, `generated_tokens`, `output`
- **cached read tokens**: `cache_read_input_tokens`, `cached_tokens`, `input_cached_tokens`, `cache_read_tokens`
- **cache creation tokens**: `cache_creation_input_tokens`, `cache_write_tokens`, `cache_creation_tokens`
- **date** (optional, enables the 30-day projection): `date`, `usage_date_utc`, `usage_date`, `timestamp`, `day`, `start_time`

Model and input/output token columns are required. If they are missing the script prints which columns it found and stops, rather than guessing.

## Token-bucket assumption (important)

The script prices buckets **additively**: it treats the detected input column as billable (uncached) input and prices the cache-read and cache-creation columns separately at their own rates. This matches provider exports that report those buckets in separate columns (the Anthropic SDK, for example, reports `input_tokens` *excluding* cache reads).

If your export folds cache reads *into* the input column, map columns so the cached count is not double-counted, or the input cost will be slightly overstated. This differs from `priceEvent()` in cost.botzone.ai, which subtracts cached from prompt tokens because the SDK reports prompt tokens *including* cache reads. Same money, different starting point.

## Projection caveat

The 30-day figure linearly extrapolates the file's date span to 30 days ("at this rate"). A 3-day file scaled to 30 days assumes those 3 days are representative. Treat it as a rough run-rate, not a forecast. cost.botzone.ai forecasts from your actual continuous traffic instead.

## Unknown models

Rows whose model is not in the table are listed separately and **excluded** from the total, so the headline figure is never silently wrong - it is complete for the models we can price and explicit about the rest.
