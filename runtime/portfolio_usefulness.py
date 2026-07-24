"""Deterministic synthetic portfolio usefulness analysis.

PU-VALIDATE-001A tests whether two canonical portfolio snapshots can
produce an honest, evidence-linked explanation of change.

It does not:
- connect to brokers;
- fetch live prices;
- explain market causes without evidence;
- recommend trades;
- execute transactions.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


class PortfolioUsefulnessError(ValueError):
    """Raised when usefulness analysis violates its scoped contract."""


def _decimal(value: Any, *, field_name: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PortfolioUsefulnessError(
            f"{field_name} must contain a valid decimal."
        ) from exc

    if not result.is_finite():
        raise PortfolioUsefulnessError(
            f"{field_name} must contain a finite decimal."
        )

    return result


def _money(amount: Decimal, currency: str) -> dict[str, str]:
    return {
        "amount": format(amount, "f"),
        "currency": currency,
    }


def _holding_index(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    holdings = snapshot.get("holdings")

    if not isinstance(holdings, list):
        raise PortfolioUsefulnessError(
            "snapshot.holdings must be a list."
        )

    result: dict[str, dict[str, Any]] = {}

    for holding in holdings:
        holding_id = holding.get("holding_id")

        if not isinstance(holding_id, str) or not holding_id:
            raise PortfolioUsefulnessError(
                "Every holding must contain a holding_id."
            )

        if holding_id in result:
            raise PortfolioUsefulnessError(
                f"Duplicate holding ID: {holding_id}"
            )

        result[holding_id] = holding

    return result


def _cash_total(snapshot: dict[str, Any], currency: str) -> Decimal:
    balances = snapshot.get("cash_balances")

    if not isinstance(balances, list):
        raise PortfolioUsefulnessError(
            "snapshot.cash_balances must be a list."
        )

    total = Decimal("0")

    for balance in balances:
        value = balance.get("value", {})

        if value.get("currency") != currency:
            raise PortfolioUsefulnessError(
                "Cash balance currency must match base currency."
            )

        total += _decimal(
            value.get("amount"),
            field_name="cash_balance.value.amount",
        )

    return total


def _validate_snapshot(
    snapshot: dict[str, Any],
    *,
    label: str,
) -> tuple[str, str, dict[str, dict[str, Any]], Decimal]:
    portfolio_id = snapshot.get("portfolio_id")
    base_currency = snapshot.get("base_currency")
    source = snapshot.get("source", {})
    total_value = snapshot.get("total_value", {})

    if not isinstance(portfolio_id, str) or not portfolio_id:
        raise PortfolioUsefulnessError(
            f"{label}.portfolio_id must be present."
        )

    if (
        not isinstance(base_currency, str)
        or len(base_currency) != 3
        or not base_currency.isalpha()
    ):
        raise PortfolioUsefulnessError(
            f"{label}.base_currency must be explicit."
        )

    if source.get("read_only") is not True:
        raise PortfolioUsefulnessError(
            f"{label} source must remain read-only."
        )

    if total_value.get("currency") != base_currency:
        raise PortfolioUsefulnessError(
            f"{label} total currency must match base currency."
        )

    holdings = _holding_index(snapshot)
    holdings_total = Decimal("0")

    for holding_id, holding in holdings.items():
        market_value = holding.get("market_value", {})

        if market_value.get("currency") != base_currency:
            raise PortfolioUsefulnessError(
                f"{holding_id} market-value currency mismatch."
            )

        holdings_total += _decimal(
            market_value.get("amount"),
            field_name=f"{holding_id}.market_value.amount",
        )

    cash_total = _cash_total(snapshot, base_currency)

    declared_total = _decimal(
        total_value.get("amount"),
        field_name=f"{label}.total_value.amount",
    )

    calculated_total = holdings_total + cash_total

    if calculated_total != declared_total:
        raise PortfolioUsefulnessError(
            f"{label} total does not reconcile: "
            f"{calculated_total} != {declared_total}"
        )

    return (
        base_currency,
        portfolio_id,
        holdings,
        declared_total,
    )


def _preserved_source_unknowns(
    before_holdings: dict[str, dict[str, Any]],
    after_holdings: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    preserved: list[dict[str, str]] = []

    for holding_id in sorted(before_holdings):
        before_unknowns = before_holdings[holding_id].get(
            "unknowns",
            [],
        )
        after_unknowns = after_holdings[holding_id].get(
            "unknowns",
            [],
        )

        after_keys = {
            (
                item.get("field_name"),
                item.get("reason"),
                item.get("source_detail"),
            )
            for item in after_unknowns
        }

        for unknown in before_unknowns:
            key = (
                unknown.get("field_name"),
                unknown.get("reason"),
                unknown.get("source_detail"),
            )

            if key not in after_keys:
                raise PortfolioUsefulnessError(
                    "A source unknown disappeared between snapshots: "
                    f"{holding_id}.{unknown.get('field_name')}"
                )

            preserved.append(
                {
                    "holding_id": holding_id,
                    "field_name": str(
                        unknown.get("field_name")
                    ),
                    "reason": str(unknown.get("reason")),
                }
            )

    return preserved


def build_usefulness_report(
    before: dict[str, Any],
    after: dict[str, Any],
    *,
    scenario_id: str,
) -> dict[str, Any]:
    (
        before_currency,
        before_portfolio_id,
        before_holdings,
        before_total,
    ) = _validate_snapshot(before, label="before")

    (
        after_currency,
        after_portfolio_id,
        after_holdings,
        after_total,
    ) = _validate_snapshot(after, label="after")

    if before_portfolio_id != after_portfolio_id:
        raise PortfolioUsefulnessError(
            "Snapshots must represent the same portfolio."
        )

    if before_currency != after_currency:
        raise PortfolioUsefulnessError(
            "Snapshot currencies must match."
        )

    if set(before_holdings) != set(after_holdings):
        raise PortfolioUsefulnessError(
            "The first usefulness scenario requires identical holding IDs."
        )

    before_cash = _cash_total(before, before_currency)
    after_cash = _cash_total(after, after_currency)

    if before_cash != after_cash:
        raise PortfolioUsefulnessError(
            "Cash change is outside PU-VALIDATE-001A scenario 1."
        )

    contributors: list[dict[str, Any]] = []

    for holding_id in before_holdings:
        before_holding = before_holdings[holding_id]
        after_holding = after_holdings[holding_id]

        before_value = _decimal(
            before_holding["market_value"]["amount"],
            field_name=f"{holding_id}.before_market_value",
        )
        after_value = _decimal(
            after_holding["market_value"]["amount"],
            field_name=f"{holding_id}.after_market_value",
        )

        change = after_value - before_value

        if change > 0:
            direction = "POSITIVE"
        elif change < 0:
            direction = "NEGATIVE"
        else:
            direction = "UNCHANGED"

        contributors.append(
            {
                "holding_id": holding_id,
                "symbol": after_holding["symbol"],
                "change": _money(
                    change,
                    before_currency,
                ),
                "direction": direction,
            }
        )

    contributors.sort(
        key=lambda item: (
            -abs(_decimal(
                item["change"]["amount"],
                field_name="contributor.change",
            )),
            item["holding_id"],
        )
    )

    portfolio_change = after_total - before_total
    contributor_total = sum(
        (
            _decimal(
                item["change"]["amount"],
                field_name="contributor.change",
            )
            for item in contributors
        ),
        Decimal("0"),
    )

    if contributor_total != portfolio_change:
        raise PortfolioUsefulnessError(
            "Holding changes do not reconcile with portfolio change."
        )

    largest = contributors[0]["holding_id"]

    supported_facts = [
        {
            "fact_id": "FACT-PORTFOLIO-VALUE-CHANGE",
            "statement": (
                f"Portfolio value changed from "
                f"{before_currency} {format(before_total, 'f')} "
                f"to {after_currency} {format(after_total, 'f')}, "
                f"a net change of "
                f"{before_currency} {format(portfolio_change, 'f')}."
            ),
            "evidence_refs": [
                f"{before['snapshot_id']}.total_value",
                f"{after['snapshot_id']}.total_value",
            ],
        }
    ]

    for contributor in contributors:
        holding_id = contributor["holding_id"]
        symbol = contributor["symbol"]
        amount = contributor["change"]["amount"]

        supported_facts.append(
            {
                "fact_id": f"FACT-{holding_id}-VALUE-CHANGE",
                "statement": (
                    f"{symbol} market value changed by "
                    f"{before_currency} {amount}."
                ),
                "evidence_refs": [
                    (
                        f"{before['snapshot_id']}."
                        f"holdings.{holding_id}.market_value"
                    ),
                    (
                        f"{after['snapshot_id']}."
                        f"holdings.{holding_id}.market_value"
                    ),
                ],
            }
        )

    causal_unknowns = [
        (
            f"Reason for {item['symbol']} "
            "market-value change"
        )
        for item in contributors
    ]

    causal_unknowns.extend(
        [
            "Income contribution during the period",
            "Corporate-action contribution during the period",
        ]
    )

    return {
        "milestone": "PU-VALIDATE-001A",
        "scenario_id": scenario_id,
        "before_snapshot_id": before["snapshot_id"],
        "after_snapshot_id": after["snapshot_id"],
        "portfolio_value_change": _money(
            portfolio_change,
            before_currency,
        ),
        "contributors": contributors,
        "largest_absolute_contributor": largest,
        "supported_facts": supported_facts,
        "causal_explanation": {
            "state": "INSUFFICIENT_EVIDENCE",
            "claim": None,
            "unknowns": causal_unknowns,
        },
        "preserved_source_unknowns": _preserved_source_unknowns(
            before_holdings,
            after_holdings,
        ),
        "review_next": [
            "Obtain period-specific price evidence",
            "Obtain income and distribution evidence",
            "Check for corporate actions",
            "Preserve provider provenance",
        ],
        "evidence_limitations": [
            (
                "Synthetic snapshots do not prove real broker "
                "compatibility."
            ),
            (
                "Market-value changes identify contribution, "
                "not cause."
            ),
            (
                "No period-specific price, income, or "
                "corporate-action evidence is attached."
            ),
        ],
        "recommendations_prohibited": True,
        "execution_prohibited": True,
    }
