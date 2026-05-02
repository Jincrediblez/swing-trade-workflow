# US Stock Research Workflow

> Source-of-truth operating model for US swing-trade research.

## Overview

This workflow has three first-class modes:

```text
scan -> deep_dive -> position_review
```

The repo automates the signal-gathering core, but not the full investment decision. Reports must say clearly when they are drafts, incomplete, or ready for manual judgment.

## Mode Definitions

### 1. `scan`

Purpose: fast triage of a single symbol or a small basket.

Automated sections:
- snapshot
- price history
- technical signals
- capital signals
- derivatives signals
- recent news

Expected output:
- `pass`, `watch`, or `reject` style verdict
- no full thesis
- no claim of completion beyond the scan layer

Use when:
- reacting to a move
- scanning a watchlist
- deciding whether a name deserves a deep dive

### 2. `deep_dive`

Purpose: pre-trade research draft aligned to the richer US workflow.

Automated sections:
- snapshot
- price history
- technical signals
- capital signals
- derivatives signals
- recent news

Manual or external-skill sections:
- macro regime summary
- fundamental summary
- trade-plan completion
- catalyst calendar details

Expected output:
- structured research draft
- explicit completeness state
- clear note if manual input is still required

Use when:
- a name passed scan
- you want a written pre-trade file
- you want the workflow sections aligned before making a decision

### 3. `position_review`

Purpose: monitor an existing position against the original thesis and current confirmation signals.

Required context:
- cost basis or entry price
- position size
- review date
- original thesis note when available

Automated sections:
- technical signals
- capital signals
- derivatives signals
- recent news

Expected output:
- thesis status draft
- hold / add / reduce / exit review section
- explicit note that final execution remains manual

## Workflow Layers

### Layer A: Automated signal gathering

Local scripts gather:
- Futu snapshot
- daily kline history
- technical anomaly output
- capital anomaly output
- derivatives anomaly output
- recent news

If a source is unavailable, the report must say `Data unavailable from local automation`.

### Layer B: Structured research drafting

The report builder turns normalized inputs into one of the three supported report types. Each report includes:

- mode
- data timestamp
- completeness flags
- missing-source disclosures
- final action state

### Layer C: Manual decision layer

Still manual:
- macro interpretation
- fundamental interpretation
- trade sizing
- final trade decision
- order execution

## Completeness Semantics

Use these rules consistently:

- `automated_complete=true`
  All expected automated inputs for the selected mode were gathered.
- `manual_input_required=true`
  The selected mode still depends on human or external-skill input.
- `missing_sources`
  Any unavailable automated input must be listed.

For `deep_dive`, missing macro or fundamental summaries means the report is incomplete even if the automated signals are present.

## Template Mapping

| Mode | Primary template / output shape |
|------|---------------------------------|
| `scan` | `templates/us/07_quick_scan.md` |
| `deep_dive` | `templates/us/05_trade_plan.md` plus structured report sections |
| `position_review` | `templates/us/06_position_track.md` |

## CLI Mapping

```bash
python scripts/run_workflow.py --symbol US.NVDA --mode scan
python scripts/run_workflow.py --symbol US.NVDA --mode deep_dive
python scripts/run_workflow.py --symbol US.NVDA --mode position_review --cost-basis 120
python scripts/run_workflow.py --mode watchlist
```

## Daily Automation

The scheduled workflow is limited to `scan`. It is meant to create deterministic first-pass reports for a fixed basket, not to replace deep-dive research.

## Non-goals

This repo does not currently automate:
- macro data synthesis
- fundamental data synthesis
- final trade sizing
- autonomous trade execution

Those gaps are intentional and must remain explicit in docs and reports.
