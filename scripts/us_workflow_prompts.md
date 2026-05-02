# US Workflow Prompt Pack

Use these prompts when you want outputs that match the repo's three operating modes.

## Template A: `scan`

Purpose: quick triage only.

```text
Please run a scan-style review for US.XXX.

Required sections:
1. Snapshot
2. Price history
3. Technical signals
4. Capital signals
5. Derivatives signals
6. Recent news

Output rules:
- Final state must be one of: pass / watch / reject
- Do not write a full thesis
- If any source is missing, say "data unavailable from local automation"
- Use the quick-scan structure from templates/us/07_quick_scan.md
```

## Template B: `deep_dive`

Purpose: full research draft with explicit pending fields.

```text
Please prepare a deep-dive draft for US.XXX using the repo's deep_dive mode.

Required sections:
1. Macro summary
2. Fundamental summary
3. Snapshot
4. Price history
5. Technical signals
6. Capital-flow confirmation
7. Derivatives confirmation
8. Recent news
9. Trade plan draft
10. Risk calendar
11. Final decision state

Output rules:
- If macro or fundamentals are missing, mark them as pending manual or external-skill input
- Do not claim the report is complete unless those sections are filled
- Keep the result aligned to the repo's completeness flags
```

## Template C: `position_review`

Purpose: review an existing position.

```text
I hold US.XXX.

Position context:
- Cost basis: $XX
- Entry price: $XX
- Position size: ___
- Review date: YYYY-MM-DD
- Original thesis: ___

Required sections:
1. Position context
2. Thesis status
3. Technical health
4. Capital-flow health
5. Derivatives health
6. News and catalysts
7. Risk calendar
8. Hold / add / reduce / exit review

Output rules:
- Treat this as a review draft, not an execution instruction
- If any data source is missing, disclose it explicitly
- Focus on whether the original thesis is intact, weakened, or broken
```

## Template D: external-skill augmentation

Purpose: fill the deep-dive sections that local automation does not complete.

```text
For US.XXX, provide only the sections that local automation leaves incomplete:

1. Macro regime summary
2. Fundamental summary
3. Catalyst calendar
4. Trade-plan completion inputs

Output rules:
- Use concise research language
- State assumptions clearly
- Do not rewrite the automated sections
```
