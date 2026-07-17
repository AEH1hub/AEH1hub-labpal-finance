"""LU-LIVE-001 deterministic live-understanding orchestration.

This module accepts an already normalized provider-evidence record,
preserves it without mutation, and delegates reasoning to FI-REAS-001.

It performs no provider network requests and never silently falls back
to mock evidence.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.alpha_vantage_market_price_adapter import validate_record
from runtime.unified_reasoning_pipeline import run_reasoning_pipeline


class LiveUnderstandingValidationError(ValueError):
    """Raised when live-understanding input is unusable or prohibited."""


def _require_text(name: str, value: str) -> str:
    """Return a normalized non-empty string or raise a bounded error."""

    if not isinstance(value, str) or not value.strip():
        raise LiveUnderstandingValidationError(
            f"{name} must be a non-empty string."
        )

    return value.strip()


def _unique_strings(values: list[str]) -> list[str]:
    """Preserve first occurrence while removing empty duplicates."""

    output: list[str] = []
    seen: set[str] = set()

    for value in values:
        if not isinstance(value, str):
            continue

        normalized = value.strip()

        if normalized and normalized not in seen:
            seen.add(normalized)
            output.append(normalized)

    return output


def _canonical_freshness(
    evidence: dict[str, Any],
    *,
    market_session_state: str,
    reference_time: str,
) -> dict[str, str]:
    """Return a scoped freshness assessment without rewriting evidence.

    The preserved provider record uses its original schema vocabulary.
    LU-LIVE exposes a separate canonical assessment because exact quote
    time, timezone, currency, and real-time/delayed status are unknown.
    """

    return {
        "state": "FRESHNESS_UNKNOWN",
        "scope": "CURRENT_MARKET_UNDERSTANDING",
        "reason": (
            "The provider supplied a trading date but no exact quote "
            "timestamp, exchange timezone, currency, or delay status."
        ),
        "provider_freshness_state": str(
            evidence.get("freshness_state", "UNKNOWN_FRESHNESS")
        ),
        "market_session_state": market_session_state,
        "reference_time": reference_time,
    }


def run_live_understanding_pipeline(
    *,
    execution_id: str,
    executing_actor: str,
    provider: str,
    requested_symbol: str,
    normalized_evidence: dict[str, Any],
    market_session_state: str,
    reference_time: str,
    additional_unknowns: list[str] | None = None,
) -> dict[str, Any]:
    """Orchestrate one preserved normalized provider-evidence record.

    Responsibilities:
    1. Validate normalized evidence against the existing evidence schema.
    2. Reject mock evidence in the live path.
    3. Preserve the evidence record without mutation.
    4. Derive a scoped canonical freshness assessment.
    5. Construct an FI-REAS-001-compatible research payload.
    6. Invoke the existing unified reasoning pipeline.
    7. Return provenance, freshness, limitations, and reasoning separately.

    This function performs no provider network request and never falls
    back to mock evidence.
    """

    execution_id = _require_text("execution_id", execution_id)
    executing_actor = _require_text(
        "executing_actor",
        executing_actor,
    )
    provider = _require_text("provider", provider)
    requested_symbol = _require_text(
        "requested_symbol",
        requested_symbol,
    ).upper()
    market_session_state = _require_text(
        "market_session_state",
        market_session_state,
    )
    reference_time = _require_text(
        "reference_time",
        reference_time,
    )

    if not isinstance(normalized_evidence, dict):
        raise LiveUnderstandingValidationError(
            "normalized_evidence must be an object."
        )

    preserved_evidence = deepcopy(normalized_evidence)

    validation_errors = validate_record(preserved_evidence)

    if validation_errors:
        raise LiveUnderstandingValidationError(
            "Normalized evidence failed schema validation: "
            + " | ".join(validation_errors)
        )

    if preserved_evidence.get("is_mock") is True:
        raise LiveUnderstandingValidationError(
            "Mock evidence is prohibited in the LU-LIVE path."
        )

    returned_symbol = str(
        preserved_evidence.get("asset_or_topic", "")
    ).strip().upper()

    if returned_symbol != requested_symbol:
        raise LiveUnderstandingValidationError(
            "Returned evidence subject does not match requested_symbol."
        )

    if str(preserved_evidence.get("source_name", "")).strip() != provider:
        raise LiveUnderstandingValidationError(
            "Provider identity does not match the evidence source."
        )

    provider_unknowns = _unique_strings(
        list(preserved_evidence.get("unknowns", []))
    )

    preserved_additional_unknowns = _unique_strings(
        list(additional_unknowns or [])
    )

    canonical_freshness = _canonical_freshness(
        preserved_evidence,
        market_session_state=market_session_state,
        reference_time=reference_time,
    )

    evidence_id = str(preserved_evidence["evidence_id"])

    reasoning_payload = {
        "execution_id": execution_id,
        "executing_actor": executing_actor,
        "scope": {
            "domain": "FINANCE",
            "purpose": (
                "Interpret one preserved normalized provider-evidence "
                "record within a research-only live-understanding scope"
            ),
            "asset_or_topic": requested_symbol,
            "verification_scope": (
                "PRESERVED_PROVIDER_EVIDENCE_AND_REASONING"
            ),
        },
        "research_question": {
            "research_question_id": (
                f"RQ-LU-LIVE-{requested_symbol}-001"
            ),
            "original_question": (
                f"What does this preserved {provider} evidence "
                f"demonstrate about {requested_symbol} within the "
                "current research-only scope?"
            ),
            "question_type": "COMPANY_RESEARCH",
            "created_at": reference_time,
            "requested_horizon": "CURRENT_RESEARCH_SCOPE",
            "user_objective_state": "RESEARCH_ONLY",
            "evidence_connection_state": "CONNECTED_UNTESTED",
            "evidence_mode": "LIVE_EVIDENCE_CONNECTED",
            "action_boundary_state": "RESEARCH_ONLY",
            "source_requirements": [
                (
                    "Independent provider evidence is required before "
                    "broader verification"
                ),
                (
                    "Exact quote timing and delay status are required "
                    "before claiming current market freshness"
                ),
            ],
            "evidence_records": [
                deepcopy(preserved_evidence)
            ],
            "source_facts": [
                {
                    "claim_id": (
                        f"SF-LU-LIVE-{requested_symbol}-001"
                    ),
                    "claim_text": str(
                        preserved_evidence["claim_text"]
                    ),
                    "claim_classification": "SOURCE_FACT",
                    "freshness_state": "CURRENT",
                }
            ],
            "source_interpretations": [],
            "labpal_interpretations": [
                {
                    "claim_id": (
                        f"LPI-LU-LIVE-{requested_symbol}-001"
                    ),
                    "claim_text": (
                        "The preserved provider record is admissible "
                        "for bounded research review, but its unknown "
                        "timestamp, timezone, currency, delay status, "
                        "and lack of independent-provider agreement "
                        "prevent broader verification."
                    ),
                    "claim_classification": (
                        "LABPAL_INTERPRETATION"
                    ),
                    "freshness_state": "CURRENT",
                }
            ],
            "unknowns": [
                (
                    "Independent provider agreement has not been "
                    "established."
                ),
                (
                    "The evidence does not establish suitability, "
                    "recommendation, or execution authority."
                ),
            ],
            "stale_evidence_warnings": [
                canonical_freshness["reason"]
            ],
            "action_boundary_warnings": [
                (
                    "Research-only scope: no recommendation or "
                    "execution conclusion is permitted."
                )
            ],
            "next_safe_actions": [
                "Preserve an independent provider observation.",
                (
                    "Obtain explicit quote timing, timezone, currency, "
                    "and delay-status evidence."
                ),
            ],
        },
        "challenging_evidence_ids": [],
        "contradictions": [],
        "additional_unknowns": (
            provider_unknowns
            + preserved_additional_unknowns
        ),
        "excluded_evidence": [],
        "previous_understanding": None,
        "next_evidence_needed": [
            "Independent provider evidence",
            "Explicit quote-timing evidence",
            "Provider delay-status evidence",
        ],
    }

    reasoning_result = run_reasoning_pipeline(
        reasoning_payload
    )

    if preserved_evidence != normalized_evidence:
        raise LiveUnderstandingValidationError(
            "The normalized evidence input was mutated."
        )

    combined_unknowns = _unique_strings(
        provider_unknowns
        + preserved_additional_unknowns
        + list(reasoning_result.get("unknowns", []))
    )

    limitations = _unique_strings(
        [
            str(
                preserved_evidence.get(
                    "reliability_notes",
                    "",
                )
            ),
            canonical_freshness["reason"],
            (
                "A single provider observation does not establish "
                "independent agreement."
            ),
            (
                "Provider retrieval does not equal verification, "
                "recommendation, or authority."
            ),
        ]
    )

    return {
        "milestone": "LU-LIVE-001",
        "execution_id": execution_id,
        "executing_actor": executing_actor,
        "provider_record_valid": True,
        "evidence_classification": "LIVE_EVIDENCE",
        "fixture_classification": (
            "PRESERVED_PROVIDER_RESPONSE_NOT_LIVE_REQUEST"
        ),
        "mock_fallback_used": False,
        "provenance": {
            "provider": provider,
            "requested_symbol": requested_symbol,
            "returned_symbol": returned_symbol,
            "source_url": preserved_evidence["source_url"],
            "evidence_id": evidence_id,
            "retrieved_at": preserved_evidence["retrieved_at"],
            "published_at": preserved_evidence["published_at"],
            "market_session_state": market_session_state,
        },
        "canonical_freshness": canonical_freshness,
        "normalized_evidence": deepcopy(
            preserved_evidence
        ),
        "unknowns": combined_unknowns,
        "limitations": limitations,
        "reasoning_result": reasoning_result,
        "reasoning_decision_state": reasoning_result[
            "decision_state"
        ],
        "reasoning_review_state": reasoning_result[
            "review_state"
        ],
        "history_preserved": (
            reasoning_result.get("history_preserved") is True
        ),
    }
