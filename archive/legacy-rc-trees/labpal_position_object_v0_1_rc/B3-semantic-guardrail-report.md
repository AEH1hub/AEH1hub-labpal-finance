# FI-001A-RC-B3 — Semantic Guardrail Tests

## Purpose

B3 tests schema-valid objects that still violate LabPal's truth rules. JSON Schema passed in B2; B3 adds semantic guardrails.

## Results

| Fixture | Semantic result | Violations |
|---|---:|---|
| `pc-004-standing-dca.fixture.json` | PASS |  |
| `pc-001-xagusd-discrete.fixture.json` | PASS |  |
| `sg1-profit-as-proof.schema-valid.fixture.json` | FAIL | SG-001: Positive outcome used as proof of decision quality. |
| `sg2-delta-as-transaction.schema-valid.fixture.json` | FAIL | SG-002: Checkpoint delta/contextual linkage promoted into transaction event. |
| `sg3-ai-claim-as-supported.schema-valid.fixture.json` | FAIL | SG-003: AI-only analysis used as sole support for appropriateness judgment. |
| `sg4-derived-purpose-as-supported.schema-valid.fixture.json` | FAIL | SG-004: Derived context labeled as supported historical purpose. |

## Good news

- The valid DISCRETE and STANDING fixtures pass the first semantic guardrails.
- The guardrails catch profit-as-proof, checkpoint-delta-as-transaction, AI-as-sole-confirmation, and derived-context-as-historical wording.

## Bad news / risk

- These guardrails are simple pattern checks, not a full reasoning engine.
- Semantic safety cannot be solved by schema alone.
- Future runtime tests must evaluate AI-origin events, review events, and contradiction visibility.

## Unresolved reality

- Direct source conflict is still untested.
- Broker statement ingestion is still untested.
- Human review workflows are still unimplemented.

## B3 Verdict

**PASS AS FIRST SEMANTIC GUARDRAIL LAYER.** The RC package can now distinguish schema validity from semantic validity.

## Next required milestone

**FI-001A-RC-B4 — Event Model & Append-Only Provenance Skeleton.** Create the minimum JSON definitions for OriginEvent, ReviewEvent, VerificationEvent, SelectionEvent, and ClaimRelationship so AI-origin and human-review behavior can be tested directly.
