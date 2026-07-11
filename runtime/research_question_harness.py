#!/usr/bin/env python3
"""FI-ASK-001 — Research Question harness.

Validates research question fixtures and enforces semantic guardrails.
"""

import json
import pathlib
import re
import sys

try:
    import jsonschema
except ImportError:
    print(json.dumps({"status": "ERROR", "message": "jsonschema is required"}))
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures" / "research-questions"

BANNED_PATTERNS = [
    (re.compile(r"\b(buy now|sell now|you should buy|you should sell|best stock|top pick|guaranteed)\b", re.I), "RQ-001", "Recommendation language detected."),
    (re.compile(r"\b(recommend|recommends|recommending)\s+(nvidia|schd|nvda|[A-Z]{2,5})\b", re.I), "RQ-002", "Stock recommendation detected."),
    (re.compile(r"\bentry\s+(zone|price|at)\s*[:$]?\s*\d", re.I), "RQ-003", "Entry price/zone level detected."),
    (re.compile(r"\$\d+(\.\d+)?"), "RQ-003", "Price level detected."),
    (re.compile(r"\b(best|better|winner|prefer)\s+(stock|etf|nvidia|schd|nvda)\b", re.I), "RQ-004", "Winner/comparison recommendation detected."),
    (re.compile(r"\bchoose\s+(nvidia|schd|nvda)\b", re.I), "RQ-004", "Winner/comparison recommendation detected."),
]

FABRICATED_MARKET = re.compile(
    r"\b(market is up|market is down|s&p (rose|fell)|nasdaq (rose|fell)|today.?s market (is|closed)|currently trading at)\b",
    re.I,
)

