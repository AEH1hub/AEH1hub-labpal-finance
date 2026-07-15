# LU-UX-001 — LabPal Understanding Experience Specification

**Status:** CANDIDATE — EXPERIENCE REVIEW REQUIRED
**Milestone:** LU-UX-001
**Platform dependency:** LU-001
**Reasoning dependency:** FI-REAS-001
**Verification dependency:** CI-001

## 1. Purpose

LU-UX-001 defines LabPal's first visual Understanding Experience.

Its purpose is to make one complete reasoning journey inspectable and understandable without changing the underlying reasoning behavior.

The experience must help a person understand:

- what question was asked;
- what evidence was considered;
- what evidence supported the current view;
- what evidence challenged it;
- what remains unknown;
- what contradictions remain unresolved;
- what Current Understanding was adopted;
- what Decision and Review states were produced;
- why the result was accepted, rejected, or marked for revision;
- what evidence is needed next.

LU-UX-001 is not a decorative dashboard.

It is a human-facing explanation layer over earned reasoning.

## 2. Governing principle

> Platform presentation must not rewrite understanding.

The same reasoning result must preserve the same meaning whether viewed:

- as direct Python output;
- through the LU-001 REST API;
- through the LU-UX-001 interface;
- through a future authorized application.

The interface may organize and explain information.

It must not silently change, hide, strengthen, or weaken the reasoning result.

## 3. Experience objective

The first experience must demonstrate one complete reasoning journey:

```text
Research Question
        ↓
Evidence Considered
        ↓
Supporting and Challenging Evidence
        ↓
Unknowns
        ↓
Contradictions
        ↓
Current Understanding
        ↓
Decision State
        ↓
Review State
        ↓
Reasoning Summary
        ↓
Next Evidence Needed
```

A user should be able to explain the result without requiring knowledge of the underlying JSON structure.

## 4. Initial users

The initial experience is designed for:

- the founder;
- engineers;
- reviewers;
- research users;
- future institutional operators;
- controlled usability-test participants.

It is not yet intended for unrestricted public financial use.

## 5. Initial scope

LU-UX-001 includes:

- one responsive web experience;
- deterministic reasoning examples;
- consumption of LU-001-compatible responses;
- visual separation of facts, interpretations, unknowns, and contradictions;
- visible Decision and Review states;
- visible rejection explanations;
- visible next evidence needed;
- accessibility-conscious semantic structure;
- deterministic experience verification;
- an experience report.

## 6. Non-goals

LU-UX-001 does not initially include:

- authentication;
- user accounts;
- persistent storage;
- live-provider orchestration;
- portfolio tracking;
- broker execution;
- autonomous recommendations;
- price alerts;
- payments;
- subscriptions;
- institutional governance execution;
- production analytics;
- external proof;
- public beta.

These require separate earned milestones.

## 7. Information architecture

### 7.1 Experience header

Display:

- LabPal identity;
- experience name;
- API version;
- reasoning milestone;
- evidence-mode label;
- execution identifier;
- repository or demonstration state.

The header must clearly distinguish deterministic demonstration data from live evidence.

### 7.2 Research Question

Display:

- original question;
- question type;
- action boundary;
- evidence mode;
- verification scope.

The original question must remain unchanged.

### 7.3 Current Understanding

Display:

- current statement;
- status;
- selected claim identifier;
- verification notice;
- previous understanding when available.

Current Understanding must never appear as unquestionable truth.

### 7.4 Decision and Review

Display:

- Decision state;
- Review state;
- why the state was produced;
- whether revision is required;
- whether the result is ready for review.

A rejected or revision-required result must remain understandable rather than appearing as a generic error.

### 7.5 Evidence considered

Display every evidence identifier considered by the reasoning result.

Separate evidence into:

- supporting evidence;
- challenging evidence;
- excluded evidence.

Empty states must be explicit.

An empty evidence collection must not be visually mistaken for verified absence.

### 7.6 Claims

Claims must preserve their classifications:

- source fact;
- source interpretation;
- LabPal interpretation.

Where available, display:

- claim identifier;
- claim text;
- classification;
- freshness state;
- connected evidence identifier;
- origin collection.

