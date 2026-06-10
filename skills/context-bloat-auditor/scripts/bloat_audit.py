#!/usr/bin/env python3
"""
context-bloat-auditor: find context that is inflating a prompt's cost.

Reads a prompt or agent-run dump (a text file, or stdin) and reports:
  - total context size in tokens and the input cost per call (and per month)
  - REPEATED content: blocks that appear more than once - a hard, quantifiable
    waste figure in tokens and dollars
  - the LARGEST blocks - candidates to trim, summarise, or move out of the prompt

The repeated-content figure is exact waste (you are sending identical bytes
twice). The largest-blocks list is where to look next, not guaranteed waste.

Token counts are estimated at ~4 chars/token (no provider tokeniser is bundled
and this skill never asks for an API key) - treat them as estimates, good to
roughly +/-15% for English prose.

Usage:
    python3 bloat_audit.py prompt.txt --model claude-sonnet-4-6 --calls-per-month 50000
    cat run_dump.txt | python3 bloat_audit.py - --model gpt-4o
"""

import argparse
import re
import sys
from collections import OrderedDict

INPUT_PRICE = {  # USD per 1M input tokens (vendored; update quarterly)
    "claude-opus-4-7": 15.0, "claude-sonnet-4-6": 3.0, "claude-haiku-4-5": 0.8,
    "gpt-4o": 2.5, "gpt-4o-mini": 0.15, "gpt-4-turbo": 10.0,
    "gemini-2.5-pro": 1.25, "gemini-2.5-flash": 0.075,
}

CHARS_PER_TOKEN = 4.0


def est_tokens(text):
    return max(0, round(len(text) / CHARS_PER_TOKEN))


def money(x):
    return f"${x:,.2f}"


def money_fine(x):
    # per-call costs are fractions of a cent; show enough precision to be non-zero
    if x and abs(x) < 0.01:
        return f"${x:.4f}"
    return f"${x:,.2f}"


def norm_key(block):
    # normalise whitespace so trivially-different repeats still match
    return re.sub(r"\s+", " ", block).strip().lower()


def split_blocks(text):
    # a block is a run of non-empty lines separated by blank line(s)
    raw = re.split(r"\n\s*\n", text)
    return [b.strip() for b in raw if b.strip()]


def analyze(text, price):
    total_tokens = est_tokens(text)
    cost_per_call = total_tokens * price / 1_000_000

    blocks = split_blocks(text)
    groups = OrderedDict()  # key -> {"sample": str, "count": int, "tokens": int}
    for b in blocks:
        k = norm_key(b)
        if len(k) < 25:  # ignore tiny blocks (closing braces, short labels)
            continue
        if k not in groups:
            groups[k] = {"sample": b, "count": 0, "tokens": est_tokens(b)}
        groups[k]["count"] += 1

    duplicates = [g for g in groups.values() if g["count"] > 1]
    duplicates.sort(key=lambda g: g["tokens"] * (g["count"] - 1), reverse=True)

    wasted_tokens = sum(g["tokens"] * (g["count"] - 1) for g in duplicates)
    wasted_cost_per_call = wasted_tokens * price / 1_000_000

    largest = sorted(groups.values(), key=lambda g: g["tokens"], reverse=True)[:5]

    return {
        "total_tokens": total_tokens,
        "cost_per_call": cost_per_call,
        "duplicates": duplicates,
        "wasted_tokens": wasted_tokens,
        "wasted_cost_per_call": wasted_cost_per_call,
        "largest": largest,
        "price": price,
    }


def first_line(s, n=64):
    line = s.strip().splitlines()[0] if s.strip() else ""
    return (line[:n] + "...") if len(line) > n else line


def render(r, model, calls):
    L = []
    L.append("=" * 60)
    L.append("CONTEXT BLOAT AUDIT")
    L.append("=" * 60)
    L.append("")
    L.append(f"Model: {model}   (estimates at ~{CHARS_PER_TOKEN:.0f} chars/token)")
    L.append(f"Total context: ~{r['total_tokens']:,} tokens "
             f"= {money_fine(r['cost_per_call'])} per call (input only)")
    if calls:
        L.append(f"  At {calls:,} calls/month: {money(r['cost_per_call'] * calls)}/mo just to send this context")
    L.append("")

    L.append("Repeated content (exact waste - you are sending these twice or more):")
    L.append("-" * 60)
    if r["duplicates"]:
        for g in r["duplicates"][:8]:
            waste_tok = g["tokens"] * (g["count"] - 1)
            waste_call = waste_tok * r["price"] / 1_000_000
            extra = ""
            if calls:
                extra = f", {money(waste_call * calls)}/mo"
            L.append(f"  x{g['count']}  ~{g['tokens']:,} tok each  "
                     f"-> wastes ~{waste_tok:,} tok/call ({money_fine(waste_call)}/call{extra})")
            L.append(f"        \"{first_line(g['sample'])}\"")
        L.append("")
        total_month = (f", {money(r['wasted_cost_per_call'] * calls)}/mo" if calls else "")
        L.append(f"  TOTAL repeated-content waste: ~{r['wasted_tokens']:,} tokens/call "
                 f"= {money_fine(r['wasted_cost_per_call'])}/call{total_month}")
    else:
        L.append("  None found. No duplicated blocks - good.")
    L.append("")

    L.append("Largest blocks (where to look next - trim, summarise, or move out):")
    L.append("-" * 60)
    for g in r["largest"]:
        share = (g["tokens"] / r["total_tokens"] * 100) if r["total_tokens"] else 0
        L.append(f"  ~{g['tokens']:,} tok ({share:.0f}% of context)  "
                 f"\"{first_line(g['sample'])}\"")
    L.append("")
    L.append("  Big static blocks that repeat across calls are also caching candidates")
    L.append("  (see the prompt-caching-advisor skill). Big per-call blobs (pasted files,")
    L.append("  logs, full tool outputs) are candidates to truncate or fetch on demand.")
    L.append("")
    L.append("-" * 60)
    L.append("Want this continuously across all your traffic, not just one prompt? "
             "-> cost.botzone.ai")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Audit a prompt/run for context bloat.")
    ap.add_argument("file", help="prompt or run dump (text file), or - for stdin")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--calls-per-month", type=int, default=0)
    args = ap.parse_args()

    price = INPUT_PRICE.get(args.model)
    if price is None:
        print(f"Unknown model '{args.model}'. Known: {', '.join(INPUT_PRICE)}", file=sys.stderr)
        sys.exit(2)

    if args.file == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

    if not text.strip():
        print("Empty input - nothing to audit.", file=sys.stderr)
        sys.exit(1)

    print(render(analyze(text, price), args.model, args.calls_per_month))


if __name__ == "__main__":
    main()
