"""
Data normalization and formatting utilities for the research workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _safe_list(raw: Any) -> List[Any]:
    if isinstance(raw, list):
        return raw
    if raw is None:
        return []
    return [raw]


def _extract_content(raw: Optional[Dict[str, Any]], empty_message: str) -> str:
    if not raw or "data" not in raw:
        return empty_message

    data = raw["data"]
    if isinstance(data, dict):
        content = data.get("content")
        if content:
            return str(content).strip()

    return empty_message


def _normalize_publish_time(raw_value: Any) -> str:
    if raw_value is None:
        return ""

    value = str(raw_value).strip()
    if not value:
        return ""

    if value.isdigit():
        try:
            return datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M")
        except (OverflowError, ValueError):
            return value
    return value


def normalize_snapshot(raw: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not raw or "data" not in raw:
        return None

    items = _safe_list(raw["data"])
    if not items:
        return None

    snap = items[0]
    return {
        "code": snap.get("code", "N/A"),
        "name": snap.get("name", "N/A"),
        "last_price": snap.get("last_price"),
        "open": snap.get("open"),
        "high": snap.get("high"),
        "low": snap.get("low"),
        "prev_close": snap.get("prev_close"),
        "volume": snap.get("volume"),
        "turnover": snap.get("turnover"),
        "source": "futuapi",
    }


def normalize_price_history(raw: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not raw or "data" not in raw:
        return []

    rows = []
    for item in _safe_list(raw["data"]):
        rows.append(
            {
                "time": item.get("time", ""),
                "open": item.get("open"),
                "high": item.get("high"),
                "low": item.get("low"),
                "close": item.get("close"),
                "volume": item.get("volume"),
            }
        )
    return rows


def normalize_signal_block(
    raw: Optional[Dict[str, Any]],
    *,
    source: str,
    empty_message: str,
) -> Dict[str, Any]:
    content = _extract_content(raw, empty_message)
    return {
        "content": content,
        "available": bool(raw and "data" in raw),
        "source": source,
    }


def normalize_news_items(raw: Optional[Dict[str, Any]], max_items: int = 10) -> List[Dict[str, str]]:
    if not raw or "data" not in raw:
        return []

    news_items: List[Dict[str, str]] = []
    for item in _safe_list(raw["data"])[:max_items]:
        title = str(item.get("title", "")).replace("<em>", "").replace("</em>", "").strip()
        news_items.append(
            {
                "title": title or "Untitled item",
                "publish_time": _normalize_publish_time(item.get("publish_time", "")),
                "url": str(item.get("url", "")).strip(),
                "source": "futu-news-search",
            }
        )
    return news_items


def calculate_technical_stats(price_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate basic technical statistics from normalized price history."""
    if not price_history:
        return {}

    closes = [row["close"] for row in price_history if isinstance(row.get("close"), (int, float))]
    volumes = [row["volume"] for row in price_history if isinstance(row.get("volume"), (int, float))]

    if not closes:
        return {}

    def ma(values: List[float], period: int) -> Optional[float]:
        if len(values) < period:
            return None
        return sum(values[-period:]) / period

    current = closes[-1]
    first = closes[0]

    return {
        "current_price": current,
        "period_high": max(row.get("high", 0) for row in price_history),
        "period_low": min(row.get("low", float("inf")) for row in price_history),
        "ma_5": ma(closes, 5),
        "ma_20": ma(closes, 20),
        "ma_50": ma(closes, 50),
        "avg_volume": sum(volumes) / len(volumes) if volumes else 0,
        "latest_volume": volumes[-1] if volumes else 0,
        "price_change_pct": ((current - first) / first * 100) if first else 0,
    }


def format_snapshot(snapshot: Optional[Dict[str, Any]]) -> str:
    if not snapshot:
        return "Data unavailable from local automation."

    def fmt_price(value: Any) -> str:
        return f"${value}" if value is not None else "N/A"

    volume = snapshot.get("volume")
    turnover = snapshot.get("turnover")
    volume_text = f"{volume:,}" if isinstance(volume, (int, float)) else "N/A"
    turnover_text = f"${turnover:,.0f}" if isinstance(turnover, (int, float)) else "N/A"

    lines = [
        "| Field | Value |",
        "|------|------|",
        f"| Code | {snapshot.get('code', 'N/A')} |",
        f"| Name | {snapshot.get('name', 'N/A')} |",
        f"| Last price | {fmt_price(snapshot.get('last_price'))} |",
        f"| Open | {fmt_price(snapshot.get('open'))} |",
        f"| High | {fmt_price(snapshot.get('high'))} |",
        f"| Low | {fmt_price(snapshot.get('low'))} |",
        f"| Previous close | {fmt_price(snapshot.get('prev_close'))} |",
        f"| Volume | {volume_text} |",
        f"| Turnover | {turnover_text} |",
        f"| Source | {snapshot.get('source', 'N/A')} |",
    ]
    return "\n".join(lines)


