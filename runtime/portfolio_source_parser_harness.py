"""Deterministic and adversarial harness for PU-INGEST-001B."""

from __future__ import annotations

import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from runtime.portfolio_source_parser import (
    PortfolioSourceParserError,
    parse_portfolio_source,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-ingestion"
    / "source-export-redacted.fixture.csv"
)
EXPECTED_PATH = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-ingestion"
    / "source-export-expected.fixture.json"
)
SCHEMA_PATH = (
    ROOT_DIR
    / "schemas"
    / "portfolio-snapshot.v0.1-pu.schema.json"
)
IMPORTED_AT = datetime(2026, 7, 24, 18, 5, tzinfo=timezone.utc)


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema_errors(payload: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    return sorted(
        error.message for error in validator.iter_errors(payload)
    )


def _expect_rejection(
    source_text: str,
    *,
    expected_message: str,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary_directory:
        source_path = Path(temporary_directory) / "synthetic-invalid.csv"
        source_path.write_text(source_text, encoding="utf-8")
        before_hash = _source_hash(source_path)
        observed_message = ""
        rejected = False

        try:
            parse_portfolio_source(
                source_path,
                imported_at=IMPORTED_AT,
            )
        except (PortfolioSourceParserError, ValueError) as exc:
            rejected = True
            observed_message = str(exc)

        after_hash = _source_hash(source_path)

    return {
        "rejected": rejected,
        "expected_message_present": (
            expected_message.lower() in observed_message.lower()
        ),
        "source_unchanged": before_hash == after_hash,
        "no_partial_result": rejected,
        "observed_message": observed_message,
    }


def main() -> None:
    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    source_hash_before = _source_hash(SOURCE_PATH)
    first_result = parse_portfolio_source(
        SOURCE_PATH,
        imported_at=IMPORTED_AT,
    )
    second_result = parse_portfolio_source(
        SOURCE_PATH,
        imported_at=IMPORTED_AT,
    )
    source_hash_after = _source_hash(SOURCE_PATH)
    first_output = first_result.to_dict()
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    snapshot = first_output["snapshot"]
    schema_errors = _schema_errors(snapshot)

    header, main_row, vuag_row, cash_row = source_text.splitlines()
    missing_column_header = header.replace(",quantity", "")
    missing_column_main = main_row.replace(",2.0000", "")
    duplicate_holding_row = vuag_row.replace("VUAG", "MAIN", 1)
    mixed_currency_row = vuag_row.replace(",CHF,120.00", ",USD,120.00")
    naive_timestamp_row = main_row.replace(
        "2026-07-24T20:00:00+02:00",
        "2026-07-24T20:00:00",
    )
    invalid_decimal_row = main_row.replace(",2.0000,", ",not-a-decimal,")
    formula_name_row = main_row.replace(
        "Main Street Capital",
        "=FORMULA",
    )
    cash_with_symbol = cash_row.replace(",,,,12.50", ",CASH,,,12.50")

    adversarial_cases = {
        "missing_required_column": _expect_rejection(
            "\n".join(
                (
                    missing_column_header,
                    missing_column_main,
                    vuag_row,
                    cash_row,
                )
            )
            + "\n",
            expected_message="missing required columns",
        ),
        "malformed_decimal": _expect_rejection(
            "\n".join((header, invalid_decimal_row, vuag_row, cash_row))
            + "\n",
            expected_message="valid decimal",
        ),
        "timezone_naive": _expect_rejection(
            "\n".join((header, naive_timestamp_row, vuag_row, cash_row))
            + "\n",
            expected_message="timezone information",
        ),
        "duplicate_row": _expect_rejection(
            "\n".join((header, main_row, main_row, cash_row)) + "\n",
            expected_message="duplicates an earlier row",
        ),
        "duplicate_holding": _expect_rejection(
            "\n".join(
                (header, main_row, duplicate_holding_row, cash_row)
            )
            + "\n",
            expected_message="duplicates holding",
        ),
        "mixed_currency": _expect_rejection(
            "\n".join((header, main_row, mixed_currency_row, cash_row))
            + "\n",
            expected_message="explicit FX evidence",
        ),
        "formula_like_text": _expect_rejection(
            "\n".join((header, formula_name_row, vuag_row, cash_row))
            + "\n",
            expected_message="formula-like",
        ),
        "cash_holding_fields": _expect_rejection(
            "\n".join((header, main_row, vuag_row, cash_with_symbol))
            + "\n",
            expected_message="holding-only fields",
        ),
    }

    checks = {
        "milestone": first_output["milestone"] == "PU-INGEST-001B",
        "deterministic_output": first_output == second_result.to_dict(),
        "expected_fixture_parity": first_output == expected,
        "snapshot_schema_valid": not schema_errors,
        "source_unchanged": (
            source_hash_before
            == source_hash_after
            == snapshot["source"]["provenance"]["source_sha256"]
        ),
        "source_read_only": snapshot["source"]["read_only"] is True,
        "decimal_strings_preserved": (
            snapshot["holdings"][0]["quantity"] == "2.0000"
        ),
        "currency_explicit": snapshot["base_currency"] == "CHF",
        "timestamp_timezone_explicit": (
            snapshot["observed_at"] == "2026-07-24T18:00:00+00:00"
        ),
        "holding_rows_parsed": len(snapshot["holdings"]) == 2,
        "cash_row_parsed": len(snapshot["cash_balances"]) == 1,
        "total_reconciles": (
            snapshot["total_value"]["amount"] == "246.40"
        ),
        "unknown_preserved": (
            snapshot["holdings"][0]["unknowns"][0]["reason"]
            == "SOURCE_FIELD_EMPTY"
        ),
        "row_provenance_preserved": (
            [item["source_row_number"] for item in first_output["row_provenance"]]
            == [4, 2, 3]
        ),
        "field_provenance_preserved": all(
            "market_value" in item["source_fields"]
            for item in first_output["row_provenance"]
        ),
        "recommendations_prohibited": (
            first_output["recommendations_prohibited"] is True
        ),
        "execution_prohibited": (
            first_output["execution_prohibited"] is True
        ),
        "adversarial_cases_rejected": all(
            all(
                case_result[key]
                for key in (
                    "rejected",
                    "expected_message_present",
                    "source_unchanged",
                    "no_partial_result",
                )
            )
            for case_result in adversarial_cases.values()
        ),
    }

    valid = all(checks.values())
    report = {
        "milestone": "PU-INGEST-001B",
        "status": "PASS" if valid else "FAIL",
        "checks": checks,
        "schema_errors": schema_errors,
        "adversarial_cases": adversarial_cases,
        "accepted_source": "LABPAL_NEUTRAL_CSV",
        "boundaries": {
            "read_only": True,
            "synthetic_or_redacted_only": True,
            "currency_conversion": False,
            "recommendations": False,
            "execution": False,
        },
    }

    print(json.dumps(report, indent=2, sort_keys=True))

    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
