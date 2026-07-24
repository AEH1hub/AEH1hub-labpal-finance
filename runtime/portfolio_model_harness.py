"""Deterministic verification harness for PU-INGEST-001A."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from runtime.portfolio_model import (
    Holding,
    Money,
    PortfolioSnapshot,
    PortfolioSource,
    SourceProvenance,
    SourceType,
    Unknown,
    UnknownReason,
    model_contract,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT_DIR / "schemas" / "portfolio-snapshot.v0.1-pu.schema.json"
FIXTURE_PATH = (
    ROOT_DIR
    / "fixtures"
    / "portfolio-ingestion"
    / "founder-portfolio-expected.fixture.json"
)


def build_snapshot() -> PortfolioSnapshot:
    observed_at = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)

    source = PortfolioSource(
        source_id="SOURCE-FOUNDER-001",
        provider_name="FOUNDER_FIXTURE",
        source_type=SourceType.MANUAL_FIXTURE,
        account_reference="ACCOUNT-REDACTED-001",
        read_only=True,
        provenance=SourceProvenance(
            source_filename="founder-portfolio-export.fixture.csv",
            source_sha256="a" * 64,
            imported_at=datetime(
                2026,
                7,
                19,
                12,
                5,
                tzinfo=timezone.utc,
            ),
            source_row_count=2,
        ),
    )

    holdings = (
        Holding(
            holding_id="HOLDING-VUAG-001",
            symbol="VUAG",
            name="Vanguard S&P 500 UCITS ETF",
            quantity=Decimal("1.2500"),
            market_value=Money(
                amount=Decimal("125.50"),
                currency="CHF",
            ),
            weight=Decimal(
                "0.5437229437229437229437229437"
            ),
            observed_at=observed_at,
            average_entry_price=Money(
                amount=Decimal("91.20"),
                currency="CHF",
            ),
        ),
        Holding(
            holding_id="HOLDING-MAIN-001",
            symbol="MAIN",
            name="Main Street Capital",
            quantity=Decimal("2.0000"),
            market_value=Money(
                amount=Decimal("105.40"),
                currency="CHF",
            ),
            weight=Decimal(
                "0.4562770562770562770562770563"
            ),
            observed_at=observed_at,
            average_entry_price=None,
            unknowns=(
                Unknown(
                    field_name="average_entry_price",
                    reason=UnknownReason.SOURCE_FIELD_EMPTY,
                    source_detail=(
                        "The source row did not contain "
                        "an average entry price."
                    ),
                ),
            ),
        ),
    )

    return PortfolioSnapshot(
        snapshot_id="SNAPSHOT-FOUNDER-001",
        portfolio_id="PORTFOLIO-FOUNDER-001",
        base_currency="CHF",
        observed_at=observed_at,
        source=source,
        holdings=holdings,
        cash_balances=(),
        total_value=Money(
            amount=Decimal("230.90"),
            currency="CHF",
        ),
    )


def validate_schema(payload: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    return sorted(
        error.message
        for error in validator.iter_errors(payload)
    )


def main() -> None:
    snapshot = build_snapshot()
    first_output = snapshot.to_dict()
    second_output = snapshot.to_dict()

    expected = json.loads(
        FIXTURE_PATH.read_text(encoding="utf-8")
    )

    schema_errors = validate_schema(first_output)

    checks = {
        "milestone": (
            model_contract()["milestone"] == "PU-INGEST-001A"
        ),
        "deterministic_serialization": first_output == second_output,
        "fixture_parity": first_output == expected,
        "schema_valid": not schema_errors,
        "source_read_only": first_output["source"]["read_only"] is True,
        "provenance_preserved": (
            first_output["source"]["provenance"]["source_sha256"]
            == "a" * 64
        ),
        "currency_explicit": (
            first_output["total_value"]["currency"] == "CHF"
        ),
        "timestamp_explicit": (
            first_output["observed_at"]
            == "2026-07-19T12:00:00+00:00"
        ),
        "unknown_preserved": (
            first_output["holdings"][0]["unknowns"][0]["reason"]
            == "SOURCE_FIELD_EMPTY"
        ),
        "execution_prohibited": (
            model_contract()["properties"]["allows_execution"]
            is False
        ),
        "recommendations_prohibited": (
            model_contract()["properties"]["allows_recommendations"]
            is False
        ),
    }

    valid = all(checks.values())

    report = {
        "milestone": "PU-INGEST-001A",
        "status": "PASS" if valid else "FAIL",
        "checks": checks,
        "schema_errors": schema_errors,
        "entity_contract": model_contract(),
    }

    print(json.dumps(report, indent=2, sort_keys=True))

    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
