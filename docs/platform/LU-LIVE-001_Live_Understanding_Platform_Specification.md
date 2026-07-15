# LU-LIVE-001 — Live Understanding Platform Specification

**Status:** CANDIDATE — PLATFORM REVIEW REQUIRED
**Milestone:** LU-LIVE-001
**Reasoning dependency:** FI-REAS-001
**Platform dependency:** LU-001
**Experience dependency:** LU-UX-001
**Verification dependency:** CI-001

## 1. Purpose

LU-LIVE-001 defines LabPal's first bounded live-evidence flow.

Its purpose is to allow external provider evidence to enter the existing LabPal reasoning, API and Understanding Experience layers without silently changing the meaning, authority or verification state of the result.

The milestone does not create a new reasoning engine.

It connects one controlled live-evidence path to the capabilities already earned by LabPal.

## 2. Governing principle

> Live evidence may enter LabPal only when its provenance, freshness, scope, limitations and unknowns remain visible throughout retrieval, normalization, reasoning, API transport and human presentation.

Provider retrieval does not equal verification.

A successful API response does not automatically establish truth, completeness, suitability or decision authority.

## 3. Initial scope

LU-LIVE-001 should support one bounded provider flow:

```text
External Provider
        ↓
Provider Adapter
        ↓
Normalized Evidence Record
        ↓
Unified Reasoning Pipeline
        ↓
Understanding Platform API
        ↓
Understanding Experience
```

The initial scope must remain research-only.

## 4. Responsibilities

LU-LIVE-001 is responsible for:

- accepting one explicitly supported live-evidence request;
- retrieving evidence through a server-side provider adapter;
- preserving provider identity;
- preserving request and response timestamps;
- preserving observation timestamps where supplied;
- preserving source symbols or identifiers;
- normalizing provider output into an existing evidence structure;
- recording freshness and staleness;
- preserving provider warnings and limitations;
- preserving unknowns created by missing or ambiguous data;
- invoking FI-REAS-001 without changing reasoning rules;
- transporting the reasoning result through LU-001;
- presenting live evidence through LU-UX-001 with an unmistakable live-evidence label;
- returning explainable failures.

## 5. Non-responsibilities

LU-LIVE-001 does not:

- create autonomous financial recommendations;
- execute trades;
- choose a winning asset;
- determine suitability;
- average conflicting provider values silently;
- select a preferred provider silently;
- claim independent-provider agreement;
- create persistent session storage;
- add user accounts;
- add authentication or authorization;
- add billing or subscriptions;
- activate AI agents;
- integrate an LLM;
- deploy publicly;
- prove production readiness;
- prove external decision quality.

## 6. Evidence classifications

Every evidence record must declare one classification:

- `LIVE_EVIDENCE`
- `MOCK_EVIDENCE`
- `HISTORICAL_EVIDENCE`

The classification must remain visible in:

- normalized evidence;
- reasoning output;
- API response;
- Understanding Experience.

Mock or historical evidence must never be presented as live.

## 7. Provenance requirements

Every live evidence record must preserve:

- provider name;
- provider endpoint or function identity;
- requested symbol or subject;
- provider-returned symbol or subject;
- retrieval timestamp;
- provider observation timestamp, when available;
- latest trading day or equivalent source date, when available;
- raw response fingerprint or preservation reference;
- adapter version;
- evidence identifier;
- source type;
- request scope;
- limitations;
- warnings;
- unknowns.

Provider credentials must never be stored in evidence records.

## 8. Freshness states

Every live evidence record must declare one freshness state:

- `CURRENT`
- `STALE`
- `HISTORICAL`
- `FRESHNESS_UNKNOWN`
- `NOT_APPLICABLE`

Freshness must be determined within an explicit scope.

A record may be current for one purpose and insufficient for another.

Freshness must never be inferred only from retrieval time when the provider supplies an older observation date.

## 9. Market-session context

Where the evidence depends on market timing, the record must preserve a market-session state such as:

- `PRE_MARKET`
- `REGULAR_SESSION`
- `POST_CLOSE`
- `MARKET_CLOSED`
- `SESSION_UNKNOWN`

Market-session state must come from an explicit calendar or session guard.

The system must not infer that a quote is intraday merely because it was retrieved during market hours.

The system must not label post-close retrieval as after-hours evidence unless the provider explicitly identifies the returned observation as after-hours.

## 10. Credential behavior

Provider credentials must:

- remain server-side;
- be supplied through environment or secret management;
- never appear in browser JavaScript;
- never appear in API responses;
- never appear in logs intended for users;
- never be committed to the repository.

Missing credentials must produce an explicit failure.

The system must not silently fall back to mock evidence.

## 11. Provider failure behavior

The system must preserve and distinguish:

- missing credentials;
- rate limits;
- provider error messages;
- malformed provider responses;
- missing symbols;
- missing prices or values;
- nonnumeric values;
- missing observation dates;
- empty responses;
- network failures;
- timeout failures;
- freshness uncertainty.

