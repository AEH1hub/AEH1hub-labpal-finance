# CI-001 — Repository Verification Gate

**Status:** CANDIDATE — ENGINEERING REVIEW REQUIRED
**Milestone:** CI-001
**Scope:** Deterministic repository verification
**Primary branch target:** `main`

## 1. Purpose

CI-001 defines LabPal's first automated repository verification gate.

Its purpose is to ensure that proposed repository changes cannot be treated as safely integrated merely because they compile locally, appear correct during manual review or contain a persuasive pull-request description.

CI-001 converts existing local verification responsibilities into one repeatable repository operation.

## 2. Governing principle

> A capability is earned only when specification, runtime, verification, report and repository history agree.

For changes protected by CI-001, repository history must also contain an independently executed verification result.

Local success remains evidence.

It is not, by itself, repository proof.

## 3. Responsibility

CI-001 is responsible for verifying that active repository changes preserve:

- dependency integrity;
- Python compilation;
- duplicate-key integrity;
- LU-001 API behavior;
- FI-REAS-001 reasoning behavior;
- B6 runtime behavior;
- Research Question behavior;
- deterministic execution;
- formatting integrity within the defined scope.

## 4. Initial verification scope

The initial CI-001 scope includes:

- active Python modules under `runtime/`;
- `requirements.txt`;
- `requirements-dev.txt`;
- deterministic harnesses that require no external credentials;
- repository whitespace checks;
- static detection of repeated dictionary keys.

The initial scope does not include:

- archived Python artifacts;
- live external-provider requests;
- credential-dependent validation;
- public deployment tests;
- browser usability tests;
- production security validation;
- regulatory review;
- autonomous remediation.

## 5. Required checks

CI-001 must execute:

1. runtime dependency installation;
2. development dependency installation;
3. dependency integrity through `pip check`;
4. Python compilation for active runtime modules;
5. Ruff duplicate-key analysis using rule `F601`;
6. LU-001 Understanding Platform harness;
7. FI-REAS-001 Unified Reasoning Pipeline harness;
8. FI-001A-RC-B6 harness;
9. FI-ASK-001 Research Question harness;
10. Git whitespace validation where repository history is available.

## 6. Failure behavior

The verification operation must:

- stop when a required gate fails;
- identify the failed gate;
- return a nonzero exit status;
- preserve the failure in GitHub Actions history;
- never silently convert failure into success;
- never use mock fallback to conceal missing dependencies;
- never require provider credentials for deterministic verification.

A failed repository check is evidence.

It must not be hidden or overwritten.

## 7. Approval behavior

A successful CI execution means only that the defined deterministic repository checks passed for the tested commit.

It does not establish:

- production readiness;
- external validity;
- regulatory compliance;
- security certification;
- user understanding;
- commercial value;
- provider reliability;
- autonomous authority.

## 8. Execution environments

CI-001 must be executable:

- locally through `scripts/verify_repository.sh`;
- remotely through GitHub Actions;
- without external provider credentials;
- from a clean dependency environment.

The local and remote operations must invoke the same verification script.

This prevents the GitHub workflow and local engineering process from silently diverging.

## 9. Workflow events

The GitHub Actions workflow must run:

- for pull requests targeting `main`;
- for pushes to `main`;
- through manual workflow dispatch when authorized.

## 10. Check identity

The primary GitHub Actions job should be named:

`LabPal Repository Verification`

This name should remain stable so it may later become a required branch-protection check.

## 11. Security boundaries

The workflow must:

- use no provider credentials;
- expose no secrets;
- avoid network calls other than dependency installation;
- use least-required GitHub permissions;
- avoid automatically modifying repository files;
- avoid committing generated changes;
- avoid autonomous merging.

## 12. Completion gates

CI-001 earns its states as follows.

### `SPECIFICATION_COMPLETE`

This specification completely defines the verification responsibility, scope, required checks and boundaries.

### `RUNTIME_DEMONSTRATED`

The local verification script executes the complete required check set.

### `HARNESS_PASSING`

The local script exits successfully after all required checks pass.

### `REPORT_COMPLETE`

The CI-001 report records the implementation, execution evidence, defects found, corrections and limitations.

### `MERGED`

The specification, script, workflow, dependencies and report are reviewed and merged into `main`.

### `GITHUB_CHECK_PROVEN`

A GitHub Actions execution completes successfully against the committed workflow.

This state cannot be earned through local execution alone.

## 13. Known limitations

CI-001 initially verifies deterministic repository integrity.

It does not yet provide:

- branch protection enforcement;
- independent human review;
- deployment verification;
- browser testing;
- integration with persistent storage;
- secret scanning policy;
- dependency vulnerability scanning;
- code coverage measurement;
- provider-health monitoring;
- production observability.

These are future responsibilities and must not be assumed.

## 14. Knowledge Heritage

CI-001 exists because repository history demonstrated that:

- syntactically valid Python can contain duplicate dictionary keys;
- narrow harness assertions can miss institutional data loss;
- worktrees may lack their own verification environments;
- pull-request descriptions can claim checks that GitHub did not execute;
- merges without automated checks permit repository truth and stated verification to diverge.

The correction history from LU-001-RC1 and LU-001-RC2 is preserved as evidence for this milestone.

CI-001 is therefore not introduced as generic tooling.

It is an earned institutional response to an observed repository failure mode.

## 15. Success condition

CI-001 succeeds when the same deterministic verification operation:

- passes locally;
- runs through GitHub Actions;
- records failures visibly;
- records success visibly;
- protects the active runtime from repeated dictionary keys;
- preserves all previously earned reasoning and platform behavior.

A green check means the defined checks passed.

It does not mean LabPal is externally proven.