The interface must not style all claims as equally verified.

### 7.7 Unknown landscape

Display every material unknown.

Unknowns must be presented as valid institutional information, not as missing UI content or system failure.

> Unknown does not mean ignored. It means the current evidence has not earned a conclusion.

### 7.8 Contradictions

Display unresolved contradictions prominently.

The experience must distinguish:

- no contradiction recorded;
- contradiction recorded and unresolved;
- prior understanding challenged;
- revision required.

### 7.9 Reasoning summary

Display the preserved human-readable reasoning summary exactly as received from the API unless an explicitly labeled presentation summary is separately generated.

LU-UX-001 must not manufacture hidden reasoning.

### 7.10 Next evidence needed

Display the evidence needed to improve the current understanding.

This section should answer:

> What would help LabPal understand this better?

It must not present next evidence as an investment instruction or action recommendation.

### 7.11 History and provenance

Display:

- history-preserved state;
- previous understanding;
- execution identifier;
- request identifier;
- reasoning dependency;
- API version.

## 8. Visual semantics

Visual treatment must communicate epistemic meaning consistently.

- **Evidence:** structured, traceable, and source-associated.
- **Unknowns:** visible but not styled as failures.
- **Contradictions:** prominent and distinct from ordinary warnings.
- **Current Understanding:** important but provisional.
- **Decision states:** clear text labels; never color-only.
- **Rejections:** explainable; a bare red error is insufficient.

## 9. LabPal brand system

LU-UX-001 must establish one reusable LabPal interface standard.

The visual language should communicate:

- disciplined understanding;
- calm institutional confidence;
- transparency;
- traceability;
- evolving knowledge;
- respectful uncertainty;
- human and machine communion.

Avoid:

- speculative trading aesthetics;
- casino-style financial visuals;
- excessive neon effects;
- opaque AI imagery;
- urgency-based recommendation design;
- unearned confidence scores.

## 10. Responsive behavior

The interface must work across mobile, tablet, and desktop.

On smaller screens:

- the original question remains visible early;
- Current Understanding and Decision state remain prominent;
- unknowns and contradictions remain accessible;
- evidence cards stack vertically;
- normal content requires no horizontal scrolling.

## 11. Accessibility

Preserve:

- semantic heading hierarchy;
- keyboard navigation;
- visible focus states;
- sufficient color contrast;
- text labels in addition to color;
- readable line lengths;
- meaningful button labels;
- reduced-motion compatibility where animation exists.

Accessibility is a product responsibility, not a later decoration.

## 12. API boundary

The interface must consume LU-001-compatible output.

It must not duplicate:

- Research Question validation;
- evidence validation;
- semantic guardrails;
- decision derivation;
- review-state derivation;
- Current Understanding selection;
- contradiction logic;
- unknown preservation.

Those remain responsibilities of FI-REAS-001 and LU-001.

## 13. Initial deterministic scenarios

The first experience must support:

1. valid research cycle;
2. insufficient evidence;
3. challenged understanding;
4. prohibited recommendation.

### Valid research cycle

Show:

- evidence exists;
- Current Understanding exists;
- decision is ready for review;
- unknowns remain visible.

### Insufficient evidence

Show:

- no evidence was considered;
- no supported conclusion was earned;
- decision is `INSUFFICIENT_EVIDENCE`;
- next evidence needed is visible.

### Challenged understanding

Show:

- supporting and challenging evidence;
- unresolved contradiction;
- previous understanding;
- revision-required state.

### Prohibited recommendation

Show:

- the request violated a semantic boundary;
- the invalid claim remains auditable;
- no prohibited Current Understanding was adopted;
- rule `RQ-020` caused revision to be required.

## 14. Trust requirements

The experience must make it possible to answer:

- Where did this conclusion come from?
- What evidence supports it?
- What challenges it?
- What is still unknown?
- What changed from the previous understanding?
- Why did LabPal accept or reject the reasoning?
- What evidence could change the result?

Trust must be earned through inspectability.

## 15. Interaction principles

The initial experience may allow a user to:

- choose a deterministic scenario;
- inspect evidence;
- expand claim details;
- inspect unknowns and contradictions;
- review previous understanding;
- copy structured identifiers;
- switch between visual and raw structured output.

