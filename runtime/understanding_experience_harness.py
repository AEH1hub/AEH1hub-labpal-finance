"""Deterministic verification harness for LU-UX-001."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE_ROOT = ROOT / "experience"
DATA_ROOT = EXPERIENCE_ROOT / "data"

EXPECTED_SCENARIOS = {
    "valid-research-cycle": {
        "decision_state": "READY_FOR_REVIEW",
        "review_state": "READY_FOR_REVIEW",
        "validation_valid": True,
    },
    "insufficient-evidence": {
        "decision_state": "INSUFFICIENT_EVIDENCE",
        "review_state": "REVISION_REQUIRED",
        "validation_valid": True,
    },
    "challenged-understanding": {
        "decision_state": "REVISION_REQUIRED",
        "review_state": "REVISION_REQUIRED",
        "validation_valid": True,
    },
    "prohibited-recommendation": {
        "decision_state": "REVISION_REQUIRED",
        "review_state": "REVISION_REQUIRED",
        "validation_valid": False,
    },
}

REQUIRED_RESULT_FIELDS = {
    "preserved_question",
    "evidence_considered",
    "supporting_evidence",
    "challenging_evidence",
    "excluded_evidence",
    "unknowns",
    "contradictions",
    "claims",
    "current_understanding",
    "decision_state",
    "review_state",
    "reasoning_summary",
    "next_evidence_needed",
    "history_preserved",
    "validation_results",
}

REQUIRED_HTML_IDS = {
    "scenario-select",
    "experience-status",
    "reasoning-experience",
    "question-text",
    "question-type",
    "evidence-mode",
    "action-boundary",
    "execution-id",
    "understanding-statement",
    "verification-notice",
    "decision-state",
    "review-state",
    "evidence-list",
    "unknown-list",
    "contradiction-list",
    "next-evidence-list",
    "reasoning-summary",
    "raw-json",
}

REQUIRED_JAVASCRIPT_TOKENS = {
    "renderExperience",
    "loadScenario",
    "./data/${scenarioId}.json",
    "evidence_considered",
    "unknowns",
    "contradictions",
    "next_evidence_needed",
    "current_understanding",
    "decision_state",
    "review_state",
}

REQUIRED_CSS_TOKENS = {
    ".reasoning-experience",
    ".understanding-panel",
    ".state-grid",
    ".content-grid",
    ".status-message",
    "@media (max-width: 760px)",
}


def load_json(path: Path) -> dict[str, Any]:
    """Load one JSON object from disk."""

    return json.loads(path.read_text(encoding="utf-8"))


def check_manifest() -> dict[str, Any]:
    """Verify the scenario manifest."""

    manifest_path = DATA_ROOT / "manifest.json"
    manifest = load_json(manifest_path)

    observed = {
        item["scenario_id"]: item
        for item in manifest["scenarios"]
    }

    checks = {
        "manifest_exists": manifest_path.is_file(),
        "milestone": manifest.get("milestone") == "LU-UX-001",
        "reasoning_dependency": (
            manifest.get("reasoning_dependency") == "FI-REAS-001"
        ),
        "platform_dependency": (
            manifest.get("platform_dependency") == "LU-001"
        ),
        "scenario_set": set(observed) == set(EXPECTED_SCENARIOS),
    }

    for scenario_id, expected in EXPECTED_SCENARIOS.items():
        item = observed.get(scenario_id, {})

        checks[f"{scenario_id}.decision_state"] = (
            item.get("decision_state")
            == expected["decision_state"]
        )
        checks[f"{scenario_id}.review_state"] = (
            item.get("review_state")
            == expected["review_state"]
        )
        checks[f"{scenario_id}.validation_valid"] = (
            item.get("validation_valid")
            is expected["validation_valid"]
        )

        filename = item.get("filename")
        checks[f"{scenario_id}.file_exists"] = (
            isinstance(filename, str)
            and (DATA_ROOT / filename).is_file()
        )

    return {
        "case": "manifest",
        "checks": checks,
        "valid": all(checks.values()),
    }


def check_scenario(
    scenario_id: str,
    expected: dict[str, Any],
) -> dict[str, Any]:
    """Verify one generated reasoning payload."""

    path = DATA_ROOT / f"{scenario_id}.json"
    payload = load_json(path)

    metadata = payload["experience_metadata"]
    result = payload["result"]

    missing_fields = sorted(
        REQUIRED_RESULT_FIELDS - set(result)
    )

    checks = {
        "file_exists": path.is_file(),
        "scenario_id": metadata.get("scenario_id") == scenario_id,
        "evidence_label": (
            metadata.get("evidence_label")
            == "DETERMINISTIC_FIXTURE_NOT_LIVE_EVIDENCE"
        ),
        "reasoning_milestone": (
            metadata.get("reasoning_milestone") == "FI-REAS-001"
        ),
        "metadata_history_preserved": (
            metadata.get("history_preserved") is True
        ),
        "required_fields": not missing_fields,
        "question_preserved": bool(
            result["preserved_question"]["original_question"]
        ),
        "decision_state": (
            result["decision_state"]
            == expected["decision_state"]
        ),
        "review_state": (
            result["review_state"]
            == expected["review_state"]
        ),
        "validation_state": (
            result["validation_results"]["valid"]
            is expected["validation_valid"]
        ),
        "history_preserved": result["history_preserved"] is True,
    }

    if scenario_id == "prohibited-recommendation":
        current = result["current_understanding"]

        checks["invalid_claim_not_adopted"] = (
            current["selected_claim_id"] is None
            and current["current_statement"].startswith(
                "No admissible Current Understanding was adopted"
            )
        )

        observed_rules = {
            violation["rule_id"]
            for violation in result["validation_results"][
                "research_question_semantic_violations"
            ]
        }
        checks["rq_020_preserved"] = "RQ-020" in observed_rules

    return {
        "case": scenario_id,
        "missing_fields": missing_fields,
        "checks": checks,
        "valid": all(checks.values()),
    }


def check_static_runtime() -> dict[str, Any]:
    """Verify the HTML, JavaScript and CSS integration contract."""

    html_path = EXPERIENCE_ROOT / "index.html"
    javascript_path = EXPERIENCE_ROOT / "assets" / "app.js"
    css_path = EXPERIENCE_ROOT / "assets" / "styles.css"

    html = html_path.read_text(encoding="utf-8")
    javascript = javascript_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")

    missing_html_ids = sorted(
        element_id
        for element_id in REQUIRED_HTML_IDS
        if f'id="{element_id}"' not in html
    )

    missing_javascript_tokens = sorted(
        token
        for token in REQUIRED_JAVASCRIPT_TOKENS
        if token not in javascript
    )

    missing_css_tokens = sorted(
        token
        for token in REQUIRED_CSS_TOKENS
        if token not in css
    )

    checks = {
        "html_exists": html_path.is_file() and bool(html.strip()),
        "javascript_exists": (
            javascript_path.is_file() and bool(javascript.strip())
        ),
        "css_exists": css_path.is_file() and bool(css.strip()),
        "html_contract": not missing_html_ids,
        "javascript_contract": not missing_javascript_tokens,
        "css_contract": not missing_css_tokens,
    }

    return {
        "case": "static_runtime",
        "missing_html_ids": missing_html_ids,
        "missing_javascript_tokens": missing_javascript_tokens,
        "missing_css_tokens": missing_css_tokens,
        "checks": checks,
        "valid": all(checks.values()),
    }


def main() -> int:
    """Execute all LU-UX-001 deterministic checks."""

    cases = [
        check_manifest(),
        *[
            check_scenario(scenario_id, expected)
            for scenario_id, expected
            in EXPECTED_SCENARIOS.items()
        ],
        check_static_runtime(),
    ]

    status = (
        "PASS"
        if all(case["valid"] for case in cases)
        else "FAIL"
    )

    output = {
        "milestone": "LU-UX-001",
        "status": status,
        "case_count": len(cases),
        "cases": cases,
    }

    print(json.dumps(output, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
