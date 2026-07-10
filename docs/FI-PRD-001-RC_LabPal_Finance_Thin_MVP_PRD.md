# FI-PRD-001-RC — LabPal Finance Thin MVP PRD

**Status:** RC draft aligned to FI-001A-RC-B6 evidence  
**Scope:** Thin MVP product behavior only — not full LPOS architecture

## Purpose

LabPal Finance helps people preserve market and investment thoughts before hindsight changes the story. The thin MVP must earn trust by preserving truth correctly before any optimization or recommendation surface is added.

## Proven behavior (B2–B6)

The release-candidate runtime demonstrates:

1. **Preserve claims and provenance** — append-only events; prior claims are not silently overwritten.
2. **Distinguish fact / interpretation / unknown** — scoped truth positions; UNKNOWN is valid.
3. **Review without overwriting** — structured review adds meaning; it does not rewrite history.
4. **Derive Current Understanding** — selection is visible; contradictions remain visible; selection ≠ verification.

## Thin MVP user flows (FI-PROT-001)

1. **Quick Capture** — instrument/subject, raw thought, optional evidence fragment, under 60 seconds.
2. **Structured Review** — continuity (DISCRETE / STANDING), evidence class, decision rule; AI-origin UNREVIEWED visible.
3. **Current Understanding** — preserved thought, fact/interpretation/unknown, contradictions/challenges.
4. **Profit Evidence Panel** — illustrative only; profit ≠ proof of decision quality.

## Research horizon (organization only)

Users may tag a thesis horizon (now, 3 months, 6 months, 1 year) for organization. This does not generate forecasts or recommendations.

## Allowed user intents

- Preserve why a thesis is being considered
- Surface facts, interpretations, and unknowns
- Identify evidence needed before an idea is testable
- Identify what would invalidate a thesis
- Compare a thesis against a stated objective
- Show what remains unknown

## Blocked in this MVP

- Personalized buy/sell recommendations
- Live entry zones or guaranteed profit signals
- Stock ranking for immediate action
- Broker execution
- Composite profitability scores
- Autonomous recommendation engine

## Constitutional constraints (unchanged)

Position ≠ Trade · Profit ≠ Proof · Fact ≠ Interpretation · Contradictory evidence must not be averaged into false certainty.

## Gate after prototype

FI-PROT-001-T1 must pass with genuine founder capture evidence before FI-CD-FIN-001.
