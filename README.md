# Swing Trade Workflow by Jincredible

> US swing-trade research workflow with explicit `scan`, `deep_dive`, and `position_review` modes.

## What This Repo Does

This repo is a structured research system for US swing trades. It keeps the richer workflow as the source of truth, but it is explicit about what is automated locally and what still needs manual or external-skill input.

Core method:

```text
Fundamental inflection + technical timing + capital / derivatives confirmation
```

## Operating Modes

| Mode | Purpose | Local automation | Output |
|------|---------|------------------|--------|
| `scan` | Fast triage of a symbol | Snapshot, price history, technical, capital, derivatives, news | Pass / watch / reject style scan report |
| `deep_dive` | Pre-trade research draft | Same automated sections as `scan` plus structured placeholders for macro, fundamentals, and trade plan | Incomplete or ready-for-manual-decision research report |
| `position_review` | Post-entry monitoring | Same automated sections as `scan` plus position context | Hold / add / reduce / exit review draft |
| `watchlist` | Queue template | Template only | Markdown watchlist |

## Automation Boundaries

### Automated locally
- Quote snapshot and daily price history via Futu scripts
- Technical anomaly signals
- Capital anomaly signals
- Derivatives anomaly signals
- Recent news collection

### Expected from manual or external-skill input
- Macro regime summary
- Fundamental summary
- Full trade-plan sizing and catalyst calendar
- Final investment decision

### Advisory templates only
- Watchlist management
- Detailed deep-dive writeups
- Position-review journaling

## CLI

```bash
# Fast scan
python scripts/run_workflow.py --symbol US.INTC --mode scan --output ./reports

# Deep-dive draft with pending macro/fundamental sections
python scripts/run_workflow.py --symbol US.INTC --mode deep_dive --output ./reports

# Deep-dive draft with manual summaries filled in
python scripts/run_workflow.py \
  --symbol US.INTC \
  --mode deep_dive \
  --macro-summary "Rates stable, QQQ trend constructive, semis still leading." \
  --fundamental-summary "Revenue acceleration and guidance improvement remain intact." \
  --review-date 2026-05-09 \
  --output ./reports

# Position review
python scripts/run_workflow.py \
  --symbol US.INTC \
  --mode position_review \
  --cost-basis 81.5 \
  --entry-price 79.0 \
  --position-size "6% account" \
  --review-date 2026-05-09 \
  --thesis "Post-earnings continuation with options support." \
  --output ./reports

# Watchlist template
python scripts/run_workflow.py --mode watchlist --output ./reports
```

## Report Contract

Every generated report now includes:

- `symbol`
- `mode`
- `generated_at`
- `as_of`
- `completeness`
- `sources_used`
- `final_action`

Deep-dive reports explicitly show when macro or fundamental inputs are still pending.

## Project Structure

```text
swing-trade-workflow/
├── README.md
├── WORKFLOW.md
├── WORKFLOW_US.md
├── templates/
├── scripts/
├── reports/
├── output/
└── .github/workflows/
```

## Scheduled Scan

The scheduled GitHub workflow now runs the supported `scan` path instead of a placeholder no-op. It is a deterministic basket scan, not a full deep-dive engine.

## Example Output States

- `scan_complete`: automation gathered the expected scan inputs
- `watch`: scan completed with missing sources or mixed evidence
- `incomplete`: deep-dive report still needs manual or external-skill input
- `ready_for_manual_decision`: deep-dive sections are populated and ready for final human judgment
- `review_required`: position review draft generated and waiting on manual decision

## Disclaimer

This repo generates research artifacts and decision support. It does not place trades or make autonomous trading decisions.
