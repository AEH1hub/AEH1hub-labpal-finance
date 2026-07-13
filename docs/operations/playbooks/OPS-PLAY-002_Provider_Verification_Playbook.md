# OPS-PLAY-002 — Provider Verification Playbook

**Status:** CANDIDATE — OPERATIONAL REVIEW REQUIRED

## Purpose

Determine whether an external provider can be used within a stated scope while preserving provenance, limitations, failure behavior, and disagreement.

## Scope

Applies to external data providers used by LabPal. It does not establish universal truth, provider superiority, investment suitability, or permanent reliability.

## Preconditions

- provider purpose documented;
- credentials stored outside the repository;
- expected response structure known;
- test identifiers defined;
- failure tests exist;
- mock and live paths separated.

## Required evidence

Provider name, retrieval timestamp, source identifier, raw artifact, normalized response, content hash where applicable, credential state without secrets, transport result, invalid-input result, missing-key result, known limitations, and material unknowns.

## Procedure

1. Confirm scope.
2. Confirm credentials are protected.
3. Run deterministic normalization tests.
4. Run missing-key, invalid-identifier, and transport-failure tests.
5. Perform a live request when authorized.
6. Preserve raw and normalized evidence.
7. Record timestamps, contradictions, limitations, and unknowns.
8. Produce an explanation record.

## Approval criteria

Approve within scope only when provenance is preserved, tests pass, failure behavior is explicit, no silent mock fallback exists, secrets are protected, and limitations are documented.

## Rejection criteria

Reject or revise when provenance is missing, credentials are exposed, failures are silently converted into success, mock data is represented as live, timestamps are synthesized, or material contradictions are hidden.
