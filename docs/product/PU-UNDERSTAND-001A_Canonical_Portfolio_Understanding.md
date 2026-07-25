# PU-UNDERSTAND-001A — Canonical Portfolio Understanding

**Status:** Implementation candidate
**Depends on:** PU-INGEST-001A, PU-INGEST-001B, PU-VALIDATE-001A, SEC-BASE-001
**Data authority:** Synthetic and redacted only

## Purpose

Transform one valid canonical `PortfolioSnapshot` into a deterministic,
browser-ready Portfolio Understanding without redefining the source facts,
inventing explanations, judging diversification, recommending investments, or
gaining execution authority.

## Understanding boundary

The output describes the current state of one snapshot:

- portfolio identity, observation time, total value, holdings, and cash;
- exact holding weights and canonical unknowns;
- factual statements linked to canonical evidence references;
- source identity and provenance;
- limitations, missing evidence, and human review-next actions.

It does not compare periods, retrieve live evidence, explain why market values
exist or changed, assess diversification, approve an investment decision,
recommend a transaction, or execute a transaction.

## Review state

`READY_FOR_REVIEW` means only that a deterministic factual single-snapshot
understanding is ready for human review. It does not mean the portfolio is
approved, suitable, diversified, or that any investment decision is approved.

## Deterministic transformation

- Input must validate against `portfolio-snapshot.v0.1-pu.schema.json`.
- Holdings and cash must reconcile exactly to canonical total value.
- Decimal strings, weights, timestamps, unknowns, and source provenance remain
  unchanged in meaning.
- Holdings and balances use stable identifier ordering.
- Every factual statement carries at least one canonical evidence reference.
- The same valid input produces the same JSON object.
- Malformed, incomplete, inconsistent, or unreconciled canonical input fails
  closed without a partial understanding.

## Authority boundary

The output permanently exposes `recommendations_prohibited: true` and
`execution_prohibited: true`. Holding-value causes remain explicitly unknown
until separate evidence exists. The milestone introduces no broker connection,
portfolio file retention, live data, recommendation, order, or execution path.

## Browser handoff

The next read-only browser milestone may render this JSON directly. It must not
rename review states, reinterpret unknowns as conclusions, transform evidence
requirements into claims, or infer recommendations from composition.

## Definition of done

- the neutral synthetic snapshot produces the expected understanding fixture;
- CHF 246.40 total value, two holdings, and CHF 12.50 cash are preserved;
- MAIN and VUAG weights remain exact;
- MAIN average entry price remains unknown;
- all factual statements remain evidence-linked;
- source provenance and synthetic/redacted limitations remain visible;
- holding-value causes and diversification conclusions are not invented;
- recommendation and execution capability remain prohibited;
- output is deterministic and schema-valid;
- malformed canonical input fails closed;
- focused, security, and repository verification gates pass.
