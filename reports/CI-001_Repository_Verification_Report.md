# CI-001 — Repository Verification Report

**Status:** CANDIDATE — GITHUB CHECK REQUIRED
**Milestone:** CI-001
**Verification scope:** Deterministic active-repository verification
**Primary branch target:** `main`

## Purpose

CI-001 introduces LabPal's first shared repository verification operation.

The milestone converts previously manual verification responsibilities into one executable script that can run both locally and through GitHub Actions.

Its purpose is to prevent repository changes from being treated as safely integrated merely because they compile locally, appear correct during manual inspection or contain a persuasive pull-request description.

## Origin and Knowledge Heritage

CI-001 was earned through an observed repository failure pattern.

LU-001-RC1 introduced a duplicate Python dictionary key. The file remained syntactically valid, but Python silently retained only the later value. A previously earned capability disappeared from the API response.

LU-001-RC2 corrected the defect and strengthened the harness.

The incident demonstrated that:

- syntactic validity is not sufficient;
- narrow harnesses may miss institutional data loss;
- local worktrees may lack verification environments;
- pull-request descriptions may claim checks that GitHub did not execute;
- automated repository verification was necessary before further product expansion.

## Implemented artifacts

- `.github/workflows/labpal-verification.yml`
- `scripts/verify_repository.sh`
- `docs/operations/CI-001_Repository_Verification_Gate.md`
- `reports/CI-001_Repository_Verification_Report.md`
- `requirements-dev.txt`

## Dependency record

The initial development verification dependency is:

- `ruff==0.15.21`

Runtime dependencies remain recorded separately in `requirements.txt`.

## Verification scope

The shared operation verifies:

1. dependency integrity through `pip check`;
2. repeated dictionary-key integrity using Ruff rule `F601`;
3. Python compilation for active runtime modules;
4. LU-001 Understanding Platform behavior;
5. FI-REAS-001 Unified Reasoning Pipeline behavior;
6. FI-001A-RC-B6 behavior;
7. FI-ASK-001 Research Question behavior;
8. Git whitespace integrity.

The operation performs no live provider requests and requires no provider credentials.

## Successful local result

The shared verification operation completed successfully with:

- dependency integrity — PASS;
- duplicate dictionary-key integrity — PASS;
- Python compilation — PASS;
- LU-001 API harness — PASS, 10 cases;
- FI-REAS-001 harness — PASS, 4 cases;
- FI-001A-RC-B6 harness — PASS;
- FI-ASK-001 Research Question harness — PASS;
- Git whitespace integrity — PASS.

The script returned exit code `0`.

## Failure-propagation result

Failure behavior was tested by invoking the script with a nonexistent Ruff executable.

The operation:

- stopped at the duplicate dictionary-key gate;
- identified the failed gate;
- printed a failure result;
- returned exit code `1`;
- did not continue as if verification had succeeded.

Failure propagation therefore passed.

## Existing non-blocking finding

A full default Ruff scan reported one existing `F841` finding:

- `runtime/labpal_rc_harness.py`
- local variable `claim_by_id` is assigned but never used.

This finding is not part of the initial CI-001 blocking scope.

CI-001 initially enforces rule `F601`, which directly protects against the repository defect that earned this milestone.

Expansion to broader lint enforcement requires a separate review of existing code-quality debt.

## GitHub Actions design

The workflow:

- runs for pull requests targeting `main`;
- runs for pushes to `main`;
- supports manual workflow dispatch;
- uses read-only repository permissions;
- installs runtime and development dependencies;
- invokes the same `scripts/verify_repository.sh` operation used locally;
- contains no provider credentials;
- performs no autonomous modifications or merges.

## Completion gates

| Gate | State |
|---|---|
| Specification | COMPLETE LOCALLY |
| Runtime | DEMONSTRATED LOCALLY |
| Harness | PASSING LOCALLY |
| Report | COMPLETE — REVIEW REQUIRED |
| Repository History | PENDING COMMIT, REVIEW AND MERGE |
| GitHub Check | NOT YET PROVEN |

## Known limitations

CI-001 does not yet provide:

- branch-protection enforcement;
- independent human review;
- full Ruff rule enforcement;
- code coverage measurement;
- dependency vulnerability scanning;
- secret scanning policy;
- deployment verification;
- browser testing;
- production monitoring;
- external-provider validation;
- production security certification.

## Completion assessment

CI-001 may be marked `MERGED` only after its artifacts are committed, reviewed and merged into `main`.

CI-001 may be marked `GITHUB_CHECK_PROVEN` only after GitHub Actions executes the committed workflow successfully.

Local execution alone cannot earn that state.

## Conclusion

CI-001 demonstrates that LabPal can convert an observed repository failure into preserved institutional knowledge and then into automated protection.

A green CI result means the defined deterministic repository checks passed.

It does not mean LabPal is production-ready or externally proven.
