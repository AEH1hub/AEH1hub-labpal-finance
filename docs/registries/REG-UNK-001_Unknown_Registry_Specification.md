# REG-UNK-001 — Unknown Registry Specification

**Status:** CANDIDATE — FOUNDATION REVIEW REQUIRED
**Depends on:** FI-FOUND-001, FI-FOUND-002, GOV-001

## Purpose

The Unknown Registry preserves what LabPal does not currently understand, why it remains unknown and what evidence could change that state.

Unknown is a valid epistemic state.

An unknown must not be replaced with an assumption merely to complete an answer, report or workflow.

## Core principle

LabPal must be able to explain:

- what is unknown;
- why it is unknown;
- whether the unknown is material;
- what is blocked by it;
- what evidence is needed;
- what investigation has already occurred;
- how the unknown changed over time.

## Required fields

Every unknown record must contain:

- `unknown_id`;
- `title`;
- `question`;
- `scope`;
- `reason_unknown`;
- `materiality`;
- `status`;
- `created_at`;
- `last_reviewed_at`;
- `created_by`;
- `evidence_needed`;
- `blocked_by`;
- `blocks`;
- `related_evidence_ids`;
- `related_claim_ids`;
- `related_understanding_ids`;
- `investigation_history`;
- `resolution_conditions`;
- `resolution_record`;
- `provenance`.

## Unknown states

- `IDENTIFIED`
- `INVESTIGATING`
- `PARTIALLY_UNDERSTOOD`
- `RESOLUTION_PROPOSED`
- `RESOLVED_WITHIN_SCOPE`
- `REOPENED`
- `RETIRED`

## State rules

`IDENTIFIED` means the unknown has been preserved but investigation has not yet produced sufficient evidence.

`INVESTIGATING` means evidence gathering is active.

`PARTIALLY_UNDERSTOOD` means part of the question is supported, but material uncertainty remains.

`RESOLUTION_PROPOSED` means a possible resolution exists but has not passed review.

`RESOLVED_WITHIN_SCOPE` requires:

- explicit scope;
- supporting evidence;
- review record;
- unresolved limitations;
- resolution timestamp.

`REOPENED` means new evidence or contradiction invalidated the prior resolution.

`RETIRED` means the unknown is no longer operationally relevant. Retirement does not erase its history.

## Materiality

Materiality must be one of:

- `LOW`
- `MODERATE`
- `HIGH`
- `CRITICAL`
- `UNASSESSED`

Materiality is not certainty.

## Prohibited behavior

LabPal must not:

- convert an unknown into a fact without evidence;
- hide an unknown to make a report appear complete;
- close an unknown solely because sources agree;
- close an unknown solely because an outcome was profitable;
- erase investigation failures;
- silently replace the original question;
- represent partial understanding as complete resolution.

## Resolution rule

Resolution must answer:

- What became understood?
- Within what scope?
- Which evidence resolved it?
- Which limitations remain?
- What could reopen it?
- Who or what reviewed the resolution?

## Historical integrity

Every state transition must be append-only or otherwise preserve previous states.

A resolved unknown may be reopened when reality demands revision.
