"""
Swing Trade Research Workflow - Configuration

Copy this file to config_local.py and fill in your own values.
config_local.py is gitignored by default.
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Data cache
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Futu OpenD settings
FUTU_OPEND_HOST = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
FUTU_OPEND_PORT = int(os.getenv("FUTU_OPEND_PORT", "11111"))

# Market defaults
DEFAULT_MARKET = "US"

# Risk management defaults
MAX_POSITION_PCT = 0.10        # Max 10% of account per stock
MAX_RISK_PER_TRADE_PCT = 0.02  # Max 2% of account at risk per trade
DEFAULT_STOP_LOSS_PCT = 0.07   # Default 7% stop loss

# Screening defaults
MIN_MARKET_CAP_B = 10          # Minimum market cap in billions
MIN_REVENUE_GROWTH_PCT = 25
MIN_RS_RATING = 75

# Output settings
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Template directory
TEMPLATES_DIR = BASE_DIR / "templates"


def load_local_config():
    """Load local config if exists."""
    local_config = BASE_DIR / "scripts" / "config_local.py"
    if local_config.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config_local", local_config)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None