It must not initially allow:

- direct trade execution;
- hidden prompt manipulation;
- modification of reasoning results after execution;
- suppression of challenging evidence;
- conversion of unknowns into assumptions;
- automatic recommendation generation.

## 16. Empty states

Every empty state must explain its meaning.

Examples:

- `No supporting evidence was recorded.`
- `No challenging evidence was recorded.`
- `No contradiction is recorded within this scope.`
- `No previous understanding is preserved.`
- `No admissible Current Understanding was adopted.`

An empty state must never silently imply success.

## 17. Failure states

The interface must distinguish:

- malformed request;
- oversized request;
- reasoning rejection;
- insufficient evidence;
- platform unavailability;
- unexpected infrastructure failure.

Reasoning rejection is not infrastructure failure.

## 18. Memory responsibilities

### Engineering Memory

Preserved through:

- specification;
- source code;
- component structure;
- deterministic fixtures;
- experience harness;
- report;
- repository history.

### Understanding Memory

Presented through:

- original question;
- evidence;
- claims;
- unknowns;
- contradictions;
- Current Understanding;
- previous understanding;
- Decision and Review states;
- reasoning summary;
- next evidence needed.

### Organizational Memory

Preserved through:

- usability observations;
- design decisions;
- rejected interface patterns;
- accessibility findings;
- behavioral test results;
- post-test revisions.

## 19. Knowledge Heritage

Every significant interface decision should preserve:

- the problem observed;
- the available evidence;
- the selected design;
- alternatives considered;
- limitations;
- test result;
- reason for revision.

Documentation explains the interface.

Knowledge Heritage explains how the institution learned to make the interface understandable.

## 20. Initial technical boundary

LU-UX-001 may use a simple browser-based implementation that consumes deterministic or local LU-001 responses.

Prioritize:

- clarity;
- inspectability;
- deterministic behavior;
- minimal tooling complexity;
- easy local execution;
- later API connectivity.

Framework choice must not become more important than comprehension.

## 21. Verification plan

Verification must include:

- rendering all four scenarios;
- preserving original question text;
- preserving every unknown;
- preserving contradictions;
- preserving Decision and Review states;
- confirming prohibited claims are not presented as Current Understanding;
- responsive checks;
- keyboard-access checks;
- deterministic output checks;
- regression verification through CI-001.

## 22. Usability success criteria

Before external proof, the founder test should verify whether a person can identify:

1. the question;
2. the Current Understanding;
3. the Decision state;
4. at least one unknown;
5. supporting or challenging evidence;
6. any contradiction;
7. why revision is required;
8. what evidence is needed next.

Later external testing must use uncoached participants.

A visually attractive page that users cannot correctly explain does not pass.

## 23. Completion gates

### `SPECIFICATION_COMPLETE`

The experience responsibility, hierarchy, boundaries, and verification criteria are completely specified.

### `RUNTIME_DEMONSTRATED`

The visual experience renders the required scenarios locally.

### `HARNESS_PASSING`

Deterministic experience verification passes.

### `REPORT_COMPLETE`

The experience report records implementation, verification, defects, corrections, and limitations.

### `MERGED`

All milestone artifacts are reviewed and merged into `main`.

### `EXTERNALLY_PROVEN`

Independent users demonstrate that they can understand the reasoning journey without coaching.

This state is not earned by implementation alone.

## 24. Initial artifact plan

LU-UX-001 should initially produce:

- `docs/experience/LU-UX-001_Understanding_Experience_Specification.md`;
- an experience runtime under `prototypes/` or a dedicated application directory;
- an experience verification harness;
- deterministic scenario data sourced from LU-001-compatible outputs;
- `reports/LU-UX-001_Understanding_Experience_Report.md`.

Any dependency additions must be explicit and reviewable.

## 25. Success condition

LU-UX-001 succeeds when a person can inspect one complete LabPal reasoning result and accurately understand:

- what was asked;
- what evidence was considered;
- what remains unknown;
- what is contradicted;
- what Current Understanding exists;
- why the Decision and Review states were produced;
- what evidence is needed next.

The experience must make understanding visible without silently changing it.
