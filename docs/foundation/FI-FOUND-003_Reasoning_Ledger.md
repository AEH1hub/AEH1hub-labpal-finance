# FI-FOUND-003 — Reasoning Ledger

**Status:** CANDIDATE — FOUNDATION REVIEW REQUIRED  
**Depends on:** FI-FOUND-001, FI-FOUND-002, REG-UNK-001, REG-EVID-001

## Purpose

The Reasoning Ledger preserves the auditable path by which LabPal arrived at a Current Understanding.

It records decision-relevant evidence and explicit reasoning summaries.

It does not require or preserve private chain-of-thought.

## Central questions

The ledger must help answer:

- How did we arrive at this understanding?
- Which evidence was considered?
- Which evidence was excluded?
- Why was evidence excluded?
- Which contradictions remained?
- Which unknowns remained?
- Which method was applied?
- What changed from the previous understanding?
- What could change the current understanding again?

## Required fields

Every reasoning-ledger entry must contain:

- `ledger_id`;
- `need`;
- `question`;
- `scope`;
- `created_at`;
- `created_by`;
- `method`;
- `considered_evidence_ids`;
- `supporting_evidence_ids`;
- `challenging_evidence_ids`;
- `excluded_evidence`;
- `material_unknown_ids`;
- `contradictions`;
- `assumptions`;
- `reasoning_summary`;
- `current_understanding_id`;
- `previous_understanding_id`;
- `revision_reason`;
- `review_state`;
- `review_record_ids`;
- `next_evidence_needed`;
- `history`.

## Reasoning summary

The reasoning summary must be concise enough to review and complete enough to explain the adopted interpretation.

It should state:

- the relevant evidence;
- the relationship between evidence;
- the material limitations;
- the unresolved alternatives;
- why the current interpretation was selected for the stated scope.

It must not claim certainty beyond the evidence.

## Excluded evidence

Excluded evidence must preserve:

- evidence identifier;
- exclusion reason;
- excluded by;
- timestamp;
- scope of exclusion.

Exclusion from one reasoning path does not erase the evidence.

## Assumptions

Assumptions must be explicit.

Each assumption must identify:

- statement;
- reason required;
- evidence status;
- risk if false;
- method of testing;
- expiry or review condition.

An assumption is not evidence.

## Review states

- `DRAFT`
- `READY_FOR_REVIEW`
- `REVIEWED`
- `CHALLENGED`
- `REVISION_REQUIRED`
- `ACCEPTED_WITHIN_SCOPE`
- `SUPERSEDED`

## Prohibited behavior

The Reasoning Ledger must not:

- fabricate evidence;
- expose private internal chain-of-thought;
- hide rejected alternatives;
- convert assumptions into facts;
- treat selection as verification;
- overwrite earlier reasoning history;
- conceal material contradictions;
- claim that an interpretation is final for all contexts.

## Revision rule

A revision must preserve:

- the prior ledger entry;
- the new evidence or contradiction;
- the reason for revision;
- the changed understanding;
- the unchanged understanding;
- the reviewer;
- the effective scope.

## Relationship to the Livigence Graph

The Livigence Graph explains why an understanding exists.

The Reasoning Ledger preserves the reviewable path used to construct that explanation.
