# PU-INGEST-001B — Deterministic Portfolio Source Parser

**Status:** Verified merge candidate
**Depends on:** PU-INGEST-001A, SEC-BASE-001, PU-VALIDATE-001A

## Purpose

Prove that one named, bounded, synthetic source format can become LabPal's
canonical `PortfolioSnapshot` without changing financial meaning, losing
provenance, fabricating missing information, or expanding system authority.

## Accepted source

The first source is `LABPAL_NEUTRAL_CSV`. It is a UTF-8, read-only,
synthetic/redacted CSV with these columns:

- `row_type`
- `portfolio_id`
- `account_reference`
- `base_currency`
- `observed_at`
- `symbol`
- `name`
- `quantity`
- `market_value`
- `currency`
- `average_entry_price`

`row_type` is either `HOLDING` or `CASH`. Holding-only fields must be empty
for cash rows. All rows describe one portfolio at one timezone-aware
observation time.

## Deterministic normalization

- Decimal values are parsed without binary floating-point arithmetic.
- Identifiers derive from canonical source facts and stable row order.
- Holdings and cash balances are serialized through `portfolio_model.py`.
- Empty average-entry price becomes an explicit `SOURCE_FIELD_EMPTY`
  `Unknown`.
- Source filename, SHA-256 digest, import time, row count, source row number,
  and source field names remain available as provenance.
- Equivalent input and an identical explicit import time produce identical
  parser output.
- The original source hash is checked again after parsing.

## Failure boundary

The parser fails closed for missing or unexpected columns, duplicate columns,
duplicate rows, duplicate holdings, malformed decimals, negative holding
values, timezone-naive timestamps, inconsistent portfolio metadata,
formula-like text, oversized inputs, and unsupported row types.

The current canonical contract contains one base-currency total and no
FX-evidence object. Mixed-currency input is therefore rejected. LabPal does
not silently convert or discard those values.

## Authority boundary

This milestone does not connect to a broker, retain real portfolio files,
retrieve prices, recommend transactions, transmit orders, or execute
transactions. Fixtures are synthetic and account references are redacted.

## Definition of done

- the neutral source parses into a schema-valid canonical snapshot;
- expected fixture parity passes;
- deterministic output passes;
- row and field provenance passes;
- source non-mutation passes;
- malformed-input adversarial cases pass;
- security verification passes;
- complete repository verification passes.
