# PU-MVP-001 — LabPal Finance Portfolio Understanding MVP

Status: Ready for repository review
Depends on: DOC-ALIGN-001

## Objective

Connect one real portfolio in read-only mode and produce evidence-linked Portfolio and Holding Understandings that improve one investor's clarity.

## Initial user

The founder using real Trading 212 and IBKR holdings.

## Included

- multiple broker accounts;
- read-only acquisition;
- canonical portfolio normalization;
- holdings, cash, currencies, values, weights, entry, results, income, and contribution;
- Portfolio Understanding;
- Holding Understanding;
- evidence provenance;
- unknowns and limitations;
- plain-language review states;
- versioned understanding snapshots; and
- deterministic validation.

## Excluded initially

- trade execution;
- autonomous buy or sell instructions;
- portfolio optimization;
- tax filing;
- social features;
- public screening;
- full Knowledge Heritage;
- invented missing data; and
- opaque score-only conclusions.

## Screens

### Connect Portfolio

Broker, access mode, permissions, last refresh, coverage, provenance, and limitations.

### Portfolio Understanding Home

- current explanation;
- valuation period and currency;
- positive and negative contributors;
- allocation and weight explanation;
- income explanation;
- positions requiring attention;
- latest understanding changes; and
- evidence freshness.

### Holding Understanding

- factual holding data;
- Current Understanding;
- Why This Understanding?;
- Evidence;
- What Changed?;
- Bullish Developments;
- Bearish Developments;
- Portfolio Impact;
- Unknowns;
- What to Review Next?; and
- Evidence Required.

### Understanding Alert Detail

Affected component, previous and current versions, evidence delta, why it matters, unknowns, and review direction.

### Understanding History

Immutable version events linked to evidence and reasoning changes.

## Canonical entities

### PortfolioSource

`id`, `provider`, `account_id`, `access_mode`, `base_currency`, `connected_at`, `refreshed_at`, `coverage`, `provenance`, `limitations`

### Portfolio

`id`, `owner_id`, `valuation_currency`, `source_ids`, `accounts`, `holdings`, `cash_balances`, `snapshot_at`, `data_quality`, `unknowns`

### Holding

`id`, `instrument_id`, `source_positions`, `quantity`, `average_entry`, `market_value`, `portfolio_weight`, `realized_result`, `unrealized_result`, `income_received`, `first_owned_at`, `currencies`, `provenance`, `unknowns`

### EvidenceRecord

`id`, `subject_id`, `source_type`, `source_identity`, `observed_at`, `effective_at`, `retrieved_at`, `content_hash`, `facts`, `provenance`, `quality`, `limitations`

### Understanding

`id`, `subject_id`, `subject_type`, `component`, `version`, `as_of`, `claims`, `supporting_evidence_ids`, `contradicting_evidence_ids`, `reasoning`, `justification`, `unknowns`, `limitations`, `internal_state`, `user_state`, `previous_version_id`

### UnderstandingChange

`id`, `subject_id`, `component`, `previous_understanding_id`, `current_understanding_id`, `severity`, `change_summary`, `why_it_matters`, `evidence_added`, `evidence_removed`, `contradictions`, `unknowns`, `review_direction`, `detected_at`

## Logical API capabilities

Exact routes must follow existing repository conventions.

- register a read-only portfolio source;
- refresh a source;
- fetch consolidated portfolio snapshot;
- fetch Portfolio Understanding;
- list holdings;
- fetch Holding Understanding;
- fetch Understanding Changes;
- fetch Understanding History; and
- inspect evidence.

## First vertical slice

```text
Connect source
  ↓
Preserve raw provenance
  ↓
Normalize canonical portfolio
  ↓
Validate totals, currency, identity, and timestamps
  ↓
Expose holdings and portfolio snapshot
  ↓
Surface missing data as unknown
  ↓
Run deterministic fixture verification
```

## Vertical Slice 1 acceptance criteria

1. One real or faithfully exported portfolio source is represented read-only.
2. Source provenance is preserved.
3. Normalized totals reproduce source totals within declared tolerances.
4. Quantity, value, weight, currency, and timestamp are explicit.
5. Missing source fields become unknowns and are never fabricated.
6. A deterministic fixture produces the same normalized output.
7. No execution permissions are requested.
8. Output follows existing validation and Live Understanding contracts.
9. README and roadmap reflect the implemented reality.

## Usefulness test

After the first Portfolio Understanding is rendered, the founder should be able to answer:

- What moved my portfolio?
- Which holdings mattered most and why?
- What changed since the last review?
- What evidence supports the explanation?
- What remains uncertain?
- What deserves attention next?

Rendering alone is not success. Improved clarity and factual accuracy are success.
