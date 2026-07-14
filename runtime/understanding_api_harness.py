"""Deterministic harness for LU-001 Understanding Platform."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx

from runtime.understanding_api import (
    app,
    load_example_fixture,
)
from runtime.unified_reasoning_pipeline import (
    run_reasoning_pipeline,
)


async def request(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    **kwargs: Any,
) -> httpx.Response:
    return await client.request(method, path, **kwargs)


def parity_fields(result: dict[str, Any]) -> dict[str, Any]:
    """Return reasoning fields that transport must preserve."""

    keys = [
        "preserved_question",
        "evidence_considered",
        "supporting_evidence",
        "challenging_evidence",
        "excluded_evidence",
        "unknowns",
        "contradictions",
        "claims",
        "current_understanding",
        "decision_state",
        "review_state",
        "reasoning_summary",
        "next_evidence_needed",
        "history_preserved",
        "validation_results",
    ]

    return {
        key: result[key]
        for key in keys
    }


async def main() -> int:
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://labpal.test",
    ) as client:
        cases: list[dict[str, Any]] = []

        health = await request(
            client,
            "GET",
            "/v1/health",
        )
        cases.append({
            "case": "health",
            "valid": (
                health.status_code == 200
                and health.json()["status"] == "available"
                and health.json()["reasoning_dependency"]
                == "FI-REAS-001"
            ),
        })

        capabilities = await request(
            client,
            "GET",
            "/v1/capabilities",
        )
        capabilities_body = capabilities.json()

        earned_capabilities = {
            item["capability"]: item
            for item in capabilities_body["earned"]
        }

        lu001_capability = earned_capabilities.get(
            "LU-001_UNDERSTANDING_PLATFORM",
            {},
        )

        cases.append({
            "case": "capabilities",
            "valid": (
                capabilities.status_code == 200
                and capabilities_body["version"] == "v1"
                and capabilities_body["in_progress"] == []
                and lu001_capability.get("state") == "MERGED"
                and lu001_capability.get("repository_state")
                == "MERGED"
                and lu001_capability.get("external_proof")
                == "NOT_EARNED"
                and "LU-001_EXTERNALLY_PROVEN"
                in capabilities_body["not_earned"]
                and "LU-001_MERGED"
                not in capabilities_body["not_earned"]
            ),
        })

        examples = await request(
            client,
            "GET",
            "/v1/examples",
        )
        examples_body = examples.json()

        cases.append({
            "case": "examples",
            "valid": (
                examples.status_code == 200
                and examples_body["label"]
                == "DETERMINISTIC_FIXTURES_NOT_LIVE_EVIDENCE"
                and len(examples_body["examples"]) == 4
            ),
        })

        fixture_cases = [
            (
                "valid_research_cycle",
                "valid-research-cycle.fixture.json",
                200,
                "READY_FOR_REVIEW",
            ),
            (
                "insufficient_evidence",
                "insufficient-evidence.fixture.json",
                200,
                "INSUFFICIENT_EVIDENCE",
            ),
            (
                "challenged_understanding",
                "challenged-understanding.fixture.json",
                200,
                "REVISION_REQUIRED",
            ),
            (
                "prohibited_recommendation",
                "prohibited-recommendation.fixture.json",
                200,
                "REVISION_REQUIRED",
            ),
        ]

        for (
            case_name,
            filename,
            expected_status,
            expected_decision,
        ) in fixture_cases:
            payload = load_example_fixture(filename)
            direct_result = run_reasoning_pipeline(payload)

            response = await request(
                client,
                "POST",
                "/v1/reason",
                json=payload,
                headers={
                    "x-request-id": f"LU-001-{case_name}",
                },
            )

            response_body = response.json()
            api_result = response_body.get("result", {})

            cases.append({
                "case": case_name,
                "expected_http_status": expected_status,
                "observed_http_status": response.status_code,
                "expected_decision": expected_decision,
                "observed_decision": api_result.get(
                    "decision_state"
                ),
                "parity_preserved": (
                    parity_fields(api_result)
                    == parity_fields(direct_result)
                ),
                "valid": (
                    response.status_code == expected_status
                    and api_result.get("decision_state")
                    == expected_decision
                    and parity_fields(api_result)
                    == parity_fields(direct_result)
                ),
            })

        prohibited_payload = load_example_fixture(
            "prohibited-recommendation.fixture.json"
        )

        prohibited_response = await request(
            client,
            "POST",
            "/v1/reason",
            json=prohibited_payload,
        )

        prohibited_result = prohibited_response.json()[
            "result"
        ]

        cases.append({
            "case": "invalid_claim_not_adopted",
            "valid": (
                prohibited_result[
                    "current_understanding"
                ]["selected_claim_id"] is None
                and prohibited_result[
                    "current_understanding"
                ]["current_statement"].startswith(
                    "No admissible Current Understanding"
                )
            ),
        })

        malformed = await request(
            client,
            "POST",
            "/v1/reason",
            json={
                "execution_id": "LU-INVALID-001",
            },
            headers={
                "x-request-id": "LU-INVALID-001",
            },
        )

        malformed_body = malformed.json()

        cases.append({
            "case": "malformed_request",
            "valid": (
                malformed.status_code == 422
                and malformed_body["error"]["error_code"]
                == "REQUEST_VALIDATION_FAILED"
                and malformed_body["error"]["request_id"]
                == "LU-INVALID-001"
                and "traceback"
                not in str(malformed_body).lower()
            ),
        })

        oversized = await request(
            client,
            "POST",
            "/v1/reason",
            content=b"x",
            headers={
                "content-length": "1000001",
                "content-type": "application/json",
                "x-request-id": "LU-OVERSIZED-001",
            },
        )

        oversized_body = oversized.json()

        cases.append({
            "case": "oversized_request",
            "valid": (
                oversized.status_code == 413
                and oversized_body["error"]["error_code"]
                == "REQUEST_VALIDATION_FAILED"
                and oversized_body["error"]["request_id"]
                == "LU-OVERSIZED-001"
                and oversized_body["error"]["details"][
                    "maximum_bytes"
                ] == 1000000
            ),
        })

    status = (
        "PASS"
        if all(case["valid"] for case in cases)
        else "FAIL"
    )

    output = {
        "milestone": "LU-001",
        "status": status,
        "case_count": len(cases),
        "cases": cases,
    }

    print(json.dumps(output, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
