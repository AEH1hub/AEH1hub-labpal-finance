# LU-001 — LabPal Understanding Platform Specification

**Status:** CANDIDATE — PLATFORM REVIEW REQUIRED
**Milestone:** LU-001
**Layer:** Platform
**Primary dependency:** FI-REAS-001 Unified Reasoning Pipeline
**Initial interface:** Versioned REST API

## 1. Purpose

The LabPal Understanding Platform exposes LabPal's merged reasoning capability through a stable, versioned and reviewable platform interface.

Its purpose is not to invent new reasoning.

Its purpose is to make already-earned reasoning accessible consistently to:

* deterministic harnesses;
* web applications;
* future domain applications;
* authorized services;
* future human and machine collaborators.

The platform must preserve the behavior, boundaries and explainability of the Unified Reasoning Pipeline.

## 2. Governing principle

> The same valid input must produce materially equivalent reasoning output regardless of whether the pipeline is invoked directly in Python, through the REST API, through a future web interface, or through another authorized application.

Transport must not silently change understanding.

## 3. Architectural position

```text
Layer 1 — Institution
Constitution
Governance
Playbooks
Standards

        ↓

Layer 2 — Reasoning
Research Question
Evidence
Claims
Unknowns
Contradictions
Current Understanding
Decision
Review

        ↓

Layer 3 — Platform
REST API
Request validation
Response serialization
Versioning
Health reporting
Capability reporting

        ↓

Layer 4 — Applications
Finance
Logistics
Sustainability
Compliance
Research
Future domains
```

LU-001 begins Layer 3.

## 4. Primary responsibility

LU-001 must:

1. receive a versioned platform request;
2. validate the transport-level request;
3. preserve the original payload;
4. invoke `run_reasoning_pipeline()` without duplicating its business logic;
5. return a structured versioned response;
6. preserve validation failures and reasoning rejections;
7. expose health and capability information;
8. produce deterministic API verification evidence;
9. preserve enough knowledge for future engineers to understand why and how the interface works.

## 5. Explicit non-responsibilities

LU-001 must not:

* rewrite the Unified Reasoning Pipeline;
* weaken existing semantic rules;
* generate financial recommendations;
* select winners;
* fabricate evidence;
* replace unknowns with assumptions;
* hide contradictions;
* contact market-data providers from browser code;
* expose provider credentials;
* implement persistent storage;
* implement authentication;
* implement user accounts;
* implement scheduling;
* implement telemetry collection;
* implement the Chief Justice engine;
* implement autonomous correction;
* implement the final production UX;
* prove external product usefulness;
* claim regulatory approval.

Those responsibilities require separate earned milestones.

## 6. Initial API surface

### `GET /v1/health`

Purpose:

Confirm that the platform process is available.

Expected response:

```json
{
  "service": "labpal-understanding-platform",
  "version": "v1",
  "status": "available",
  "reasoning_dependency": "FI-REAS-001"
}
```

A successful health response proves process availability only.

It does not prove reasoning validity, provider availability, external truth or product usefulness.

### `GET /v1/capabilities`

Purpose:

Expose the capabilities currently earned by this API version.

Expected capability states include:

* `SPECIFICATION_COMPLETE`
* `RUNTIME_DEMONSTRATED`
* `HARNESS_PASSING`
* `REPORT_COMPLETE`
* `MERGED`
* `EXTERNALLY_PROVEN`

The endpoint must distinguish earned capabilities from planned capabilities.

A capability must not be reported as earned merely because it appears on the roadmap.

### `GET /v1/examples`

Purpose:

Expose safe fixture-compatible example identifiers or sample request structures.

Examples must be:

* deterministic;
* explicitly labeled;
* free of credentials;
* free of fabricated live claims;
* unsuitable for being mistaken for current external reality.

### `POST /v1/reason`

Purpose:

Invoke the merged Unified Reasoning Pipeline through a versioned HTTP interface.

The endpoint must accept a fixture-compatible FI-REAS-001 payload.

The endpoint must return the reasoning result without silently changing:

* the original question;
* evidence identifiers;
* supporting evidence;
* challenging evidence;
* unknowns;
* contradictions;
* claims;
* Current Understanding;
* Decision state;
* Review state;
* validation results;
* next evidence needed;
* history-preservation state.

## 7. Request contract

The first `POST /v1/reason` request must contain:

