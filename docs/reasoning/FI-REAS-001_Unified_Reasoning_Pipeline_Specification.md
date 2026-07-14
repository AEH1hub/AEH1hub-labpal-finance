# FI-REAS-001 — Unified Reasoning Pipeline Specification

**Status:** CANDIDATE — REASONING REVIEW REQUIRED
**Milestone:** FI-REAS-001
**Depends on:** Research Question Object, Evidence Records, Claim/Event models, Current Understanding, Reasoning Ledger, Unknown Registry, Evidence Registry and Operational Playbooks

## Purpose

The Unified Reasoning Pipeline connects LabPal's existing reasoning responsibilities into one reproducible and reviewable execution path.

It transforms a preserved question and scoped evidence into a Current Understanding and reviewable Decision state without hiding uncertainty, contradictions, exclusions or history.

## Governing principles

- Understanding is earned. It is never assumed.
- Responsibilities are earned. They are never assumed.
- Evidence precedes conclusion.
- Fact is not interpretation.
- Selection does not equal verification.
- Agreement does not equal validity.
- Every approval must be explainable.
- Every rejection must be explainable.
- Every operation must be reproducible.
- Understanding matures through preserved revision, not replacement.
- Capabilities are integrated before new capabilities are introduced.

## Pipeline stages

1. Question preservation
2. Intent classification
3. Scope establishment
4. Evidence-requirement derivation
5. Evidence collection or receipt
6. Evidence validation
7. Claim construction
8. Challenge construction
9. Unknown and contradiction preservation
10. Current Understanding derivation
11. Decision-state derivation
12. Review
13. Reasoning Ledger entry
14. Report generation
15. History preservation

## Stage contract

Every stage must define:

- stage identifier;
- purpose;
- inputs;
- outputs;
- dependencies;
- authority;
- validation rules;
- failure states;
- preserved unknowns;
- provenance;
- history relationship.

A later stage may not silently rewrite an earlier stage's primary record.

## Required pipeline input

The minimum input must contain:

- pipeline execution identifier;
- original question;
- question identifier;
- question type;
- scope;
- action boundary;
- evidence mode;
- evidence records;
- existing claims where applicable;
- existing understanding where applicable;
- execution timestamp;
- executing actor.

## Required pipeline output

The minimum output must contain:

- execution identifier;
- preserved question;
- classified intent;
- scope;
- considered evidence identifiers;
- supporting evidence identifiers;
- challenging evidence identifiers;
- excluded evidence with reasons;
- material unknowns;
- contradictions;
- generated claims;
- Current Understanding;
- Decision state;
- review state;
- reasoning summary;
- next evidence needed;
- history references;
- validation results.

## Intent stage

Intent classification must preserve the original wording.

Classification must not change the user's question into a safer or more convenient question without recording the transformation.

Prohibited intents must be blocked with an explanation.

## Evidence stage

Evidence must retain provenance, timestamps, freshness, source identity, limitations and mock state.

Evidence registration does not equal verification.

Unknown timestamps must remain unknown.

## Claim stage

Claims must distinguish:

- SOURCE_FACT;
- SOURCE_INTERPRETATION;
- LABPAL_INTERPRETATION;
- USER_STATEMENT;
- UNKNOWN.

A LabPal interpretation must not be presented as a sourced fact.

## Challenge stage

The pipeline must actively preserve:

- challenging evidence;
- competing interpretations;
- contradictions;
- unresolved alternatives;
- material unknowns.

Absence of challenge evidence must not be represented as proof.

## Current Understanding stage

Current Understanding must state:

- scope;
- current statement;
- supporting evidence;
- challenging evidence;
- contradictions;
- material unknowns;
- limitations;
- previous understanding;
- revision reason;
- next evidence needed;
- verification notice.

## Decision states

Initial permitted states are:

- RESEARCH_ONLY
- INSUFFICIENT_EVIDENCE
- BLOCKED_BY_UNKNOWN
- READY_FOR_REVIEW
- REVISION_REQUIRED
- ACCEPTED_WITHIN_SCOPE
- DEFERRED

FI-REAS-001 must not produce:

- buy or sell instructions;
- entry prices;
- ranking winners;
- autonomous financial recommendations;
- unsupported confidence percentages;
- claims of universal verification.

## Review stage

Every approval or rejection must preserve:

- decision;
- authority;
- scope;
- evidence reviewed;
- applicable rules;
- supporting reasons;
- challenging reasons;
- unknowns;
- limitations;
- reviewer;
- timestamp;
- next evidence required.

A bare PASS or FAIL is insufficient.

## Reasoning Ledger stage

The pipeline must generate an auditable reasoning summary.

It must not expose or require private chain-of-thought.

The summary must explain the evidence relationship, alternatives, limitations and reason for the adopted scoped interpretation.

## Failure states

The pipeline must fail safely when:

- the original question is missing;
- scope is missing;
- evidence provenance is missing;
- mock evidence is unlabeled;
- a required timestamp is fabricated;
- facts and interpretations are mixed;
- material contradictions are concealed;
- action-boundary rules are violated;
- history would be overwritten;
- a decision exceeds earned authority.

## Determinism boundary

Given identical normalized inputs, rules and versioned dependencies, the pipeline must produce structurally equivalent output.

External reality may produce different evidence.

That difference must remain visible and must not be treated automatically as a pipeline defect.

## Acceptance criteria

FI-REAS-001 is ready for review when:

- the runtime executes one complete pipeline;
- valid fixtures pass;
- adversarial fixtures fail for the correct reason;
- unknowns and contradictions remain visible;
- no primary evidence is rewritten;
- Current Understanding preserves history;
- Decision state remains within authority;
- every approval and rejection is explainable;
- the human-readable report matches the machine output;
- existing regressions continue to pass.

## Package boundary

This milestone does not:

- create the LU-001 web interface;
- activate autonomous recommendations;
- implement private chain-of-thought storage;
- replace the Evidence or Unknown registries;
- implement the Chief Justice engine;
- introduce a new domain;
- close FI-ASK-003-RC1;
- begin FI-ASK-004.
