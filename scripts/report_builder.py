"""
Report builder for generating structured research reports.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from data_formatter import (
    format_snapshot,
    format_kline,
    format_technical_anomaly,
    format_option_anomalies,
    format_news_items,
    calculate_technical_stats,
    save_report,
)


class ResearchReport:
    """Builds a structured swing trade research report."""
    
    def __init__(self, symbol: str, company_name: str = ""):
        self.symbol = symbol
        self.company_name = company_name or symbol
        self.sections: List[str] = []
        self.metadata = {
            "symbol": symbol,
            "company": company_name,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.data: Dict[str, Any] = {}
    
    def add_header(self) -> "ResearchReport":
        """Add report header."""
        header = f"""# {self.company_name} ({self.symbol}) 投研分析报告

> **生成时间**：{self.metadata["generated_at"]}  
> **分析类型**：Swing Trade 共振分析  
> **风格标签**：拐点 / 超级成长 / 大盘科技 / 大趋势

---

"""
        self.sections.append(header)
        return self
    
    def add_toc(self) -> "ResearchReport":
        """Add table of contents."""
        toc = """## 目录

1. [行情快照](#一行情快照)
2. [价格走势](#二价格走势)
3. [基本面摘要](#三基本面摘要)
4. [技术异动](#四技术异动)
5. [期权/衍生品信号](#五期权衍生品信号)
6. [新闻与催化](#六新闻与催化)
7. [综合判断](#七综合判断)
8. [交易计划建议](#八交易计划建议)

---

"""
        self.sections.append(toc)
        return self
    
    def add_snapshot(self, snapshot_data: Dict[str, Any]) -> "ResearchReport":
        """Add market snapshot section."""
        self.sections.append("## 一、行情快照\n")
        self.sections.append(format_snapshot(snapshot_data))
        self.sections.append("\n---\n\n")
        self.data["snapshot"] = snapshot_data
        return self
    
    def add_kline(self, kline_data: Dict[str, Any]) -> "ResearchReport":
        """Add K-line analysis section."""
        self.sections.append("## 二、价格走势\n")
        self.sections.append(format_kline(kline_data, num_rows=15))
        
        # Add stats
        if "data" in kline_data and kline_data["data"]:
            stats = calculate_technical_stats(kline_data["data"])
            if stats:
                self.sections.append("\n### 技术统计\n")
                self.sections.append(f"| 指标 | 数值 |\n|------|------|\n")
                self.sections.append(f"| 当前价 | ${stats['current_price']:.2f} |\n")
                self.sections.append(f"| 区间最高价 | ${stats['period_high']:.2f} |\n")
                self.sections.append(f"| 区间最低价 | ${stats['period_low']:.2f} |\n")
                if stats.get("ma_5"):
                    self.sections.append(f"| MA5 | ${stats['ma_5']:.2f} |\n")
                if stats.get("ma_20"):
                    self.sections.append(f"| MA20 | ${stats['ma_20']:.2f} |\n")
                if stats.get("ma_50"):
                    self.sections.append(f"| MA50 | ${stats['ma_50']:.2f} |\n")
                self.sections.append(f"| 区间涨跌幅 | {stats['price_change_pct']:.1f}% |\n")
        
        self.sections.append("\n---\n\n")
        self.data["kline"] = kline_data
        return self
    
    def add_fundamentals(self, content: str) -> "ResearchReport":
        """Add fundamental analysis section."""
        self.sections.append("## 三、基本面摘要\n\n")
        self.sections.append(content)
        self.sections.append("\n\n---\n\n")
        return self
    
    def add_technical_anomaly(self, anomaly_data: Dict[str, Any]) -> "ResearchReport":
        """Add technical anomaly section."""
        self.sections.append("## 四、技术异动\n")
        self.sections.append(format_technical_anomaly(anomaly_data))
        self.sections.append("\n---\n\n")
        self.data["technical"] = anomaly_data
        return self
    
    def add_options(self, options_data: Dict[str, Any]) -> "ResearchReport":
        """Add options/derivatives section."""
        self.sections.append("## 五、期权/衍生品信号\n")
        self.sections.append(format_option_anomalies(options_data))
        self.sections.append("\n---\n\n")
        self.data["options"] = options_data
        return self
    
    def add_news(self, news_data: Dict[str, Any]) -> "ResearchReport":
        """Add news section."""
        self.sections.append("## 六、新闻与催化\n")
        self.sections.append(format_news_items(news_data, max_items=10))
        self.sections.append("\n---\n\n")
        self.data["news"] = news_data
        return self
    
    def add_conclusion(
        self,
        fundamental_score: int = 0,
        technical_score: int = 0,
        capital_score: int = 0,
        sentiment_score: int = 0,
        recommendation: str = "",
        reasoning: str = "",
        trade_plan: Optional[Dict[str, str]] = None,
    ) -> "ResearchReport":
        """Add conclusion and recommendation."""
        avg_score = (fundamental_score + technical_score + capital_score + sentiment_score) / 4
        
        def fmt_score(score: int) -> str:
            return f"{score}/5" if score else "N/A"
        
        trade_plan = trade_plan or {}
        
        conclusion = f"""## 七、综合判断

| 维度 | 评分 | 状态 |
|------|------|------|
| 基本面 | {fmt_score(fundamental_score)} | |
| 技术面 | {fmt_score(technical_score)} | |
| 资金面 | {fmt_score(capital_score)} | |
| 情绪面 | {fmt_score(sentiment_score)} | |
| **综合** | **{round(avg_score, 1)}/5** | |

### 共振判断
{reasoning}

### 操作建议
**{recommendation}**

---

## 八、交易计划建议

### 买入方案
- **触发条件**：{trade_plan.get("trigger", "___")}
- **买入区间**：{trade_plan.get("buy_range", "$___ - $___")}
- **仓位建议**：{trade_plan.get("position_size", "___% 账户资金")}

### 止损
- **止损价**：{trade_plan.get("stop_loss", "$___")}
- **止损幅度**：{trade_plan.get("stop_loss_pct", "___%")}

### 目标位
- 第一目标：{trade_plan.get("target_1", "$___（减仓 ___%）")}
- 第二目标：{trade_plan.get("target_2", "$___（减仓 ___%）")}
- 第三目标：{trade_plan.get("target_3", "$___（清仓）")}

---

*本报告由 Swing Trade Research Workflow 自动生成，仅供参考，不构成投资建议。*
"""
        self.sections.append(conclusion)
        return self
    
    def build(self) -> str:
        """Build the complete report."""
        return "\n".join(self.sections)
    
    def save(self, output_dir: str = "./output") -> str:
        """Save report to file and return path."""
        content = self.build()
        return save_report(content, self.symbol, output_dir)


def build_quick_report(
    symbol: str,
    company_name: str = "",
    snapshot: Optional[Dict] = None,
    kline: Optional[Dict] = None,
    fundamentals: str = "",
    technical: Optional[Dict] = None,
    options: Optional[Dict] = None,
    news: Optional[Dict] = None,
    fundamental_score: int = 0,
    technical_score: int = 0,
    capital_score: int = 0,
    sentiment_score: int = 0,
    recommendation: str = "",
    reasoning: str = "",
    trade_plan: Optional[Dict[str, str]] = None,
    output_dir: str = "./output"
) -> str:
    """Build a quick research report from available data."""
    report = ResearchReport(symbol, company_name=company_name)
    report.add_header().add_toc()

    if snapshot:
        report.add_snapshot(snapshot)
    if kline:
        report.add_kline(kline)
    if fundamentals:
        report.add_fundamentals(fundamentals)
    if technical:
        report.add_technical_anomaly(technical)
    if options:
        report.add_options(options)
    if news:
        report.add_news(news)

    report.add_conclusion(
        fundamental_score=fundamental_score,
        technical_score=technical_score,
        capital_score=capital_score,
        sentiment_score=sentiment_score,
        recommendation=recommendation or "请根据上述数据手动填写综合判断和交易计划。",
        reasoning=reasoning,
        trade_plan=trade_plan,
    )

    return report.save(output_dir)
