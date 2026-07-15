# LU-UX-001 — LabPal Understanding Experience Report

**Status:** CANDIDATE — COMPLETION REVIEW REQUIRED
**Milestone:** LU-UX-001
**Verification scope:** Local deterministic browser experience
**Platform dependency:** LU-001
**Reasoning dependency:** FI-REAS-001
**Repository verification dependency:** CI-001

## Purpose

LU-UX-001 presents one complete LabPal reasoning result through a human-facing browser experience without silently changing the meaning of the underlying reasoning output.

The milestone verifies that the existing FI-REAS-001 reasoning result can be transported through LU-001-compatible structures and presented visually while preserving evidence, unknowns, contradictions, Current Understanding, Decision state, Review state and next evidence needed.

## Completion gates

| Gate | Result |
|---|---|
| Specification | PASS |
| Runtime | PASS |
| Browser demonstration | PASS |
| Harness | PASS |
| Report | COMPLETE — REVIEW REQUIRED |
| Repository history | PENDING REVIEW AND MERGE |
| External proof | NOT EARNED |

## Implemented artifacts

- `docs/experience/LU-UX-001_Understanding_Experience_Specification.md`
- `experience/index.html`
- `experience/assets/app.js`
- `experience/assets/styles.css`
- `experience/data/manifest.json`
- four deterministic reasoning scenario files
- `runtime/understanding_experience_harness.py`
- `reports/LU-UX-001_Understanding_Experience_Report.md`

## Demonstrated scenarios

### Valid research cycle

The experience displayed:

- a preserved Research Question;
- one explicitly mock evidence record;
- five material unknowns;
- no recorded contradiction;
- a bounded Current Understanding;
- `READY_FOR_REVIEW` Decision and Review states;
- explicit next evidence requirements.

### Insufficient evidence

The experience displayed:

- no connected evidence;
- an explicit empty evidence state;
- preserved unknowns;
- `INSUFFICIENT_EVIDENCE`;
- `REVISION_REQUIRED`;
- evidence required before broader understanding.

### Challenged understanding

The experience displayed:

- supporting evidence;
- challenging evidence;
- a visible unresolved contradiction;
- preserved previous understanding;
- `REVISION_REQUIRED`.

### Prohibited recommendation

The experience preserved the prohibited claim for audit while refusing to adopt it as Current Understanding.

It displayed:

- `REVISION_REQUIRED`;
- the absence of an admissible selected claim;
- an explainable rejection;
- preserved rule `RQ-020`;
- next safe evidence requirements.

## Harness verification

The LU-UX-001 deterministic harness verifies:

- the scenario manifest;
- all four required scenarios;
- expected Decision and Review states;
- validation-state preservation;
- required reasoning fields;
- preserved questions and history;
- static HTML element integrity;
- JavaScript reasoning-field integration;
- CSS experience structure;
- prohibited claims cannot become Current Understanding;
- rule `RQ-020` remains visible.

## Browser demonstration

The experience was served locally and inspected in a browser.

The valid research cycle displayed:

- the original IBM Research Question;
- evidence considered;
- material unknowns;
- explicit contradiction empty state;
- Current Understanding;
- Decision and Review states;
- reasoning summary;
- next evidence needed;
- structured raw output.

The remaining scenarios were available through the deterministic scenario selector.

## Principles demonstrated

- Platform presentation must not rewrite understanding.
- Unknown does not mean ignored.
- Empty states must be explicit.
- Contradictions remain visible.
- Invalid reasoning may be preserved without being adopted.
- Selection does not equal verification.
- Trust is earned through inspectability.
- Deterministic fixture evidence must not be represented as live evidence.
- Knowledge Heritage records why the interface behaves as it does.

## Evidence record

LU-UX-001 evidence includes:

- versioned deterministic scenario outputs;
- direct Decision and Review state assertions;
- manifest integrity checks;
- static integration checks;
- browser inspection;
- the LU-UX-001 harness result;
- the complete CI-001 repository verification result;
- repository commits `64ba8f4` and `1f0ab88`.

## Knowledge Heritage

LU-UX-001 preserves the lesson that a technically valid reasoning result is not yet a usable product.

The system must make its reasoning inspectable without simplifying uncertainty into false certainty.

The experience therefore treats:

- unknowns as first-class information;
- contradictions as visible evidence;
- rejection as an explainable outcome;
- empty states as meaningful states;
- raw structured output as available for inspection.

This knowledge should later inform LabPal Finance, LabPal Energy, LabPal Waste, logistics, sustainability, compliance and other domain experiences.

## Known limitations

LU-UX-001 currently:

- uses deterministic fixture outputs;
- does not perform live provider requests;
- does not persist sessions;
- has no authentication;
- has no user accounts;
- has no database;
- has no payment or subscription system;
- has no AI-agent authority;
- has no LLM integration;
- has no public production deployment;
- has no independent usability evidence;
- has no security or privacy certification;
- has not earned external proof.

## Completion assessment

LU-UX-001 may be marked `MERGED` only after:

- the experience harness passes;
- the full repository verification operation passes;
- the harness, verification-script update and report are committed;
- the pull request is reviewed;
- GitHub Actions completes successfully;
- the branch is merged into `main`.

LU-UX-001 must not be marked `EXTERNALLY_PROVEN` until independent users can accurately understand the experience in a deployed environment.

## Conclusion

LU-UX-001 demonstrates LabPal's first visual reasoning experience.

It converts structured reasoning into an inspectable human experience while preserving evidence, uncertainty, contradictions, rejection logic and history.

The experience does not prove external product value.

It proves that LabPal's earned reasoning can be made visible without silently rewriting it.
