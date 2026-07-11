# FI-UX-001 — Understanding-First Experience Specification

**Status:** ACTIVE FOUNDATION  
**Scope:** Product philosophy, interaction model, evidence journey, Livigence responsibilities, convergence design language, and action-boundary policy.  
**Applies to:** LabPal Finance first, then future LabPal sector packs.

---

## 1. North Star

> **LabPal is an Understanding Engine powered by Livigence, the Living Evidence Engine. It transforms fragmented information into trustworthy understanding by gathering, connecting, evaluating, preserving, and evolving evidence through time while clearly separating facts, interpretations, uncertainty, and action boundaries so people can make better judgments and solve complex problems with confidence.**

LabPal exists to help people reach clearer understanding before important action.

Finance is the first implementation domain. The engine is broader than finance.

---

## 2. Mission

> **Help people understand complex situations before making important decisions.**

LabPal should reduce confusion, expose what is known and unknown, preserve evidence and history, and support better judgment without disguising analysis as certainty.

---

## 3. Permanent Product Promise

Every LabPal answer should leave the user with a better understanding than when they arrived.

Every answer should clearly distinguish:

- What is observed.
- What is evidenced.
- What is inferred.
- What is uncertain.
- What may change.
- What is safe to do next.

Every screen should silently answer five questions:

| User need | LabPal responsibility |
|---|---|
| What is happening? | Current Understanding |
| Why do we believe this? | Evidence |
| What is still unknown? | Unknowns |
| What could change this? | Invalidation / revision conditions |
| What is safe to do next? | Action Boundary |

---

## 4. Immutable Runtime Principles

FI-UX-001 does not replace the existing Constitution, Genome, Position Object, semantic guardrails, or runtime principles.

The following remain unchanged:

- Position ≠ Trade
- Profit ≠ Proof
- Fact ≠ Interpretation
- UNKNOWN is a valid state
- Unexecuted ≠ Rejected
- Accepted ≠ Verified
- Selection ≠ Verification
- Human acceptance ≠ Verification
- AI assistance ≠ confirmation authority
- Reviews and revisions are append-only
- Material contradictions remain visible
- Historical wording must not be silently rewritten
- Source preservation does not equal claim endorsement

The interface may become simpler. The epistemic discipline must not become weaker.

---

## 5. Understanding-First Interaction Model

The user should not be required to understand LabPal’s internal architecture before using it.

The primary experience should begin with one natural-language entry point:

> **What would you like to understand?**

Examples:

- How is the market today?
- What is happening with Nvidia?
- Why did silver move today?
- Compare SCHD vs VIG.
- Should I investigate this company?
- What changed since last week?

Ask, Quick Capture, Investigate, Research Question Objects, Position Objects, and Current Understanding remain valid internal workflow states.

They should not be the user’s first architectural burden.

### Internal flow

Question or thought  
→ Intent classification  
→ Evidence gathering  
→ Evidence classification  
→ Evidence quality review  
→ Current Understanding  
→ Judgment support  
→ Action boundary  
→ Preservation  
→ Optional investigation  
→ Optional Position Object  
→ Review and learning

---

## 6. Evidence Journey

Every question follows the same evidence journey:

1. **Question**
2. **Evidence Gathering**
3. **Evidence Classification**
4. **Evidence Quality**
5. **Understanding**
6. **Judgment Support**
7. **Action Boundary**
8. **Preservation**
9. **Learning**

This journey should remain consistent across sectors.

Only the evidence sources and domain rules change.

---

## 7. Understanding Levels

Understanding should build progressively without pretending certainty.

| Level | Meaning |
|---|---|
| U0 | Question received |
| U1 | Evidence gathered |
| U2 | Evidence classified |
| U3 | Contradictions identified |
| U4 | Unknowns identified |
| U5 | Current Understanding produced |
| U6 | Investigation completed |
| U7 | Outcome reviewed |
| U8 | Understanding evolved |

### Rules

- A higher level does not automatically mean the conclusion is correct.
- A level indicates process progress, not confidence or truth probability.
- Understanding levels must not become a disguised numeric confidence score.
- U5 Current Understanding remains a working interpretation unless separately verified within scope.
- U8 must preserve earlier states and revisions rather than overwrite them.

---

## 8. Livigence — Living Evidence Engine

> **Livigence is LabPal’s Living Evidence Engine. It continuously gathers, connects, evaluates, preserves, and evolves evidence through time so understanding improves without losing history, uncertainty, contradiction, or provenance.**

### Engineering responsibilities

Livigence is responsible for:

1. Gathering evidence.
2. Preserving provenance.
3. Measuring freshness.
4. Detecting contradictions.
5. Separating fact from interpretation.
6. Preserving uncertainty.
7. Identifying action boundaries.
8. Recording revisions.
9. Evolving understanding.
10. Never hiding history.

### Living evidence

Living evidence is not merely live data.

It is evidence with:

