# FI-ASK-003-RC1 — Reality Confirmation Observations

**Status:** ACTIVE — PARTIAL EVIDENCE
**Provider:** Alpha Vantage
**Observation date:** 2026-07-12
**Evidence type:** Founder-operated live-provider observation

## Purpose

Observe whether the first live evidence provider behaves consistently under changing real-world conditions before connecting a second provider.

This report records observations. It does not rank the provider, establish universal reliability, or authorize recommendations.

## Observation RC1-001 — Missing credential

The adapter was executed without `ALPHA_VANTAGE_API_KEY` loaded.

Observed result:

- Status: FAIL
- Error: `ALPHA_VANTAGE_API_KEY is missing.`
- Mock fallback used: false

### Finding

The adapter failed visibly and did not silently substitute mock evidence.

## Observation RC1-002 — Personal credential loaded

The local environment was reloaded from the ignored `.env` file.

Observed checks:

- Key present: true
- Placeholder removed: true
- Key length: 16
- Key value was not committed to Git

### Evidence boundary

This confirms environment loading. It does not independently establish provider account ownership beyond successful provider access.

## Observation RC1-003 — Non-demo symbol request

Symbol:

`MSFT`

First retrieval time:

`2026-07-12T06:13:18.309544+00:00`

Provider response:

- Latest trading day: `2026-07-10`
- Price: `385.1000`
- Volume: `24644605`
- Change: `0.7400`
- Change percent: `0.1925%`
- Source type: `MARKET_PRICE`
- Classification: `SOURCE_FACT`
- Mock fallback: false

Missing metadata remained explicit:

- no exact quote timestamp;
- no exchange timezone;
- no currency;
- no real-time/delayed declaration in the payload.

## Observation RC1-004 — Repeated request

Second retrieval time:

`2026-07-12T06:13:28.273651+00:00`

The second response preserved the same:

- symbol;
- trading date;
- price;
- volume;
- change;
- change percentage.

### Finding

Two calls approximately ten seconds apart produced consistent provider evidence.

This is initial repeated-call evidence only. It does not prove long-term provider stability.

## Observation RC1-005 — Weekend behavior

The observations occurred on Sunday, 2026-07-12.

The provider returned the latest trading day as Friday, 2026-07-10.

### Finding

The adapter preserved retrieval time separately from the provider's trading date and did not present Sunday as a trading day.

## Security observation

The credential used during this session was exposed outside the local environment and must be rotated.

No replacement credential should be recorded in this report, source control, screenshots, or conversation transcripts.

## Current RC1 status

Completed:

- missing-key behavior;
- personal-key loading;
- non-demo symbol request;
- initial repeated-call consistency;
- weekend behavior;
- unknown preservation;
- no mock fallback.

Still required:

- market-hours observation;
- after-hours observation;
- observations across multiple days;
- invalid-symbol live-provider behavior;
- natural rate-limit behavior;
- rotated-key confirmation.

## Current conclusion

**NEW PROVIDER BEHAVIOR OBSERVED**

LabPal has demonstrated that one real provider can be accessed with a local personal credential and normalized consistently during an initial weekend observation.

FI-ASK-003-RC1 remains active.

## Observation RC1-006 — Replacement credential confirmation

A replacement credential was entered through silent terminal input, written only to the ignored local `.env` file, and reloaded into the shell environment.

Observed checks:

- key present: true;
- placeholder removed: true;
- key length: 16;
- `.env` remained ignored by Git.

A subsequent live request for `MSFT` returned:

- status: `PASS`;
- retrieval time: `2026-07-12T14:17:47.218229+00:00`;
- latest trading day: `2026-07-10`;
- provider-reported price: `385.1000`;
- source type: `MARKET_PRICE`;
- classification: `SOURCE_FACT`;
- mock fallback used: false.

### Finding

The replacement credential functioned successfully without being printed, committed, or included in the provider provenance URL.

This confirms operational credential replacement. It does not establish long-term provider reliability.