* `execution_id`;
* `executing_actor`;
* `scope`;
* `research_question`.

It may also contain:

* `challenging_evidence_ids`;
* `contradictions`;
* `additional_unknowns`;
* `excluded_evidence`;
* `previous_understanding`;
* `next_evidence_needed`.

Transport validation must not replace FI-REAS-001 schema or semantic validation.

The platform may reject malformed HTTP input before pipeline invocation.

Valid transport input must still be evaluated by the reasoning pipeline.

## 8. Response contract

A successful pipeline invocation must return:

* API version;
* request identifier;
* milestone identifier;
* preserved question;
* evidence considered;
* supporting evidence;
* challenging evidence;
* excluded evidence;
* unknowns;
* contradictions;
* claims;
* Current Understanding;
* Decision state;
* Review state;
* reasoning summary;
* next evidence needed;
* history-preservation state;
* validation results.

The platform must preserve the distinction between:

* transport success;
* schema validity;
* semantic validity;
* reasoning acceptance;
* reasoning rejection;
* external verification.

An HTTP success response may contain a valid, explainable reasoning rejection.

## 9. Error contract

Errors must be structured and explainable.

Each platform error should preserve:

* `error_code`;
* `message`;
* `scope`;
* `request_id`, when available;
* `details`;
* `next_action`, when known.

Initial platform error classes:

* `MALFORMED_JSON`
* `REQUEST_VALIDATION_FAILED`
* `PIPELINE_INPUT_REJECTED`
* `PIPELINE_EXECUTION_FAILED`
* `INTERNAL_PLATFORM_ERROR`

The API must not return internal stack traces, credentials or confidential environment values to clients.

## 10. Decision and HTTP semantics

HTTP status and reasoning state are different responsibilities.

Examples:

* malformed HTTP input may return a client error;
* a valid request producing `INSUFFICIENT_EVIDENCE` may still return an HTTP success response;
* a valid prohibited request may return an HTTP success response containing an explainable `REVISION_REQUIRED` reasoning result;
* an unexpected runtime defect must return a platform error without fabricating a reasoning result.

The platform must not treat reasoning rejection as infrastructure failure.

## 11. Versioning

The initial API namespace is:

```text
/v1
```

Versioning protects clients from silent breaking changes.

A breaking change includes:

* removing response fields;
* changing field meaning;
* changing Decision-state semantics;
* changing error semantics;
* changing the accepted request contract incompatibly.

New optional fields may be introduced within `v1` only when they do not break existing clients.

A future incompatible interface requires a new version.

## 12. Determinism and parity

LU-001 must prove invocation parity.

For the same deterministic fixture:

```text
Direct Python invocation
and
REST API invocation
```

must produce materially equivalent reasoning fields.

Transport-specific fields such as request identifiers or API metadata may differ.

Reasoning content must not differ silently.

Parity comparison must include:

* preserved question;
* evidence considered;
* unknowns;
* contradictions;
* Current Understanding;
* Decision state;
* Review state;
* validation results;
* history preservation.

## 13. Provider boundary

External providers are not part of the first LU-001 reasoning endpoint.

Provider architecture remains:

```text
Client
    ↓
LabPal Platform API
    ↓
Authorized provider adapter
    ↓
External provider
```

Provider credentials must remain server-side.

No Alpha Vantage, Twelve Data, FMP or other provider key may be exposed through:

* browser JavaScript;
* React public environment variables;
* Vite public environment variables;
* API responses;
* logs;
* committed files;
* fixtures.

Provider orchestration requires a separate milestone.

## 14. Environment model

Future deployment environments must remain separated:

```text
development
staging
production
```

Each environment must use separate secrets and configuration.

Deterministic tests must not require live provider keys.

Live-provider tests must remain explicit integration tests rather than mandatory unit or harness dependencies.

## 15. Security boundaries

The first platform runtime must:

* validate request bodies;
* limit accepted payload size;
* reject malformed input;
* avoid dynamic code execution;
* avoid logging secrets;
* avoid returning stack traces;
* avoid browser-side provider credentials;
* preserve existing action boundaries.

Authentication, authorization and rate limiting are required before unrestricted public use, but are not part of the first deterministic API milestone.

The initial deployment, if any, must be treated as a controlled prototype rather than an unrestricted production service.

## 16. Memory responsibilities

