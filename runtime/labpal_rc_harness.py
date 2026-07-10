#!/usr/bin/env python3
import json
import pathlib
import sys
from collections import defaultdict

try:
    import jsonschema
except ImportError:
    print(json.dumps({"status":"ERROR","message":"jsonschema is required"}))
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

position_schema = load(ROOT / "schemas" / "position-object-v0.1-rc.schema.json")
event_schema = load(ROOT / "schemas" / "event-model-v0.1-rc-b4.schema.json")
claim_schema = load(ROOT / "schemas" / "claim-v0.1-rc-b4.schema.json")

def schema_errors(schema, obj):
    v = jsonschema.Draft202012Validator(schema)
    return [e.message for e in v.iter_errors(obj)]

def semantic_violations(obj):
    violations = []
    review = (obj.get("observation_and_review", {}).get("decision_process_review") or "").lower()
    if "good decision because the financial outcome was positive" in review:
        violations.append({"rule_id":"SG-001","message":"Positive outcome used as proof of decision quality."})
    for a in obj.get("material_assertions", []):
        claim = a.get("claim", "").lower()
        basis = a.get("evidence_basis")
        source = str(a.get("source_reference", "")).lower()
        scope = a.get("scope", "").lower()
        if "proves" in claim and "purchase transaction occurred" in claim and basis == "CONTEXTUAL_LINKAGE":
            violations.append({"rule_id":"SG-002","message":"Checkpoint delta promoted into transaction event."})
        if ("ai" in source or "ai analysis" in claim) and a.get("assertion_state") == "SUPPORTED" and ("appropriateness" in scope or "appropriate" in claim):
            violations.append({"rule_id":"SG-003","message":"AI-only support used for appropriateness judgment."})
    dp = obj.get("decision_purpose", {})
    if dp.get("purpose_state") == "SUPPORTED" and "derived" in str(dp.get("source_reference", "")).lower():
        violations.append({"rule_id":"SG-004","message":"Derived context labeled as supported historical purpose."})
    return violations

def derive(claims, events, context_id):
    claim_by_id = {c["claim_id"]: c for c in claims}
    by_subject = defaultdict(list)
    for e in events:
        by_subject[e["subject_id"]].append(e)

    candidates = []
    for c in claims:
        cid = c["claim_id"]
        evs = by_subject[cid]
        verifications = [e for e in evs if e["event_type"] == "VERIFICATION_EVENT"]
        supports = [e for e in verifications if e["payload"]["verification_result"] == "SUPPORTS"]
        challenges = [e for e in verifications if e["payload"]["verification_result"] == "CHALLENGES"]
        selections = [e for e in evs if e["event_type"] == "SELECTION_EVENT" and e["payload"]["context_id"] == context_id]
        candidates.append({
            "claim_id": cid,
            "claim_text": c["claim_text"],
            "selected": any(e["payload"]["selection_decision"] == "SELECTED" for e in selections),
            "support_scopes": [e["payload"]["verification_scope"] for e in supports],
            "challenge_scopes": [e["payload"]["verification_scope"] for e in challenges]
        })

    selected = [c for c in candidates if c["selected"]]
    if len(selected) != 1:
        return {
            "status":"UNRESOLVED",
            "reason":"Current Understanding requires exactly one selected claim for this prototype context.",
            "candidates":candidates
        }

    chosen = selected[0]
    relationships = []
    contradictions = []
    for e in events:
        if e["event_type"] == "CLAIM_RELATIONSHIP_EVENT" and e["subject_id"] == chosen["claim_id"]:
            relationships.append(e["payload"])
        if e["event_type"] == "SELECTION_EVENT" and e["subject_id"] == chosen["claim_id"] and e["payload"]["context_id"] == context_id:
            contradictions.extend(e["payload"].get("mandatory_contradictions", []))

    return {
        "status":"WORKING_INTERPRETATION",
        "context_id":context_id,
        "selected_claim_id":chosen["claim_id"],
        "current_statement":chosen["claim_text"],
        "verification_notice":"Selection does not equal verification.",
        "support_scopes":chosen["support_scopes"],
        "challenge_scopes":chosen["challenge_scopes"],
        "relationships":relationships,
        "mandatory_contradiction_event_ids":sorted(set(contradictions)),
        "history_preserved":True
    }

def main():
    position_files = [
        ROOT / "fixtures" / "pc-001-xagusd-discrete.fixture.json",
        ROOT / "fixtures" / "pc-004-standing-dca.fixture.json",
    ]
    positions = [load(p) for p in position_files]
    claims = load(ROOT / "fixtures" / "claims.fixture.json")
    events = load(ROOT / "fixtures" / "events.fixture.json")

    schema_results = []
    semantic_results = []
    for path, obj in zip(position_files, positions):
        errs = schema_errors(position_schema, obj)
        schema_results.append({"file":path.name,"valid":not errs,"errors":errs})
        sem = semantic_violations(obj)
        semantic_results.append({"file":path.name,"valid":not sem,"violations":sem})

    for c in claims:
        errs = schema_errors(claim_schema, c)
        schema_results.append({"file":c["claim_id"],"valid":not errs,"errors":errs})
    for e in events:
        errs = schema_errors(event_schema, e)
        schema_results.append({"file":e["event_id"],"valid":not errs,"errors":errs})

    current = derive(claims, events, "CTX-RC-READINESS")
    status = "PASS" if all(x["valid"] for x in schema_results + semantic_results) and current["status"] == "WORKING_INTERPRETATION" else "FAIL"
    output = {
        "milestone":"FI-001A-RC-B6",
        "status":status,
        "schema_validation":schema_results,
        "semantic_validation":semantic_results,
        "current_understanding":current
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if status == "PASS" else 1)

if __name__ == "__main__":
    main()
