"""
Convert a generated markdown research report into a styled PDF.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


FONT_NAME = "ReportSans"


def _register_report_font() -> str:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            registerFont(TTFont(FONT_NAME, candidate))
            return FONT_NAME

    fallback = "STSong-Light"
    registerFont(UnicodeCIDFont(fallback))
    return fallback


def _insert_breaks(text: str) -> str:
    def break_url(match: re.Match) -> str:
        url = match.group(0)
        for token in ["/", "-", "_", "?", "&amp;", "="]:
            url = url.replace(token, f"{token}&#8203;")
        return url

    text = re.sub(r"https?://[^\s<]+", break_url, text)
    return text


def _normalize_inline(text: str) -> str:
    text = text.replace("<br/>", "[[BR]]")
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"\s*\(#.*?\)", "", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = _insert_breaks(text)
    text = text.replace("  ", " ")
    text = text.replace("[[BR]]", "<br/>")
    return text


def _parse_table(lines: List[str]) -> List[List[str]]:
    rows: List[List[str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def _build_styles():
    font_name = _register_report_font()

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCN",
            parent=styles["Title"],
            fontName=font_name,
            fontSize=20,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading1CN",
            parent=styles["Heading1"],
            fontName=font_name,
            fontSize=17,
            leading=22,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Heading2CN",
            parent=styles["Heading2"],
            fontName=font_name,
            fontSize=12.8,
            leading=18,
            textColor=colors.HexColor("#1d4ed8"),
            spaceBefore=7,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCN",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=9.8,
            leading=15.8,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
            alignment=TA_LEFT,
            wordWrap="CJK",
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaCN",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=9.0,
            leading=14.2,
            textColor=colors.HexColor("#475569"),
            spaceAfter=6,
            wordWrap="CJK",
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletCN",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=9.8,
            leading=15.8,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=4,
            wordWrap="CJK",
        )
    )
    styles.add(
        ParagraphStyle(
            name="LinkCN",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=8.6,
            leading=13.5,
            leftIndent=12,
            textColor=colors.HexColor("#334155"),
            spaceAfter=5,
            wordWrap="CJK",
        )
    )
    return styles


def markdown_to_story(markdown_text: str):
    styles = _build_styles()
    story = []
    lines = markdown_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 8))
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = _parse_table(table_lines)
            if rows:
                table = Table(
                    [[Paragraph(_normalize_inline(cell), styles["BodyCN"]) for cell in row] for row in rows],
                    repeatRows=1,
                    hAlign="LEFT",
                )
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                            ("LEFTPADDING", (0, 0), (-1, -1), 5),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 6))
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(_normalize_inline(stripped[2:]), styles["TitleCN"]))
            i += 1
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(_normalize_inline(stripped[3:]), styles["Heading1CN"]))
            i += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(_normalize_inline(stripped[4:]), styles["Heading2CN"]))
            i += 1
            continue

        if stripped.startswith("> "):
            story.append(Paragraph(_normalize_inline(stripped[2:]), styles["MetaCN"]))
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            story.append(Paragraph(_normalize_inline("• " + stripped[2:]), styles["BulletCN"]))
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            if "http" in stripped:
                label, _, link = stripped.partition(": http")
                story.append(Paragraph(_normalize_inline(label + ":"), styles["BulletCN"]))
                story.append(Paragraph(_normalize_inline("http" + link), styles["LinkCN"]))
            elif "https://" in stripped:
                story.append(Paragraph(_normalize_inline(stripped), styles["LinkCN"]))
            else:
                story.append(Paragraph(_normalize_inline(stripped), styles["BulletCN"]))
            i += 1
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith(("#", "|", ">", "-", "*")) or re.match(r"^\d+\.\s+", nxt):
                break
            paragraph_lines.append(nxt)
            i += 1
        paragraph_text = "<br/>".join(paragraph_lines)
        if paragraph_text.startswith("链接：") or paragraph_text.startswith("链接:"):
            story.append(Paragraph(_normalize_inline(paragraph_text), styles["LinkCN"]))
        else:
            story.append(Paragraph(_normalize_inline(paragraph_text), styles["BodyCN"]))

    return story


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawRightString(doc.pagesize[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def export_markdown_to_pdf(markdown_path: str, pdf_path: str) -> str:
    markdown = Path(markdown_path)
    output = Path(pdf_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    story = markdown_to_story(markdown.read_text(encoding="utf-8"))
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=markdown.stem,
        author="Codex",
    )
    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    return str(output)


def main():
    parser = argparse.ArgumentParser(description="Export markdown report to PDF")
    parser.add_argument("--input", required=True, help="Markdown report path")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()
    result = export_markdown_to_pdf(args.input, args.output)
    print(result)


if __name__ == "__main__":
    main()
