# PU-VALIDATE-001A — Synthetic Founder Usefulness Validation

**Status:** Active
**Depends on:** PU-INGEST-001A and SEC-BASE-001
**Data authority:** Synthetic and redacted only

## Objective

Determine whether LabPal's canonical portfolio contract can produce a useful,
evidence-disciplined explanation of portfolio change before implementing a real
broker source parser.

## Founder questions

The validation must help the founder answer:

1. What moved the portfolio?
2. Which holdings mattered most?
3. What changed since the previous snapshot?
4. Which facts support the explanation?
5. Which causal explanations remain unsupported?
6. What remains unknown?
7. What deserves review next?

## Validation boundary

This milestone uses only synthetic and redacted portfolio snapshots.

It must not:

- process a real portfolio export;
- connect to a broker;
- retrieve live prices;
- execute or transmit trades;
- recommend buying or selling;
- fabricate reasons for market movements;
- represent calculated contribution as causal evidence;
- hide missing information.

## Required scenarios

### Scenario 1 — Positive and negative contributors

Two deterministic snapshots must show:

- one positive holding contribution;
- one negative holding contribution;
- an explicit total portfolio change;
- deterministic contributor ranking.

### Scenario 2 — Insufficient causal evidence

LabPal may calculate which holding changed most, but it must not claim why the
holding changed without supporting evidence.

The causal explanation must remain explicitly unknown.

### Scenario 3 — Preserved source unknown

A missing source value must remain represented as an Unknown and must not be
filled through inference.

## Required outputs

The validation report must include:

- before and after snapshot identity;
- total portfolio-value change;
- holding-level contributions;
- largest absolute contributor;
- supported factual statements;
- unsupported causal questions;
- explicit unknowns;
- review-next requirements;
- evidence limitations;
- recommendation and execution prohibition.

## Acceptance criteria

PU-VALIDATE-001A passes only when:

1. both snapshots satisfy the canonical portfolio contract;
2. totals reproduce the sum of holding and cash values;
3. contribution calculations are deterministic;
4. positive and negative contributors are classified correctly;
5. contributor ranking is deterministic;
6. facts are separated from causal interpretation;
7. unsupported causes remain unknown;
8. existing source unknowns remain preserved;
9. no recommendation or execution output exists;
10. repeated runs produce identical output;
11. a deterministic harness verifies every requirement;
12. the repository verification workflow invokes the new harness.

## Completion decision

This milestone does not prove production usefulness.

It proves only whether the synthetic canonical portfolio can produce an
honest, reviewable, and potentially useful Portfolio Understanding foundation.

Real founder testing requires separate approval after deterministic validation.
