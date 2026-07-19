# DOC-ALIGN-001 — Repository Synchronization

Status: Official gateway milestone
Purpose: Make product, philosophy, architecture, terminology, roadmap, and implementation intent describe one reality.

## Product Contract

**LabPal is an Understanding Platform.**

**LabPal Finance is a Portfolio Understanding product.**

It connects to one or more portfolios, preserves evidence, reasons transparently, builds and justifies multiple understandings for each holding and the portfolio as a whole, and explains:

- what changed;
- which understanding changed;
- why it changed;
- why it matters;
- what evidence supports it;
- what remains uncertain; and
- what deserves attention next.

It supports human judgment. It does not replace it.

## Philosophy

1. Reality comes first.
2. Evidence before conclusions.
3. Evidence quality matters.
4. Reasoning before justification.
5. Understanding before decisions.
6. Transparency before trust.
7. Uncertainty is information.
8. Human judgment remains central.
9. Learning compounds.
10. Clean work stays synchronized.

## Core abstraction

An `Understanding` is a versioned object, not a summary string.

It contains:

- subject and scope;
- current claims;
- supporting and contradicting evidence;
- reasoning;
- justification;
- unknowns;
- limitations;
- review state; and
- change history.

## Portfolio Understanding

Initial components:

- Performance
- Contribution
- Allocation and Weight
- Income
- Risk
- Diversification
- Growth
- Market
- Sector
- Trend
- News
- Time
- Bullish
- Bearish
- Portfolio Health
- Attention

Each component owns evidence, reasoning, unknowns, limitations, and history.

## Holding Understanding

Initial components:

- Dividend
- Earnings
- Cash Flow
- Valuation
- Growth
- Risk
- Market
- Sector
- Trend
- News
- Bullish
- Bearish
- Time
- Opportunity and Attention

Required page sequence:

1. Current Understanding
2. Why This Understanding?
3. Evidence
4. What Changed?
5. Bullish Developments
6. Bearish Developments
7. Portfolio Impact
8. Unknowns and Limitations
9. What Should Be Reviewed Next?
10. Evidence Required
11. Plain-language Review State

## Understanding Change Detection

Every alert must answer:

1. What changed?
2. Which understanding changed?
3. Why did it change?
4. Why does it matter?
5. What evidence supports it?
6. What remains uncertain?
7. What deserves review next?

Green means supported or strengthened.
Yellow means material review is needed.
Red means the prior understanding is no longer sufficiently supported.

These colors never mean buy, hold, or sell.

Internal states such as `READY_FOR_REVIEW` may remain in engineering contracts, but the interface must translate them into specific explanations.

## Understanding History and Knowledge Heritage

Price history shows what the market did.

Understanding History shows how evidence, reasoning, unknowns, and justified conclusions changed over time.

Historical versions must not be silently rewritten. Corrections are new events linked to earlier versions.

Knowledge Heritage is a later capability built from preserved evidence lineage, revisions, outcomes, and lessons.

## Accepted decisions

### ADR-0001

LabPal is an Understanding Platform. Finance is the first domain, not the company identity.

### ADR-0002

Use Portfolio Understanding rather than Portfolio Manager. Management and tracking are supporting capabilities.

### ADR-0003

Understanding Alerts replace unexplained status labels and price-only alerts.

### ADR-0004

Repository synchronization is a mandatory gate after each completed milestone.

## Roadmap

### Phase 1 — Foundation

Complete, subject to repository-specific verification records.

### DOC-ALIGN-001

Current.

Definition of done:

- README aligned;
- Product Contract recorded;
- philosophy and canonical architecture documented;
- Finance model documented;
- terminology locked;
- decisions recorded;
- roadmap refreshed;
- PU-MVP-001 accepted; and
- repository-specific links, branches, commands, and CI status verified.

### Phase 2 — Portfolio Understanding MVP

1. Canonical read-only portfolio ingestion
2. Portfolio Understanding
3. Holding Understanding
4. Understanding Change Detection
5. Understanding History

### Phase 3 — Knowledge Heritage

Historical reasoning, evidence lineage, outcome-informed learning, and carefully governed cross-domain knowledge.

## Feature admission test

Every feature must state:

- which understanding it improves;
- which user problem it solves;
- which evidence supports it;
- how it is justified;
- what uncertainty remains;
- how it will be verified; and
- how it preserves human judgment.
