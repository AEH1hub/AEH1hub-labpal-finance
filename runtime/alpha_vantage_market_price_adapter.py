#!/usr/bin/env python3
"""FI-ASK-003 — Alpha Vantage market-price adapter.

Retrieves one GLOBAL_QUOTE response and converts it into a LabPal
Live Evidence Record. It never falls back silently to mock evidence.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from jsonschema import Draft202012Validator, FormatChecker


PROVIDER_NAME = "Alpha Vantage"
BASE_URL = "https://www.alphavantage.co/query"
SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "live-evidence-record.v0.1-ask.schema.json"
)


class ProviderError(RuntimeError):
    """Raised when the live provider cannot produce valid evidence."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _public_source_url(symbol: str) -> str:
    """Return a provenance URL without exposing the API key."""
    return f"{BASE_URL}?function=GLOBAL_QUOTE&symbol={symbol}"


def fetch_raw_quote(
    symbol: str,
    api_key: str,
    timeout_seconds: int = 15,
) -> dict[str, Any]:
    """Fetch one raw GLOBAL_QUOTE response."""

    normalized_symbol = symbol.strip().upper()
    if not normalized_symbol:
        raise ProviderError("Symbol must not be empty.")

    query = urlencode(
        {
            "function": "GLOBAL_QUOTE",
            "symbol": normalized_symbol,
            "apikey": api_key,
        }
    )
    url = f"{BASE_URL}?{query}"

    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset)
    except HTTPError as exc:
        raise ProviderError(
            f"Provider HTTP error: {exc.code} {exc.reason}"
        ) from exc
    except URLError as exc:
        raise ProviderError(
            f"Provider connection error: {exc.reason}"
        ) from exc
    except TimeoutError as exc:
        raise ProviderError("Provider request timed out.") from exc

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ProviderError("Provider returned malformed JSON.") from exc

    if not isinstance(payload, dict):
        raise ProviderError("Provider response must be a JSON object.")

    for provider_error_key in ("Error Message", "Information", "Note"):
        message = payload.get(provider_error_key)
        if message:
            raise ProviderError(
                f"Provider returned {provider_error_key}: {message}"
            )

    return payload


def normalize_quote(
    payload: dict[str, Any],
    requested_symbol: str,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Convert Alpha Vantage GLOBAL_QUOTE JSON into Live Evidence Record."""

    quote = payload.get("Global Quote")
    if not isinstance(quote, dict) or not quote:
        raise ProviderError("Provider response contained no Global Quote.")

    symbol = str(quote.get("01. symbol", "")).strip().upper()
    price = str(quote.get("05. price", "")).strip()
    trading_day = str(
        quote.get("07. latest trading day", "")
    ).strip()
    volume = str(quote.get("06. volume", "")).strip()
    change = str(quote.get("09. change", "")).strip()
    change_percent = str(
        quote.get("10. change percent", "")
    ).strip()

    if not symbol:
        raise ProviderError("Provider response is missing symbol.")
    if not price:
        raise ProviderError("Provider response is missing price.")
    if not trading_day:
        raise ProviderError(
            "Provider response is missing latest trading day."
        )

    try:
        numeric_price = float(price)
    except ValueError as exc:
        raise ProviderError(
            f"Provider price is not numeric: {price!r}"
        ) from exc

    if numeric_price < 0:
        raise ProviderError("Provider price must not be negative.")

    unknowns = [
        "Provider supplied a trading date but no exact quote timestamp.",
        "Provider did not supply the exchange timezone.",
        "Provider did not supply the trading currency.",
        "Provider payload did not identify whether the quote was real-time or delayed.",
    ]

    summary_parts = [
        f"symbol={symbol}",
        f"price={price}",
        f"latest_trading_day={trading_day}",
    ]
    if volume:
        summary_parts.append(f"volume={volume}")
    if change:
        summary_parts.append(f"change={change}")
    if change_percent:
        summary_parts.append(f"change_percent={change_percent}")

    return {
        "evidence_id": (
            f"AV-GLOBAL-QUOTE-{symbol}-{trading_day}"
        ),
        "source_name": PROVIDER_NAME,
        "source_url": _public_source_url(symbol),
        "source_type": "MARKET_PRICE",
        "retrieved_at": retrieved_at or _utc_now(),
        "published_at": None,
        "freshness_state": "RECENT",
        "asset_or_topic": symbol,
        "claim_text": (
            f"{symbol} had a provider-reported price of {price} "
            f"for the latest trading day {trading_day}."
        ),
        "claim_classification": "SOURCE_FACT",
        "source_quote_or_summary": "; ".join(summary_parts),
        "labpal_notes": (
            "Real Alpha Vantage GLOBAL_QUOTE response. "
            "No recommendation or suitability conclusion."
        ),
        "unknowns": unknowns,
        "reliability_notes": (
            "Provider response preserved as received. "
            "Exact quote time, exchange timezone, currency, and "
            "real-time/delayed status were not supplied in the payload."
        ),
        "is_mock": False,
        "mock_label": None,
    }


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return schema-validation errors for one evidence record."""

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    return sorted(
        error.message
        for error in validator.iter_errors(record)
    )


def fetch_live_evidence(
    symbol: str,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Fetch, normalize, and validate one live evidence record."""

    key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
    if not key:
        raise ProviderError(
            "ALPHA_VANTAGE_API_KEY is missing."
        )

    payload = fetch_raw_quote(symbol, key)
    record = normalize_quote(payload, symbol)

    errors = validate_record(record)
    if errors:
        raise ProviderError(
            "Live Evidence Record failed schema validation: "
            + " | ".join(errors)
        )

    return record


def main() -> int:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "IBM"

    try:
        record = fetch_live_evidence(symbol)
    except ProviderError as exc:
        print(
            json.dumps(
                {
                    "milestone": "FI-ASK-003",
                    "status": "FAIL",
                    "error": str(exc),
                    "mock_fallback_used": False,
                },
                indent=2,
            )
        )
        return 1

    print(
        json.dumps(
            {
                "milestone": "FI-ASK-003",
                "status": "PASS",
                "provider": PROVIDER_NAME,
                "record": record,
                "mock_fallback_used": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
