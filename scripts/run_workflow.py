#!/usr/bin/env python3
"""
Swing Trade Research Workflow - Main Entry Point

Usage:
    python run_workflow.py --symbol US.INTC --output ./reports
    python run_workflow.py --symbol US.NVDA --mode quick
    python run_workflow.py --mode watchlist
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from report_builder import build_quick_report


def run_futu_script(script_name: str, args: list) -> Optional[dict]:
    """Run a Futu API script and return JSON output."""
    futu_scripts = SCRIPT_DIR.parent / ".codex" / "skills" / "futuapi" / "scripts"
    if not futu_scripts.exists():
        # Try alternate paths
        futu_scripts = Path.home() / ".codex" / "skills" / "futuapi" / "scripts"
    
    script_path = futu_scripts / script_name
    if not script_path.exists():
        print(f"Warning: Script not found: {script_path}")
        return None
    
    cmd = [sys.executable, str(script_path)] + args + ["--json"]
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        
        # Parse JSON from output (may have log lines before/after JSON)
        output = result.stdout
        # Extract the first complete JSON object or array
        for i, char in enumerate(output):
            if char in "{[":
                # Use bracket matching to find the end of JSON
                stack = [char]
                end_char = "}" if char == "{" else "]"
                for j in range(i + 1, len(output)):
                    c = output[j]
                    if c == "{" or c == "[":
                        stack.append(c)
                    elif c == "}" or c == "]":
                        if stack:
                            stack.pop()
                            if not stack:
                                try:
                                    return json.loads(output[i:j+1])
                                except json.JSONDecodeError:
                                    break
                else:
                    # Reached end of string, try parsing anyway
                    try:
                        return json.loads(output[i:])
                    except json.JSONDecodeError:
                        continue
        return None
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return None


def run_anomaly_script(skill_name: str, symbol: str, days: int = 30) -> Optional[dict]:
    """Run an anomaly detection script."""
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
        print(f"Warning: Script not found: {script_path}")
        return None
    
    cmd = [
        sys.executable, str(script_path),
        symbol, "--time-range", str(days), "--json"
    ]
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        output = result.stdout
        for i, char in enumerate(output):
            if char in "{[":
                stack = [char]
                end_char = "}" if char == "{" else "]"
                for j in range(i + 1, len(output)):
                    c = output[j]
                    if c == "{" or c == "[":
                        stack.append(c)
                    elif c == "}" or c == "]":
                        if stack:
                            stack.pop()
                            if not stack:
                                try:
                                    return json.loads(output[i:j+1])
                                except json.JSONDecodeError:
                                    break
                else:
                    try:
                        return json.loads(output[i:])
                    except json.JSONDecodeError:
                        continue
        return None
    except Exception as e:
        print(f"Error running {skill_name}: {e}")
        return None


def run_news_search(keyword: str, size: int = 10) -> Optional[dict]:
    """Run news search via curl."""
    import subprocess
    
    cmd = [
        "curl", "-sG", "https://ai-news-search.futunn.com/news_search",
        "-H", "User-Agent: futunn-news-search/0.0.2 (Skill)",
        "--data-urlencode", f"keyword={keyword}",
        "--data-urlencode", f"size={size}",
        "--data-urlencode", "news_type=1",
        "--data-urlencode", "lang=en",
        "--data-urlencode", "sort_type=2",
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def run_full_workflow(symbol: str, output_dir: str):
    """Run the complete 7-step workflow for a symbol."""
    print(f"\n{'='*60}")
    print(f"Swing Trade Research Workflow: {symbol}")
    print(f"{'='*60}\n")
    
    # Step 1-2: Setup
    print("[1/7] 宏观方向 + 初筛: 用户需手动确认")
    print("[2/7] 股票筛选: 用户需手动执行\n")
    
    # Step 3-7: Data collection
    print("[3/7] 收集基本面数据...")
    print("      (建议手动查询财报数据或使用 mx-finance-data)")
    
    print("\n[4/7] 收集行情数据...")
    snapshot = run_futu_script("quote/get_snapshot.py", [symbol])
    kline = run_futu_script("quote/get_kline.py", [symbol, "--ktype", "1d", "--num", "60"])
    
    print("[5/7] 检测技术异动...")
    technical = run_anomaly_script("futu-technical-anomaly", symbol, 30)
    
    print("[6/7] 检测衍生品信号...")
    options = run_anomaly_script("futu-derivatives-anomaly", symbol, 30)
    
    print("[7/7] 收集新闻...")
    news = run_news_search(keyword=symbol.split(".")[-1], size=10)
    
    # Build report
    print("\n[*] 生成研究报告...")
    report_path = build_quick_report(
        symbol=symbol,
        snapshot=snapshot,
        kline=kline,
        technical=technical,
        options=options,
        news=news,
        output_dir=output_dir,
    )
    
    print(f"\n{'='*60}")
    print(f"✅ 报告已生成: {report_path}")
    print(f"{'='*60}\n")
    
    return report_path


def generate_watchlist_template(output_path: str):
    """Generate a watchlist template."""
    template = """# Swing Trade 观察清单

**更新日期**：{date}
**观察市场**：美股

---

## 当前持仓

| 代码 | 公司 | 买入价 | 当前价 | 止损价 | 目标价 | 仓位% | 盈亏% | 状态 |
|------|------|--------|--------|--------|--------|-------|-------|------|

---

## 重点关注（准备买入）

| 代码 | 公司 | 当前价 | 买入触发价 | 止损价 | 目标价 | 优先级 | 等待信号 |
|------|------|--------|-----------|--------|--------|--------|---------|

---

## 观察跟踪（研究中）

| 代码 | 公司 | 当前价 | 关注原因 | 需要验证的点 | 预计研究完成 |
|------|------|--------|---------|-------------|-------------|

---

*Generated by Swing Trade Research Workflow*
""".format(date=__import__("datetime").datetime.now().strftime("%Y-%m-%d"))
    
    Path(output_path).write_text(template, encoding="utf-8")
    print(f"Watchlist template saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Swing Trade Research Workflow"
    )
    parser.add_argument(
        "--symbol", "-s",
        help="Stock symbol (e.g., US.INTC, US.NVDA)"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Output directory for reports"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "quick", "watchlist"],
        default="full",
        help="Workflow mode"
    )
    
    args = parser.parse_args()
    
    if args.mode == "watchlist":
        output = Path(args.output) / "watchlist.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        generate_watchlist_template(str(output))
        return
    
    if not args.symbol:
        print("Error: --symbol is required for full/quick mode")
        sys.exit(1)
    
    run_full_workflow(args.symbol, args.output)


if __name__ == "__main__":
    main()
