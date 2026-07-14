"""LU-001 LabPal Understanding Platform API.

This module exposes the merged FI-REAS-001 reasoning pipeline through a
versioned HTTP interface. It must not duplicate or weaken reasoning logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from runtime.unified_reasoning_pipeline import (
    PipelineValidationError,
    run_reasoning_pipeline,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "reasoning-pipeline"

SERVICE_NAME = "labpal-understanding-platform"
API_VERSION = "v1"
REASONING_DEPENDENCY = "FI-REAS-001"
MAX_REQUEST_BYTES = 1_000_000


class ReasoningRequest(BaseModel):
    """Transport contract for the FI-REAS-001-compatible payload."""

    model_config = ConfigDict(extra="forbid")

    execution_id: str = Field(min_length=1)
    executing_actor: str = Field(min_length=1)
    scope: dict[str, Any]
    research_question: dict[str, Any]
    challenging_evidence_ids: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    additional_unknowns: list[str] = Field(default_factory=list)
    excluded_evidence: list[Any] = Field(default_factory=list)
    previous_understanding: dict[str, Any] | None = None
    next_evidence_needed: list[str] = Field(default_factory=list)


def platform_error(
    *,
    status_code: int,
    error_code: str,
    message: str,
    scope: str,
    request_id: str | None,
    details: Any,
    next_action: str | None,
) -> JSONResponse:
    """Return a bounded and explainable platform error."""

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "error_code": error_code,
                "message": message,
                "scope": scope,
                "request_id": request_id,
                "details": details,
                "next_action": next_action,
            }
        },
    )


app = FastAPI(
    title="LabPal Understanding Platform",
    version="1.0.0",
    description=(
        "Versioned transport interface for the merged FI-REAS-001 "
        "Unified Reasoning Pipeline."
    ),
)


@app.middleware("http")
async def enforce_request_size(
    request: Request,
    call_next: Any,
) -> Any:
    """Reject oversized requests before application processing."""

    content_length = request.headers.get("content-length")

    if content_length is not None:
        try:
            request_size = int(content_length)
        except ValueError:
            return platform_error(
                status_code=400,
                error_code="REQUEST_VALIDATION_FAILED",
                message="The Content-Length header is invalid.",
                scope="transport",
                request_id=request.headers.get("x-request-id"),
                details={},
                next_action="Send a valid Content-Length header.",
            )

        if request_size > MAX_REQUEST_BYTES:
            return platform_error(
                status_code=413,
                error_code="REQUEST_VALIDATION_FAILED",
                message="The request body exceeds the permitted size.",
                scope="transport",
                request_id=request.headers.get("x-request-id"),
                details={
                    "maximum_bytes": MAX_REQUEST_BYTES,
                    "observed_bytes": request_size,
                },
                next_action="Reduce the request payload.",
            )

    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def handle_request_validation(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return structured transport validation failures."""

    request_id = request.headers.get("x-request-id")

    return platform_error(
        status_code=422,
        error_code="REQUEST_VALIDATION_FAILED",
        message="The request did not satisfy the LU-001 transport contract.",
        scope="transport",
        request_id=request_id,
        details=exc.errors(),
        next_action="Correct the request fields and submit it again.",
    )


@app.get("/v1/health")
def health() -> dict[str, Any]:
    """Report process availability without overclaiming validity."""

    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "status": "available",
        "reasoning_dependency": REASONING_DEPENDENCY,
    }


@app.get("/v1/capabilities")
def capabilities() -> dict[str, Any]:
    """Report earned and unearned capabilities separately."""

    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "earned": [
            {
                "capability": (
                    "FI-REAS-001_UNIFIED_REASONING_PIPELINE"
                ),
                "state": "MERGED",
            },
            {
                "capability": "LU-001_PLATFORM_SPECIFICATION",
                "state": "SPECIFICATION_COMPLETE",
            },
            {
                "capability": "LU-001_UNDERSTANDING_PLATFORM",
                "state": "MERGED",
                "evidence_scope": (
                    "DETERMINISTIC_REPOSITORY_VERIFICATION"
                ),
                "repository_state": "MERGED",
                "external_proof": "NOT_EARNED",
            },
        ],
        "in_progress": [],
        "not_earned": [
            "LU-001_EXTERNALLY_PROVEN",
            "AUTHENTICATION",
            "PERSISTENCE",
            "PROVIDER_ORCHESTRATION",
            "PUBLIC_PRODUCTION_READINESS",
        ],
    }


@app.get("/v1/examples")
def examples() -> dict[str, Any]:
    """Expose deterministic fixture identifiers without live claims."""

    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "label": "DETERMINISTIC_FIXTURES_NOT_LIVE_EVIDENCE",
        "examples": [
            "valid-research-cycle.fixture.json",
            "insufficient-evidence.fixture.json",
            "challenged-understanding.fixture.json",
            "prohibited-recommendation.fixture.json",
        ],
    }


@app.post("/v1/reason", response_model=None)
def reason(
    payload: ReasoningRequest,
    request: Request,
) -> Any:
    """Delegate reasoning to FI-REAS-001 without changing its logic."""

    request_id = (
        request.headers.get("x-request-id")
        or str(uuid4())
    )
    pipeline_payload = payload.model_dump(mode="python")

    try:
        result = run_reasoning_pipeline(pipeline_payload)
    except PipelineValidationError as exc:
        return platform_error(
            status_code=422,
            error_code="PIPELINE_INPUT_REJECTED",
            message=str(exc),
            scope="reasoning-input",
            request_id=request_id,
            details={},
            next_action="Correct the pipeline input and retry.",
        )
    except Exception:
        return platform_error(
            status_code=500,
            error_code="PIPELINE_EXECUTION_FAILED",
            message="The reasoning pipeline could not complete.",
            scope="platform-runtime",
            request_id=request_id,
            details={},
            next_action=(
                "Preserve the request identifier and review platform logs."
            ),
        )

    return {
        "api_version": API_VERSION,
        "request_id": request_id,
        "result": result,
    }


def load_example_fixture(filename: str) -> dict[str, Any]:
    """Load a deterministic local fixture for development or verification."""

    allowed = {
        "valid-research-cycle.fixture.json",
        "insufficient-evidence.fixture.json",
        "challenged-understanding.fixture.json",
        "prohibited-recommendation.fixture.json",
    }

    if filename not in allowed:
        raise ValueError("Requested example fixture is not permitted.")

    path = FIXTURE_ROOT / filename
    return json.loads(path.read_text(encoding="utf-8"))
