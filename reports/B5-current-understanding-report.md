# FI-001A-RC-B5 — Current Understanding Derivation Test

## Purpose

B5 tests whether LabPal can derive a useful Current Understanding from claims and append-only events without voting, averaging, overwriting history, or hiding contradiction.

## Input

- Claim A: "The five-layer Position Object appears sufficient for MVP implementation."
- Claim B: "The five-responsibility Decision Object core survives, but implementation semantics require continuity-type specialization."
- Origin events
- Review event
- Verification events
- Claim relationship event
- Selection event

## Derived result

The current working interpretation is Claim B, but Claim B is not globally verified or canonical.

The derived Current Understanding must show:

- Claim A remains preserved.
- Claim A was accepted by Amadou as a working observation.
- Claim A is supported in historical thin-object preservation scope.
- Claim A is challenged in cross-continuity-type sufficiency scope.
- Claim B is a proposed revision of Claim A.
- Claim B is selected for RC-readiness context.
- Selection does not equal verification.

## Good news

- Current Understanding can be derived without storing review_state or verification_state on the claim.
- Claim A is preserved rather than overwritten.
- Scope-sensitive support/challenge survives.
- The model produces a useful conclusion without fake consensus.

## Bad news / risk

- The derivation logic is still a simple prototype.
- Selection of Claim B relies on policy logic that must remain inspectable.
- No runtime UI has yet proven that users understand this distinction.

## Unresolved reality

- Claim B still needs runtime testing.
- Contradiction firewall enforcement is not yet implemented as product behavior.
- Supersession semantics remain untested because no claim has earned SUPERSEDES.

## B5 Verdict

**PASS AS DERIVATION PROTOTYPE.**

B5 proves that the append-only event skeleton can produce a scoped Current Understanding view without overwriting prior claims or turning review into verification.

## Next required milestone

**FI-001A-RC-B6 — Minimal Runtime Harness.**

Build a tiny script or test harness that validates schema, runs semantic guardrails, loads claims/events, and emits Current Understanding from fixtures.
