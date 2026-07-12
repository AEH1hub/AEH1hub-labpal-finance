# REG-EVID-001 — Evidence Registry Specification

**Status:** CANDIDATE — FOUNDATION REVIEW REQUIRED
**Depends on:** FI-FOUND-001, FI-FOUND-002, GOV-001, GOV-002

## Purpose

The Evidence Registry provides permanent identity, provenance, state and relationships for evidence preserved by LabPal.

Filenames may locate artifacts.

They must not be the only identity of evidence.

## Evidence identity

Every registered item must receive a permanent identifier.

Example:

`EV-MARKET-000001`

An identifier must not be reused after retirement, invalidation or deletion of a derivative artifact.

## Required fields

Every evidence record must contain:

- `evidence_id`;
- `evidence_type`;
- `title`;
- `scope`;
- `observation`;
- `source_name`;
- `source_type`;
- `source_location`;
- `source_identifier`;
- `observed_at`;
- `retrieved_at`;
- `published_at`;
- `registered_at`;
- `registered_by`;
- `content_hash`;
- `artifact_location`;
- `validation_state`;
- `review_state`;
- `freshness_state`;
- `is_mock`;
- `mock_label`;
- `unknowns`;
- `limitations`;
- `related_claim_ids`;
- `related_unknown_ids`;
- `related_understanding_ids`;
- `supersedes`;
- `superseded_by`;
- `history`.

Unknown timestamps must remain unknown.

They must not be synthesized.

## Evidence states

### Validation state

- `UNVALIDATED`
- `STRUCTURE_VALIDATED`
- `SEMANTICALLY_VALIDATED`
- `INVALID`
- `VALIDATION_UNRESOLVED`

### Review state

- `NOT_REVIEWED`
- `REVIEWED`
- `CHALLENGED`
- `REJECTED_FOR_SCOPE`
- `ACCEPTED_FOR_SCOPE`

### Freshness state

- `CURRENT`
- `STALE`
- `HISTORICAL`
- `FRESHNESS_UNKNOWN`
- `NOT_APPLICABLE`

Acceptance for one scope does not make evidence valid for every scope.

## Evidence relationships

Evidence may:

- support a claim;
- challenge a claim;
- contradict another evidence record;
- duplicate another record;
- supersede a derivative record;
- resolve an unknown;
- create a new unknown;
- contribute to a Current Understanding.

Relationships must state their reason.

## Source preservation

LabPal must preserve enough source information to allow later review without exposing secrets.

Credentials, API keys and private tokens must never be stored in evidence provenance.

## Mock evidence

Mock evidence must be explicitly labeled.

Mock evidence may validate structure and workflow.

Mock evidence may not be represented as proof of current external reality.

## Contradiction rule

Contradictory evidence must remain visible.

LabPal must not:

- average disagreement automatically;
- select a preferred source silently;
- delete an inconvenient record;
- treat provider agreement as proof of validity.

## Mutation rule

Primary evidence must not be rewritten.

Corrections to metadata or interpretation must create a preserved correction or revision record.

## Registration rule

Registration means:

> This evidence has been preserved and identified.

Registration does not mean:

> This evidence is true, sufficient or verified.
