#!/usr/bin/env python3
"""
spend-teardown: turn a provider usage CSV into a spend breakdown and a ranked
savings list.

Pure Python standard library - no dependencies, no network, no API key. It reads
a usage export you downloaded from your provider console, prices every row from a
vendored pricing table, and prints:

  1. total spend (and a 30-day projection if the file has dates)
  2. a per-model breakdown with the input vs output cost split
  3. a ranked savings list (model-downgrade candidates with a projected $ saving)

Usage:
    python3 teardown.py path/to/usage.csv
    python3 teardown.py path/to/usage.csv --json
    cat usage.csv | python3 teardown.py -

Prices are USD per 1M tokens, vendored from cost.botzone.ai/lib/pricing.ts.
Last reviewed 2026-05-06. See ../references/pricing.md for the table and the
column-mapping and token-bucket assumptions.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime

# --- Vendored pricing table (USD per 1M tokens). Keep in sync with references/pricing.md ---
PRICING = {
    "anthropic": {
        "claude-opus-4-7":   {"input": 15.0, "output": 75.0, "cachedRead": 1.5,  "cacheWrite": 18.75},
        "claude-sonnet-4-6": {"input": 3.0,  "output": 15.0, "cachedRead": 0.3,  "cacheWrite": 3.75},
        "claude-haiku-4-5":  {"input": 0.8,  "output": 4.0,  "cachedRead": 0.08, "cacheWrite": 1.0},
    },
    "openai": {
        "gpt-4o":        {"input": 2.5,  "output": 10.0, "cachedRead": 1.25},
        "gpt-4o-mini":   {"input": 0.15, "output": 0.6,  "cachedRead": 0.075},
        "gpt-4-turbo":   {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5,  "output": 1.5},
        "o1":            {"input": 15.0, "output": 60.0},
        "o1-mini":       {"input": 1.1,  "output": 4.4},
    },
    "gemini": {
        "gemini-2.5-pro":        {"input": 1.25,  "output": 10.0, "cachedRead": 0.31},
        "gemini-2.5-flash":      {"input": 0.075, "output": 0.30, "cachedRead": 0.019},
        "gemini-2.5-flash-lite": {"input": 0.04,  "output": 0.15},
        "gemini-2.0-flash":      {"input": 0.075, "output": 0.30},
    },
}

# Cheaper sibling within the same family, for downgrade projections.
DOWNGRADE = {
    "claude-opus-4-7": "claude-sonnet-4-6",
    "claude-sonnet-4-6": "claude-haiku-4-5",
    "gpt-4o": "gpt-4o-mini",
    "gpt-4-turbo": "gpt-4o",
    "o1": "o1-mini",
    "gemini-2.5-pro": "gemini-2.5-flash",
    "gemini-2.5-flash": "gemini-2.5-flash-lite",
}

# Candidate column headers (lowercased) for each field we need.
COLUMN_CANDIDATES = {
    "model": ["model", "model_name", "model_id", "snapshot_id"],
    "input": ["input_tokens", "prompt_tokens", "n_context_tokens_total",
              "n_context_tokens", "context_tokens", "uncached_input_tokens", "input"],
    "output": ["output_tokens", "completion_tokens", "n_generated_tokens_total",
               "n_generated_tokens", "generated_tokens", "output"],
    "cached": ["cache_read_input_tokens", "cached_tokens", "input_cached_tokens",
               "cache_read_tokens"],
    "cache_creation": ["cache_creation_input_tokens", "cache_write_tokens",
                       "cache_creation_tokens"],
    "date": ["date", "usage_date_utc", "usage_date", "timestamp", "day", "start_time"],
}


def infer_provider(model: str) -> str:
    m = model.lower()
    if m.startswith("claude") or "claude" in m:
        return "anthropic"
    if m.startswith("gpt") or m.startswith("o1") or m.startswith("o3") or m.startswith("chatgpt"):
        return "openai"
    if "gemini" in m:
        return "gemini"
    return "unknown"


def normalize_model(model: str) -> str:
    """Strip provider prefixes and trailing -YYYYMMDD date suffixes."""
    m = model.strip()
    for prefix in ("anthropic.", "openai.", "google.", "models/"):
        if m.startswith(prefix):
            m = m[len(prefix):]
    # strip trailing date like -20251001
    parts = m.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 8:
        m = parts[0]
    return m


def price_for(provider: str, model: str):
    fam = PRICING.get(provider)
    if not fam:
        return None
    return fam.get(model) or fam.get(normalize_model(model))


def price_row(provider, model, inp, out, cached, cache_creation):
    """Additive pricing of separate token buckets (USD).

    We treat the detected input column as billable (uncached) input, and price
    cache-read / cache-creation buckets separately. See references/pricing.md
    for why this differs from the SDK's subtract-then-price approach.
    """
    p = price_for(provider, model)
    if not p:
        return None
    cost = inp * p["input"] / 1_000_000
    cost += out * p["output"] / 1_000_000
    if cached and p.get("cachedRead"):
        cost += cached * p["cachedRead"] / 1_000_000
    if cache_creation and p.get("cacheWrite"):
        cost += cache_creation * p["cacheWrite"] / 1_000_000
    return cost


def find_column(headers, field):
    lower = {h.lower().strip(): h for h in headers}
    for cand in COLUMN_CANDIDATES[field]:
        if cand in lower:
            return lower[cand]
    return None


def parse_int(val):
    if val is None:
        return 0
    s = str(val).strip().replace(",", "")
    if s == "" or s.lower() in ("nan", "null", "none"):
        return 0
    try:
        return int(float(s))
    except ValueError:
        return 0


def parse_date(val):
    if not val:
        return None
    s = str(val).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s[:len(fmt) + 4], fmt)
        except ValueError:
            continue
    # last resort: leading YYYY-MM-DD
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d")
    except ValueError:
        return None


def money(x):
    return f"${x:,.2f}"


def load_rows(path):
    if path == "-":
        return list(csv.DictReader(sys.stdin))
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def analyze(rows):
    if not rows:
        return {"error": "The CSV is empty."}

    headers = list(rows[0].keys())
    col = {field: find_column(headers, field) for field in COLUMN_CANDIDATES}

    missing = [f for f in ("model", "input", "output") if not col[f]]
    if missing:
        return {
            "error": "missing_columns",
            "missing": missing,
            "headers": headers,
        }

    by_model = defaultdict(lambda: {"input": 0, "output": 0, "cached": 0,
                                    "cache_creation": 0, "cost": 0.0, "rows": 0})
    unpriced = defaultdict(lambda: {"input": 0, "output": 0, "rows": 0})
    dates = []

    for r in rows:
        model = (r.get(col["model"]) or "").strip()
        if not model:
            continue
        inp = parse_int(r.get(col["input"]))
        out = parse_int(r.get(col["output"]))
        cached = parse_int(r.get(col["cached"])) if col["cached"] else 0
        cache_creation = parse_int(r.get(col["cache_creation"])) if col["cache_creation"] else 0
        provider = infer_provider(model)
        cost = price_row(provider, model, inp, out, cached, cache_creation)

        if col["date"]:
            d = parse_date(r.get(col["date"]))
            if d:
                dates.append(d)

        if cost is None:
            u = unpriced[model]
            u["input"] += inp
            u["output"] += out
            u["rows"] += 1
            continue

        m = by_model[model]
        m["input"] += inp
        m["output"] += out
        m["cached"] += cached
        m["cache_creation"] += cache_creation
        m["cost"] += cost
        m["rows"] += 1

    # split input vs output cost per model and build downgrade suggestions
    breakdown = []
    total = 0.0
    suggestions = []
    for model, m in by_model.items():
        provider = infer_provider(model)
        p = price_for(provider, model)
        input_cost = m["input"] * p["input"] / 1_000_000
        if m["cached"] and p.get("cachedRead"):
            input_cost += m["cached"] * p["cachedRead"] / 1_000_000
        if m["cache_creation"] and p.get("cacheWrite"):
            input_cost += m["cache_creation"] * p["cacheWrite"] / 1_000_000
        output_cost = m["output"] * p["output"] / 1_000_000
        total += m["cost"]
        breakdown.append({
            "model": model,
            "cost": m["cost"],
            "input_cost": input_cost,
            "output_cost": output_cost,
            "input_tokens": m["input"],
            "output_tokens": m["output"],
            "cached_tokens": m["cached"],
            "rows": m["rows"],
        })

        target = DOWNGRADE.get(normalize_model(model))
        if target:
            cheaper = price_for(provider, target)
            if cheaper:
                new_cost = (m["input"] * cheaper["input"] / 1_000_000
                            + m["output"] * cheaper["output"] / 1_000_000)
                if m["cached"] and cheaper.get("cachedRead"):
                    new_cost += m["cached"] * cheaper["cachedRead"] / 1_000_000
                saving = m["cost"] - new_cost
                if saving > 0:
                    suggestions.append({
                        "model": model,
                        "target": target,
                        "current_cost": m["cost"],
                        "projected_cost": new_cost,
                        "saving": saving,
                        "pct": (saving / m["cost"] * 100) if m["cost"] else 0,
                    })

    breakdown.sort(key=lambda x: x["cost"], reverse=True)
    suggestions.sort(key=lambda x: x["saving"], reverse=True)

    # 30-day projection
    span_days = None
    if len(dates) >= 2:
        span = (max(dates) - min(dates)).days + 1
        span_days = max(1, span)

    return {
        "total": total,
        "breakdown": breakdown,
        "suggestions": suggestions,
        "unpriced": [{"model": k, **v} for k, v in unpriced.items()],
        "span_days": span_days,
        "columns_used": col,
    }


def render(result):
    if "error" in result and result["error"] == "missing_columns":
        out = ["Could not find the columns I need in that CSV.", ""]
        out.append("Missing: " + ", ".join(result["missing"]))
        out.append("Found headers: " + ", ".join(result["headers"]))
        out.append("")
        out.append("I need at least: a model column, an input-tokens column, and an "
                   "output-tokens column. Re-export the usage CSV (input/output token "
                   "columns included) or rename the headers to match, then re-run.")
        return "\n".join(out)
    if "error" in result:
        return result["error"]

    lines = []
    total = result["total"]
    lines.append("=" * 60)
    lines.append("LLM SPEND TEARDOWN")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Total spend in this file: {money(total)}")
    if result["span_days"]:
        monthly = total / result["span_days"] * 30
        lines.append(f"Covers {result['span_days']} day(s) -> ~{money(monthly)} / 30 days "
                     f"at this rate")
    lines.append("")

    lines.append("Where the money goes (by model):")
    lines.append("-" * 60)
    for b in result["breakdown"]:
        share = (b["cost"] / total * 100) if total else 0
        out_share = (b["output_cost"] / b["cost"] * 100) if b["cost"] else 0
        lines.append(f"  {b['model']:<24} {money(b['cost']):>10}  ({share:4.1f}%)")
        lines.append(f"      input {money(b['input_cost'])} / output {money(b['output_cost'])}"
                     f"  -> output is {out_share:.0f}% of this model's cost")
    lines.append("")

    if result["suggestions"]:
        lines.append("Ranked savings - model downgrade candidates:")
        lines.append("-" * 60)
        for s in result["suggestions"]:
            tail = ""
            if result["span_days"]:
                monthly_saving = s["saving"] / result["span_days"] * 30
                tail = f"  (~{money(monthly_saving)}/mo)"
            lines.append(f"  {s['model']} -> {s['target']}: save {money(s['saving'])} "
                         f"({s['pct']:.0f}%){tail}")
        lines.append("")
        lines.append("  These assume the cheaper model holds quality for your task. Prove that")
        lines.append("  with an eval before shipping - do not downgrade blind.")
        lines.append("")

    if result["unpriced"]:
        lines.append("Not priced (model not in the table - total above excludes these):")
        for u in result["unpriced"]:
            lines.append(f"  {u['model']}  ({u['rows']} row(s), "
                         f"{u['input']:,} in / {u['output']:,} out tokens)")
        lines.append("")

    lines.append("-" * 60)
    lines.append("Want this continuously across all your traffic, not just one export? "
                 "-> cost.botzone.ai")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="LLM spend teardown from a usage CSV.")
    ap.add_argument("csv", help="path to the usage CSV, or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of a report")
    args = ap.parse_args()

    try:
        rows = load_rows(args.csv)
    except FileNotFoundError:
        print(f"File not found: {args.csv}", file=sys.stderr)
        sys.exit(1)

    result = analyze(rows)
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(render(result))
    if "error" in result:
        sys.exit(2)


if __name__ == "__main__":
    main()