- origin;
- retrieval time;
- publication time where available;
- freshness state;
- scope;
- classification;
- revision history;
- contradiction links;
- unknowns;
- effect on Current Understanding.

Evidence may become stale, contradicted, superseded in scope, or newly relevant. It must not disappear silently.

---

## 9. Convergence Design Language

The Convergence Symbol represents the transformation of fragmented reality into coherent understanding.

Fragmented inputs may include:

- questions;
- observations;
- prices;
- news;
- filings;
- documents;
- charts;
- memories;
- prior decisions;
- external research;
- contradictions;
- outcomes.

These fragments converge through Livigence into:

Evidence  
→ Understanding  
→ Judgment support  
→ Action boundary  
→ Learning

### Design principle

Every interface component should answer:

> **Does this reduce fragmentation and increase trustworthy understanding?**

If not, it should not be part of the primary LabPal experience.

### Visual philosophy

- Fragments may be visually distinct before classification.
- Convergence should show relationships, not erase differences.
- Facts, interpretations, unknowns, and contradictions should remain visually distinguishable.
- The Convergence Symbol is not decoration; it represents the product’s operating model.
- Complexity may exist underneath, but the user experience should remain calm, readable, and progressive.

---

## 10. Compare Evidence Across Independent Sources

LabPal should not merely compare market prices.

It should compare evidence across independent sources.

Examples:

- Prices across exchanges or data providers.
- Company filings versus news coverage.
- Central-bank statements versus market expectations.
- Multiple weather providers.
- Government reports versus academic research.
- Issuer factsheets versus third-party commentary.

### Rules

- Independent agreement may strengthen support but does not prove truth.
- Repeated reporting of the same original source is not independent confirmation.
- Source interpretation must remain separate from LabPal interpretation.
- Conflicting evidence must remain visible.
- Freshness and scope must be displayed.

---

## 11. Sector Packs

LabPal uses one Understanding Engine with domain-specific Sector Packs.

Each Sector Pack defines:

- permitted evidence sources;
- source-quality hierarchy;
- freshness expectations;
- domain classifications;
- action-boundary policy;
- regulatory constraints;
- invalidation rules;
- required unknowns;
- review cadence.

### Finance Pack

Possible evidence types:

- market prices;
- exchange data;
- issuer filings;
- fund factsheets;
- earnings releases;
- macroeconomic data;
- rates and yields;
- currency data;
- dividend and distribution records;
- sector breadth;
- news catalysts;
- analyst research, clearly classified as interpretation.

### Weather Pack

Possible evidence types:

- forecast models;
- radar;
- satellite observations;
- station observations;
- official warnings;
- historical climate data.

### Healthcare Pack — future gated

Possible evidence types:

- clinical guidelines;
- peer-reviewed trials;
- regulatory approvals;
- medicine information;
- authorized patient data.

Healthcare implementation requires dedicated safety, privacy, regulatory, and clinical-review gates.

### Additional future packs

- Business
- Government
- Education
- Engineering
- Research

The engine remains consistent. The evidence and action rules change by domain.

---

## 12. Finance Price-Area Language

LabPal must not disguise a personalized buy recommendation as neutral research.

Avoid:

> Buy here.

Avoid:

> LabPal recommends buying between X and Y.

Preferred analytical language:

> **Based on the available evidence, these price areas deserve further investigation because…**

The analysis should then explain:

- why the area is relevant;
- which sources support it;
- which evidence challenges it;
- which assumptions were used;
- the applicable time horizon;
- what would invalidate the assessment;
- when the assessment becomes stale;
- whether transaction costs, taxes, liquidity, currency, and risk boundaries are known;
- whether the analysis is general research or potentially personalized action language.

### Action-boundary rule

An evidence-supported price area is not automatically:

- a recommendation;
- an entry instruction;
- an executable order;
- a guarantee;
- proof of future profitability.

The user retains decision responsibility.

Future price-area functionality requires deterministic validity checks, source freshness, risk boundaries, and regulatory review before release.

---

## 13. Daily Intelligence

Daily Intelligence is an evidence service, not a signal service.

Possible subscriptions:

- Market Intelligence Daily
- Dividend Watch
- Commodity Watch
- AI Industry Watch
- Renewable Energy Watch
- Swiss Market Watch
- Global Macro Watch

Every update should answer:

1. What changed?
2. Why does it matter?
3. What evidence supports this?
4. What evidence challenges it?
5. What remains unknown?
6. What deserves attention next?

### Delivery rules

- Include timestamps and source references.
- Distinguish new evidence from repeated reporting.
- Label stale evidence.
- Preserve prior understanding when material changes occur.
- Do not use urgency, fear, or certainty to manufacture action.
- Do not present a daily update as a guaranteed trading opportunity.

---

## 14. Interaction Principles

