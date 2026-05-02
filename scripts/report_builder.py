"""
Mode-aware report builder for generating structured research reports.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from data_formatter import (
    SaveOptions,
    format_manual_summary,
    format_news_items,
    format_position_context,
    format_price_history,
    format_risk_calendar,
    format_signal_block,
    format_snapshot,
    format_trade_plan,
    save_report,
)


class ResearchReport:
    """Build workflow reports that match the repo's supported operating modes."""

    def __init__(
        self,
        *,
        symbol: str,
        mode: str,
        report_data: Dict[str, Any],
        output_dir: str = "./output",
        as_of: Optional[str] = None,
        company_name: str = "",
    ):
        self.symbol = symbol
        self.mode = mode
        self.output_dir = output_dir
        self.company_name = company_name or symbol
        self.report_data = report_data
        self.sections: List[str] = []
        self.metadata = {
            "symbol": symbol,
            "company": self.company_name,
            "mode": mode,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "as_of": as_of or datetime.now().strftime("%Y-%m-%d"),
            "completeness": report_data.get("completeness", {}),
            "sources_used": report_data.get("sources_used", []),
            "final_action": report_data.get("final_action", "pending"),
        }

    def add_frontmatter(self) -> "ResearchReport":
        completeness = self.metadata["completeness"]
        sources = ", ".join(self.metadata["sources_used"]) or "manual"
        self.sections.append(
            "\n".join(
                [
                    "---",
                    f"symbol: {self.metadata['symbol']}",
                    f"mode: {self.metadata['mode']}",
                    f"generated_at: {self.metadata['generated_at']}",
                    f"as_of: {self.metadata['as_of']}",
                    f"completeness: {completeness}",
                    f"sources_used: {sources}",
                    f"final_action: {self.metadata['final_action']}",
                    "---",
                    "",
                ]
            )
        )
        return self

    def add_header(self) -> "ResearchReport":
        completeness = self.metadata["completeness"]
        self.sections.append(
            "\n".join(
                [
                    f"# {self.company_name} ({self.symbol})",
                    "",
                    f"> **Mode**: `{self.mode}`  ",
                    f"> **Generated at**: {self.metadata['generated_at']}  ",
                    f"> **As of**: {self.metadata['as_of']}  ",
                    f"> **Final action state**: `{self.metadata['final_action']}`  ",
                    f"> **Automated complete**: `{completeness.get('automated_complete', False)}`  ",
                    f"> **Manual input required**: `{completeness.get('manual_input_required', False)}`  ",
                    f"> **Missing sources**: {', '.join(completeness.get('missing_sources', [])) or 'none'}",
                    "",
                    "---",
                    "",
                ]
            )
        )
        return self

    def add_scan_sections(self) -> "ResearchReport":
        self.sections.extend(
            [
                "## Market Snapshot\n",
                format_snapshot(self.report_data.get("snapshot")),
                "\n\n## Price History\n",
                format_price_history(self.report_data.get("price_history", []), num_rows=12),
                "\n\n## Technical Signals\n",
                format_signal_block(self.report_data.get("technical_signals")),
                "\n\n## Capital Signals\n",
                format_signal_block(self.report_data.get("capital_signals")),
                "\n\n## Derivatives Signals\n",
                format_signal_block(self.report_data.get("derivatives_signals")),
                "\n\n## News\n",
                format_news_items(self.report_data.get("news_items", [])),
                "\n\n## Final Verdict\n",
                self.report_data.get("decision_summary", "Pending decision summary."),
            ]
        )
        return self

    def add_deep_dive_sections(self) -> "ResearchReport":
        self.sections.extend(
            [
                "## Macro Summary\n",
                format_manual_summary(
                    self.report_data.get("macro_summary"),
                    "Macro summary pending manual or external-skill input.",
                ),
                "\n\n## Fundamental Summary\n",
                format_manual_summary(
                    self.report_data.get("fundamental_summary"),
                    "Fundamental summary pending manual or external-skill input.",
                ),
                "\n\n## Market Snapshot\n",
                format_snapshot(self.report_data.get("snapshot")),
                "\n\n## Price History\n",
                format_price_history(self.report_data.get("price_history", []), num_rows=15),
                "\n\n## Technical Signals\n",
                format_signal_block(self.report_data.get("technical_signals")),
                "\n\n## Confirmation: Capital Flow\n",
                format_signal_block(self.report_data.get("capital_signals")),
                "\n\n## Confirmation: Derivatives\n",
                format_signal_block(self.report_data.get("derivatives_signals")),
                "\n\n## Confirmation: News\n",
                format_news_items(self.report_data.get("news_items", [])),
                "\n\n## Trade Plan\n",
                format_trade_plan(self.report_data.get("trade_plan")),
                "\n\n## Risk Calendar\n",
                format_risk_calendar(self.report_data.get("position_context")),
                "\n\n## Final Decision\n",
                self.report_data.get("decision_summary", "Decision pending manual completion."),
            ]
        )
        return self

    def add_position_review_sections(self) -> "ResearchReport":
        self.sections.extend(
            [
                "## Position Context\n",
                format_position_context(self.report_data.get("position_context")),
                "\n\n## Thesis Status\n",
                self.report_data.get(
                    "thesis_status",
                    "Original thesis status pending manual review.",
                ),
                "\n\n## Technical Health\n",
                format_signal_block(self.report_data.get("technical_signals")),
                "\n\n## Confirmation Health: Capital Flow\n",
                format_signal_block(self.report_data.get("capital_signals")),
                "\n\n## Confirmation Health: Derivatives\n",
                format_signal_block(self.report_data.get("derivatives_signals")),
                "\n\n## News And Catalysts\n",
                format_news_items(self.report_data.get("news_items", [])),
                "\n\n## Risk Calendar\n",
                format_risk_calendar(self.report_data.get("position_context")),
                "\n\n## Review Decision\n",
                self.report_data.get("decision_summary", "Review decision pending."),
            ]
        )
        return self

    def build(self) -> str:
        self.add_frontmatter().add_header()

        if self.mode == "scan":
            self.add_scan_sections()
        elif self.mode == "deep_dive":
            self.add_deep_dive_sections()
        elif self.mode == "position_review":
            self.add_position_review_sections()
        else:
            self.sections.append(f"Unsupported mode: {self.mode}")

        return "\n".join(self.sections).rstrip() + "\n"

    def save(self) -> str:
        return save_report(
            self.build(),
            SaveOptions(
                symbol=self.symbol,
                mode=self.mode,
                output_dir=self.output_dir,
                as_of=self.metadata["as_of"],
            ),
        )


def build_report(
    *,
    symbol: str,
    mode: str,
    report_data: Dict[str, Any],
    output_dir: str = "./output",
    as_of: Optional[str] = None,
    company_name: str = "",
) -> str:
    report = ResearchReport(
        symbol=symbol,
        mode=mode,
        report_data=report_data,
        output_dir=output_dir,
        as_of=as_of,
        company_name=company_name,
    )
    return report.save()
