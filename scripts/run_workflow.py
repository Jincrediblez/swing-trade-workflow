#!/usr/bin/env python3
"""
Workflow orchestrator for scan, deep-dive, and position-review reports.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from data_formatter import (
    normalize_news_items,
    normalize_price_history,
    normalize_signal_block,
    normalize_snapshot,
)
from report_builder import build_report


def _extract_json_output(output: str) -> Optional[Dict[str, Any]]:
    for i, char in enumerate(output):
        if char not in "{[":
            continue
        stack = [char]
        for j in range(i + 1, len(output)):
            current = output[j]
            if current in "{[":
                stack.append(current)
            elif current in "}]":
                if stack:
                    stack.pop()
                if not stack:
                    try:
                        return json.loads(output[i : j + 1])
                    except json.JSONDecodeError:
                        break
    return None


def run_futu_script(script_name: str, args: List[str]) -> Optional[Dict[str, Any]]:
    futu_scripts = SCRIPT_DIR.parent / ".codex" / "skills" / "futuapi" / "scripts"
    if not futu_scripts.exists():
        futu_scripts = Path.home() / ".codex" / "skills" / "futuapi" / "scripts"

    script_path = futu_scripts / script_name
    if not script_path.exists():
        return None

    cmd = [sys.executable, str(script_path)] + args + ["--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return _extract_json_output(result.stdout)
    except Exception:
        return None


def run_anomaly_script(skill_name: str, symbol: str, days: int = 30) -> Optional[Dict[str, Any]]:
    skill_dir = Path.home() / ".codex" / "skills" / skill_name / "scripts"
    script_map = {
        "futu-technical-anomaly": "handle_technical_anomaly.py",
        "futu-capital-anomaly": "handle_capital_anomaly.py",
        "futu-derivatives-anomaly": "handle_derivatives_anomaly.py",
    }
    script_name = script_map.get(skill_name)
    if not script_name:
        return None

    script_path = skill_dir / script_name
    if not script_path.exists():
        return None

    cmd = [sys.executable, str(script_path), symbol, "--time-range", str(days), "--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return _extract_json_output(result.stdout)
    except Exception:
        return None


def run_news_search(keyword: str, size: int = 10) -> Optional[Dict[str, Any]]:
    cmd = [
        "curl",
        "-sG",
        "https://ai-news-search.futunn.com/news_search",
        "-H",
        "User-Agent: futunn-news-search/0.0.2 (Skill)",
        "--data-urlencode",
        f"keyword={keyword}",
        "--data-urlencode",
        f"size={size}",
        "--data-urlencode",
        "news_type=1",
        "--data-urlencode",
        "lang=en",
        "--data-urlencode",
        "sort_type=2",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)
    except Exception:
        return None


def _pending_summary(label: str, source: str) -> Dict[str, str]:
    return {
        "status": "pending",
        "source": source,
        "content": label,
    }


def _manual_summary(content: Optional[str], source: str, pending_label: str) -> Dict[str, str]:
    if content and content.strip():
        return {
            "status": "provided",
            "source": source,
            "content": content.strip(),
        }
    return _pending_summary(pending_label, source)


def _build_trade_plan(mode: str, review_date: Optional[str]) -> Dict[str, str]:
    if mode == "scan":
        return {}
    return {
        "entry_trigger": "Pending manual completion after confirmation review",
        "buy_range": "Pending",
        "stop_loss": "Pending",
        "risk_per_trade": "Pending",
        "target_1": "Pending",
        "target_2": "Pending",
        "review_date": review_date or "Pending",
    }


def _build_position_context(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    if args.mode != "position_review" and not args.review_date:
        return None

    return {
        "symbol": args.symbol,
        "cost_basis": args.cost_basis if args.cost_basis is not None else "Pending",
        "entry_price": args.entry_price if args.entry_price is not None else "Pending",
        "position_size": args.position_size or "Pending",
        "review_date": args.review_date or "Pending",
        "thesis": args.thesis or "",
    }


def _build_completeness(
    *,
    mode: str,
    snapshot: Optional[Dict[str, Any]],
    price_history: List[Dict[str, Any]],
    technical_signals: Dict[str, Any],
    capital_signals: Dict[str, Any],
    derivatives_signals: Dict[str, Any],
    news_items: List[Dict[str, str]],
    macro_summary: Optional[Dict[str, str]],
    fundamental_summary: Optional[Dict[str, str]],
) -> Dict[str, Any]:
    missing_sources: List[str] = []

    if not snapshot:
        missing_sources.append("snapshot")
    if not price_history:
        missing_sources.append("price_history")
    if not technical_signals.get("available"):
        missing_sources.append("technical_signals")
    if not capital_signals.get("available"):
        missing_sources.append("capital_signals")
    if not derivatives_signals.get("available"):
        missing_sources.append("derivatives_signals")
    if not news_items:
        missing_sources.append("news_items")
    if mode == "deep_dive":
        if not macro_summary or macro_summary.get("status") != "provided":
            missing_sources.append("macro_summary")
        if not fundamental_summary or fundamental_summary.get("status") != "provided":
            missing_sources.append("fundamental_summary")

    return {
        "automated_complete": len(missing_sources) == 0,
        "manual_input_required": mode in {"deep_dive", "position_review"},
        "missing_sources": missing_sources,
    }


def _build_decision_summary(mode: str, completeness: Dict[str, Any]) -> str:
    missing = completeness.get("missing_sources", [])
    if mode == "scan":
        if missing:
            return (
                "Watch: scan completed with gaps. Review the missing sections before "
                "promoting this symbol to deep_dive."
            )
        return "Scan complete: classify manually as pass, watch, or reject based on the gathered signals."

    if mode == "deep_dive":
        if missing:
            return (
                "Deep-dive draft: report is incomplete. Fill the pending macro, "
                "fundamental, and trade-plan inputs before marking the setup trade-ready."
            )
        return "Deep-dive complete: finalize the thesis, sizing, and execution decision manually."

    return (
        "Position review draft: confirm whether the original thesis is intact, "
        "weakened, or broken before deciding hold, add, reduce, or exit."
    )


def collect_report_data(args: argparse.Namespace) -> Dict[str, Any]:
    symbol = args.symbol
    keyword = symbol.split(".")[-1]

    snapshot = normalize_snapshot(run_futu_script("quote/get_snapshot.py", [symbol]))
    price_history = normalize_price_history(
        run_futu_script("quote/get_kline.py", [symbol, "--ktype", "1d", "--num", "60"])
    )
    technical_signals = normalize_signal_block(
        run_anomaly_script("futu-technical-anomaly", symbol, 30),
        source="futu-technical-anomaly",
        empty_message="Data unavailable from local automation.",
    )
    capital_signals = normalize_signal_block(
        run_anomaly_script("futu-capital-anomaly", symbol, 30),
        source="futu-capital-anomaly",
        empty_message="Data unavailable from local automation.",
    )
    derivatives_signals = normalize_signal_block(
        run_anomaly_script("futu-derivatives-anomaly", symbol, 30),
        source="futu-derivatives-anomaly",
        empty_message="Data unavailable from local automation.",
    )
    news_items = normalize_news_items(run_news_search(keyword=keyword, size=10))

    macro_summary = _manual_summary(
        args.macro_summary,
        "manual_or_external_skill",
        "Macro summary pending manual or external-skill input.",
    )
    fundamental_summary = _manual_summary(
        args.fundamental_summary,
        "manual_or_external_skill",
        "Fundamental summary pending manual or external-skill input.",
    )
    position_context = _build_position_context(args)
    trade_plan = _build_trade_plan(args.mode, args.review_date)

    completeness = _build_completeness(
        mode=args.mode,
        snapshot=snapshot,
        price_history=price_history,
        technical_signals=technical_signals,
        capital_signals=capital_signals,
        derivatives_signals=derivatives_signals,
        news_items=news_items,
        macro_summary=macro_summary,
        fundamental_summary=fundamental_summary,
    )

    if args.mode == "scan":
        final_action = "watch" if completeness["missing_sources"] else "scan_complete"
    elif args.mode == "deep_dive":
        final_action = "incomplete" if completeness["missing_sources"] else "ready_for_manual_decision"
    else:
        final_action = "review_required"

    return {
        "snapshot": snapshot,
        "price_history": price_history,
        "technical_signals": technical_signals,
        "capital_signals": capital_signals,
        "derivatives_signals": derivatives_signals,
        "news_items": news_items,
        "fundamental_summary": fundamental_summary,
        "macro_summary": macro_summary,
        "trade_plan": trade_plan,
        "position_context": position_context,
        "thesis_status": args.thesis or "Original thesis pending manual restatement.",
        "completeness": completeness,
        "final_action": final_action,
        "sources_used": [
            "futuapi",
            "futu-technical-anomaly",
            "futu-capital-anomaly",
            "futu-derivatives-anomaly",
            "futu-news-search",
        ],
        "decision_summary": _build_decision_summary(args.mode, completeness),
    }


def generate_watchlist_template(output_path: str) -> None:
    template = """# Swing Trade Watchlist

