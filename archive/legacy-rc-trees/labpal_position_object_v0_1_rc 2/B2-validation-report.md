# FI-001A-RC-B2 — Schema Validation & Failure Fixtures
## Purpose
Validate that Position Object v0.1-RC accepts the two earned fixtures and rejects known anti-patterns: unsupported confidence, missing provenance, broad CONFIRMED labels, unearned continuity types, and unearned assertion states.
## Results
| Fixture | Expected | Actual | Result | Key error |
|---|---:|---:|---:|---|
| `pc-001-xagusd-discrete.fixture.json` | PASS | PASS | ✅ |  |
| `pc-004-standing-dca.fixture.json` | PASS | PASS | ✅ |  |
| `fail-supported-without-source.fixture.json` | FAIL | FAIL | ✅ | 'source_reference' is a required property |
| `fail-supported-without-evidence-basis.fixture.json` | FAIL | FAIL | ✅ | 'evidence_basis' is a required property |
| `fail-unknown-without-unknown-reason.fixture.json` | FAIL | FAIL | ✅ | 'unknown_reason' is a required property |
| `fail-unsupported-continuity-type.fixture.json` | FAIL | FAIL | ✅ | 'HYBRID' is not one of ['DISCRETE', 'STANDING'] |
| `fail-numeric-confidence.fixture.json` | FAIL | FAIL | ✅ | Additional properties are not allowed ('numeric_confidence' was unexpected) |
| `fail-object-level-confirmed.fixture.json` | FAIL | FAIL | ✅ | Additional properties are not allowed ('object_certainty' was unexpected) |
| `fail-parked-conflicted-state.fixture.json` | FAIL | FAIL | ✅ | 'CONFLICTED' is not one of ['SUPPORTED', 'UNKNOWN'] |

## B2 Verdict

**PASS — the RC schema rejects the first set of certainty/provenance failure modes.**

## Good news

- Both valid fixtures pass.
- `SUPPORTED` assertions require provenance.
- `UNKNOWN` assertions require an unknown reason.
- Numeric confidence is rejected.
- Object-level `CONFIRMED` is rejected.
- `CONFLICTED` remains parked and cannot enter v0.1-RC yet.

## Bad news / risk

- Schema validation catches structure, not truth. A false claim with a source can still pass schema validation.
- Append-only event behavior is not enforced by this static schema.
- Runtime contradiction firewall is still untested.

## Unresolved reality

- We need semantic validation beyond JSON Schema.
- We need runtime tests for AI-origin, review events, and contradiction visibility.
- We need fixtures for direct source conflicts once real conflict evidence exists.

## Next required milestone

**FI-001A-RC-B3 — Semantic Guardrail Tests**

Test rules that JSON Schema alone cannot enforce:
1. A `SUPPORTED` assertion must not be treated as complete object truth.
2. A fixture may not infer a transaction event from a checkpoint delta.
3. AI-originated claims must begin as unreviewed.
4. Contradictory evidence linked to active understanding must surface.
