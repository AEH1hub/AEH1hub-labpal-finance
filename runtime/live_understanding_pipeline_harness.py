"""Deterministic verification for LU-LIVE-001 orchestration.

This harness uses only preserved provider evidence. It performs no
network requests and requires no provider credentials.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from runtime.live_understanding_pipeline import (
    LiveUnderstandingValidationError,
    run_live_understanding_pipeline,
)


ROOT = Path(__file__).resolve().parents[1]

FIXTURE_PATH = (
    ROOT
    / "fixtures"
    / "live-understanding"
    / "alpha-vantage-ibm-preserved.fixture.json"
)


def load_fixture() -> dict[str, Any]:
    """Load a fresh copy of the preserved provider fixture."""

    return json.loads(
        FIXTURE_PATH.read_text(encoding="utf-8")
    )


def run_pipeline(
    fixture: dict[str, Any],
) -> dict[str, Any]:
    """Invoke LU-LIVE using deterministic fixture metadata."""

    return run_live_understanding_pipeline(
        execution_id="LU-LIVE-EXEC-001",
        executing_actor="LU-LIVE-001-HARNESS",
        provider=fixture["provider"],
        requested_symbol=fixture["requested_symbol"],
        normalized_evidence=fixture["normalized_evidence"],
        market_session_state=fixture[
            "market_session_state"
        ],
        reference_time="2026-07-12T00:00:00+00:00",
        additional_unknowns=[
            (
                "Independent provider agreement has not "
                "been established."
            )
        ],
    )


def check_preserved_provider_success() -> dict[str, Any]:
    """Verify the bounded preserved-provider success path."""

    fixture = load_fixture()
    original_fixture = deepcopy(fixture)
    original_evidence = deepcopy(
        fixture["normalized_evidence"]
    )

    result = run_pipeline(fixture)
    expected = fixture["expected"]

    provider_unknowns = original_evidence.get(
        "unknowns",
        [],
    )

    preserved_unknowns = result.get("unknowns", [])

    checks = {
        "milestone": (
            result.get("milestone") == "LU-LIVE-001"
        ),
        "provider_record_valid": (
            result.get("provider_record_valid")
            is expected["provider_record_valid"]
        ),
        "evidence_classification": (
            result.get("evidence_classification")
            == "LIVE_EVIDENCE"
        ),
        "mock_fallback_not_used": (
            result.get("mock_fallback_used")
            is expected["mock_fallback_used"]
        ),
        "provider_preserved": (
            result.get("provenance", {}).get("provider")
            == fixture["provider"]
        ),
        "requested_symbol_preserved": (
            result.get("provenance", {}).get(
                "requested_symbol"
            )
            == fixture["requested_symbol"]
        ),
        "canonical_freshness": (
            result.get("canonical_freshness", {}).get(
                "state"
            )
            == expected["canonical_freshness_state"]
        ),
        "normalized_evidence_unchanged": (
            fixture["normalized_evidence"]
            == original_evidence
            and result.get("normalized_evidence")
            == original_evidence
        ),
        "fixture_unchanged": (
            fixture == original_fixture
        ),
        "provider_unknowns_preserved": all(
            unknown in preserved_unknowns
            for unknown in provider_unknowns
        ),
        "reasoning_decision_state": (
            result.get("reasoning_decision_state")
            == expected["reasoning_decision_state"]
        ),
        "reasoning_review_state": (
            result.get("reasoning_review_state")
            == expected["reasoning_review_state"]
        ),
        "reasoning_result_present": (
            isinstance(
                result.get("reasoning_result"),
                dict,
            )
            and result["reasoning_result"].get(
                "milestone"
            )
            == "FI-REAS-001"
        ),
        "history_preserved": (
            result.get("history_preserved") is True
        ),
    }

    return {
        "case": "preserved_provider_success",
        "checks": checks,
        "valid": all(checks.values()),
    }


def expect_validation_error(
    *,
    case_name: str,
    fixture: dict[str, Any],
    expected_message: str,
    invocation: Callable[[], dict[str, Any]],
) -> dict[str, Any]:
    """Verify bounded rejection without mutating fixture evidence."""

    original_fixture = deepcopy(fixture)
    observed_message = ""
    error_raised = False
    unexpected_result: dict[str, Any] | None = None

    try:
        unexpected_result = invocation()
    except LiveUnderstandingValidationError as exc:
        error_raised = True
        observed_message = str(exc)

    checks = {
        "validation_error_raised": error_raised,
        "expected_boundary_named": (
            expected_message.lower()
            in observed_message.lower()
        ),
        "no_reasoning_result_returned": (
            unexpected_result is None
        ),
        "fixture_unchanged_after_rejection": (
            fixture == original_fixture
        ),
    }

    return {
        "case": case_name,
        "observed_error": observed_message,
        "checks": checks,
        "valid": all(checks.values()),
    }


def check_mock_evidence_rejected() -> dict[str, Any]:
    """Verify that the live path refuses mock evidence."""

    fixture = load_fixture()
    fixture["normalized_evidence"]["is_mock"] = True
    fixture["normalized_evidence"]["mock_label"] = (
        "MOCK_EVIDENCE — NOT LIVE DATA"
    )

    return expect_validation_error(
        case_name="mock_evidence_rejected",
        fixture=fixture,
        expected_message="mock evidence",
        invocation=lambda: run_pipeline(fixture),
    )


def check_invalid_evidence_rejected() -> dict[str, Any]:
    """Verify rejection of schema-invalid evidence."""

    fixture = load_fixture()

    fixture["normalized_evidence"].pop(
        "evidence_id",
        None,
    )

    return expect_validation_error(
        case_name="invalid_evidence_rejected",
        fixture=fixture,
        expected_message="schema validation",
        invocation=lambda: run_pipeline(fixture),
    )


def check_missing_evidence_rejected() -> dict[str, Any]:
    """Verify rejection when no usable evidence record is supplied."""

    fixture = load_fixture()
    fixture["normalized_evidence"] = {}

    return expect_validation_error(
        case_name="missing_evidence_rejected",
        fixture=fixture,
        expected_message="normalized evidence",
        invocation=lambda: run_pipeline(fixture),
    )


def check_provider_identity_mismatch_rejected() -> dict[str, Any]:
    """Verify rejection when provider identity does not agree."""

    fixture = load_fixture()
    fixture["provider"] = "Different Provider"

    return expect_validation_error(
        case_name="provider_identity_mismatch_rejected",
        fixture=fixture,
        expected_message="provider",
        invocation=lambda: run_pipeline(fixture),
    )


def check_symbol_mismatch_rejected() -> dict[str, Any]:
    """Verify rejection when the returned subject differs."""

    fixture = load_fixture()
    fixture["requested_symbol"] = "AAPL"

    return expect_validation_error(
        case_name="symbol_mismatch_rejected",
        fixture=fixture,
        expected_message="requested_symbol",
        invocation=lambda: run_pipeline(fixture),
    )


def check_repeated_call_non_mutation() -> dict[str, Any]:
    """Verify repeated orchestration never mutates preserved input."""

    fixture = load_fixture()
    original_fixture = deepcopy(fixture)
    original_evidence = deepcopy(
        fixture["normalized_evidence"]
    )

    first_result = run_pipeline(fixture)
    second_result = run_pipeline(fixture)
    third_result = run_pipeline(fixture)

    checks = {
        "fixture_unchanged": (
            fixture == original_fixture
        ),
        "evidence_unchanged": (
            fixture["normalized_evidence"]
            == original_evidence
        ),
        "first_result_preserved": (
            first_result.get("normalized_evidence")
            == original_evidence
        ),
        "second_result_preserved": (
            second_result.get("normalized_evidence")
            == original_evidence
        ),
        "third_result_preserved": (
            third_result.get("normalized_evidence")
            == original_evidence
        ),
        "decision_state_stable": (
            first_result.get("reasoning_decision_state")
            == second_result.get("reasoning_decision_state")
            == third_result.get("reasoning_decision_state")
            == "READY_FOR_REVIEW"
        ),
        "review_state_stable": (
            first_result.get("reasoning_review_state")
            == second_result.get("reasoning_review_state")
            == third_result.get("reasoning_review_state")
            == "READY_FOR_REVIEW"
        ),
        "history_preserved": all(
            result.get("history_preserved") is True
            for result in (
                first_result,
                second_result,
                third_result,
            )
        ),
    }

    return {
        "case": "repeated_call_non_mutation",
        "checks": checks,
        "valid": all(checks.values()),
    }


def main() -> int:
    """Execute the current LU-LIVE-001 deterministic suite."""

    cases = [
        check_preserved_provider_success(),
        check_mock_evidence_rejected(),
        check_invalid_evidence_rejected(),
        check_missing_evidence_rejected(),
        check_provider_identity_mismatch_rejected(),
        check_symbol_mismatch_rejected(),
        check_repeated_call_non_mutation(),
    ]

    status = (
        "PASS"
        if all(case["valid"] for case in cases)
        else "FAIL"
    )

    output = {
        "milestone": "LU-LIVE-001",
        "status": status,
        "case_count": len(cases),
        "cases": cases,
    }

    print(json.dumps(output, indent=2))

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