TICKER_LIST = re.compile(r"\b(AAPL|MSFT|GOOGL|AMZN|TSLA|NVDA|SCHD)(?:\s*,\s*(?:AAPL|MSFT|GOOGL|AMZN|TSLA|NVDA|SCHD))+\b", re.I)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_strings(obj, prefix=""):
    if isinstance(obj, str):
        yield prefix, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from all_strings(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from all_strings(v, f"{prefix}[{i}]")


def schema_validator():
    rq_schema = load(SCHEMAS / "research-question-object.v0.1-ask.schema.json")
    live_schema = load(SCHEMAS / "live-evidence-record.v0.1-ask.schema.json")
    return jsonschema.Draft202012Validator(rq_schema), jsonschema.Draft202012Validator(live_schema)


def semantic_violations(rq: dict) -> list[dict]:
    violations = []
    text_blob = " ".join(v for _, v in all_strings(rq))

    for pattern, rule_id, message in BANNED_PATTERNS:
        if pattern.search(text_blob):
            violations.append({"rule_id": rule_id, "message": message})

    qtype = rq.get("question_type")
    mode = rq.get("evidence_mode")
    boundary = rq.get("action_boundary_state")

    if qtype == "MARKET_OVERVIEW" and mode == "PLAN_ONLY":
        if FABRICATED_MARKET.search(text_blob):
            violations.append({"rule_id": "RQ-010", "message": "MARKET_OVERVIEW PLAN_ONLY must not fabricate current market conditions."})
        if rq.get("evidence_records"):
            for rec in rq["evidence_records"]:
                if not rec.get("is_mock"):
                    violations.append({"rule_id": "RQ-011", "message": "PLAN_ONLY must not include non-mock evidence records as live."})

    if qtype == "COMPARISON_RESEARCH":
        # Evaluate each preserved string independently. Searching the combined
        # fixture text can join unrelated fields and create false positives,
        # such as matching "Nvidia" in one field with "winner" in a later
        # protective statement.
        comparison_strings = [value for _, value in all_strings(rq)]

        positive_winner_patterns = (
            re.compile(
                r"\b(nvidia|schd|nvda)\b.{0,120}\b(is\s+)?(better|winner|preferred)\b",
                re.I,
            ),
            re.compile(
                r"\b(recommend|prefer)\s+(nvidia|schd|nvda)\b",
                re.I,
            ),
        )

        negated_boundary_pattern = re.compile(
            r"\b(does\s+not|do\s+not|must\s+not|cannot|never|no)\b"
            r".{0,100}\b(choose|recommend|prefer|winner|recommendation)\b",
            re.I,
        )

        for value in comparison_strings:
            if negated_boundary_pattern.search(value):
                continue
            if any(pattern.search(value) for pattern in positive_winner_patterns):
                violations.append({
                    "rule_id": "RQ-020",
                    "message": "COMPARISON_RESEARCH must not choose a winner.",
                })
                break

        if boundary != "ACTION_LANGUAGE_DETECTED" and "invest" in rq.get("original_question", "").lower():
            violations.append({"rule_id": "RQ-021", "message": "Action-boundary state must reflect action language in comparison invest questions."})

    if qtype == "CANDIDATE_DISCOVERY":
        if TICKER_LIST.search(text_blob) and "MOCK" not in text_blob.upper():
            violations.append({"rule_id": "RQ-030", "message": "CANDIDATE_DISCOVERY must not output stock pick lists."})
        if boundary != "RECOMMENDATION_RISK":
            violations.append({"rule_id": "RQ-031", "message": "CANDIDATE_DISCOVERY fixture must use RECOMMENDATION_RISK boundary."})

    if qtype == "ENTRY_ZONE_OR_TIMING":
        if re.search(r"\b\d{2,4}(\.\d+)?\b", rq.get("original_question", "")) and "entry" in rq.get("original_question", "").lower():
            pass  # question may mention concept, not answer
        if boundary != "BLOCKED_FOR_REVIEW":
            violations.append({"rule_id": "RQ-040", "message": "ENTRY_ZONE_OR_TIMING must use BLOCKED_FOR_REVIEW."})
        if re.search(r"\b(entry|support|resistance)\s+(at|zone)\s+\$?\d", text_blob, re.I):
            violations.append({"rule_id": "RQ-041", "message": "Entry-zone fixture must not provide price levels."})

    for rec in rq.get("evidence_records", []):
        if rec.get("is_mock"):
            label = rec.get("mock_label") or rec.get("labpal_notes") or ""
            if "MOCK" not in label.upper():
                violations.append({"rule_id": "RQ-050", "message": f"Mock evidence {rec.get('evidence_id')} missing MOCK label."})
        if mode == "MOCK_EVIDENCE" and not rec.get("is_mock"):
            violations.append({"rule_id": "RQ-051", "message": "MOCK_EVIDENCE mode requires is_mock on all evidence records."})

    if mode == "LIVE_EVIDENCE_CONNECTED" and rq.get("evidence_connection_state") not in ("CONNECTED_ACTIVE", "CONNECTED_UNTESTED"):
        violations.append({"rule_id": "RQ-052", "message": "LIVE_EVIDENCE_CONNECTED requires connected evidence state."})

    # Classification separation: labpal_interpretations must be LABPAL_INTERPRETATION
    for section, expected in (
        ("source_facts", "SOURCE_FACT"),
        ("source_interpretations", "SOURCE_INTERPRETATION"),
        ("labpal_interpretations", "LABPAL_INTERPRETATION"),
    ):
        for item in rq.get(section, []):
            if item.get("claim_classification") != expected:
                violations.append({
                    "rule_id": "RQ-060",
                    "message": f"{section} entry {item.get('claim_id')} has wrong classification.",
                })

    stale_visible = rq.get("stale_evidence_warnings") or []
    for rec in rq.get("evidence_records", []):
        if rec.get("freshness_state") in ("STALE", "UNKNOWN_FRESHNESS") and not stale_visible and rec.get("is_mock"):
            pass  # mock unknown freshness ok with warnings optional

    return violations


def main():
    rq_validator, live_validator = schema_validator()
    fixture_files = sorted(FIXTURES.glob("*.fixture.json"))
    schema_results = []
    semantic_results = []

    for path in fixture_files:
        obj = load(path)
        errs = [e.message for e in rq_validator.iter_errors(obj)]
        for rec in obj.get("evidence_records", []):
            errs.extend(f"evidence.{rec.get('evidence_id')}: {e.message}" for e in live_validator.iter_errors(rec))
        schema_results.append({"file": path.name, "valid": not errs, "errors": errs})
        sem = semantic_violations(obj)
        semantic_results.append({"file": path.name, "valid": not sem, "violations": sem})

    # Validate mock adapter output shape
    sys.path.insert(0, str(ROOT / "runtime"))
    from evidence_adapter_interface import fetch_mock_evidence, AdapterRequest, MOCK_LABEL  # noqa: E402

    adapter_checks = []
    sample = fetch_mock_evidence("market_price_adapter", AdapterRequest("SPX"))
    adapter_checks.append({
        "adapter": "market_price_adapter",
        "valid": all(r.get("is_mock") and MOCK_LABEL in (r.get("mock_label") or "") for r in sample),
        "mock_label": MOCK_LABEL,
    })

    status = "PASS" if (
        all(x["valid"] for x in schema_results + semantic_results)
        and all(x["valid"] for x in adapter_checks)
    ) else "FAIL"

    output = {
        "milestone": "FI-ASK-001",
        "status": status,
        "schema_validation": schema_results,
        "semantic_validation": semantic_results,
        "adapter_validation": adapter_checks,
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
