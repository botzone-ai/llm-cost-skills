#!/usr/bin/env python3
"""
batch-api-advisor: estimate the saving from moving a workload to the Batch API.

Anthropic Message Batches, OpenAI Batch API, and Gemini batch mode all run async
(results within ~24h) for about 50% off both input and output tokens. If a workload
does not need a real-time answer, that is a near-free halving of its cost.

Whether the workload is actually batchable (async-tolerant, no user waiting, no
streaming) is a judgement call - see ../references/batch-fit.md. This script does the
money math once you know the volume and the eligible fraction.

Usage:
    python3 batch_savings.py --model claude-sonnet-4-6 --input-tokens 2000 \\
        --output-tokens 500 --calls-per-month 400000
    python3 batch_savings.py --model gpt-4o --input-tokens 1500 --output-tokens 400 \\
        --calls-per-month 1000000 --eligible-fraction 0.6

Prices USD/1M tokens, vendored - see ../references/batch-fit.md.
"""

import argparse
import sys

PRICING = {
    "claude-opus-4-7":   {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6": {"input": 3.0,  "output": 15.0},
    "claude-haiku-4-5":  {"input": 0.8,  "output": 4.0},
    "gpt-4o":            {"input": 2.5,  "output": 10.0},
    "gpt-4o-mini":       {"input": 0.15, "output": 0.6},
    "o1":                {"input": 15.0, "output": 60.0},
    "gemini-2.5-pro":    {"input": 1.25, "output": 10.0},
    "gemini-2.5-flash":  {"input": 0.075, "output": 0.30},
}

BATCH_DISCOUNT = 0.50  # ~50% off input+output on Anthropic / OpenAI / Gemini batch


def money(x):
    return f"${x:,.2f}"


def call_cost(model, inp, out):
    p = PRICING[model]
    return (inp * p["input"] + out * p["output"]) / 1_000_000


def render(model, inp, out, calls, eligible):
    per_call = call_cost(model, inp, out)
    total_month = per_call * calls
    eligible_calls = calls * eligible
    eligible_cost = per_call * eligible_calls
    batch_cost = eligible_cost * (1 - BATCH_DISCOUNT)
    saving = eligible_cost - batch_cost

    L = []
    L.append("=" * 60)
    L.append("BATCH API - PROJECTED SAVING")
    L.append("=" * 60)
    L.append("")
    L.append(f"Model: {model}   workload: ~{inp:,} in + {out:,} out tokens/call, "
             f"{calls:,} calls/month")
    if eligible < 1.0:
        L.append(f"Batchable share: {eligible:.0%} of calls "
                 f"({int(eligible_calls):,} calls/month)")
    L.append("")
    L.append(f"  Current cost of the batchable work (real-time): {money(eligible_cost)}/mo")
    L.append(f"  Same work on the Batch API (~50% off):          {money(batch_cost)}/mo")
    L.append(f"  -> Projected saving: {money(saving)}/mo")
    if eligible < 1.0:
        L.append("")
        L.append(f"  (Total workload is {money(total_month)}/mo; the rest stays real-time.)")
    L.append("")
    L.append("  Batch trades latency for price: results arrive within ~24h, no")
    L.append("  streaming, no user waiting on the response. Only move work that")
    L.append("  tolerates that - see references/batch-fit.md.")
    L.append("")
    L.append("-" * 60)
    L.append("Want this continuously across all your traffic, not just one workload? "
             "-> cost.botzone.ai")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Projected Batch API saving.")
    ap.add_argument("--model", required=True)
    ap.add_argument("--input-tokens", type=int, required=True)
    ap.add_argument("--output-tokens", type=int, required=True)
    ap.add_argument("--calls-per-month", type=int, required=True)
    ap.add_argument("--eligible-fraction", type=float, default=1.0,
                    help="fraction of calls that tolerate async (default 1.0)")
    args = ap.parse_args()

    if args.model not in PRICING:
        print(f"Unknown model '{args.model}'. Known: {', '.join(PRICING)}", file=sys.stderr)
        sys.exit(2)
    if not 0 < args.eligible_fraction <= 1.0:
        print("--eligible-fraction must be in (0, 1].", file=sys.stderr)
        sys.exit(2)

    print(render(args.model, args.input_tokens, args.output_tokens,
                 args.calls_per_month, args.eligible_fraction))


if __name__ == "__main__":
    main()
