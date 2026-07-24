"""Deterministic neutral-CSV portfolio parser for PU-INGEST-001B.

The parser is deliberately read-only and accepts synthetic or explicitly
redacted input only. It does not connect to brokers, convert currencies,
recommend transactions, or execute transactions.
"""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from runtime.portfolio_model import (
    CashBalance,
    Holding,
    Money,
    PortfolioModelError,
    PortfolioSnapshot,
    PortfolioSource,
    SourceProvenance,
    SourceType,
    Unknown,
    UnknownReason,
    parse_decimal,
    require_aware_datetime,
    require_currency,
    require_non_empty,
)


MILESTONE = "PU-INGEST-001B"
MAX_SOURCE_BYTES = 1_000_000
MAX_SOURCE_ROWS = 10_000
MAX_FIELD_LENGTH = 512
REQUIRED_COLUMNS = (
    "row_type",
    "portfolio_id",
    "account_reference",
    "base_currency",
    "observed_at",
    "symbol",
    "name",
    "quantity",
    "market_value",
    "currency",
    "average_entry_price",
)


class PortfolioSourceParserError(ValueError):
    """Raised when a source cannot safely become a canonical snapshot."""


@dataclass(frozen=True)
class RowProvenance:
    """Trace one canonical entity to its neutral-CSV source row."""

    entity_id: str
    source_row_number: int
    source_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "source_row_number": self.source_row_number,
            "source_fields": list(self.source_fields),
        }


@dataclass(frozen=True)
class PortfolioParseResult:
    """Canonical result plus parser-boundary provenance and authority."""

    snapshot: PortfolioSnapshot
    row_provenance: tuple[RowProvenance, ...]
    source_unchanged: bool
    recommendations_prohibited: bool = True
    execution_prohibited: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "milestone": MILESTONE,
            "snapshot": self.snapshot.to_dict(),
            "row_provenance": [
                item.to_dict()
                for item in sorted(
                    self.row_provenance,
                    key=lambda value: value.entity_id,
                )
            ],
            "source_unchanged": self.source_unchanged,
            "recommendations_prohibited": self.recommendations_prohibited,
            "execution_prohibited": self.execution_prohibited,
        }


def _parse_timestamp(value: str, *, field_name: str) -> datetime:
    normalized = require_non_empty(value, field_name=field_name)

    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PortfolioSourceParserError(
            f"{field_name} must be an ISO-8601 timestamp."
        ) from exc

    try:
        return require_aware_datetime(parsed, field_name=field_name)
    except PortfolioModelError as exc:
        raise PortfolioSourceParserError(str(exc)) from exc


def _safe_text(value: str, *, field_name: str) -> str:
    normalized = require_non_empty(value, field_name=field_name)

    if len(normalized) > MAX_FIELD_LENGTH:
        raise PortfolioSourceParserError(
            f"{field_name} exceeds the maximum field length."
        )

    if normalized[0] in ("=", "+", "-", "@"):
        raise PortfolioSourceParserError(
            f"{field_name} contains a prohibited formula-like value."
        )

    return normalized


def _read_source(source_path: Path) -> tuple[bytes, list[dict[str, str]]]:
    if not source_path.is_file():
        raise PortfolioSourceParserError("source_path must be a regular file.")

    source_bytes = source_path.read_bytes()

    if len(source_bytes) > MAX_SOURCE_BYTES:
        raise PortfolioSourceParserError("source exceeds the size limit.")

    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PortfolioSourceParserError("source must be UTF-8 text.") from exc

    reader = csv.DictReader(source_text.splitlines())

    if reader.fieldnames is None:
        raise PortfolioSourceParserError("source must contain a header row.")

    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise PortfolioSourceParserError(
            "source contains duplicate column names."
        )

    missing = sorted(set(REQUIRED_COLUMNS) - set(reader.fieldnames))
    unexpected = sorted(set(reader.fieldnames) - set(REQUIRED_COLUMNS))

    if missing:
        raise PortfolioSourceParserError(
            f"source is missing required columns: {', '.join(missing)}."
        )

    if unexpected:
        raise PortfolioSourceParserError(
            f"source contains unsupported columns: {', '.join(unexpected)}."
        )

    rows = list(reader)

    if not rows:
        raise PortfolioSourceParserError(
            "source must contain at least one data row."
        )

    if len(rows) > MAX_SOURCE_ROWS:
        raise PortfolioSourceParserError("source exceeds the row limit.")

    for row_number, row in enumerate(rows, start=2):
        if None in row:
            raise PortfolioSourceParserError(
                f"source row {row_number} contains extra fields."
            )

        for field_name, value in row.items():
            if value is None:
                raise PortfolioSourceParserError(
                    f"source row {row_number} is structurally incomplete."
                )

            if len(value) > MAX_FIELD_LENGTH:
                raise PortfolioSourceParserError(
                    f"source row {row_number} field {field_name} "
                    "exceeds the maximum field length."
                )

    return source_bytes, rows


