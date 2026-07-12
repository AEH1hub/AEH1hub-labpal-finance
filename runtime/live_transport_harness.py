#!/usr/bin/env python3
"""FI-ASK-003 — deterministic transport failure validation."""

from __future__ import annotations

import json
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from runtime.alpha_vantage_market_price_adapter import (
    ProviderError,
    fetch_raw_quote,
)


class FakeHeaders:
    def get_content_charset(self):
        return "utf-8"


class FakeResponse:
    def __init__(self, body: str):
        self._body = BytesIO(body.encode("utf-8"))
        self.headers = FakeHeaders()

    def read(self):
        return self._body.read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def expect_provider_error(name, side_effect, expected_text):
    try:
        with patch(
            "runtime.alpha_vantage_market_price_adapter.urlopen",
            side_effect=side_effect,
        ):
            fetch_raw_quote("IBM", "test-key")
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


def expect_payload_error(name, body, expected_text):
    try:
        with patch(
            "runtime.alpha_vantage_market_price_adapter.urlopen",
            return_value=FakeResponse(body),
        ):
            fetch_raw_quote("IBM", "test-key")
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


def main():
    results = [
        expect_payload_error(
            "malformed_json",
            "{not-json",
            "Provider returned malformed JSON",
        ),
        expect_provider_error(
            "http_error",
            HTTPError(
                url="https://example.invalid",
                code=503,
                msg="Service Unavailable",
                hdrs=None,
                fp=None,
            ),
            "Provider HTTP error: 503",
        ),
        expect_provider_error(
            "connection_error",
            URLError("network unavailable"),
            "Provider connection error",
        ),
        expect_provider_error(
            "timeout",
            TimeoutError(),
            "Provider request timed out",
        ),
        expect_payload_error(
            "provider_error_message_transport",
            json.dumps({"Error Message": "Invalid API call."}),
            "Provider returned Error Message",
        ),
        expect_payload_error(
            "provider_information_transport",
            json.dumps({"Information": "API call frequency exceeded."}),
            "Provider returned Information",
        ),
        expect_payload_error(
            "provider_note_transport",
            json.dumps({"Note": "Rate limit reached."}),
            "Provider returned Note",
        ),
    ]

    status = "PASS" if all(item["valid"] for item in results) else "FAIL"

    print(
        json.dumps(
            {
                "milestone": "FI-ASK-003-TRANSPORT",
                "status": status,
                "transport_validation": results,
            },
            indent=2,
        )
    )

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
