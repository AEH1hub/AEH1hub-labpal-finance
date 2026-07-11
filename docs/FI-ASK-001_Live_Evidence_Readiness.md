# FI-ASK-001 — Live Evidence Readiness

**Milestone:** FI-ASK-001 — Research Question Object + Live Evidence Adapter Interface
**Status:** Interface and fixtures built. Live analysis not yet connected.

## What live analysis means (in LabPal)

Live analysis means LabPal can **gather available sources**, **timestamp them**, **separate facts from interpretations**, **surface unknowns**, and **preserve action boundaries** — like a disciplined human researcher.

Live analysis is **sourced research support**. It is not a recommendation engine.

## What live analysis does not mean

- Personalized buy/sell recommendations
- Stock rankings or “best stock” lists
- Entry zones or price targets
- Broker execution
- Composite profitability scores
- Fabricated current market answers when sources are not connected

## Research Question Object

The Research Question Object (`schemas/research-question-object.v0.1-ask.schema.json`) captures:

- The original question (preserved verbatim)
- Question type and horizon
- Evidence connection state and evidence mode
- Action boundary state
- Required sources, evidence records, and classified claims
- Unknowns, stale evidence warnings, and safe next actions

Purpose: move from **question → structured understanding** with provenance intact.

## Live Evidence Record

Each evidence record (`schemas/live-evidence-record.v0.1-ask.schema.json`) must include:

- Source name, URL, type, retrieved/published timestamps
- Freshness state
- Claim text and classification
- Source quote/summary and LabPal notes
- Unknowns and reliability notes

**Recording a source does not mean LabPal endorses the claim.**

## Evidence adapter interface

`runtime/evidence_adapter_interface.py` defines future adapter slots:

| Adapter | Purpose |
|---------|---------|
| `market_price_adapter` | Prices / index levels (timestamped) |
| `news_adapter` | Dated news catalysts |
| `filings_or_factsheet_adapter` | Filings, fund factsheets |
| `rates_yields_adapter` | Rates and yields context |
| `sector_breadth_adapter` | Sector breadth / leadership |

**Current status:** mock output only, labeled `MOCK_EVIDENCE — NOT LIVE DATA`. No real APIs called.

## Claim classification

| Class | Meaning |
|-------|---------|
| `SOURCE_FACT` | Directly supported by a cited source |
| `SOURCE_INTERPRETATION` | Source’s framing or analysis |
| `LABPAL_INTERPRETATION` | LabPal-organized reading — not proof |
| `USER_STATEMENT` | User’s own words |
| `UNKNOWN` | Not yet classified |

Facts, source interpretations, and LabPal interpretations **must remain separate**.

## Freshness and stale evidence

| State | Policy |
|-------|--------|
| `CURRENT` | Within defined freshness window for the source type |
| `RECENT` | Usable with caution; show age |
| `STALE` | Visible warning; do not treat as current truth |
| `UNKNOWN_FRESHNESS` | Freshness not established — show as unknown |

Stale or unknown freshness must remain **visible** in the Research Question Object.

## Action-boundary policy

| State | Meaning |
|-------|---------|
| `RESEARCH_ONLY` | No action language detected |
| `ACTION_LANGUAGE_DETECTED` | Invest/buy framing — structure research only |
| `RECOMMENDATION_RISK` | Question implies picks/rankings — blocked |
| `BLOCKED_FOR_REVIEW` | Entry-zone/timing — future gated |

Entry zones are **future gated**. No price levels without sourced evidence, risk boundary, and review.

## Harness

```bash
.venv/bin/python runtime/research_question_harness.py
```

Validates fixtures and enforces: no recommendations, no entry prices, no fabricated live market status, mock evidence clearly labeled.

## Next milestone

**FI-ASK-002 — Real Evidence Source Adapter**

Select and connect real sources (market prices, news, filings/factsheets, rates/yields, sector breadth) with timestamping, freshness policy, and action-boundary enforcement.