LU-001 must preserve three distinct memory responsibilities.

### Engineering Memory

Explains how to rebuild and verify the platform.

Includes:

* specification;
* runtime;
* harness;
* report;
* repository history;
* dependency versions;
* deployment instructions.

### Understanding Memory

Explains why a reasoning result exists.

Includes:

* original question;
* evidence;
* unknowns;
* contradictions;
* Current Understanding;
* Decision and Review states;
* reasoning summaries;
* next evidence needed.

### Organizational Memory

Explains how the institution improves.

Future records may include:

* deployment decisions;
* incidents;
* API compatibility changes;
* user observations;
* beta feedback;
* architectural decisions;
* postmortems.

LU-001 begins Engineering Memory for the platform layer and transports Understanding Memory without rewriting it.

## 17. Knowledge Heritage requirement

Every LU-001 artifact must help a future engineer answer:

* Why was this platform interface created?
* Which merged capability does it expose?
* How does it work?
* Why does it work this way?
* Which alternatives or non-goals were preserved?
* What evidence verified parity?
* Which limitations remain?
* Which rules must never silently change?
* Which future milestones depend on this interface?

Documentation explains the API.

Knowledge Heritage explains the institutional understanding that formed the API.

## 18. Initial runtime recommendation

The first implementation should use FastAPI because:

* the reasoning engine is already Python;
* request and response models can be typed;
* OpenAPI documentation is generated automatically;
* deterministic test clients can exercise routes without network deployment;
* reasoning logic can remain in the existing runtime module.

The first runtime should contain no duplicated reasoning rules.

Its core operation should remain equivalent to:

```python
result = run_reasoning_pipeline(payload)
```

## 19. Initial verification scenarios

The LU-001 harness must verify:

1. health endpoint;
2. capabilities endpoint;
3. valid research-cycle request;
4. insufficient-evidence request;
5. challenged-understanding request;
6. prohibited-recommendation request;
7. malformed request;
8. direct-runtime/API parity;
9. invalid reasoning is not adopted as Current Understanding;
10. existing FI-REAS-001 regressions remain passing.

## 20. Completion gates

### Stage 1 — `SPECIFICATION_COMPLETE`

Earned when:

* the platform contract is versioned;
* responsibilities and non-responsibilities are explicit;
* request, response and error semantics are defined;
* provider and credential boundaries are explicit;
* memory and Knowledge Heritage requirements are preserved.

### Stage 2 — `RUNTIME_DEMONSTRATED`

Earned when:

* the FastAPI application imports successfully;
* all initial endpoints execute;
* `/v1/reason` delegates to FI-REAS-001;
* no reasoning logic is duplicated;
* malformed requests fail safely.

### Stage 3 — `HARNESS_PASSING`

Earned when:

* all API scenarios pass deterministically;
* direct invocation and API invocation demonstrate parity;
* FI-REAS-001 regressions remain passing.

### Stage 4 — `REPORT_COMPLETE`

Earned when:

* implementation evidence is summarized;
* test results are preserved;
* limitations are explicit;
* completion and non-completion states are recorded;
* Knowledge Heritage is sufficient for future engineers.

### Stage 5 — `MERGED`

Earned when:

* specification, runtime, harness and report are committed;
* pull-request scope is reviewed;
* repository history agrees;
* changes are merged into `main`.

### Stage 6 — `EXTERNALLY_PROVEN`

Not earned by LU-001 alone.

Requires later evidence from:

* deployed use;
* independent users;
* production-like operation;
* security and privacy review;
* defect observations;
* product-value evidence.

## 21. Initial artifact plan

LU-001 should initially produce:

* `docs/platform/LU-001_Understanding_Platform_Specification.md`
* `runtime/understanding_api.py`
* `runtime/understanding_api_harness.py`
* `reports/LU-001_Understanding_Platform_Report.md`

Dependency changes may include:

* FastAPI;
* Uvicorn;
* HTTPX or an equivalent deterministic test client.

Any dependency change must be explicit and reviewable.

## 22. Success condition

LU-001 succeeds when LabPal can demonstrate:

> The merged reasoning engine can be invoked through a stable versioned API while preserving materially identical reasoning behavior, explicit boundaries, explainability, history and unknowns.

LU-001 does not succeed merely because an HTTP server starts.

It succeeds when platform transport and reasoning truth remain in communion without either silently changing the other.
