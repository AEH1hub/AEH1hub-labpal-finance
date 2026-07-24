"""Canonical portfolio domain model for PU-INGEST-001.

This module represents normalized, read-only portfolio facts.

It does not:
- connect to brokers;
- execute transactions;
- recommend trades;
- fabricate missing information;
- fetch live market data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any


class PortfolioModelError(ValueError):
    """Raised when canonical portfolio data violates the model contract."""


class SourceType(str, Enum):
    """Supported source classes for the first portfolio-ingestion slice."""

    BROKER_EXPORT = "BROKER_EXPORT"
    MANUAL_FIXTURE = "MANUAL_FIXTURE"


class UnknownReason(str, Enum):
    """Canonical reasons why a source value is unavailable."""

    SOURCE_FIELD_MISSING = "SOURCE_FIELD_MISSING"
    SOURCE_FIELD_EMPTY = "SOURCE_FIELD_EMPTY"
    SOURCE_VALUE_INVALID = "SOURCE_VALUE_INVALID"
    SOURCE_DOES_NOT_PROVIDE_FIELD = "SOURCE_DOES_NOT_PROVIDE_FIELD"


def parse_decimal(value: str | int | Decimal, *, field_name: str) -> Decimal:
    """Convert a source value into an exact Decimal."""

    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PortfolioModelError(
            f"{field_name} must be a valid decimal value."
        ) from exc

    if not parsed.is_finite():
        raise PortfolioModelError(f"{field_name} must be finite.")

    return parsed


def require_non_empty(value: str, *, field_name: str) -> str:
    """Require non-empty canonical text."""

    normalized = value.strip()

    if not normalized:
        raise PortfolioModelError(f"{field_name} must not be empty.")

    return normalized


def require_currency(value: str) -> str:
    """Normalize and validate a three-letter currency code."""

    currency = require_non_empty(value, field_name="currency").upper()

    if len(currency) != 3 or not currency.isalpha():
        raise PortfolioModelError(
            "currency must be a three-letter alphabetic code."
        )

    return currency


def require_aware_datetime(value: datetime, *, field_name: str) -> datetime:
    """Require an explicitly timezone-aware timestamp."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise PortfolioModelError(
            f"{field_name} must include timezone information."
        )

    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class Money:
    """An exact monetary amount with explicit currency."""

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "amount",
            parse_decimal(self.amount, field_name="money.amount"),
        )
        object.__setattr__(self, "currency", require_currency(self.currency))

    def to_dict(self) -> dict[str, str]:
        return {
            "amount": format(self.amount, "f"),
            "currency": self.currency,
        }


@dataclass(frozen=True)
class Unknown:
    """An explicit record of data that was unavailable from the source."""

    field_name: str
    reason: UnknownReason
    source_detail: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "field_name",
            require_non_empty(self.field_name, field_name="unknown.field_name"),
        )
        object.__setattr__(
            self,
            "source_detail",
            require_non_empty(
                self.source_detail,
                field_name="unknown.source_detail",
            ),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "field_name": self.field_name,
            "reason": self.reason.value,
            "source_detail": self.source_detail,
        }


@dataclass(frozen=True)
class SourceProvenance:
    """Immutable identifying information about the imported source."""

    source_filename: str
    source_sha256: str
    imported_at: datetime
    source_row_count: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_filename",
            require_non_empty(
                self.source_filename,
                field_name="provenance.source_filename",
            ),
        )

        digest = require_non_empty(
            self.source_sha256,
            field_name="provenance.source_sha256",
        ).lower()

        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise PortfolioModelError(
                "provenance.source_sha256 must be a SHA-256 hex digest."
            )

        object.__setattr__(self, "source_sha256", digest)
        object.__setattr__(
            self,
            "imported_at",
            require_aware_datetime(
                self.imported_at,
                field_name="provenance.imported_at",
            ),
        )

        if self.source_row_count < 0:
            raise PortfolioModelError(
                "provenance.source_row_count must not be negative."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_filename": self.source_filename,
            "source_sha256": self.source_sha256,
            "imported_at": self.imported_at.isoformat(),
            "source_row_count": self.source_row_count,
        }


@dataclass(frozen=True)
class PortfolioSource:
    """The read-only source from which a portfolio snapshot was derived."""

    source_id: str
    provider_name: str
    source_type: SourceType
    account_reference: str
    read_only: bool
    provenance: SourceProvenance

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_id",
            require_non_empty(self.source_id, field_name="source.source_id"),
        )
        object.__setattr__(
            self,
            "provider_name",
            require_non_empty(
                self.provider_name,
                field_name="source.provider_name",
            ),
        )
        object.__setattr__(
            self,
            "account_reference",
            require_non_empty(
                self.account_reference,
                field_name="source.account_reference",
            ),
        )

        if self.read_only is not True:
            raise PortfolioModelError(
                "Portfolio sources must be explicitly read-only."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "provider_name": self.provider_name,
            "source_type": self.source_type.value,
            "account_reference": self.account_reference,
            "read_only": self.read_only,
            "provenance": self.provenance.to_dict(),
        }


