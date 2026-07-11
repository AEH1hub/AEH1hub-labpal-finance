#!/usr/bin/env python3
"""FI-ASK-001 — Live Evidence Adapter Interface (mock only).

Defines expected adapter shapes for future live evidence sources.
No real API calls are made in this milestone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


MOCK_LABEL = "MOCK_EVIDENCE — NOT LIVE DATA"


@dataclass
class AdapterRequest:
    asset_or_topic: str
    horizon: str = "NOW"
    context: dict[str, Any] = field(default_factory=dict)


class EvidenceAdapter(Protocol):
    adapter_id: str
    source_type: str

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        ...


def _mock_record(
    evidence_id: str,
    source_name: str,
    source_type: str,
    asset_or_topic: str,
    claim_text: str,
    claim_classification: str,
    source_quote_or_summary: str,
    freshness_state: str = "UNKNOWN_FRESHNESS",
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "evidence_id": evidence_id,
        "source_name": source_name,
        "source_url": f"mock://labpal/{source_type.lower()}/{evidence_id}",
        "source_type": source_type,
        "retrieved_at": now,
        "published_at": None,
        "freshness_state": freshness_state,
        "asset_or_topic": asset_or_topic,
        "claim_text": claim_text,
        "claim_classification": claim_classification,
        "source_quote_or_summary": source_quote_or_summary,
        "labpal_notes": MOCK_LABEL,
        "unknowns": ["Mock data — not suitable for market decisions"],
        "reliability_notes": "Prototype mock adapter output only.",
        "is_mock": True,
        "mock_label": MOCK_LABEL,
    }


class MarketPriceAdapter:
    adapter_id = "market_price_adapter"
    source_type = "MARKET_PRICE"

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        return [
            _mock_record(
                f"MOCK-PRICE-{request.asset_or_topic}",
                "Mock Market Price Feed",
                "MOCK",
                request.asset_or_topic,
                f"[MOCK] Illustrative price context placeholder for {request.asset_or_topic}",
                "SOURCE_FACT",
                "Mock quote — not a live price.",
            )
        ]


class NewsAdapter:
    adapter_id = "news_adapter"
    source_type = "NEWS"

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        return [
            _mock_record(
                f"MOCK-NEWS-{request.asset_or_topic}",
                "Mock News Feed",
                "MOCK",
                request.asset_or_topic,
                f"[MOCK] Illustrative news headline placeholder for {request.asset_or_topic}",
                "SOURCE_INTERPRETATION",
                "Mock headline — not a live news item.",
            )
        ]


class FilingsOrFactsheetAdapter:
    adapter_id = "filings_or_factsheet_adapter"
    source_type = "FILING"

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        return [
            _mock_record(
                f"MOCK-FILING-{request.asset_or_topic}",
                "Mock Filings / Factsheet",
                "MOCK",
                request.asset_or_topic,
                f"[MOCK] Illustrative filing/factsheet reference for {request.asset_or_topic}",
                "SOURCE_FACT",
                "Mock filing excerpt — not a live document.",
            )
        ]


class RatesYieldsAdapter:
    adapter_id = "rates_yields_adapter"
    source_type = "RATES_YIELDS"

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        return [
            _mock_record(
                "MOCK-RATES",
                "Mock Rates / Yields Feed",
                "MOCK",
                "RATES",
                "[MOCK] Illustrative rates/yields context placeholder",
                "SOURCE_FACT",
                "Mock rate data — not live.",
            )
        ]


class SectorBreadthAdapter:
    adapter_id = "sector_breadth_adapter"
    source_type = "SECTOR_BREADTH"

    def fetch(self, request: AdapterRequest) -> list[dict[str, Any]]:
        return [
            _mock_record(
                "MOCK-BREADTH",
                "Mock Sector Breadth Feed",
                "MOCK",
                "MARKET",
                "[MOCK] Illustrative sector breadth placeholder",
                "SOURCE_INTERPRETATION",
                "Mock breadth reading — not live.",
            )
        ]


ADAPTERS: dict[str, EvidenceAdapter] = {
    "market_price_adapter": MarketPriceAdapter(),
    "news_adapter": NewsAdapter(),
    "filings_or_factsheet_adapter": FilingsOrFactsheetAdapter(),
    "rates_yields_adapter": RatesYieldsAdapter(),
    "sector_breadth_adapter": SectorBreadthAdapter(),
}


def fetch_mock_evidence(adapter_id: str, request: AdapterRequest) -> list[dict[str, Any]]:
    adapter = ADAPTERS.get(adapter_id)
    if not adapter:
        raise ValueError(f"Unknown adapter: {adapter_id}")
    return adapter.fetch(request)


def adapter_catalog() -> list[dict[str, str]]:
    return [
        {"adapter_id": a.adapter_id, "source_type": a.source_type, "status": "MOCK_ONLY"}
        for a in ADAPTERS.values()
    ]
