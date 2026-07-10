# LabPal Finance — Position Object v0.1-RC

This package contains the first evidence-earned release-candidate definition for the LabPal Finance Position Object.

## Included

- `position-object-v0.1-rc.schema.json`
- `fixtures/pc-001-xagusd-discrete.fixture.json`
- `fixtures/pc-004-standing-dca.fixture.json`
- `rc-validation-notes.md`

## Core responsibilities

1. Identity
2. Decision Purpose
3. Reasoning + Evidence
4. Governing Rules
5. Observation + Review

## P12 blockers encoded

- `continuity_type` must distinguish `DISCRETE` and `STANDING`.
- Material assertions must preserve scoped `SUPPORTED` or `UNKNOWN` truth positions.
- Every `SUPPORTED` assertion must include `evidence_basis` and `source_reference`.

## Explicit exclusions from v0.1-RC

- Numeric confidence
- Reentry trigger
- Structured counterfactual analysis
- Universal Same/New/Related classification
- SUSPENDED lifecycle state
- Understanding Revision
- Full Transition Passport
- Object-level `CONFIRMED` or completeness scores

This RC is not verified software and is not canonical LPOS architecture. It is the smallest currently evidence-earned schema candidate for runtime testing.
