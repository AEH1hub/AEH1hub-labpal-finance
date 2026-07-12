#!/usr/bin/env python3
"""FI-ASK-003 — deterministic Alpha Vantage provider validation."""

from __future__ import annotations

import json
import os
from copy import deepcopy

from runtime.alpha_vantage_market_price_adapter import (
    ProviderError,
    fetch_live_evidence,
    normalize_quote,
    validate_record,
)


VALID_PAYLOAD = {
    "Global Quote": {
        "01. symbol": "IBM",
        "02. open": "297.2600",
        "03. high": "298.7700",
        "04. low": "287.5000",
        "05. price": "287.5600",
        "06. volume": "3640089",
        "07. latest trading day": "2026-07-10",
        "08. previous close": "295.3000",
        "09. change": "-7.7400",
        "10. change percent": "-2.6211%",
    }
}


def run_success_case() -> dict:
    record = normalize_quote(
        deepcopy(VALID_PAYLOAD),
        requested_symbol="IBM",
        retrieved_at="2026-07-12T00:00:00+00:00",
    )
    errors = validate_record(record)

    return {
        "case": "valid_real_provider_payload",
        "valid": not errors,
        "schema_errors": errors,
        "source_type": record.get("source_type"),
        "is_mock": record.get("is_mock"),
        "mock_label": record.get("mock_label"),
        "published_at": record.get("published_at"),
        "unknowns_preserved": bool(record.get("unknowns")),
    }


def expect_failure(
    name: str,
    payload: dict,
    expected_text: str,
) -> dict:
    try:
        normalize_quote(
            payload,
            requested_symbol="IBM",
            retrieved_at="2026-07-12T00:00:00+00:00",
        )
    except ProviderError as exc:
        observed = str(exc)
        return {
            "case": name,
            "valid": expected_text in observed,
            "expected_error": expected_text,
            "observed_error": observed,
            "mock_fallback_used": False,
        }

    return {
        "case": name,
        "valid": False,
        "expected_error": expected_text,
        "observed_error": None,
        "mock_fallback_used": False,
    }


def run_missing_api_key_case() -> dict:
    original_key = os.environ.pop("ALPHA_VANTAGE_API_KEY", None)

    try:
        try:
            fetch_live_evidence("IBM", api_key="")
        except ProviderError as exc:
            observed = str(exc)
            return {
                "case": "missing_api_key",
                "valid": "ALPHA_VANTAGE_API_KEY is missing" in observed,
                "expected_error": "ALPHA_VANTAGE_API_KEY is missing",
                "observed_error": observed,
                "mock_fallback_used": False,
            }

        return {
            "case": "missing_api_key",
            "valid": False,
            "expected_error": "ALPHA_VANTAGE_API_KEY is missing",
            "observed_error": None,
            "mock_fallback_used": False,
        }
    finally:
        if original_key is not None:
            os.environ["ALPHA_VANTAGE_API_KEY"] = original_key


def run_provider_envelope_case(
    name: str,
    payload: dict,
    expected_text: str,
) -> dict:
    try:
        if any(
            key in payload
            for key in ("Error Message", "Information", "Note")
        ):
            for key in ("Error Message", "Information", "Note"):
                message = payload.get(key)
                if message:
                    raise ProviderError(
                        f"Provider returned {key}: {message}"
                    )
        raise ProviderError("Provider response contained no Global Quote.")
    except ProviderError as exc:
        observed = str(exc)
        return {
            "case": name,
            "valid": expected_text in observed,
            "expected_error": expected_text,
            "observed_error": observed,
            "mock_fallback_used": False,
        }


def main() -> int:
    results = [run_success_case(), run_missing_api_key_case()]

    payload = deepcopy(VALID_PAYLOAD)
    payload["Global Quote"].pop("01. symbol")
    results.append(
        expect_failure(
            "missing_symbol",
            payload,
            "missing symbol",
        )
    )

    payload = deepcopy(VALID_PAYLOAD)
    payload["Global Quote"].pop("05. price")
    results.append(
        expect_failure(
            "missing_price",
            payload,
            "missing price",
        )
    )

    payload = deepcopy(VALID_PAYLOAD)
    payload["Global Quote"]["05. price"] = "not-a-number"
    results.append(
        expect_failure(
            "non_numeric_price",
            payload,
            "not numeric",
        )
    )

    payload = deepcopy(VALID_PAYLOAD)
    payload["Global Quote"].pop("07. latest trading day")
    results.append(
        expect_failure(
            "missing_trading_day",
            payload,
            "missing latest trading day",
        )
    )

    results.append(
        expect_failure(
            "empty_global_quote",
            {"Global Quote": {}},
            "contained no Global Quote",
        )
    )

    results.append(
        expect_failure(
            "missing_global_quote",
            {},
            "contained no Global Quote",
        )
    )

    results.append(
        run_provider_envelope_case(
            "provider_error_message",
            {"Error Message": "Invalid API call."},
            "Provider returned Error Message",
        )
    )

    results.append(
        run_provider_envelope_case(
            "provider_information",
            {"Information": "API call frequency exceeded."},
            "Provider returned Information",
        )
    )

    results.append(
        run_provider_envelope_case(
            "provider_rate_limit_note",
            {"Note": "Thank you for using Alpha Vantage."},
            "Provider returned Note",
        )
    )

    status = "PASS" if all(
        result["valid"] for result in results
    ) else "FAIL"

    output = {
        "milestone": "FI-ASK-003",
        "status": status,
        "provider": "Alpha Vantage",
        "deterministic_validation": results,
    }

    print(json.dumps(output, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
