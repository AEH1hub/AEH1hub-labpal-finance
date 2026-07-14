# LU-001 — LabPal Understanding Platform Report

**Status:** CANDIDATE — COMPLETION REVIEW REQUIRED
**Milestone:** LU-001
**Verification scope:** Local deterministic platform invocation
**Reasoning dependency:** FI-REAS-001

## Purpose

LU-001 exposes LabPal's merged Unified Reasoning Pipeline through a stable, versioned FastAPI interface.

The milestone verifies that transport does not silently change reasoning behavior.

## Completion gates

| Gate | Result |
|---|---|
| Specification | PASS |
| Runtime | PASS |
| Harness | PASS |
| Report | COMPLETE — REVIEW REQUIRED |
| Repository History | PENDING COMMIT, REVIEW AND MERGE |
| External Proof | NOT EARNED |

## Implemented artifacts

- `docs/platform/LU-001_Understanding_Platform_Specification.md`
- `runtime/understanding_api.py`
- `runtime/understanding_api_harness.py`
- `reports/LU-001_Understanding_Platform_Report.md`
- `requirements.txt`

## Dependency record

The demonstrated environment uses:

- `jsonschema==4.26.0`
- `fastapi==0.139.0`
- `uvicorn==0.51.0`
- `httpx==0.28.1`

The installed dependency graph passed `pip check`.

## API surface

### `GET /v1/health`

Reports local process availability and the FI-REAS-001 dependency.

### `GET /v1/capabilities`

Separates earned, in-progress and unearned platform capabilities.

Capability records preserve their evidence and repository scope.

### `GET /v1/examples`

Returns deterministic fixture identifiers explicitly labeled as non-live evidence.

### `POST /v1/reason`

Accepts an FI-REAS-001-compatible payload and delegates directly to `run_reasoning_pipeline()`.

The platform does not duplicate reasoning rules.

## Harness results

The deterministic API harness verifies:

- health endpoint;
- capabilities endpoint;
- examples endpoint;
- valid research cycle;
- insufficient evidence;
- challenged understanding;
- prohibited recommendation;
- invalid claims are not adopted as Current Understanding;
- malformed-request handling;
- oversized-request handling;
- direct-runtime/API parity for every reasoning fixture.

All cases passed.

## Parity result

For all four versioned reasoning fixtures, direct Python invocation and FastAPI invocation produced materially identical:

- preserved question;
- evidence considered;
- supporting evidence;
- challenging evidence;
- excluded evidence;
- unknowns;
- contradictions;
- claims;
- Current Understanding;
- Decision state;
- Review state;
- reasoning summary;
- next evidence needed;
- history-preservation state;
- validation results.

Transport-specific metadata such as API version and request identifier remained separate.

## Regression results

The following existing systems remained passing:

- `runtime/unified_reasoning_pipeline_harness.py`
- `runtime/labpal_rc_harness.py`
- `runtime/research_question_harness.py`

## Error behavior

Malformed requests produce:

- HTTP `422`;
- structured `REQUEST_VALIDATION_FAILED` errors;
- preserved request identifiers;
- field-level details;
- no returned traceback.

Oversized requests produce:

- HTTP `413`;
- a structured validation error;
- preserved maximum and observed size information;
- no reasoning invocation.

A valid request producing a reasoning rejection remains an HTTP success response with an explainable bounded reasoning result.

## Principles demonstrated

- Platform transport must not rewrite understanding.
- The same valid input produces materially equivalent reasoning output.
- Reasoning rejection is not infrastructure failure.
- Invalid reasoning may be preserved without becoming Current Understanding.
- Unknowns and contradictions remain visible.
- Every rejection remains explainable.
- Provider credentials remain outside client-facing code.
- Repository state and local evidence scope remain distinct.

## Memory and Knowledge Heritage

### Engineering Memory

Preserved through:

- specification;
- pinned dependencies;
- API runtime;
- deterministic harness;
- report;
- repository history.

### Understanding Memory

Transported without rewriting:

- original question;
- evidence;
- unknowns;
- contradictions;
- Current Understanding;
- Decision state;
- Review state;
- next evidence needed.

### Organizational Memory

This report records:

- the initial FastAPI response-model registration defect;
- its bounded correction;
- the use of HTTPX ASGI transport instead of deprecated TestClient behavior;
- platform boundaries and future responsibilities.

## Known limitations

LU-001 currently:

- runs only as a deterministic local candidate;
- does not persist executions;
- has no authentication or authorization;
- has no rate limiting;
- has no production monitoring;
- has no provider orchestration;
- performs no live data requests;
- has no user account system;
- has no production web interface;
- has not undergone external security review;
- has not been tested by independent users;
- has not been deployed publicly;
- has not earned production or external proof.

## Completion assessment

LU-001 may be marked `MERGED` only after:

- dependencies, runtime, harness and report are committed;
- the pull-request scope is reviewed;
- repository history agrees;
- the branch is merged into `main`.

LU-001 must not be marked `EXTERNALLY_PROVEN` until deployment, independent use, security review and product-value evidence exist.