def parse_portfolio_source(
    source_path: Path,
    *,
    imported_at: datetime,
) -> PortfolioParseResult:
    """Parse one neutral CSV into the canonical portfolio contract."""

    imported_at = require_aware_datetime(
        imported_at,
        field_name="imported_at",
    )
    source_bytes, rows = _read_source(source_path)
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()

    portfolio_ids: set[str] = set()
    account_references: set[str] = set()
    base_currencies: set[str] = set()
    observed_times: set[datetime] = set()
    row_fingerprints: set[tuple[tuple[str, str], ...]] = set()
    holding_symbols: set[str] = set()
    holding_rows: list[tuple[int, dict[str, str]]] = []
    cash_rows: list[tuple[int, dict[str, str]]] = []

    for row_number, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))

        if fingerprint in row_fingerprints:
            raise PortfolioSourceParserError(
                f"source row {row_number} duplicates an earlier row."
            )

        row_fingerprints.add(fingerprint)
        row_type = _safe_text(
            row["row_type"],
            field_name=f"row {row_number} row_type",
        ).upper()
        portfolio_ids.add(
            _safe_text(
                row["portfolio_id"],
                field_name=f"row {row_number} portfolio_id",
            )
        )
        account_references.add(
            _safe_text(
                row["account_reference"],
                field_name=f"row {row_number} account_reference",
            )
        )
        base_currency = require_currency(row["base_currency"])
        currency = require_currency(row["currency"])
        base_currencies.add(base_currency)
        observed_times.add(
            _parse_timestamp(
                row["observed_at"],
                field_name=f"row {row_number} observed_at",
            )
        )

        if currency != base_currency:
            raise PortfolioSourceParserError(
                "mixed currencies require explicit FX evidence; "
                "silent conversion is prohibited."
            )

        if row_type == "HOLDING":
            symbol = _safe_text(
                row["symbol"],
                field_name=f"row {row_number} symbol",
            ).upper()

            if symbol in holding_symbols:
                raise PortfolioSourceParserError(
                    f"source row {row_number} duplicates holding {symbol}."
                )

            holding_symbols.add(symbol)
            holding_rows.append((row_number, row))
        elif row_type == "CASH":
            cash_rows.append((row_number, row))
        else:
            raise PortfolioSourceParserError(
                f"source row {row_number} has unsupported row_type."
            )

    if len(portfolio_ids) != 1:
        raise PortfolioSourceParserError(
            "source must describe exactly one portfolio_id."
        )

    if len(account_references) != 1:
        raise PortfolioSourceParserError(
            "source must describe exactly one account_reference."
        )

    if len(base_currencies) != 1:
        raise PortfolioSourceParserError(
            "source must describe exactly one base_currency."
        )

    if len(observed_times) != 1:
        raise PortfolioSourceParserError(
            "all source rows must share one observed_at timestamp."
        )

    if not holding_rows:
        raise PortfolioSourceParserError(
            "source must contain at least one holding row."
        )

    portfolio_id = next(iter(portfolio_ids))
    account_reference = next(iter(account_references))
    base_currency = next(iter(base_currencies))
    observed_at = next(iter(observed_times))

    parsed_holding_values: list[Decimal] = []

    for row_number, row in holding_rows:
        quantity = parse_decimal(
            row["quantity"],
            field_name=f"row {row_number} quantity",
        )
        market_value = parse_decimal(
            row["market_value"],
            field_name=f"row {row_number} market_value",
        )

        if quantity < 0 or market_value < 0:
            raise PortfolioSourceParserError(
                f"source row {row_number} contains a negative holding value."
            )

        parsed_holding_values.append(market_value)

    holdings_total = sum(parsed_holding_values, Decimal("0"))

    if holdings_total <= 0:
        raise PortfolioSourceParserError(
            "holding market value total must be positive."
        )

    holdings: list[Holding] = []
    cash_balances: list[CashBalance] = []
    row_provenance: list[RowProvenance] = []

    for index, ((row_number, row), market_value) in enumerate(
        zip(holding_rows, parsed_holding_values, strict=True),
        start=1,
    ):
        symbol = row["symbol"].strip().upper()
        holding_id = f"HOLDING-{symbol}-{index:03d}"
        average_entry_text = row["average_entry_price"].strip()
        unknowns: tuple[Unknown, ...] = ()

        if average_entry_text:
            average_entry_price = Money(
                amount=parse_decimal(
                    average_entry_text,
                    field_name=(
                        f"row {row_number} average_entry_price"
                    ),
                ),
                currency=row["currency"],
            )
        else:
            average_entry_price = None
            unknowns = (
                Unknown(
                    field_name="average_entry_price",
                    reason=UnknownReason.SOURCE_FIELD_EMPTY,
                    source_detail=(
                        f"Source row {row_number}, field "
                        "average_entry_price was empty."
                    ),
                ),
            )

        holdings.append(
            Holding(
                holding_id=holding_id,
                symbol=symbol,
                name=_safe_text(
                    row["name"],
                    field_name=f"row {row_number} name",
                ),
                quantity=parse_decimal(
                    row["quantity"],
                    field_name=f"row {row_number} quantity",
                ),
                market_value=Money(
                    amount=market_value,
                    currency=row["currency"],
                ),
                weight=market_value / holdings_total,
                observed_at=observed_at,
                average_entry_price=average_entry_price,
                unknowns=unknowns,
            )
        )
        row_provenance.append(
            RowProvenance(
                entity_id=holding_id,
                source_row_number=row_number,
                source_fields=tuple(REQUIRED_COLUMNS),
            )
        )

    cash_total = Decimal("0")

    for index, (row_number, row) in enumerate(cash_rows, start=1):
        if any(
            row[field_name].strip()
            for field_name in (
                "symbol",
                "name",
                "quantity",
                "average_entry_price",
            )
        ):
            raise PortfolioSourceParserError(
                f"source cash row {row_number} contains holding-only fields."
            )

        value = parse_decimal(
            row["market_value"],
            field_name=f"row {row_number} market_value",
        )

        if value < 0:
            raise PortfolioSourceParserError(
                f"source cash row {row_number} contains a negative value."
            )

        balance_id = f"CASH-{base_currency}-{index:03d}"
        cash_total += value
        cash_balances.append(
            CashBalance(
                balance_id=balance_id,
                value=Money(amount=value, currency=row["currency"]),
                observed_at=observed_at,
            )
        )
        row_provenance.append(
            RowProvenance(
                entity_id=balance_id,
                source_row_number=row_number,
                source_fields=tuple(REQUIRED_COLUMNS),
            )
        )

    snapshot = PortfolioSnapshot(
        snapshot_id=f"SNAPSHOT-{portfolio_id}-{observed_at:%Y%m%dT%H%M%SZ}",
        portfolio_id=portfolio_id,
        base_currency=base_currency,
        observed_at=observed_at,
        source=PortfolioSource(
            source_id=f"SOURCE-{source_sha256[:16].upper()}",
            provider_name="LABPAL_NEUTRAL_CSV",
            source_type=SourceType.MANUAL_FIXTURE,
            account_reference=account_reference,
            read_only=True,
            provenance=SourceProvenance(
                source_filename=source_path.name,
                source_sha256=source_sha256,
                imported_at=imported_at,
                source_row_count=len(rows),
            ),
        ),
        holdings=tuple(holdings),
        cash_balances=tuple(cash_balances),
        total_value=Money(
            amount=holdings_total + cash_total,
            currency=base_currency,
        ),
    )

    source_unchanged = (
        hashlib.sha256(source_path.read_bytes()).hexdigest()
        == source_sha256
    )

    if not source_unchanged:
        raise PortfolioSourceParserError(
            "source changed during read-only parsing."
        )

    return PortfolioParseResult(
        snapshot=snapshot,
        row_provenance=tuple(row_provenance),
        source_unchanged=True,
    )
