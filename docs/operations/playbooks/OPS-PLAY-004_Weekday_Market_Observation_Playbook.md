# OPS-PLAY-004 — Weekday Market Observation Playbook

**Status:** CANDIDATE — OPERATIONAL REVIEW REQUIRED

## Purpose

Preserve genuine weekday regular-session and post-close provider behavior under verified market-state conditions.

## Preconditions

- correct branch and worktree active;
- Market Session Guard passes;
- system and market clocks available;
- credentials protected;
- observation report available;
- no unrelated uncommitted changes.

## Required evidence

Observation ID, symbol, local/UTC/market timestamps, session state and validity, provider, raw and normalized responses, provider timestamps, limitations, unknowns, and comparison notes.

## Regular-session procedure

1. Require `REGULAR_SESSION`, `valid: true`, and successful guard exit.
2. Execute the request.
3. Preserve all evidence.
4. Repeat later in the same session with a new observation ID.
5. Compare without forcing agreement.

## Post-close procedure

1. Require `POST_CLOSE` and `valid: true`.
2. Execute a new request.
3. Preserve all evidence.
4. Do not label the result after-hours without explicit provider support.
5. Compare with regular-session observations.

## Closure criteria

Proceed to review only when two genuine regular-session observations and one genuine post-close request exist, session classifications are valid, regressions pass, differences remain visible, and limitations are stated.
