"""
Data formatting utilities for research workflow.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd


def format_snapshot(data: Dict[str, Any]) -> str:
    """Format stock snapshot data into readable markdown."""
    if not data or "data" not in data:
        return "No snapshot data available."
    
    snap = data["data"][0] if isinstance(data["data"], list) else data["data"]
    
    lines = [
        "### 实时行情",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 代码 | {snap.get('code', 'N/A')} |",
        f"| 名称 | {snap.get('name', 'N/A')} |",
        f"| 最新价 | ${snap.get('last_price', 'N/A')} |",
        f"| 开盘 | ${snap.get('open', 'N/A')} |",
        f"| 最高 | ${snap.get('high', 'N/A')} |",
        f"| 最低 | ${snap.get('low', 'N/A')} |",
        f"| 前收 | ${snap.get('prev_close', 'N/A')} |",
        f"| 成交量 | {snap.get('volume', 'N/A'):,} |" if isinstance(snap.get('volume'), (int, float)) else f"| 成交量 | {snap.get('volume', 'N/A')} |",
        f"| 成交额 | ${snap.get('turnover', 'N/A'):,.0f} |" if isinstance(snap.get('turnover'), (int, float)) else f"| 成交额 | {snap.get('turnover', 'N/A')} |",
        "",
    ]
    return "\n".join(lines)


def format_kline(data: Dict[str, Any], num_rows: int = 10) -> str:
    """Format K-line data into markdown table."""
    if not data or "data" not in data:
        return "No K-line data available."
    
    klines = data["data"]
    if not klines:
        return "No K-line data available."
    
    # Show last N rows
    recent = klines[-num_rows:] if len(klines) > num_rows else klines
    
    lines = [
        "### 近期 K 线",
        "",
        "| 日期 | 开盘 | 最高 | 最低 | 收盘 | 成交量(M) |",
        "|------|------|------|------|------|-----------|",
    ]
    
    for k in recent:
        vol_m = k.get('volume', 0) / 1e6 if isinstance(k.get('volume'), (int, float)) else 0
        lines.append(
            f"| {k.get('time', '')[:10]} | "
            f"${k.get('open', 0):.2f} | "
            f"${k.get('high', 0):.2f} | "
            f"${k.get('low', 0):.2f} | "
            f"${k.get('close', 0):.2f} | "
            f"{vol_m:.1f}M |"
        )
    
    lines.append("")
    return "\n".join(lines)


def format_technical_anomaly(data: Dict[str, Any]) -> str:
    """Format technical anomaly data."""
    if not data or "data" not in data:
        return "No technical anomaly data available."
    
    content = data["data"].get("content", "")
    if not content:
        return "近30个自然日内无显著技术异动。"
    
    lines = ["### 技术异动信号", "", content, ""]
    return "\n".join(lines)


def format_option_anomalies(data: Dict[str, Any], max_items: int = 10) -> str:
    """Format options anomaly data."""
    if not data or "data" not in data:
        return "No options data available."
    
    content = data["data"].get("content", "")
    if not content:
        return "近30个自然日内无显著期权异动。"
    
    lines = ["### 期权异动信号", "", content, ""]
    return "\n".join(lines)


def calculate_technical_stats(klines: List[Dict]) -> Dict[str, Any]:
    """Calculate basic technical statistics from K-line data."""
    if not klines:
        return {}
    
    closes = [k["close"] for k in klines if "close" in k]
    volumes = [k["volume"] for k in klines if "volume" in k]
    
    if not closes:
        return {}
    
    current = closes[-1]
    
    # Moving averages
    def ma(values, period):
        if len(values) < period:
            return None
        return sum(values[-period:]) / period
    
    stats = {
        "current_price": current,
        "period_high": max(k.get("high", 0) for k in klines),
        "period_low": min(k.get("low", float('inf')) for k in klines),
        "ma_5": ma(closes, 5),
        "ma_20": ma(closes, 20),
        "ma_50": ma(closes, 50),
        "avg_volume": sum(volumes) / len(volumes) if volumes else 0,
        "latest_volume": volumes[-1] if volumes else 0,
        "price_change_pct": ((current - closes[0]) / closes[0] * 100) if closes[0] else 0,
    }
    
    return stats


def format_news_items(news_data: Dict[str, Any], max_items: int = 10) -> str:
    """Format news search results into markdown."""
    if not news_data or "data" not in news_data:
        return "No news data available."
    
    items = news_data["data"][:max_items]
    if not items:
        return "暂无相关新闻。"
    
    lines = ["### 最新新闻", ""]
    
    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        # Clean HTML tags
        title = title.replace("<em>", "").replace("</em>", "")
        
        pub_time = item.get("publish_time", "")
        if pub_time and pub_time.isdigit():
            pub_time = datetime.fromtimestamp(int(pub_time)).strftime("%Y-%m-%d %H:%M")
        
        url = item.get("url", "")
        lines.append(f"{i}. **{title}**")
        lines.append(f"   - 发布时间：{pub_time}")
        if url:
            lines.append(f"   - 链接：{url}")
        lines.append("")
    
    return "\n".join(lines)


def save_report(content: str, symbol: str, output_dir: str = "./output") -> str:
    """Save formatted report to file."""
    from pathlib import Path
    import os
    
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{symbol.replace('.', '_')}_{timestamp}.md"
    filepath = out / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(filepath)
