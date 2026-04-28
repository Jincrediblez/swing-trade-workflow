"""
Chart generation utilities for research workflow.
Requires: matplotlib, pandas
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False


def generate_price_chart(
    klines: List[Dict[str, Any]],
    symbol: str,
    output_path: str,
    show_ma: bool = True,
    figsize: tuple = (14, 8)
) -> Optional[str]:
    """Generate a price + volume chart from K-line data."""
    if not CHARTS_AVAILABLE:
        print("Warning: matplotlib/pandas not installed. Skipping chart generation.")
        return None
    
    if not klines:
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(klines)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    
    # Calculate MAs
    if show_ma:
        df["ma_5"] = df["close"].rolling(window=5).mean()
        df["ma_20"] = df["close"].rolling(window=20).mean()
        df["ma_50"] = df["close"].rolling(window=50).mean()
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=figsize,
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True
    )
    fig.suptitle(f"{symbol} Price Chart", fontsize=14, fontweight="bold")
    
    # Price chart
    ax1.plot(df["time"], df["close"], label="Close", color="black", linewidth=1.5)
    
    if show_ma:
        ax1.plot(df["time"], df["ma_5"], label="MA5", color="orange", alpha=0.8, linewidth=1)
        ax1.plot(df["time"], df["ma_20"], label="MA20", color="blue", alpha=0.8, linewidth=1)
        ax1.plot(df["time"], df["ma_50"], label="MA50", color="red", alpha=0.8, linewidth=1)
    
    ax1.set_ylabel("Price ($)")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)
    
    # Volume chart
    colors = ["green" if c >= o else "red" for c, o in zip(df["close"], df["open"])]
    ax2.bar(df["time"], df["volume"], color=colors, alpha=0.7, width=0.8)
    ax2.set_ylabel("Volume")
    ax2.set_xlabel("Date")
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    return output_path


def generate_summary_chart(
    stats: Dict[str, Any],
    symbol: str,
    output_path: str,
    figsize: tuple = (10, 6)
) -> Optional[str]:
    """Generate a summary stats visualization."""
    if not CHARTS_AVAILABLE:
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f"{symbol} Key Statistics", fontsize=14, fontweight="bold")
    
    # Price levels
    levels = {
        "Current": stats.get("current_price", 0),
        "Period High": stats.get("period_high", 0),
        "Period Low": stats.get("period_low", 0),
        "MA5": stats.get("ma_5", 0) or 0,
        "MA20": stats.get("ma_20", 0) or 0,
        "MA50": stats.get("ma_50", 0) or 0,
    }
    
    colors = ["#2ecc71", "#e74c3c", "#3498db", "#f39c12", "#9b59b6", "#1abc9c"]
    
    items = list(levels.items())
    y_pos = range(len(items))
    vals = [v for _, v in items]
    
    bars = ax.barh(y_pos, vals, color=colors[:len(items)], alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([k for k, _ in items])
    ax.set_xlabel("Price ($)")
    ax.grid(True, alpha=0.3, axis="x")
    
    # Add value labels
    for bar, val in zip(bars, vals):
        if val:
            ax.text(val, bar.get_y() + bar.get_height()/2, f" ${val:.2f}",
                   va="center", fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    return output_path


def generate_watchlist_charts(
    symbols_data: Dict[str, List[Dict]],
    output_dir: str
) -> List[str]:
    """Generate charts for multiple symbols in watchlist."""
    if not CHARTS_AVAILABLE:
        return []
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    generated = []
    for symbol, klines in symbols_data.items():
        chart_path = output_path / f"{symbol.replace('.', '_')}_chart.png"
        result = generate_price_chart(klines, symbol, str(chart_path))
        if result:
            generated.append(result)
    
    return generated
