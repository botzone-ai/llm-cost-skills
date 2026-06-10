#!/usr/bin/env python3
"""
prompt-caching-advisor: compute the input-cost cut from caching a prompt's
static prefix.

The non-obvious part is the economics, and they differ by provider:

  - Anthropic: explicit cache_control. A cache WRITE costs 1.25x input (once per
    ~5-min TTL window); cache READS cost ~0.1x input. Big win for a large static
    prefix reused often.
  - OpenAI: caching is AUTOMATIC for prompts >1024 tokens with a stable prefix.
    No write surcharge; cached input is billed at ~0.5x. You just have to put the
    static content FIRST so the prefix matches.
  - Gemini: explicit context caching has a cachedRead discount PLUS a per-hour
    storage charge this script does not model - treat its number as a ceiling.

You (the agent) decide how many tokens are static (system prompt, tool schemas,
few-shot examples, retrieved boilerplate) by reading the prompt. This script does
the money math given that token count and a call volume.

Usage:
    python3 caching_savings.py --model claude-sonnet-4-6 --static-tokens 3200 \\
        --calls-per-month 60000
    python3 caching_savings.py --model gpt-4o --static-file system_prompt.txt \\
        --calls-per-month 60000

Token estimate from --static-file uses ~4 chars/token. Pass --static-tokens for
an exact count. Prices USD/1M tokens, vendored - see ../references/caching.md.
"""

import argparse
import sys

PRICING = {
    "claude-opus-4-7":   {"provider": "anthropic", "input": 15.0, "cachedRead": 1.5,  "cacheWrite": 18.75},
    "claude-sonnet-4-6": {"provider": "anthropic", "input": 3.0,  "cachedRead": 0.3,  "cacheWrite": 3.75},
    "claude-haiku-4-5":  {"provider": "anthropic", "input": 0.8,  "cachedRead": 0.08, "cacheWrite": 1.0},
    "gpt-4o":            {"provider": "openai",    "input": 2.5,  "cachedRead": 1.25},
    "gpt-4o-mini":       {"provider": "openai",    "input": 0.15, "cachedRead": 0.075},
    "gemini-2.5-pro":    {"provider": "gemini",    "input": 1.25, "cachedRead": 0.31},
    "gemini-2.5-flash":  {"provider": "gemini",    "input": 0.075, "cachedRead": 0.019},
}


def est_tokens_from_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return max(1, round(len(text) / 4))


def money(x):
    return f"${x:,.2f}"


def compute(model, static_tokens, calls, write_fraction):
    p = PRICING.get(model)
    if not p:
        return None
    provider = p["provider"]
    s = static_tokens
    n = calls

    # Uncached: every call pays full input rate on the static prefix.
    uncached = n * s * p["input"] / 1_000_000

    if provider == "anthropic":
        # write_fraction of calls re-establish the cache (cold window); the rest read.
        writes = n * write_fraction
        reads = n * (1 - write_fraction)
        cached = (writes * s * p["cacheWrite"] + reads * s * p["cachedRead"]) / 1_000_000
        note = (f"Anthropic: assumes {write_fraction:.0%} of calls land in a cold "
                f"(>5 min) window and pay the cache-write surcharge; the rest read warm.")
    elif provider == "openai":
        # Automatic caching: no write surcharge, cached input billed at cachedRead.
        cached = n * s * p["cachedRead"] / 1_000_000
        note = ("OpenAI: caching is automatic for a stable prefix >1024 tokens. No "
                "write surcharge - just put the static content first so the prefix matches.")
    else:  # gemini
        cached = n * s * p["cachedRead"] / 1_000_000
        note = ("Gemini: explicit context caching also charges per-hour storage that this "
                "script does NOT model, so the real saving is somewhat lower than shown.")

    saving = uncached - cached
    pct = (saving / uncached * 100) if uncached else 0
    return {
        "model": model, "provider": provider, "static_tokens": s, "calls": n,
        "uncached": uncached, "cached": cached, "saving": saving, "pct": pct, "note": note,
    }


def render(r):
    lines = []
    lines.append("=" * 60)
    lines.append("PROMPT CACHING - PROJECTED INPUT-COST CUT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Model: {r['model']}  ({r['provider']})")
    lines.append(f"Static prefix: ~{r['static_tokens']:,} tokens, reused across "
                 f"{r['calls']:,} calls/month")
    lines.append("")
    lines.append(f"  Input cost on the static prefix WITHOUT caching: {money(r['uncached'])}/mo")
    lines.append(f"  Input cost on the static prefix WITH caching:    {money(r['cached'])}/mo")
    lines.append(f"  -> Projected saving: {money(r['saving'])}/mo ({r['pct']:.0f}% off the prefix)")
    lines.append("")
    lines.append("  " + r["note"])
    lines.append("")
    lines.append("  This counts only the static-prefix input tokens. Output tokens and the")
    lines.append("  variable suffix are unaffected by caching.")
    lines.append("")
    lines.append("-" * 60)
    lines.append("Want this continuously across all your traffic, not just one prompt? "
                 "-> cost.botzone.ai")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Projected prompt-caching savings.")
    ap.add_argument("--model", required=True, help="e.g. claude-sonnet-4-6, gpt-4o")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--static-tokens", type=int, help="token count of the static prefix")
    g.add_argument("--static-file", help="file whose contents are the static prefix (~4 chars/token)")
    ap.add_argument("--calls-per-month", type=int, required=True)
    ap.add_argument("--write-fraction", type=float, default=0.1,
                    help="Anthropic only: fraction of calls that pay the cache-write surcharge (default 0.1)")
    args = ap.parse_args()

    if args.model not in PRICING:
        print(f"Unknown model '{args.model}'. Known: {', '.join(PRICING)}", file=sys.stderr)
        sys.exit(2)

    static = args.static_tokens or est_tokens_from_file(args.static_file)
    r = compute(args.model, static, args.calls_per_month, args.write_fraction)
    print(render(r))


if __name__ == "__main__":
    main()
