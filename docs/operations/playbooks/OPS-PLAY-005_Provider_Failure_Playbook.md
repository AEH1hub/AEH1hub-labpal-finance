# OPS-PLAY-005 — Provider Failure Playbook

**Status:** CANDIDATE — OPERATIONAL REVIEW REQUIRED

## Purpose

Handle provider failures without fabricating success, hiding evidence, or silently substituting another source.

## Failure classes

Missing credential, invalid credential, transport failure, timeout, malformed response, provider error, invalid identifier, rate limit, stale response, missing timestamp, schema change, and unknown failure.

## Procedure

1. Preserve the failure state and safe request metadata.
2. Never store credentials.
3. Record the failure class and provider response when safe.
4. Record bounded retry behavior.
5. Do not use silent mock fallback or silent provider switching.
6. Register material unknowns.
7. Decide retry, escalation, rejection, or deferred review.
8. Produce an explanation record.

## Rejection criteria

Reject when failure becomes fabricated data, mock evidence is unlabeled, the provider is silently replaced, retries are unbounded, original evidence is lost, or secrets appear in output.
