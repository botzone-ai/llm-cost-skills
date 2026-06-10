#!/usr/bin/env python3
"""
model-downgrade-advisor: project the saving from moving a task to a cheaper model.

The money math is deterministic (this script). Whether the cheaper model actually
holds quality for YOUR task is a judgement call - see ../references/downgrade-fit.md
for the suitability rubric - and must be proven with an eval before you ship. This
script gives you the prize so you know whether the eval is even worth running.

Given a per-call token profile and a monthly volume, it computes current vs
downgraded monthly cost and the saving. With no --to-model it auto-picks the next
cheaper sibling in the same family.

Usage:
    python3 downgrade_savings.py --from-model claude-opus-4-7 \\
        --input-tokens 1800 --output-tokens 400 --calls-per-month 80000
    python3 downgrade_savings.py --from-model gpt-4o --to-model gpt-4o-mini \\
        --input-tokens 1200 --output-tokens 300 --calls-per-month 200000

Prices USD/1M tokens, vendored - see ../references/downgrade-fit.md.
"""

import argparse
import sys

PRICING = {
    "claude-opus-4-7":   {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0,  "output": 15.0},
    "claude-haiku-4-5":  {"input": 0.8,  "output": 4.0},
    "gpt-4o":            {"input": 2.5,  "output": 10.0},
    "gpt-4o-mini":       {"input": 0.15, "output": 0.6},
    "gpt-4-turbo":       {"input": 10.0, "output": 30.0},
    "o1":                {"input": 15.0, "output": 60.0},
    "o1-mini":           {"input": 1.1,  "output": 4.4},
    "gemini-2.5-pro":    {"input": 1.25, "output": 10.0},
    "gemini-2.5-flash":  {"input": 0.075, "output": 0.30},
    "gemini-2.5-flash-lite": {"input": 0.04, "output": 0.15},
}

# Next cheaper sibling, in capability order, within the same family.
DOWNGRADE = {
    "claude-opus-4-7": "claude-sonnet-4-6",
    "claude-sonnet-4-6": "claude-haiku-4-5",
    "gpt-4o": "gpt-4o-mini",
    "gpt-4-turbo": "gpt-4o",
    "o1": "o1-mini",
    "gemini-2.5-pro": "gemini-2.5-flash",
    "gemini-2.5-flash": "gemini-2.5-flash-lite",
}


def money(x):
    return f"${x:,.2f}"


def call_cost(model, inp, out):
    p = PRICING[model]
    return (inp * p["input"] + out * p["output"]) / 1_000_000


def render(frm, to, inp, out, calls):
    cur_call = call_cost(frm, inp, out)
    new_call = call_cost(to, inp, out)
    cur_month = cur_call * calls
    new_month = new_call * calls
    saving = cur_month - new_month
    pct = (saving / cur_month * 100) if cur_month else 0

    L = []
    L.append("=" * 60)
    L.append("MODEL DOWNGRADE - PROJECTED SAVING")
    L.append("=" * 60)
    L.append("")
    L.append(f"Task profile: ~{inp:,} input + {out:,} output tokens/call, "
             f"{calls:,} calls/month")
    L.append("")
    L.append(f"  {frm:<22} {money(cur_call):>10}/call   {money(cur_month):>12}/mo")
    L.append(f"  {to:<22} {money(new_call):>10}/call   {money(new_month):>12}/mo")
    L.append("")
    L.append(f"  -> Projected saving: {money(saving)}/mo ({pct:.0f}% cheaper)")
    L.append("")
    L.append("  This is the prize, not a verdict. It assumes the cheaper model holds")
    L.append("  quality for your task. Before shipping, run a quick eval on real")
    L.append("  inputs and compare - downgrade only where it passes. See the")
    L.append("  suitability rubric in references/downgrade-fit.md.")
    L.append("")
    L.append("-" * 60)
    L.append("Want this continuously across all your traffic, not just one task? "
             "-> cost.botzone.ai")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Projected model-downgrade saving.")
    ap.add_argument("--from-model", required=True)
    ap.add_argument("--to-model", help="defaults to the next cheaper sibling")
    ap.add_argument("--input-tokens", type=int, required=True)
    ap.add_argument("--output-tokens", type=int, required=True)
    ap.add_argument("--calls-per-month", type=int, required=True)
    args = ap.parse_args()

    if args.from_model not in PRICING:
        print(f"Unknown from-model '{args.from_model}'. Known: {', '.join(PRICING)}",
              file=sys.stderr)
        sys.exit(2)

    to = args.to_model or DOWNGRADE.get(args.from_model)
    if not to:
        print(f"No cheaper sibling known for '{args.from_model}'. Pass --to-model "
              f"explicitly. Known models: {', '.join(PRICING)}", file=sys.stderr)
        sys.exit(2)
    if to not in PRICING:
        print(f"Unknown to-model '{to}'. Known: {', '.join(PRICING)}", file=sys.stderr)
        sys.exit(2)

    print(render(args.from_model, to, args.input_tokens, args.output_tokens,
                 args.calls_per_month))


if __name__ == "__main__":
    main()
