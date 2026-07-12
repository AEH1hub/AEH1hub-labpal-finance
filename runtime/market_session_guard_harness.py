#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from runtime.market_session_guard import (
    classify_us_equity_session,
    expected_label_for_session,
)


UTC = ZoneInfo("UTC")


CASES = [
    (
        "weekend",
        datetime(2026, 7, 12, 15, 0, tzinfo=UTC),
        "WEEKEND",
    ),
    (
        "pre_market",
        datetime(2026, 7, 13, 12, 0, tzinfo=UTC),
        "PRE_MARKET",
    ),
    (
        "regular_session",
        datetime(2026, 7, 13, 15, 0, tzinfo=UTC),
        "REGULAR_SESSION",
    ),
    (
        "post_close",
        datetime(2026, 7, 13, 21, 0, tzinfo=UTC),
        "POST_CLOSE",
    ),
    (
        "closed",
        datetime(2026, 7, 13, 2, 0, tzinfo=UTC),
        "CLOSED",
    ),
]


def main() -> int:
    results = []

    for name, observed_at, expected in CASES:
        observed = classify_us_equity_session(observed_at)

        results.append(
            {
                "case": name,
                "expected": expected,
                "observed": observed,
                "expected_label": expected_label_for_session(observed),
                "valid": observed == expected,
            }
        )

    status = "PASS" if all(
        item["valid"] for item in results
    ) else "FAIL"

    print(
        json.dumps(
            {
                "milestone": "FI-ASK-003-RC1-G1",
                "status": status,
                "validation": results,
            },
            indent=2,
        )
    )

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
