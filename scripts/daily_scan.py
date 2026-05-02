#!/usr/bin/env python3
"""
Run deterministic scan-mode reports for a fixed symbol list.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_SYMBOLS = [
    "US.NVDA",
    "US.AMD",
    "US.MSFT",
    "US.AMZN",
    "US.GOOGL",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Daily scan runner")
    parser.add_argument("--output", default="./output/daily_scan", help="Output directory")
    parser.add_argument(
        "--symbols",
        nargs="*",
        default=DEFAULT_SYMBOLS,
        help="Symbols to scan",
    )
    parser.add_argument("--as-of", help="As-of date in YYYY-MM-DD format")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    file_stamp = (args.as_of or datetime.now().strftime("%Y-%m-%d")).replace("-", "")
    for symbol in args.symbols:
        cmd = [
            sys.executable,
            str(Path(__file__).with_name("run_workflow.py")),
            "--symbol",
            symbol,
            "--mode",
            "scan",
            "--output",
            str(output_dir),
        ]
        if args.as_of:
            cmd.extend(["--as-of", args.as_of])
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(f"Scan failed for {symbol}: {result.stderr or result.stdout}")
        generated.append(symbol)

    index_path = output_dir / "index.md"
    lines = [
        "# Daily Scan Index",
        "",
        f"Symbols scanned: {', '.join(generated)}",
        "",
    ]
    for symbol in generated:
        file_name = f"{symbol.replace('.', '_')}_scan_{file_stamp}.md"
        lines.append(f"- {symbol}: `{file_name}`")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