@dataclass(frozen=True)
class Holding:
    """One normalized portfolio holding."""

    holding_id: str
    symbol: str
    name: str
    quantity: Decimal
    market_value: Money
    weight: Decimal
    observed_at: datetime
    average_entry_price: Money | None = None
    unknowns: tuple[Unknown, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "holding_id",
            require_non_empty(
                self.holding_id,
                field_name="holding.holding_id",
            ),
        )
        object.__setattr__(
            self,
            "symbol",
            require_non_empty(
                self.symbol,
                field_name="holding.symbol",
            ).upper(),
        )
        object.__setattr__(
            self,
            "name",
            require_non_empty(self.name, field_name="holding.name"),
        )

        quantity = parse_decimal(
            self.quantity,
            field_name="holding.quantity",
        )
        weight = parse_decimal(
            self.weight,
            field_name="holding.weight",
        )

        if quantity < Decimal("0"):
            raise PortfolioModelError(
                "holding.quantity must not be negative."
            )

        if weight < Decimal("0") or weight > Decimal("1"):
            raise PortfolioModelError(
                "holding.weight must be between 0 and 1."
            )

        object.__setattr__(self, "quantity", quantity)
        object.__setattr__(self, "weight", weight)
        object.__setattr__(
            self,
            "observed_at",
            require_aware_datetime(
                self.observed_at,
                field_name="holding.observed_at",
            ),
        )

        if (
            self.average_entry_price is not None
            and self.average_entry_price.currency
            != self.market_value.currency
        ):
            raise PortfolioModelError(
                "average entry and market value currencies must match."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "holding_id": self.holding_id,
            "symbol": self.symbol,
            "name": self.name,
            "quantity": format(self.quantity, "f"),
            "market_value": self.market_value.to_dict(),
            "weight": format(self.weight, "f"),
            "observed_at": self.observed_at.isoformat(),
            "average_entry_price": (
                self.average_entry_price.to_dict()
                if self.average_entry_price is not None
                else None
            ),
            "unknowns": [
                unknown.to_dict() for unknown in self.unknowns
            ],
        }


@dataclass(frozen=True)
class CashBalance:
    """One explicit portfolio cash balance."""

    balance_id: str
    value: Money
    observed_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "balance_id",
            require_non_empty(
                self.balance_id,
                field_name="cash_balance.balance_id",
            ),
        )
        object.__setattr__(
            self,
            "observed_at",
            require_aware_datetime(
                self.observed_at,
                field_name="cash_balance.observed_at",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "balance_id": self.balance_id,
            "value": self.value.to_dict(),
            "observed_at": self.observed_at.isoformat(),
        }


@dataclass(frozen=True)
class ValidationResult:
    """Deterministic validation result for one canonical snapshot."""

    valid: bool
    checks: dict[str, bool]
    violations: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "checks": dict(sorted(self.checks.items())),
            "violations": list(self.violations),
        }


@dataclass(frozen=True)
class PortfolioSnapshot:
    """One canonical, read-only portfolio state at a specific time."""

    snapshot_id: str
    portfolio_id: str
    base_currency: str
    observed_at: datetime
    source: PortfolioSource
    holdings: tuple[Holding, ...]
    cash_balances: tuple[CashBalance, ...]
    total_value: Money
    unknowns: tuple[Unknown, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "snapshot_id",
            require_non_empty(
                self.snapshot_id,
                field_name="snapshot.snapshot_id",
            ),
        )
        object.__setattr__(
            self,
            "portfolio_id",
            require_non_empty(
                self.portfolio_id,
                field_name="snapshot.portfolio_id",
            ),
        )
        object.__setattr__(
            self,
            "base_currency",
            require_currency(self.base_currency),
        )
        object.__setattr__(
            self,
            "observed_at",
            require_aware_datetime(
                self.observed_at,
                field_name="snapshot.observed_at",
            ),
        )

        if self.total_value.currency != self.base_currency:
            raise PortfolioModelError(
                "snapshot total currency must match base currency."
            )

        holding_ids = [holding.holding_id for holding in self.holdings]

        if len(holding_ids) != len(set(holding_ids)):
            raise PortfolioModelError(
                "snapshot holding IDs must be unique."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "portfolio_id": self.portfolio_id,
            "base_currency": self.base_currency,
            "observed_at": self.observed_at.isoformat(),
            "source": self.source.to_dict(),
            "holdings": [
                holding.to_dict()
                for holding in sorted(
                    self.holdings,
                    key=lambda item: item.holding_id,
                )
            ],
            "cash_balances": [
                balance.to_dict()
                for balance in sorted(
                    self.cash_balances,
                    key=lambda item: item.balance_id,
                )
            ],
            "total_value": self.total_value.to_dict(),
            "unknowns": [
                unknown.to_dict() for unknown in self.unknowns
            ],
        }


def model_contract() -> dict[str, Any]:
    """Expose the canonical entity contract for deterministic inspection."""

    return {
        "milestone": "PU-INGEST-001A",
        "entities": [
            Money.__name__,
            Unknown.__name__,
            SourceProvenance.__name__,
            PortfolioSource.__name__,
            Holding.__name__,
            CashBalance.__name__,
            PortfolioSnapshot.__name__,
            ValidationResult.__name__,
        ],
        "properties": {
            "read_only": True,
            "uses_decimal": True,
            "requires_currency": True,
            "requires_timezone": True,
            "preserves_unknowns": True,
            "allows_execution": False,
            "allows_recommendations": False,
        },
    }
