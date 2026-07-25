"""Deterministic and fail-closed harness for PU-UNDERSTAND-001A."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker

from runtime.portfolio_understanding import (
    PortfolioUnderstandingError,
    build_portfolio_understanding,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_FIXTURE_PATH = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-ingestion"
    / "source-export-expected.fixture.json"
)
EXPECTED_PATH = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-understanding"
    / "current-portfolio-expected.fixture.json"
)
SNAPSHOT_SCHEMA_PATH = (
    ROOT_DIR
    / "schemas"
    / "portfolio-snapshot.v0.1-pu.schema.json"
)
UNDERSTANDING_SCHEMA_PATH = (
    ROOT_DIR
    / "schemas"
    / "portfolio-understanding.v0.1-pu.schema.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_errors(
    payload: dict[str, Any],
    schema_path: Path,
) -> list[str]:
    validator = Draft202012Validator(
        _load_json(schema_path),
        format_checker=FormatChecker(),
    )
    return sorted(
        error.message for error in validator.iter_errors(payload)
    )


def _expect_rejection(
    snapshot: dict[str, Any],
    mutation: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    malformed = copy.deepcopy(snapshot)
    mutation(malformed)
    before = copy.deepcopy(malformed)
    rejected = False
    observed_message = ""

    try:
        build_portfolio_understanding(malformed)
    except PortfolioUnderstandingError as exc:
        rejected = True
        observed_message = str(exc)

    return {
        "rejected": rejected,
        "input_unchanged": malformed == before,
        "no_partial_result": rejected,
        "observed_message": observed_message,
    }


def _remove_total_value(snapshot: dict[str, Any]) -> None:
    del snapshot["total_value"]


def _break_total_reconciliation(snapshot: dict[str, Any]) -> None:
    snapshot["total_value"]["amount"] = "999.99"


def _remove_required_unknown(snapshot: dict[str, Any]) -> None:
    snapshot["holdings"][0]["unknowns"] = []


def _all_statement_objects_are_evidence_linked(value: Any) -> bool:
    if isinstance(value, dict):
        if "statement" in value:
            evidence_refs = value.get("evidence_refs")

            if not isinstance(evidence_refs, list) or not evidence_refs:
                return False

        return all(
            _all_statement_objects_are_evidence_linked(item)
            for item in value.values()
        )

    if isinstance(value, list):
        return all(
            _all_statement_objects_are_evidence_linked(item)
            for item in value
        )

    return True


def main() -> None:
    parser_output = _load_json(SOURCE_FIXTURE_PATH)
    snapshot = parser_output["snapshot"]
    snapshot_before = copy.deepcopy(snapshot)
    expected = _load_json(EXPECTED_PATH)

    first = build_portfolio_understanding(snapshot)
    second = build_portfolio_understanding(snapshot)
    snapshot_errors = _schema_errors(snapshot, SNAPSHOT_SCHEMA_PATH)
    understanding_errors = _schema_errors(
        first,
        UNDERSTANDING_SCHEMA_PATH,
    )
    holdings = {
        item["symbol"]: item for item in first["holding_summaries"]
    }
    malformed_cases = {
        "missing_required_field": _expect_rejection(
            snapshot,
            _remove_total_value,
        ),
        "unreconciled_total": _expect_rejection(
            snapshot,
            _break_total_reconciliation,
        ),
        "missing_canonical_unknown": _expect_rejection(
            snapshot,
            _remove_required_unknown,
        ),
    }
    serialized_first = json.dumps(
        first,
        sort_keys=True,
        separators=(",", ":"),
    )
    serialized_second = json.dumps(
        second,
        sort_keys=True,
        separators=(",", ":"),
    )
    required_output_fields = {
        "understanding_id",
        "version",
        "portfolio_id",
        "subject",
        "scope",
        "observed_at",
        "review_state",
        "current_understanding",
        "supported_facts",
        "portfolio_composition",
        "holding_summaries",
        "cash_summary",
        "unknowns",
        "limitations",
        "evidence_required",
        "review_next",
        "source_provenance",
        "recommendations_prohibited",
        "execution_prohibited",
    }

    checks = {
        "milestone": first["version"] == "0.1-pu",
        "canonical_input_schema_valid": not snapshot_errors,
        "understanding_schema_valid": not understanding_errors,
        "expected_fixture_parity": first == expected,
        "deterministic_output": (
            first == second and serialized_first == serialized_second
        ),
        "source_input_unchanged": snapshot == snapshot_before,
        "browser_contract_complete": set(first) == required_output_fields,
        "total_value_correct": (
            first["portfolio_composition"]["total_value"]
            == {"amount": "246.40", "currency": "CHF"}
        ),
        "holding_count_correct": (
            first["portfolio_composition"]["holding_count"] == 2
            and len(first["holding_summaries"]) == 2
        ),
        "cash_value_correct": (
            first["cash_summary"]["total"]
            == {"amount": "12.50", "currency": "CHF"}
        ),
        "main_weight_preserved": (
            holdings["MAIN"]["weight"]
            == snapshot["holdings"][0]["weight"]
        ),
        "vuag_weight_preserved": (
            holdings["VUAG"]["weight"]
            == snapshot["holdings"][1]["weight"]
        ),
        "main_average_entry_unknown": (
            holdings["MAIN"]["average_entry_price"] is None
            and any(
                unknown["subject_ref"] == "HOLDING-MAIN-001"
                and unknown["field_name"] == "average_entry_price"
                and unknown["reason"] == "SOURCE_FIELD_EMPTY"
                for unknown in first["unknowns"]
            )
        ),
        "all_factual_statements_evidence_linked": (
            _all_statement_objects_are_evidence_linked(first)
        ),
        "source_provenance_visible": (
            first["source_provenance"] == snapshot["source"]
        ),
        "synthetic_redacted_limitation_visible": any(
            item["limitation_id"] == "LIMITATION-SYNTHETIC-REDACTED"
            and "synthetic/redacted" in item["statement"]
            for item in first["limitations"]
        ),
        "holding_value_reasons_not_invented": all(
            item["reason_for_value"]["state"] == "UNKNOWN"
            and item["reason_for_value"]["claim"] is None
            for item in first["holding_summaries"]
        ),
        "diversification_conclusion_not_invented": any(
            item["limitation_id"]
            == "LIMITATION-NO-DIVERSIFICATION-JUDGMENT"
            and item["statement"].startswith(
                "No diversification conclusion is supported"
            )
            for item in first["limitations"]
        ),
        "recommendations_prohibited": (
            first["recommendations_prohibited"] is True
        ),
        "execution_prohibited": first["execution_prohibited"] is True,
        "ready_for_review_not_approval": (
            first["review_state"] == "READY_FOR_REVIEW"
            and first["current_understanding"]["approval_status"]
            == "NOT_APPROVED"
            and "does not mean" in first["current_understanding"][
                "review_state_meaning"
            ]
        ),
        "malformed_input_fails_closed": all(
            case["rejected"]
            and case["input_unchanged"]
            and case["no_partial_result"]
            for case in malformed_cases.values()
        ),
    }

    valid = all(checks.values())
    output = {
        "milestone": "PU-UNDERSTAND-001A",
        "status": "PASS" if valid else "FAIL",
        "checks": checks,
        "schema_errors": {
            "canonical_input": snapshot_errors,
            "understanding": understanding_errors,
        },
        "malformed_cases": malformed_cases,
        "understanding": first,
    }

    print(json.dumps(output, indent=2, sort_keys=True))

    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