Provider failure must not become fabricated evidence.

A failed provider call must not produce a successful live-evidence claim.

## 12. Unknown preservation

Unknown is a valid state.

LU-LIVE-001 must preserve unknowns including:

- provider freshness unknown;
- observation time unknown;
- market-session applicability unknown;
- independent-provider agreement unknown;
- external validity unknown;
- provider completeness unknown;
- suitability unknown;
- user objective unknown;
- regulatory applicability unknown.

Unknowns must remain visible in the Understanding Experience.

## 13. Contradiction preservation

If provider evidence conflicts with:

- existing evidence;
- previous understanding;
- another provider;
- the requested scope;
- the provider's own metadata;

the contradiction must be preserved explicitly.

LU-LIVE-001 must not resolve contradiction through silent averaging, ranking or source preference.

## 14. Reasoning boundary

LU-LIVE-001 must delegate reasoning to FI-REAS-001.

It must not duplicate:

- semantic guardrails;
- Current Understanding selection;
- Decision-state derivation;
- Review-state derivation;
- prohibited recommendation rules;
- unknown handling;
- contradiction handling.

The same normalized evidence input must produce materially equivalent reasoning whether invoked directly or through the live platform path.

## 15. API boundary

LU-001 remains the canonical platform interface.

LU-LIVE-001 may extend the API with a narrowly scoped endpoint such as:

```text
POST /v1/live/reason
```

The endpoint must:

- validate transport input;
- invoke a supported provider adapter;
- produce normalized evidence;
- invoke FI-REAS-001;
- return structured provenance and reasoning output;
- preserve request identifiers;
- distinguish provider failure from reasoning rejection.

A reasoning rejection may still return a successful HTTP transport response when the request was processed correctly.

## 16. Experience boundary

LU-UX-001 must visually distinguish:

- live evidence;
- mock evidence;
- historical evidence;
- stale evidence;
- provider failure;
- unknown freshness;
- unresolved contradiction.

The interface must show:

- provider identity;
- evidence timestamp;
- observation date or time;
- freshness state;
- source limitations;
- unknowns;
- Current Understanding;
- Decision and Review states;
- next evidence needed.

The interface must not make live evidence appear verified merely because it is live.

## 17. Determinism and reproducibility

Live provider responses are not inherently reproducible.

Therefore LU-LIVE-001 verification must separate:

### Deterministic verification

Uses preserved provider-response fixtures to verify:

- normalization;
- provenance;
- failure handling;
- freshness behavior;
- reasoning integration;
- API transport;
- experience presentation.

### Reality observation

Uses an actual provider request to record:

- provider behavior;
- retrieval time;
- observation date;
- market-session context;
- warnings;
- unknowns;
- limitations.

Reality observation is evidence, not a deterministic test.

## 18. Completion artifacts

LU-LIVE-001 should produce:

- `docs/platform/LU-LIVE-001_Live_Understanding_Platform_Specification.md`
- one bounded provider adapter or integration runtime;
- one live-understanding orchestration runtime;
- deterministic provider fixtures;
- a deterministic live-understanding harness;
- API integration;
- experience integration;
- `reports/LU-LIVE-001_Live_Understanding_Platform_Report.md`

Any secret or API key is excluded from repository artifacts.

## 19. Completion gates

### `SPECIFICATION_COMPLETE`

The live-evidence responsibility, provenance, freshness, boundaries, failure modes and success criteria are fully specified.

### `RUNTIME_DEMONSTRATED`

One provider flow executes locally and produces normalized evidence and a reasoning result.

### `HARNESS_PASSING`

Deterministic fixtures verify success and failure paths.

### `REALITY_OBSERVED`

At least one genuine provider observation is recorded with provenance, timestamps, scope, warnings and unknowns.

### `REPORT_COMPLETE`

The implementation, evidence, failures, corrections, limitations and Knowledge Heritage are documented.

### `MERGED`

All milestone artifacts are reviewed and merged into `main`.

### `GITHUB_CHECK_PROVEN`

The committed deterministic verification passes through GitHub Actions.

### `EXTERNALLY_PROVEN`

Not earned by LU-LIVE-001 alone.

Requires later independent use, deployed operation and external validation.

## 20. Knowledge Heritage

LU-LIVE-001 must preserve the institutional lesson that live data is not automatically true, sufficient or decision-ready.

The milestone should record:

- why the provider was selected;
- what the provider actually returns;
- what the provider does not establish;
- how freshness is determined;
- how provider failures are represented;
- how unknowns were preserved;
- how contradictions were handled;
- how live evidence remained separated from recommendation authority;
- what evidence would justify future provider expansion.

## 21. Success condition

LU-LIVE-001 succeeds when LabPal demonstrates:

> One bounded live-evidence flow can enter the existing reasoning, platform and experience layers while preserving provenance, freshness, limitations, unknowns, contradictions and authority boundaries.

A provider response alone is not success.

Success requires that evidence and understanding remain in communion without live retrieval silently becoming verification, recommendation or authority.
