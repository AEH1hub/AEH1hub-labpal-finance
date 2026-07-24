# SEC-BASE-001 — Portfolio Data Protection Baseline

## Purpose

Establish the minimum repository, privacy, and security controls required
before LabPal processes a real portfolio export.

## Current evidence

The initial repository audit found:

- no tracked broker exports;
- no tracked private-key files;
- no tracked environment-secret files;
- no obvious exposed credentials;
- no identified personal or financial identifiers;
- no known vulnerable installed dependency reported by the audit;
- a synthetic portfolio fixture with a redacted account reference.

This evidence is limited to the audited repository state. It is not a claim of
production security.

## Deliverables

- `SECURITY.md`
- data-classification policy
- portfolio-ingestion threat model
- restricted-data Git ignore rules
- Dependabot configuration
- deterministic security-baseline verification
- repository-gate integration
- documented GitHub security settings

## Non-goals

This milestone does not implement:

- real portfolio parsing;
- authentication;
- user accounts;
- broker connectivity;
- order execution;
- production deployment;
- external beta;
- legal compliance certification.

## Security gate

PU-INGEST-001B may begin only after SEC-BASE-001 proves:

- private portfolio paths are ignored;
- real broker exports are prohibited from tracking;
- repository fixtures remain synthetic;
- credential files are prohibited;
- account references in public fixtures are redacted;
- ingestion design remains read-only;
- the repository verification workflow invokes the security gate.

## Product-validation relationship

SEC-BASE-001 does not prohibit synthetic product validation.

PU-VALIDATE-001A may run in parallel using only synthetic and redacted data.
No real portfolio file, account identifier, credential, or restricted
information may be used in that validation.
