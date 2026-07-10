# LabPal Finance

Evidence-earned release-candidate schemas, semantic guardrails, runtime harness, and working prototypes for LabPal Finance.

LabPal helps preserve market thoughts before hindsight changes the story. It is a research, decision-journaling, evidence-preservation, and self-audit tool — not a signal engine or broker.

## Repository layout

```
├── README.md
├── requirements.txt
├── docs/                    # PRD, test protocols
├── schemas/                 # Position, Claim, Event JSON schemas
├── fixtures/                # Valid fixtures + failure fixtures
├── guardrails/              # Semantic guardrail rules + fixtures
├── runtime/                 # B6 minimal runtime harness
├── reports/                 # B2–B6 validation reports
├── prototypes/              # UI workflow prototypes
└── archive/                 # Legacy trees, zips, derived artifacts
```

## Runtime principles (preserved)

- Position ≠ Trade
- Profit ≠ Proof
- Fact ≠ Interpretation
- UNKNOWN is a valid state
- Selection does not equal verification
- Human acceptance does not equal verification
- Reviews and revisions are append-only
- Material contradictions must remain visible

## Run the B6 harness

From the repository root:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python runtime/labpal_rc_harness.py
```

Expected result: `status: PASS` with schema validation, semantic guardrails, and Current Understanding derivation for `CTX-RC-READINESS`.

## Open the prototype

```bash
open prototypes/FI-PROT-001/index.html
```

## Current milestone

- **FI-REP-001-RC1** — repository structural correction
- **FI-PROT-001-T1** — Founder Quick Capture Test (see `docs/FI-PROT-001-T1_Founder_Quick_Capture_Test.md`)

## Explicit exclusions (this repo)

No live market data, entry zones, broker execution, autonomous recommendations, or composite profitability scores.