def format_price_history(price_history: List[Dict[str, Any]], num_rows: int = 10) -> str:
    if not price_history:
        return "Data unavailable from local automation."

    recent = price_history[-num_rows:] if len(price_history) > num_rows else price_history
    def fmt_num(value: Any) -> str:
        return f"${value:.2f}" if isinstance(value, (int, float)) else "N/A"

    lines = [
        "| Date | Open | High | Low | Close | Volume (M) |",
        "|------|------|------|------|------|-----------|",
    ]

    for row in recent:
        volume = row.get("volume", 0)
        volume_text = f"{volume / 1e6:.1f}" if isinstance(volume, (int, float)) else "N/A"
        lines.append(
            f"| {str(row.get('time', ''))[:10]} | "
            f"{fmt_num(row.get('open'))} | "
            f"{fmt_num(row.get('high'))} | "
            f"{fmt_num(row.get('low'))} | "
            f"{fmt_num(row.get('close'))} | "
            f"{volume_text} |"
        )

    stats = calculate_technical_stats(price_history)
    if stats:
        ma5 = f"${stats['ma_5']:.2f}" if stats.get("ma_5") else "N/A"
        ma20 = f"${stats['ma_20']:.2f}" if stats.get("ma_20") else "N/A"
        ma50 = f"${stats['ma_50']:.2f}" if stats.get("ma_50") else "N/A"
        lines.extend(
            [
                "",
                "| Stat | Value |",
                "|------|------|",
                f"| Current price | ${stats['current_price']:.2f} |",
                f"| Period high | ${stats['period_high']:.2f} |",
                f"| Period low | ${stats['period_low']:.2f} |",
                f"| MA5 | {ma5} |",
                f"| MA20 | {ma20} |",
                f"| MA50 | {ma50} |",
                f"| Price change | {stats['price_change_pct']:.1f}% |",
            ]
        )

    return "\n".join(lines)


def format_signal_block(signal_block: Optional[Dict[str, Any]]) -> str:
    if not signal_block:
        return "Data unavailable from local automation."

    content = str(signal_block.get("content", "")).strip()
    source = signal_block.get("source", "N/A")
    availability = "available" if signal_block.get("available") else "unavailable"

    if not content:
        content = "Data unavailable from local automation."

    return "\n".join(
        [
            f"**Source**: `{source}`",
            f"**Availability**: {availability}",
            "",
            content,
        ]
    )


def format_news_items(news_items: List[Dict[str, str]]) -> str:
    if not news_items:
        return "Data unavailable from local automation."

    lines: List[str] = []
    for index, item in enumerate(news_items, start=1):
        lines.append(f"{index}. **{item.get('title', 'Untitled item')}**")
        lines.append(f"   - Published: {item.get('publish_time', 'N/A')}")
        lines.append(f"   - Source: {item.get('source', 'N/A')}")
        if item.get("url"):
            lines.append(f"   - Link: {item['url']}")
        lines.append("")
    return "\n".join(lines).rstrip()


def format_manual_summary(summary: Optional[Dict[str, Any]], pending_label: str) -> str:
    if not summary:
        return pending_label

    if summary.get("status") == "pending":
        return summary.get("content", pending_label)

    lines = [
        f"**Status**: {summary.get('status', 'provided')}",
        f"**Source**: {summary.get('source', 'manual')}",
        "",
        summary.get("content", "").strip() or pending_label,
    ]
    return "\n".join(lines)


def format_position_context(position_context: Optional[Dict[str, Any]]) -> str:
    if not position_context:
        return "Position context missing."

    def fmt_price(value: Any) -> str:
        return f"${value}" if isinstance(value, (int, float)) else str(value)

    lines = [
        "| Field | Value |",
        "|------|------|",
        f"| Symbol | {position_context.get('symbol', 'N/A')} |",
        f"| Cost basis | {fmt_price(position_context.get('cost_basis', 'N/A'))} |",
        f"| Entry price | {fmt_price(position_context.get('entry_price', 'N/A'))} |",
        f"| Position size | {position_context.get('position_size', 'N/A')} |",
        f"| Review date | {position_context.get('review_date', 'N/A')} |",
    ]
    if position_context.get("thesis"):
        lines.extend(["", f"**Original thesis**: {position_context['thesis']}"])
    return "\n".join(lines)


def format_trade_plan(trade_plan: Optional[Dict[str, Any]]) -> str:
    if not trade_plan:
        return "Trade plan pending manual completion."

    lines = [
        "| Field | Value |",
        "|------|------|",
        f"| Entry trigger | {trade_plan.get('entry_trigger', 'Pending')} |",
        f"| Buy range | {trade_plan.get('buy_range', 'Pending')} |",
        f"| Stop loss | {trade_plan.get('stop_loss', 'Pending')} |",
        f"| Risk per trade | {trade_plan.get('risk_per_trade', 'Pending')} |",
        f"| Target 1 | {trade_plan.get('target_1', 'Pending')} |",
        f"| Target 2 | {trade_plan.get('target_2', 'Pending')} |",
        f"| Review date | {trade_plan.get('review_date', 'Pending')} |",
    ]
    return "\n".join(lines)


def format_risk_calendar(position_context: Optional[Dict[str, Any]]) -> str:
    base_lines = [
        "| Event | Date | Status |",
        "|------|------|--------|",
        f"| Review date | {position_context.get('review_date', 'Pending') if position_context else 'Pending'} | scheduled |",
        "| Earnings date | Pending manual input | pending |",
        "| FOMC / macro catalyst | Pending manual input | pending |",
        "| Sector catalyst | Pending manual input | pending |",
    ]
    return "\n".join(base_lines)


@dataclass
class SaveOptions:
    symbol: str
    mode: str
    output_dir: str = "./output"
    as_of: Optional[str] = None


def save_report(content: str, options: SaveOptions) -> str:
    out = Path(options.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    timestamp = options.as_of or datetime.now().strftime("%Y%m%d")
    clean_timestamp = timestamp.replace("-", "")
    filename = f"{options.symbol.replace('.', '_')}_{options.mode}_{clean_timestamp}.md"
    filepath = out / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)
