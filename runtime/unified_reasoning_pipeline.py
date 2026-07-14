"""FI-REAS-001 deterministic unified reasoning pipeline.

This module coordinates existing Research Question and Evidence responsibilities.
It does not perform live network requests and does not generate financial advice.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from runtime.research_question_harness import (
    schema_validator as research_question_validator,
)
from runtime.research_question_harness import semantic_violations


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCHEMA_PATH = (
    ROOT / "schemas" / "live-evidence-record.v0.1-ask.schema.json"
)

PERMITTED_DECISION_STATES = {
    "RESEARCH_ONLY",
    "INSUFFICIENT_EVIDENCE",
    "BLOCKED_BY_UNKNOWN",
    "READY_FOR_REVIEW",
    "REVISION_REQUIRED",
    "ACCEPTED_WITHIN_SCOPE",
    "DEFERRED",
}

PROHIBITED_ACTION_BOUNDARIES = {
    "RECOMMENDATION_RISK",
    "BLOCKED_FOR_REVIEW",
}


class PipelineValidationError(ValueError):
    """Raised when the pipeline input is structurally unusable."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []

    for value in values:
        if not isinstance(value, str):
            continue

        normalized = value.strip()

        if normalized and normalized not in result:
            result.append(normalized)

    return result


def _evidence_validator() -> Draft202012Validator:
    schema = _load_json(EVIDENCE_SCHEMA_PATH)

    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def _research_question_schema_validator() -> Any:
    """Resolve the reusable Research Question validator interface.

    The existing harness may return the validator directly or as part of a
    tuple. FI-REAS-001 preserves that interface instead of redefining it.
    """

    candidate = research_question_validator()

    if hasattr(candidate, "iter_errors"):
        return candidate

    if isinstance(candidate, tuple):
        for item in candidate:
            if hasattr(item, "iter_errors"):
                return item

    raise PipelineValidationError(
        "Research Question validator interface did not provide "
        "an object with iter_errors()."
    )


def _validate_required_pipeline_fields(payload: dict[str, Any]) -> None:
    required = {
        "execution_id",
        "executing_actor",
        "scope",
        "research_question",
    }

    missing = sorted(
        field
        for field in required
        if field not in payload or payload[field] in (None, "", {})
    )

    if missing:
        raise PipelineValidationError(
            "Missing required pipeline fields: " + ", ".join(missing)
        )

    if not isinstance(payload["research_question"], dict):
        raise PipelineValidationError(
            "research_question must be an object."
        )


