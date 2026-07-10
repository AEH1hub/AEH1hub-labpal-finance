# FI-001A-RC-B4 — Event Model & Append-Only Provenance Skeleton

## Purpose

Define the minimum event model needed to preserve origin, review, verification, selection, and claim relationships without overwriting history.

## Included event types

- ORIGIN_EVENT
- REVIEW_EVENT
- VERIFICATION_EVENT
- SELECTION_EVENT
- CLAIM_RELATIONSHIP_EVENT

## Validation results

| Item | Type | Expected result met | Errors |
|---|---|---:|---|
| `CLM-B4-A` | Claim | ✅ |  |
| `CLM-B4-B` | Claim | ✅ |  |
| `EVT-B4-001` | ORIGIN_EVENT | ✅ |  |
| `EVT-B4-002` | REVIEW_EVENT | ✅ |  |
| `EVT-B4-003` | VERIFICATION_EVENT | ✅ |  |
| `EVT-B4-004` | VERIFICATION_EVENT | ✅ |  |
| `EVT-B4-005` | ORIGIN_EVENT | ✅ |  |
| `EVT-B4-006` | CLAIM_RELATIONSHIP_EVENT | ✅ |  |
| `EVT-B4-007` | SELECTION_EVENT | ✅ |  |
| `fail-claim-with-stored-review-state.json` | Failure fixture | ✅ | {'claim_id': 'CLM-B4-A', 'claim_text': 'The five-layer Position Object appears sufficient for MVP implementation.', 'assertion_type': 'SYNTHETIC_INFERENCE', 'created_at': None, 'source_claim_id': None, 'review_state': 'ACCEPTED'} should not be valid under {'anyOf': [{'required': ['review_state']}, {'required': ['verification_state']}, {'required': ['confidence']}, {'required': ['confirmed']}]}; Additional properties are not allowed ('review_state' was unexpected) |
| `fail-event-not-append-only.json` | Failure fixture | ✅ | True was expected |
| `fail-review-action-modify.json` | Failure fixture | ✅ | 'MODIFY' is not one of ['ACCEPT', 'REJECT', 'REQUEST_CLARIFICATION', 'NO_POSITION'] |

## Good news

- Claims do not store review or verification status as source truth.
- AI origin survives human acceptance.
- Review, verification, selection, and relationship events are append-only.
- `MODIFY` is rejected as a review action; semantic modification must create a new claim.

## Bad news / risk

- This is still a skeleton; it does not yet derive Current Understanding automatically.
- Contradiction firewall behavior is represented but not enforced by runtime.
- Selection provenance can still be biased if candidate-set construction is opaque.

## Unresolved reality

- Need Current Understanding derivation rules.
- Need runtime test for contradiction visibility.
- Need candidate-set construction audit rule.

## B4 Verdict

**PASS AS EVENT SKELETON.** The minimum append-only event model is now encoded and validated.

## Next required milestone

**FI-001A-RC-B5 — Current Understanding Derivation Test.** Use claims + events to compute a human-readable current view without voting, averaging, overwriting, or hiding contradictions.
