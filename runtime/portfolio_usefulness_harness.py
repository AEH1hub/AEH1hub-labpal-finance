"""Deterministic verification harness for PU-VALIDATE-001A."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from runtime.portfolio_usefulness import (
    build_usefulness_report,
)


ROOT_DIR = Path(__file__).resolve().parents[1]

SNAPSHOT_SCHEMA_PATH = (
    ROOT_DIR
    / "schemas"
    / "portfolio-snapshot.v0.1-pu.schema.json"
)

REPORT_SCHEMA_PATH = (
    ROOT_DIR
    / "schemas"
    / "portfolio-usefulness-report.v0.1-pu.schema.json"
)

FIXTURE_DIR = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-validation"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(
    payload: dict[str, Any],
    schema_path: Path,
) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)

    return sorted(
        error.message
        for error in validator.iter_errors(payload)
    )


def main() -> None:
    before = load_json(
        FIXTURE_DIR / "founder-before.fixture.json"
    )
    after = load_json(
        FIXTURE_DIR / "founder-after.fixture.json"
    )
    expected = load_json(
        FIXTURE_DIR
        / "founder-usefulness-expected.fixture.json"
    )

    first_report = build_usefulness_report(
        before,
        after,
        scenario_id="FOUNDER-SYNTHETIC-CHANGE-001",
    )

    second_report = build_usefulness_report(
        before,
        after,
        scenario_id="FOUNDER-SYNTHETIC-CHANGE-001",
    )

    before_errors = schema_errors(
        before,
        SNAPSHOT_SCHEMA_PATH,
    )
    after_errors = schema_errors(
        after,
        SNAPSHOT_SCHEMA_PATH,
    )
    report_errors = schema_errors(
        first_report,
        REPORT_SCHEMA_PATH,
    )

    contributors = {
        item["holding_id"]: item
        for item in first_report["contributors"]
    }

    checks = {
        "milestone": (
            first_report["milestone"]
            == "PU-VALIDATE-001A"
        ),
        "before_snapshot_schema_valid": not before_errors,
        "after_snapshot_schema_valid": not after_errors,
        "report_schema_valid": not report_errors,
        "deterministic_output": (
            first_report == second_report
        ),
        "expected_fixture_parity": (
            first_report == expected
        ),
        "portfolio_change_correct": (
            first_report["portfolio_value_change"]
            == {
                "amount": "3.00",
                "currency": "CHF",
            }
        ),
        "positive_contributor_correct": (
            contributors["HOLDING-MAIN-001"]["direction"]
            == "POSITIVE"
            and contributors["HOLDING-MAIN-001"]["change"][
                "amount"
            ]
            == "7.00"
        ),
        "negative_contributor_correct": (
            contributors["HOLDING-VUAG-001"]["direction"]
            == "NEGATIVE"
            and contributors["HOLDING-VUAG-001"]["change"][
                "amount"
            ]
            == "-4.00"
        ),
        "largest_contributor_correct": (
            first_report["largest_absolute_contributor"]
            == "HOLDING-MAIN-001"
        ),
        "facts_evidence_linked": all(
            fact["evidence_refs"]
            for fact in first_report["supported_facts"]
        ),
        "causal_claim_not_fabricated": (
            first_report["causal_explanation"]["state"]
            == "INSUFFICIENT_EVIDENCE"
            and first_report["causal_explanation"]["claim"]
            is None
        ),
        "source_unknown_preserved": (
            {
                "holding_id": "HOLDING-MAIN-001",
                "field_name": "average_entry_price",
                "reason": "SOURCE_FIELD_EMPTY",
            }
            in first_report["preserved_source_unknowns"]
        ),
        "evidence_limitations_explicit": bool(
            first_report["evidence_limitations"]
        ),
        "recommendations_prohibited": (
            first_report["recommendations_prohibited"]
            is True
        ),
        "execution_prohibited": (
            first_report["execution_prohibited"]
            is True
        ),
    }

    valid = all(checks.values())

    output = {
        "milestone": "PU-VALIDATE-001A",
        "status": "PASS" if valid else "FAIL",
        "checks": checks,
        "schema_errors": {
            "before": before_errors,
            "after": after_errors,
            "report": report_errors,
        },
        "report": first_report,
    }

    print(json.dumps(output, indent=2, sort_keys=True))

    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