1. **Understanding before action.**
2. **One natural entry point before internal modes.**
3. **Ask only for the minimum missing context.**
4. **Gather evidence automatically where permitted and available.**
5. **Do not show internal complexity before it helps the user.**
6. **Preserve original wording.**
7. **Separate source fact, source interpretation, LabPal interpretation, and user statement.**
8. **UNKNOWN remains valid and visible.**
9. **Contradictions are surfaced, not averaged away.**
10. **Freshness and scope are part of every material claim.**
11. **Every analysis shows what could change it.**
12. **Every action-oriented output shows an action boundary.**
13. **AI-generated content preserves origin and review state.**
14. **The simplest useful path should be the default path.**
15. **Every feature must reduce fragmentation or improve understanding.**

---

## 15. Action Boundary Policy

LabPal may:

- explain;
- summarize;
- compare;
- classify;
- identify relevant evidence;
- identify contradictions;
- identify unknowns;
- identify evidence-supported areas for further investigation;
- describe scenarios;
- show invalidation conditions;
- preserve questions, evidence, and understanding states;
- support user-led investigation.

LabPal must not silently present analysis as:

- certainty;
- guaranteed outcome;
- personalized buy/sell instruction;
- executable order;
- regulated professional clearance;
- proof of profitability;
- verified fact when only inferred;
- independent confirmation when sources share one origin.

### Recommendation-risk triggers

Additional review is required when output includes:

- direct buy/sell language;
- personalized suitability claims;
- precise entry or exit instructions;
- portfolio allocation instructions;
- urgency tied to financial action;
- claims of expected profit without calibrated evidence;
- autonomous execution;
- regulated-domain decisions.

---

## 16. Understanding Response Structure

A mature LabPal response should normally include:

### What is happening
A concise Current Understanding.

### Evidence
Timestamped, scoped source facts and relevant source interpretations.

### LabPal interpretation
Clearly labeled synthesis or inference.

### Contradictions
Material evidence that challenges the working understanding.

### Unknowns
What cannot yet be established.

### What could change this
Invalidation, revision, and freshness conditions.

### Action boundary
What the analysis does and does not justify.

### Next useful step
The safest meaningful next investigation or preservation action.

The interface may progressively disclose these sections rather than overwhelming the user at once.

---

## 17. Success Criterion

FI-UX-001 succeeds when a first-time user can ask one natural question and immediately feel:

- LabPal understood the intent.
- LabPal gathered or identified the evidence needed.
- Facts and interpretations are distinguishable.
- Unknowns remain visible.
- The current understanding is clear.
- The user knows what could change the analysis.
- The user knows the boundary between understanding and action.
- The user can preserve or investigate without learning internal architecture first.

Primary test question:

> **How is the market today?**

The final system should answer with current, sourced evidence when live evidence adapters are connected. It must not answer from stale model memory while presenting the result as current.

---

## 18. Implementation Sequence

FI-UX-001 defines the experience before further prototype expansion.

Recommended sequence:

1. Preserve FI-UX-001 in the repository.
2. Review against the Constitution, Genome, B1–B6, and FI-PRD-001-RC.
3. Resolve any contradiction before implementation.
4. Define FI-UX-001-T1 acceptance tests.
5. Design the unified Understand entry point.
6. Define the Research Question Object.
7. Define the Live Evidence Record.
8. Define source adapters and freshness policy.
9. Build a sourced market-overview vertical slice.
10. Run real behavioral tests before adding additional sectors or recommendation-risk features.

---

## 19. Change Discipline

This document may evolve, but changes must be explicit.

Do not silently alter:

- the North Star;
- the permanent product promise;
- immutable runtime principles;
- the distinction between evidence and interpretation;
- action-boundary requirements;
- preservation of history and contradictions.

Every material revision should state:

- what changed;
- why it changed;
- what evidence justified the change;
- which existing behavior is affected;
- whether prior tests remain valid.

---

## 20. Current Status Board

| Area | Status | Reality |
|---|---|---|
| Constitution | STABLE | No change required |
| Genome | STABLE | Continues to guide architecture |
| Livigence | DEFINED | Living Evidence Engine responsibilities specified |
| Convergence Symbol | DEFINED FOR UX | Represents convergence without erasing distinctions |
| Understanding Engine | NORTH STAR ESTABLISHED | Applies across sectors |
| Evidence Journey | DEFINED | Shared process for every question |
| Understanding Levels | PROPOSED FOUNDATION | Requires validation before product scoring use |
| Sector Packs | PROPOSED FOUNDATION | Finance first; other sectors gated |
| RC4 Prototype | BUILT | Existing implementation baseline |
| T1 original | FAILED | Preserved behavioral evidence |
| T1-R2N | PENDING | Natural founder test still required |
| FI-ASK-001 | PAUSED | Resume after UX acceptance criteria |
| FI-UX-001 | ACTIVE FOUNDATION | This specification is the current reference |

---

## 21. Design Filter

Every future LabPal feature must answer:

> **Does this help people reach trustworthy understanding more effectively?**

If the answer is no, it does not belong in LabPal’s primary experience.
