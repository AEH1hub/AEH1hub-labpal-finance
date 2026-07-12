#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


ZURICH_TZ = ZoneInfo("Europe/Zurich")
NEW_YORK_TZ = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class MarketSessionState:
    observed_at_utc: str
    zurich_time: str
    new_york_time: str
    weekday: str
    session_state: str
    observation_allowed: bool
    requested_label: str | None
    label_valid: bool
    reason: str


def classify_us_equity_session(now: datetime) -> str:
    ny = now.astimezone(NEW_YORK_TZ)

    if ny.weekday() >= 5:
        return "WEEKEND"

    minutes = ny.hour * 60 + ny.minute

    if 4 * 60 <= minutes < 9 * 60 + 30:
        return "PRE_MARKET"

    if 9 * 60 + 30 <= minutes < 16 * 60:
        return "REGULAR_SESSION"

    if 16 * 60 <= minutes < 20 * 60:
        return "POST_CLOSE"

    return "CLOSED"


def expected_label_for_session(session_state: str) -> str:
    mapping = {
        "PRE_MARKET": "weekday-pre-market",
        "REGULAR_SESSION": "weekday-market-hours",
        "POST_CLOSE": "weekday-post-close",
        "WEEKEND": "weekend",
        "CLOSED": "closed",
    }
    return mapping[session_state]


def evaluate(requested_label: str | None = None) -> MarketSessionState:
    now = datetime.now(tz=ZoneInfo("UTC"))
    zurich = now.astimezone(ZURICH_TZ)
    new_york = now.astimezone(NEW_YORK_TZ)
    session_state = classify_us_equity_session(now)
    expected_label = expected_label_for_session(session_state)

    allowed_states = {
        "PRE_MARKET",
        "REGULAR_SESSION",
        "POST_CLOSE",
    }

    observation_allowed = session_state in allowed_states

    if requested_label is None:
        label_valid = True
        reason = f"Current session is {session_state}."
    elif requested_label == expected_label:
        label_valid = True
        reason = (
            f"Requested label matches current session: "
            f"{session_state}."
        )
    else:
        label_valid = False
        reason = (
            f"Requested label '{requested_label}' does not match "
            f"current session '{session_state}'. "
            f"Expected label: '{expected_label}'."
        )

    return MarketSessionState(
        observed_at_utc=now.isoformat(),
        zurich_time=zurich.isoformat(),
        new_york_time=new_york.isoformat(),
        weekday=new_york.strftime("%A"),
        session_state=session_state,
        observation_allowed=observation_allowed,
        requested_label=requested_label,
        label_valid=label_valid,
        reason=reason,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Determine the current US equity market session."
    )
    parser.add_argument(
        "--requested-label",
        choices=[
            "weekday-pre-market",
            "weekday-market-hours",
            "weekday-post-close",
            "weekend",
            "closed",
        ],
    )
    parser.add_argument(
        "--require-valid-label",
        action="store_true",
        help="Return a non-zero exit code when the label is invalid.",
    )

    args = parser.parse_args()
    state = evaluate(args.requested_label)

    print(json.dumps(asdict(state), indent=2))

    if args.require_valid_label and not state.label_valid:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
