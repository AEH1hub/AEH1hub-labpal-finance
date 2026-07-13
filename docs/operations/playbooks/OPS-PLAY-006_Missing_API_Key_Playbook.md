# OPS-PLAY-006 — Missing API Key Playbook

**Status:** CANDIDATE — OPERATIONAL REVIEW REQUIRED

## Purpose

Validate and handle missing provider credentials deterministically and safely.

## Procedure

1. Confirm the expected environment-variable name.
2. Isolate or remove it for the test process only.
3. Run the missing-key harness.
4. Require deterministic, explicit failure.
5. Confirm no network request occurred when authentication was required first.
6. Confirm no mock fallback and no secret exposure.
7. Preserve the result.

## Rejection criteria

Reject when the test mutates stored credentials, depends on uncontrolled global state, continues as authenticated, represents fallback data as provider evidence, or exposes secrets.
