"""Deterministic harness for FI-REAS-001."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.unified_reasoning_pipeline import run_reasoning_pipeline


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "reasoning-pipeline"


def load_fixture(filename: str) -> dict[str, Any]:
    path = FIXTURES / filename
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_case(
    *,
    name: str,
    filename: str,
    expected_decision: str,
    expected_review: str,
    expected_valid: bool,
    expected_rule: str | None = None,
) -> dict[str, Any]:
    fixture = load_fixture(filename)
    result = run_reasoning_pipeline(fixture)

    violations = result["validation_results"][
        "research_question_semantic_violations"
    ]
    observed_rules = sorted(
        {
            violation["rule_id"]
            for violation in violations
        }
    )

    checks = {
        "milestone": result["milestone"] == "FI-REAS-001",
        "decision_state": (
            result["decision_state"] == expected_decision
        ),
        "review_state": (
            result["review_state"] == expected_review
        ),
        "validation_state": (
            result["validation_results"]["valid"]
            is expected_valid
        ),
        "question_preserved": (
            result["preserved_question"]["original_question"]
            == fixture["research_question"]["original_question"]
        ),
        "history_preserved": (
            result["history_preserved"] is True
            and result["current_understanding"][
                "history_preserved"
            ] is True
        ),
    }

    if expected_rule is not None:
        checks["expected_rule"] = expected_rule in observed_rules
        checks["invalid_claim_not_adopted"] = (
            result["current_understanding"]["selected_claim_id"] is None
            and result["current_understanding"]["current_statement"].startswith(
                "No admissible Current Understanding was adopted"
            )
        )

    return {
        "case": name,
        "fixture": filename,
        "expected_decision": expected_decision,
        "observed_decision": result["decision_state"],
        "expected_review": expected_review,
        "observed_review": result["review_state"],
        "expected_validation": expected_valid,
        "observed_validation": result[
            "validation_results"
        ]["valid"],
        "expected_rule": expected_rule,
        "observed_rules": observed_rules,
        "checks": checks,
        "valid": all(checks.values()),
    }


def main() -> int:
    cases = [
        evaluate_case(
            name="valid_research_cycle",
            filename="valid-research-cycle.fixture.json",
            expected_decision="READY_FOR_REVIEW",
            expected_review="READY_FOR_REVIEW",
            expected_valid=True,
        ),
        evaluate_case(
            name="insufficient_evidence",
            filename="insufficient-evidence.fixture.json",
            expected_decision="INSUFFICIENT_EVIDENCE",
            expected_review="REVISION_REQUIRED",
            expected_valid=True,
        ),
        evaluate_case(
            name="challenged_understanding",
            filename="challenged-understanding.fixture.json",
            expected_decision="REVISION_REQUIRED",
            expected_review="REVISION_REQUIRED",
            expected_valid=True,
        ),
        evaluate_case(
            name="prohibited_recommendation",
            filename="prohibited-recommendation.fixture.json",
            expected_decision="REVISION_REQUIRED",
            expected_review="REVISION_REQUIRED",
            expected_valid=False,
            expected_rule="RQ-020",
        ),
    ]

    status = (
        "PASS"
        if all(case["valid"] for case in cases)
        else "FAIL"
    )

    output = {
        "milestone": "FI-REAS-001",
        "status": status,
        "case_count": len(cases),
        "cases": cases,
    }

    print(json.dumps(output, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
