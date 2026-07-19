# LabPal

**An operating system for disciplined understanding.**

LabPal preserves reality, connects evidence, explains current understanding, and evolves through reviewable history.

Finance is LabPal's first proving domain. It tests the wider architecture against external reality, but it is not the complete identity of LabPal.

LabPal is not a signal engine, broker, prediction service, or autonomous decision-maker.

## Identity

LabPal must be able to answer:

- What do we currently understand?
- Why does that understanding exist?
- Which evidence supports or challenges it?
- What remains unknown?
- What changed from the previous understanding?
- What evidence could change it again?
- How did we arrive at the current interpretation?

LabPal distinguishes:

- **Memory** — preserves what occurred.
- **Knowledge** — preserves facts, sources, and relationships.
- **Understanding** — connects evidence, context, contradictions, and unknowns.
- **Wisdom** — supports appropriate action within explicit authority and evidence boundaries.

## Finance as the first proving domain

LabPal Finance currently demonstrates:

- Position, Claim, and Event objects;
- append-only history;
- fact and interpretation separation;
- contradiction preservation;
- Research Question objects;
- adversarial semantic validation;
- mock-evidence separation;
- Alpha Vantage live market-price integration;
- provider failure handling;
- evidence provenance;
- Current Understanding derivation.

Finance remains a proving domain. It does not define the complete future scope of LabPal.

## Architectural hierarchy

```text
Foundation
    ↓
Governance
    ↓
Understanding
    ↓
Evidence
    ↓
Operations
    ↓
Runtime
    ↓
Services
    ↓
Domains
    ↓
Products
    ↓
Company
```

No lower layer may silently redefine a higher layer.

## Understanding Lifecycle

```text
Need
↓
Question
↓
Reality
↓
Observation
↓
Evidence
↓
Validation
↓
Preservation
↓
Connection
↓
Context
↓
Interpretation
↓
Challenge
↓
Revision
↓
Current Understanding
↓
Review
↓
History
```

Verification is always scoped.

## Core principles

- Position ≠ Trade
- Profit ≠ Proof
- Fact ≠ Interpretation
- Unknown is a valid state
- Selection does not equal verification
- Agreement does not equal validity
- Registration does not equal verification
- Assumptions are not evidence
- Connections do not automatically establish truth
- Material contradictions remain visible
- Primary evidence must not be silently rewritten
- Failed tests remain evidence
- Reality may change the architecture
- The architecture must never change reality
- New responsibilities must be earned through demonstrated evidence

## What is currently implemented

### Validated or demonstrated runtime capabilities

- Position Object schemas and semantic validation
- Claim and Event provenance
- append-only event history
- Current Understanding derivation
- Research Question validation
- adversarial guardrails
- mock/live evidence separation
- Alpha Vantage adapter and normalization
- provider envelope and failure handling
- missing-key and transport-failure validation
- evidence-source and unknown-metadata preservation
- working prototype and founder behavioral testing

### Active RC1 branch capabilities

The following exist on `feature/fi-ask-003-rc1-followup` and are not yet merged into `main`:

- Market Session Guard
- deterministic market-session harness
- corrected CLOSED-state validation
- deterministic provider-key isolation
- preserved weekend observations
- market-state labeling correction

The branch still requires genuine weekday regular-session and post-close observations.

## Merged candidate institutional architecture

These documents are version-controlled on `main` as merged candidate standards.

### Foundation

- `docs/foundation/FI-FOUND-001_Livigence_Architecture.md`
- `docs/foundation/FI-FOUND-002_Understanding_Lifecycle.md`
- `docs/foundation/FI-FOUND-003_Reasoning_Ledger.md`

### Governance

- `docs/governance/GOV-001_Constitutional_Review_Authority.md`
- `docs/governance/GOV-002_Self_Correction_and_Review_Protocol.md`

### Operations

- `docs/operations/OPS-001_Institutional_Review_Report.md`

### Registries

- `docs/registries/REG-UNK-001_Unknown_Registry_Specification.md`
- `docs/registries/REG-EVID-001_Evidence_Registry_Specification.md`

These are specifications, not active autonomous engines.

## Constitutional Review Authority

The human-readable title is **Chief Justice**.

It may review changes, require evidence, block violations, preserve failures, and issue findings.

It may not rewrite primary evidence, conceal uncertainty, approve its own high-impact changes, or make financial, legal, or safety-critical decisions autonomously.

## Registries and Reasoning Ledger

### Unknown Registry

Preserves what remains unknown, why it remains unknown, what evidence is needed, and what could reopen a scoped resolution.

### Evidence Registry

Defines permanent evidence identity such as `EV-MARKET-000001`.

Registration means evidence has been preserved and identified. It does not mean the evidence is true, sufficient, or verified.

### Reasoning Ledger

Preserves the reviewable audit trail used to explain a Current Understanding without exposing private chain-of-thought.

## Repository layout

```text
├── README.md
├── requirements.txt
├── docs/
│   ├── foundation/
│   ├── governance/
│   ├── operations/
│   ├── registries/
│   └── preserved/
├── schemas/
├── fixtures/
├── guardrails/
├── runtime/
├── reports/
├── prototypes/
└── archive/
```

