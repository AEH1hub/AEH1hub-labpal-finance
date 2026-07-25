"""Deterministic current-portfolio understanding for PU-UNDERSTAND-001A.

This module converts one valid canonical ``PortfolioSnapshot`` into a
browser-ready, read-only understanding object. It preserves source facts and
unknowns without adding market causes, diversification judgments, investment
recommendations, or execution authority.
"""

from __future__ import annotations

import copy
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


MILESTONE = "PU-UNDERSTAND-001A"
VERSION = "0.1-pu"
ROOT_DIR = Path(__file__).resolve().parents[1]
SNAPSHOT_SCHEMA_PATH = (
    ROOT_DIR / "schemas" / "portfolio-snapshot.v0.1-pu.schema.json"
)


class PortfolioUnderstandingError(ValueError):
    """Raised when canonical input cannot safely become an understanding."""


def _decimal(value: Any, *, field_name: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PortfolioUnderstandingError(
            f"{field_name} must contain a valid decimal."
        ) from exc

    if not result.is_finite():
        raise PortfolioUnderstandingError(
            f"{field_name} must contain a finite decimal."
        )

    return result


def _validate_canonical_snapshot(snapshot: dict[str, Any]) -> None:
    if not isinstance(snapshot, dict):
        raise PortfolioUnderstandingError(
            "canonical snapshot must be an object."
        )

    schema = json.loads(SNAPSHOT_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(snapshot),
        key=lambda error: (
            tuple(str(item) for item in error.absolute_path),
            error.message,
        ),
    )

    if errors:
        first = errors[0]
        location = ".".join(str(item) for item in first.absolute_path)
        prefix = f"{location}: " if location else ""
        raise PortfolioUnderstandingError(
            f"canonical snapshot failed schema validation: "
            f"{prefix}{first.message}"
        )

    base_currency = snapshot["base_currency"]
    holding_total = Decimal("0")
    cash_total = Decimal("0")
    holding_ids: set[str] = set()

    for holding in snapshot["holdings"]:
        holding_id = holding["holding_id"]

        if holding_id in holding_ids:
            raise PortfolioUnderstandingError(
                f"duplicate canonical holding ID: {holding_id}"
            )

        holding_ids.add(holding_id)
        market_value = holding["market_value"]

        if market_value["currency"] != base_currency:
            raise PortfolioUnderstandingError(
                f"{holding_id} market-value currency does not match "
                "the portfolio base currency."
            )

        holding_total += _decimal(
            market_value["amount"],
            field_name=f"{holding_id}.market_value.amount",
        )

        average_entry = holding["average_entry_price"]
        unknown_fields = {
            unknown["field_name"] for unknown in holding["unknowns"]
        }

        if average_entry is None and "average_entry_price" not in unknown_fields:
            raise PortfolioUnderstandingError(
                f"{holding_id} has no average entry price and no "
                "corresponding canonical unknown."
            )

    for balance in snapshot["cash_balances"]:
        value = balance["value"]

        if value["currency"] != base_currency:
            raise PortfolioUnderstandingError(
                f"{balance['balance_id']} cash currency does not match "
                "the portfolio base currency."
            )

        cash_total += _decimal(
            value["amount"],
            field_name=f"{balance['balance_id']}.value.amount",
        )

    declared_total = _decimal(
        snapshot["total_value"]["amount"],
        field_name="total_value.amount",
    )

    if holding_total + cash_total != declared_total:
        raise PortfolioUnderstandingError(
            "canonical snapshot total does not reconcile with holdings "
            "and cash."
        )


def _money_total(
    items: list[dict[str, Any]],
    *,
    value_key: str,
    currency: str,
) -> dict[str, str]:
    total = sum(
        (
            _decimal(
                item[value_key]["amount"],
                field_name=f"{value_key}.amount",
            )
            for item in items
        ),
        Decimal("0"),
    )
    return {"amount": format(total, "f"), "currency": currency}


def build_portfolio_understanding(
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Build one factual, deterministic understanding from one snapshot."""

    _validate_canonical_snapshot(snapshot)

    snapshot_id = snapshot["snapshot_id"]
    portfolio_id = snapshot["portfolio_id"]
    currency = snapshot["base_currency"]
    observed_at = snapshot["observed_at"]
    holdings = sorted(
        snapshot["holdings"],
        key=lambda item: item["holding_id"],
    )
    cash_balances = sorted(
        snapshot["cash_balances"],
        key=lambda item: item["balance_id"],
    )
    holdings_value = _money_total(
        holdings,
        value_key="market_value",
        currency=currency,
    )
    cash_value = _money_total(
        cash_balances,
        value_key="value",
        currency=currency,
    )

    supported_facts: list[dict[str, Any]] = [
        {
            "fact_id": "FACT-CURRENT-TOTAL-VALUE",
            "statement": (
                f"Current portfolio value is {currency} "
                f"{snapshot['total_value']['amount']}."
            ),
            "evidence_refs": [f"{snapshot_id}.total_value"],
        },
        {
            "fact_id": "FACT-CURRENT-HOLDING-COUNT",
            "statement": (
                f"The current snapshot contains {len(holdings)} holdings."
            ),
            "evidence_refs": [f"{snapshot_id}.holdings"],
        },
        {
            "fact_id": "FACT-CURRENT-CASH-VALUE",
            "statement": (
                f"Current cash value is {currency} {cash_value['amount']}."
            ),
            "evidence_refs": [f"{snapshot_id}.cash_balances"],
        },
    ]

    holding_summaries: list[dict[str, Any]] = []
    unknowns: list[dict[str, Any]] = []
    evidence_required: list[dict[str, Any]] = []

    for holding in holdings:
        holding_id = holding["holding_id"]
        evidence_root = f"{snapshot_id}.holdings.{holding_id}"
        supported_facts.append(
            {
                "fact_id": f"FACT-{holding_id}-CURRENT",
                "statement": (
                    f"{holding['symbol']} has market value "
                    f"{currency} {holding['market_value']['amount']} "
                    f"and preserved weight {holding['weight']}."
                ),
                "evidence_refs": [
                    f"{evidence_root}.symbol",
                    f"{evidence_root}.market_value",
                    f"{evidence_root}.weight",
                ],
            }
        )

        holding_summaries.append(
            {
                "holding_id": holding_id,
                "symbol": holding["symbol"],
                "name": holding["name"],
                "quantity": holding["quantity"],
                "market_value": copy.deepcopy(holding["market_value"]),
                "weight": holding["weight"],
                "observed_at": holding["observed_at"],
                "average_entry_price": copy.deepcopy(
                    holding["average_entry_price"]
                ),
                "reason_for_value": {
                    "state": "UNKNOWN",
                    "claim": None,
                    "evidence_required": (
                        "Market, income, transaction, and corporate-action "
                        "evidence would be required to explain this value."
                    ),
                },
                "evidence_refs": [evidence_root],
            }
        )

        evidence_required.append(
            {
                "requirement_id": f"EVIDENCE-{holding_id}-VALUE-CAUSE",
                "subject_ref": holding_id,
                "purpose": (
                    f"Explain why {holding['symbol']} has its observed "
                    "market value."
                ),
                "required_evidence": [
                    "market price evidence",
                    "transaction history",
                    "income and distribution evidence",
                    "corporate-action evidence",
                ],
            }
        )

        for index, unknown in enumerate(holding["unknowns"], start=1):
            unknowns.append(
                {
                    "unknown_id": f"UNKNOWN-{holding_id}-{index:03d}",
                    "subject_ref": holding_id,
                    "field_name": unknown["field_name"],
                    "reason": unknown["reason"],
                    "source_detail": unknown["source_detail"],
                    "evidence_refs": [
                        f"{evidence_root}.unknowns.{index - 1}"
                    ],
                }
            )

    for index, unknown in enumerate(snapshot["unknowns"], start=1):
        unknowns.append(
            {
                "unknown_id": f"UNKNOWN-PORTFOLIO-{index:03d}",
                "subject_ref": portfolio_id,
                "field_name": unknown["field_name"],
                "reason": unknown["reason"],
                "source_detail": unknown["source_detail"],
                "evidence_refs": [f"{snapshot_id}.unknowns.{index - 1}"],
            }
        )

    return {
        "understanding_id": (
            f"UNDERSTANDING-{snapshot_id.removeprefix('SNAPSHOT-')}"
        ),
        "version": VERSION,
        "portfolio_id": portfolio_id,
        "subject": {
            "type": "PORTFOLIO",
            "portfolio_id": portfolio_id,
            "snapshot_id": snapshot_id,
        },
        "scope": {
            "type": "CURRENT_SINGLE_SNAPSHOT",
            "base_currency": currency,
            "holding_count": len(holdings),
        },
        "observed_at": observed_at,
        "review_state": "READY_FOR_REVIEW",
        "current_understanding": {
            "statement": (
                f"The snapshot records {len(holdings)} holdings and "
                f"{currency} {cash_value['amount']} cash, with total value "
                f"{currency} {snapshot['total_value']['amount']}."
            ),
            "evidence_refs": [
                f"{snapshot_id}.holdings",
                f"{snapshot_id}.cash_balances",
                f"{snapshot_id}.total_value",
            ],
            "approval_status": "NOT_APPROVED",
            "review_state_meaning": (
                "READY_FOR_REVIEW means this factual single-snapshot "
                "understanding is ready for human review. It does not mean "
                "the portfolio or any investment decision is approved."
            ),
        },
        "supported_facts": supported_facts,
        "portfolio_composition": {
            "total_value": copy.deepcopy(snapshot["total_value"]),
            "holdings_value": holdings_value,
            "cash_value": cash_value,
            "holding_count": len(holdings),
            "evidence_refs": [
                f"{snapshot_id}.holdings",
                f"{snapshot_id}.cash_balances",
                f"{snapshot_id}.total_value",
            ],
        },
        "holding_summaries": holding_summaries,
        "cash_summary": {
            "total": cash_value,
            "balance_count": len(cash_balances),
            "balances": copy.deepcopy(cash_balances),
            "evidence_refs": [f"{snapshot_id}.cash_balances"],
        },
        "unknowns": unknowns,
        "limitations": [
            {
                "limitation_id": "LIMITATION-SYNTHETIC-REDACTED",
                "statement": (
                    "The source is synthetic/redacted and does not prove "
                    "compatibility with a real broker portfolio."
                ),
                "evidence_refs": [
                    f"{snapshot_id}.source.source_type",
                    f"{snapshot_id}.source.account_reference",
                    f"{snapshot_id}.source.provenance.source_filename",
                ],
            },
            {
                "limitation_id": "LIMITATION-SINGLE-SNAPSHOT",
                "statement": (
                    "A single snapshot describes current composition but "
                    "does not establish why holding values exist or changed."
                ),
                "evidence_refs": [f"{snapshot_id}.observed_at"],
            },
            {
                "limitation_id": "LIMITATION-NO-DIVERSIFICATION-JUDGMENT",
                "statement": (
                    "No diversification conclusion is supported by this "
                    "single canonical snapshot."
                ),
                "evidence_refs": [f"{snapshot_id}.holdings"],
            },
        ],
        "evidence_required": evidence_required,
        "review_next": [
            "Review the supported facts against their evidence references.",
            "Review preserved unknowns without filling them by inference.",
            "Obtain additional evidence before explaining holding values.",
            "Keep portfolio and investment approval outside this review state.",
        ],
        "source_provenance": copy.deepcopy(snapshot["source"]),
        "recommendations_prohibited": True,
        "execution_prohibited": True,
    }
