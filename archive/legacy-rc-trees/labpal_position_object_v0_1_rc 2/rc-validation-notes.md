# RC Validation Notes

## Good news

The schema encodes the evidence-earned core without returning to the nine-layer overbuilt model. It preserves UNKNOWN states, forces provenance for SUPPORTED assertions, and distinguishes DISCRETE from STANDING continuity.

## Bad news / risk

The schema is still conceptual JSON Schema. Runtime behavior is untested. It does not yet enforce every semantic rule that LabPal requires, such as append-only event history or contradiction firewall behavior.

## Unresolved reality

- PC-002 loss case remains missing.
- Real broker ledger reconciliation remains incomplete.
- Direct conflict / CONFLICTED assertion state is parked.
- Product/legal review remains required before any recommendation or execution behavior.

## Next required test

FI-001A-RC-B2 — Schema Validation & Failure Fixtures

Create invalid fixtures that must fail:
1. SUPPORTED assertion without source_reference.
2. SUPPORTED assertion without evidence_basis.
3. UNKNOWN assertion without unknown_reason.
4. Unsupported continuity_type.
5. Object trying to use numeric confidence.