**Updated**: {date}
**Market**: US

---

## Workflow Queue

| Symbol | State | Last review | Next action | Notes |
|------|------|------|------|------|

---

## Open Positions

| Symbol | Cost basis | Current thesis status | Next review date | Notes |
|------|------|------|------|------|

---

## Archived

| Symbol | Outcome | Closed date | Notes |
|------|------|------|------|

---

*Generated by Swing Trade Research Workflow*
""".format(date=__import__("datetime").datetime.now().strftime("%Y-%m-%d"))

    Path(output_path).write_text(template, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Swing Trade Research Workflow")
    parser.add_argument("--symbol", "-s", help="Stock symbol (e.g., US.INTC, US.NVDA)")
    parser.add_argument("--output", "-o", default="./output", help="Output directory for reports")
    parser.add_argument(
        "--mode",
        choices=["scan", "deep_dive", "position_review", "watchlist"],
        default="scan",
        help="Workflow mode",
    )
    parser.add_argument("--as-of", help="As-of date in YYYY-MM-DD format")
    parser.add_argument("--macro-summary", help="Optional macro summary text for deep_dive mode")
    parser.add_argument(
        "--fundamental-summary",
        help="Optional fundamental summary text for deep_dive mode",
    )
    parser.add_argument("--entry-price", type=float, help="Entry price for position_review mode")
    parser.add_argument("--cost-basis", type=float, help="Cost basis for position_review mode")
    parser.add_argument("--position-size", help="Position size or notional for position_review mode")
    parser.add_argument("--review-date", help="Review date for deep_dive or position_review mode")
    parser.add_argument("--thesis", help="Original thesis or current thesis note")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "watchlist":
        output = Path(args.output) / "watchlist.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        generate_watchlist_template(str(output))
        print(f"Watchlist template saved to: {output}")
        return

    if not args.symbol:
        print("Error: --symbol is required for scan, deep_dive, and position_review modes")
        sys.exit(1)

    if args.mode == "position_review" and args.cost_basis is None and args.entry_price is None:
        print("Error: position_review mode requires --cost-basis or --entry-price")
        sys.exit(1)

    report_data = collect_report_data(args)
    report_path = build_report(
        symbol=args.symbol,
        mode=args.mode,
        report_data=report_data,
        output_dir=args.output,
        as_of=args.as_of,
    )
    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