def _collect_claims(research_question: dict[str, Any]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []

    for collection_name in (
        "source_facts",
        "source_interpretations",
        "labpal_interpretations",
    ):
        collection = research_question.get(collection_name, [])

        if not isinstance(collection, list):
            continue

        for claim in collection:
            if not isinstance(claim, dict):
                continue

            preserved = dict(claim)
            preserved["origin_collection"] = collection_name
            claims.append(preserved)

    for evidence in research_question.get("evidence_records", []):
        if not isinstance(evidence, dict):
            continue

        claims.append(
            {
                "claim_id": (
                    f"CLAIM-FROM-{evidence.get('evidence_id', 'UNKNOWN')}"
                ),
                "claim_text": evidence.get("claim_text", ""),
                "claim_classification": evidence.get(
                    "claim_classification",
                    "UNKNOWN",
                ),
                "freshness_state": evidence.get(
                    "freshness_state",
                    "UNKNOWN_FRESHNESS",
                ),
                "evidence_id": evidence.get("evidence_id"),
                "origin_collection": "evidence_records",
            }
        )

    return claims


def _derive_current_statement(
    research_question: dict[str, Any],
) -> tuple[str, str | None]:
    priority_collections = (
        "labpal_interpretations",
        "source_interpretations",
        "source_facts",
    )

    for collection_name in priority_collections:
        collection = research_question.get(collection_name, [])

        if not isinstance(collection, list) or not collection:
            continue

        candidate = collection[-1]

        if not isinstance(candidate, dict):
            continue

        statement = str(candidate.get("claim_text", "")).strip()

        if statement:
            return statement, candidate.get("claim_id")

    return (
        "No sufficiently supported current interpretation is available.",
        None,
    )


def _derive_decision_state(
    *,
    action_boundary: str,
    evidence_count: int,
    unknowns: list[str],
    contradictions: list[str],
    challenging_evidence_ids: list[str],
    semantic_rule_violations: list[dict[str, Any]],
    evidence_validation_errors: list[dict[str, Any]],
) -> str:
    if semantic_rule_violations or evidence_validation_errors:
        return "REVISION_REQUIRED"

    if action_boundary in PROHIBITED_ACTION_BOUNDARIES:
        return "BLOCKED_BY_UNKNOWN"

    if contradictions or challenging_evidence_ids:
        return "REVISION_REQUIRED"

    if evidence_count == 0 and unknowns:
        return "INSUFFICIENT_EVIDENCE"

    if evidence_count == 0:
        return "RESEARCH_ONLY"

    return "READY_FOR_REVIEW"


def run_reasoning_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    """Run one deterministic and reviewable reasoning cycle."""

    _validate_required_pipeline_fields(payload)

    research_question = payload["research_question"]
    rq_schema_errors = sorted(
        error.message
        for error in _research_question_schema_validator().iter_errors(
            research_question
        )
    )
    rq_semantic_violations = semantic_violations(research_question)

    evidence_records = research_question.get("evidence_records", [])
    evidence_records = (
        evidence_records if isinstance(evidence_records, list) else []
    )

    evidence_errors: list[dict[str, Any]] = []
    evidence_validator = _evidence_validator()

    for record in evidence_records:
        evidence_id = (
            record.get("evidence_id", "UNKNOWN")
            if isinstance(record, dict)
            else "UNKNOWN"
        )

        if not isinstance(record, dict):
            evidence_errors.append(
                {
                    "evidence_id": evidence_id,
                    "errors": ["Evidence record must be an object."],
                }
            )
            continue

        errors = sorted(
            error.message
            for error in evidence_validator.iter_errors(record)
        )

        if errors:
            evidence_errors.append(
                {
                    "evidence_id": evidence_id,
                    "errors": errors,
                }
            )

    challenging_evidence_ids = _unique_strings(
        payload.get("challenging_evidence_ids", [])
    )
    contradictions = _unique_strings(
        payload.get("contradictions", [])
    )

    evidence_ids = _unique_strings(
        [
            record.get("evidence_id")
            for record in evidence_records
            if isinstance(record, dict)
        ]
    )

    supporting_evidence_ids = [
        evidence_id
        for evidence_id in evidence_ids
        if evidence_id not in challenging_evidence_ids
    ]

    evidence_unknowns: list[str] = []

    for record in evidence_records:
        if isinstance(record, dict):
            evidence_unknowns.extend(record.get("unknowns", []))

    unknowns = _unique_strings(
        list(research_question.get("unknowns", []))
        + evidence_unknowns
        + list(payload.get("additional_unknowns", []))
    )

    current_statement, selected_claim_id = _derive_current_statement(
        research_question
    )

    if rq_semantic_violations or evidence_errors:
        violated_rules = sorted(
            {
                violation.get("rule_id", "UNKNOWN_RULE")
                for violation in rq_semantic_violations
            }
        )

        rule_summary = (
            ", ".join(violated_rules)
            if violated_rules
            else "evidence validation failure"
        )

        current_statement = (
            "No admissible Current Understanding was adopted because "
            f"the input violated: {rule_summary}."
        )
        selected_claim_id = None

    action_boundary = research_question.get(
        "action_boundary_state",
        "RESEARCH_ONLY",
    )

    decision_state = _derive_decision_state(
        action_boundary=action_boundary,
        evidence_count=len(evidence_ids),
        unknowns=unknowns,
        contradictions=contradictions,
        challenging_evidence_ids=challenging_evidence_ids,
        semantic_rule_violations=rq_semantic_violations,
        evidence_validation_errors=evidence_errors,
    )

    if decision_state not in PERMITTED_DECISION_STATES:
        raise PipelineValidationError(
            f"Pipeline produced prohibited decision state: {decision_state}"
        )

    validation_passed = not (
        rq_schema_errors
        or rq_semantic_violations
        or evidence_errors
    )

    review_state = (
        "READY_FOR_REVIEW"
        if validation_passed
        and decision_state in {"READY_FOR_REVIEW", "RESEARCH_ONLY"}
        else "REVISION_REQUIRED"
    )

    reasoning_summary = (
        f"LabPal preserved the original question, considered "
        f"{len(evidence_ids)} evidence record(s), preserved "
        f"{len(unknowns)} unknown(s), "
        f"{len(contradictions)} contradiction(s), and derived "
        f"the bounded decision state {decision_state}. "
        "Selection does not equal verification."
    )

    return {
        "milestone": "FI-REAS-001",
        "execution_id": payload["execution_id"],
        "executing_actor": payload["executing_actor"],
        "scope": payload["scope"],
        "preserved_question": {
            "research_question_id": research_question.get(
                "research_question_id"
            ),
            "original_question": research_question.get(
                "original_question"
            ),
            "question_type": research_question.get("question_type"),
            "action_boundary_state": action_boundary,
            "evidence_mode": research_question.get("evidence_mode"),
        },
        "evidence_considered": evidence_ids,
        "supporting_evidence": supporting_evidence_ids,
        "challenging_evidence": challenging_evidence_ids,
        "excluded_evidence": list(
            payload.get("excluded_evidence", [])
        ),
        "unknowns": unknowns,
        "contradictions": contradictions,
        "claims": _collect_claims(research_question),
        "current_understanding": {
            "status": "WORKING_INTERPRETATION",
            "current_statement": current_statement,
            "selected_claim_id": selected_claim_id,
            "supporting_evidence_ids": supporting_evidence_ids,
            "challenging_evidence_ids": challenging_evidence_ids,
            "material_unknowns": unknowns,
            "contradictions": contradictions,
            "previous_understanding": payload.get(
                "previous_understanding"
            ),
            "verification_notice": (
                "Selection does not equal verification."
            ),
            "history_preserved": True,
        },
        "decision_state": decision_state,
        "review_state": review_state,
        "reasoning_summary": reasoning_summary,
        "next_evidence_needed": _unique_strings(
            list(research_question.get("source_requirements", []))
            + list(payload.get("next_evidence_needed", []))
        ),
        "history_preserved": True,
        "validation_results": {
            "valid": validation_passed,
            "research_question_schema_errors": rq_schema_errors,
            "research_question_semantic_violations": (
                rq_semantic_violations
            ),
            "evidence_validation_errors": evidence_errors,
        },
    }
