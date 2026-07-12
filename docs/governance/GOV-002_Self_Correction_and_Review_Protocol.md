# GOV-002 — Self-Correction and Review Protocol

**Status:** CANDIDATE — GOVERNANCE REVIEW REQUIRED

## Principle

LabPal may correct itself only within explicit authority, evidence and reversibility boundaries.

## Correction classes

### Class A — Automatic correction permitted

Low-risk, deterministic and reversible:

- whitespace;
- formatting;
- broken internal references;
- filename classification;
- missing metadata warnings;
- deterministic test isolation;
- cache or temporary-artifact cleanup.

### Class B — Proposal required

Meaning-affecting but reversible:

- schema changes;
- classification changes;
- new guardrails;
- workflow changes;
- interpretation revisions;
- provider normalization changes.

LabPal may prepare a patch and evidence report, but review is required before adoption.

### Class C — Human authorization required

High-impact:

- Constitution changes;
- financial recommendations;
- legal classifications;
- production releases;
- deletion of evidence;
- authority changes;
- security-policy changes;
- irreversible migrations.

## Required correction record

Every correction must preserve:

- correction ID;
- trigger;
- observed failure;
- evidence;
- rule authorizing correction;
- before state;
- after state;
- tests executed;
- test result;
- timestamp;
- actor;
- review state;
- reversal procedure.

## Reporting cadence

### Daily

- what passed;
- what failed;
- what changed;
- unresolved unknowns;
- corrections proposed or performed;
- alerts requiring review.

### Weekly

- repeated failures;
- recurring unknowns;
- reliability changes;
- incomplete work;
- decisions awaiting authority.

### Monthly

- responsibilities earned;
- regressions;
- architectural changes demanded by reality;
- unresolved risks;
- evidence coverage.

### Annual

- constitutional compliance;
- institutional-memory integrity;
- major revisions;
- retired assumptions;
- unresolved systemic risks.

## Failure rule

A failed test is evidence.

It may not be removed merely to make a dashboard appear green.