## Environment setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Local credentials belong in `.env`. Never commit API keys, tokens, secrets, credential-bearing URLs, or local `.env` files.

## Runtime and harness commands

```bash
.venv/bin/python runtime/labpal_rc_harness.py
.venv/bin/python runtime/research_question_harness.py
.venv/bin/python -m runtime.live_provider_harness
```

Expected result for each deterministic harness: `PASS`.

Live transport validation requires a local Alpha Vantage credential:

```bash
.venv/bin/python -m runtime.live_transport_harness
```

The Market Session Guard currently remains on `feature/fi-ask-003-rc1-followup`.

## Prototype

```bash
open prototypes/FI-PROT-001/index.html
```

Current product reality:

- working prototype exists;
- founder behavioral test exists;
- BF-002 timer behavior remains unresolved;
- five-user external validation has not happened;
- production UX has not begun.

## Current milestone states

### Validated

- Position architecture
- Claim and Event provenance
- Research Question model
- adversarial guardrails
- mock/live evidence separation
- deterministic provider validation
- Current Understanding derivation

### Demonstrated

- first live Alpha Vantage integration
- invalid-symbol handling
- weekend provider behavior
- no mock fallback during provider failure

### Merged candidate

- Livigence Architecture
- Understanding Lifecycle
- Constitutional Review Authority
- Self-Correction Protocol
- Institutional Report Standard
- Unknown Registry
- Evidence Registry
- Reasoning Ledger

### Active

- `FI-ASK-003-RC1`
- genuine weekday market-session evidence collection
- README modernization

### Pending

- weekday regular-session and post-close evidence
- RC1 closure review
- operational playbooks
- Living Heritage
- runtime registry schemas and validators
- Chief Justice engine
- automated reporting
- Progress Observatory
- external usability
- production UX
- regulatory and commercial validation

### Parked

- `FI-ASK-008 — Temporal Pattern Preservation`

FI-ASK-008 must not produce forecasting, recommendations, confidence percentages, or directional certainty.

## Explicit boundaries

LabPal may preserve evidence, retrieve live provider data, classify operational state, detect staleness, surface contradictions, preserve unknowns, and produce scoped working interpretations.

LabPal must not execute trades, recommend buys or sells, forecast direction as fact, fabricate evidence, hide failed tests, silently revise primary evidence, or declare its own interpretation verified.

## Development discipline

```text
Observe
↓
Validate
↓
Preserve
↓
Connect
↓
Interpret
↓
Review
↓
Commit
↓
Merge
↓
Archive
↓
Regression
↓
Release
```

<!-- DOC-ALIGN-001:START -->
## Product Contract and Repository Alignment

LabPal is an **Understanding Platform**.

LabPal Finance is its first proving product and is defined as a
**Portfolio Understanding** product.

It connects to one or more portfolios, preserves evidence, reasons
transparently, and builds justified understandings for portfolios and
holdings. It explains:

- what changed;
- which understanding changed;
- why it changed;
- why it matters;
- what evidence supports it;
- what remains uncertain; and
- what deserves attention next.

LabPal supports human judgment. It does not replace it.

The canonical understanding pipeline is:

```text
Reality
  ↓
Evidence
  ↓
Evidence Quality
  ↓
Reasoning
  ↓
Understanding
  ↓
Justification
  ↓
Decision Support
  ↓
Human Judgment
  ↓
Outcome
  ↓
Learning
```

The current gateway milestone is
[`DOC-ALIGN-001`](docs/alignment/DOC-ALIGN-001_Repository_Synchronization.md).

The next product specification is
[`PU-MVP-001`](docs/product/PU-MVP-001_Portfolio_Understanding_MVP.md).

The initial Portfolio Understanding implementation sequence is:

1. Read-only portfolio connection.
2. Portfolio Understanding.
3. Holding Understanding.
4. Understanding Change Detection.
5. Understanding History.

> Nothing becomes part of LabPal until the repository knows it exists.

<!-- DOC-ALIGN-001:END -->

## Roadmap

### Finance proving domain

```text
Complete RC1 weekday evidence
↓
Review RC1 for closure
↓
Merge RC1 follow-up
↓
Begin FI-ASK-004
```

### Institutional architecture

```text
Operational Playbooks
↓
Living Heritage
↓
Registry schemas and validators
↓
Institutional reporting runtime
↓
Constitutional Review engine
↓
Progress Observatory
```

### Product

```text
Repair BF-002
↓
Integrate evidence workflow
↓
Run five external usability sessions
↓
Begin production UX
```

## Overall project assessment

LabPal has a strong technical and epistemic foundation, versioned institutional architecture, validated evidence-preservation concepts, and a first demonstrated live-provider integration.

It remains early in runtime institutional systems, multi-provider validation, external usability, production UX, regulatory review, and commercial proof.

A universal completion percentage is intentionally not used.

Progress is represented through explicit evidence states:

```text
VALIDATED
DEMONSTRATED
MERGED CANDIDATE
ACTIVE
PENDING
PARKED
NOT STARTED
```

## Current Understanding

LabPal is becoming an operating system for disciplined understanding.

Finance is the first proving domain used to test that operating system against reality.
