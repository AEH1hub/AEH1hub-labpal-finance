# OPS-PLAY-003 — Weekend Observation Playbook

**Status:** CANDIDATE — OPERATIONAL REVIEW REQUIRED

## Purpose

Observe and preserve provider behavior when the relevant market is closed for the weekend.

## Scope

Weekend evidence does not prove weekday, regular-session, post-close, or after-hours behavior.

## Procedure

1. Run the Market Session Guard.
2. Confirm a weekend-closed state.
3. Execute the provider request.
4. Preserve raw and normalized responses.
5. Record local, UTC, market-timezone, and provider timestamps.
6. Label returned data as current, stale, historical, unknown, or not applicable.
7. Do not call data after-hours unless the provider explicitly does so.
8. Preserve errors, empty responses, limitations, and unknowns.
9. Explain what the observation proves and does not prove.

## Rejection criteria

Reject or revise when the session state is wrong, timestamps are incorrect, weekend evidence is generalized to weekday validity, stale data is mislabeled, or provider errors are hidden.
