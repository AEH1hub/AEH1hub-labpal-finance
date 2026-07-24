# Portfolio Ingestion Threat Model

**Milestone:** SEC-BASE-001
**Status:** Baseline security model
**Scope:** Portfolio Understanding ingestion
**Last reviewed:** 2026-07-24

## 1. Purpose

This document defines the baseline threat model for LabPal Portfolio
Understanding ingestion.

Portfolio ingestion transforms a user-supplied source into LabPal's
canonical portfolio snapshot. It must do so without exposing private
financial data, fabricating missing information, modifying the source, or
enabling financial execution.

The model must be reviewed whenever source types, retention, storage,
deployment architecture, access boundaries, or system authority changes.

## 2. Security objectives

Portfolio ingestion must remain read-only, preserve source provenance,
preserve unknown values explicitly, reject malformed input safely, and
produce deterministic output for equivalent input.

It must prevent credential exposure, unauthorized retention, silent
financial corruption, execution authority, and real portfolio data entering
Git history.

## 3. Protected assets

Protected portfolio information includes holdings, quantities, cost basis,
average entry prices, cash balances, market values, currencies, income,
allocation, concentration, transactions, and portfolio totals.

Protected identity information includes account references, account
numbers, names, email addresses, residential addresses, tax identifiers,
bank identifiers, broker customer identifiers, and identifying metadata.

Protected authentication material includes API keys, tokens, session
credentials, cookies, private keys, certificates, credential-bearing URLs,
and local environment files.

Integrity assets include original sources, hashes, row counts, timestamps,
currencies, canonical output, validation results, and unknown records.

## 4. Trust boundaries

Every portfolio source must be treated as untrusted input.

```text
Untrusted portfolio source
        |
        v
Input and size validation
        |
        v
Source-specific parser
        |
        v
Normalization boundary
        |
        v
Canonical portfolio contract
        |
        v
Deterministic validation
```

A filename, extension, provider label, or familiar structure is not proof
that a source is safe, complete, authentic, or financially accurate.

## 5. Threat actors

Relevant threat sources include accidental users, malformed broker exports,
malicious files, compromised local processes, vulnerable dependencies,
unauthorized persons, accidental developer commits, and implementation
defects that change financial meaning.

Accidental disclosure and accidental corruption are primary risks even
where no intentional attacker exists.

## 6. Primary threats and mitigations

### T-001 — Private portfolio data committed to Git

Real exports, statements, databases, logs, or account files could enter
repository history.

Controls include restrictive ignore rules, synthetic fixtures, staged-file
review, restricted-file scanning, and immediate incident handling.

### T-002 — Credential disclosure

Keys, tokens, cookies, certificates, or credentials could appear in code,
fixtures, documentation, errors, screenshots, or logs.

Controls include environment-managed secrets, ignored local files,
placeholder examples, redacted failures, and secret review before merge.

### T-003 — Malicious or malformed input

Crafted files could cause parser confusion, path access, code execution,
invalid output, or excessive resource use.

Controls include strict source validation, bounded input, no macro
execution, no dynamic code execution, and explicit rejection.

### T-004 — Silent financial corruption

Quantities, values, currencies, timestamps, signs, or decimal precision
could change without detection.

Controls include decimal-safe arithmetic, explicit currencies and
timezones, schema validation, deterministic output, fixture parity, and no
silent currency conversion.

### T-005 — Provenance loss

LabPal could lose the ability to explain where imported values originated.

Controls include preserving sanitized source identity, source hash,
provider, source type, row count, import time, and validation outcome.

### T-006 — Sensitive logging

Portfolio rows, account identifiers, credentials, or raw source contents
could enter logs or exception traces.

Controls include structural logging, identifier redaction, synthetic
harnesses, and review of errors and failure messages.

### T-007 — Unnecessary retention

Raw portfolio files could remain stored longer than required or in an
unapproved location.

Controls include no repository storage, explicit retention decisions,
temporary processing isolation, deletion rules, and documented backups.

### T-008 — Cross-user exposure

A future hosted service could expose one user's portfolio to another user.

Controls include prohibiting multi-user hosting until authentication,
authorization, user-scoped storage, and access-control tests exist.

### T-009 — Parser authority expansion

Ingestion could begin recommending trades, transmitting orders, modifying
accounts, or interpreting unsupported fields silently.

Controls include read-only authority, explicit unknowns, canonical
validation, and separate approval for any new responsibility.

### T-010 — Dependency compromise

A vulnerable or malicious dependency could damage parser integrity or
repository security.

Controls include minimal dependencies, dependency integrity checks,
Dependabot, vulnerability review, and controlled dependency changes.

### T-011 — Spreadsheet formula injection

Formula-like values could later execute when viewed or exported through
spreadsheet software.

Controls include treating cells only as data, never evaluating formulas,
sanitizing future exports, and testing formula-like synthetic fixtures.

### T-012 — Resource exhaustion

Oversized files, rows, strings, nesting, or archive expansion could exhaust
memory, CPU, storage, or processing time.

Controls include explicit file, payload, row, field, and expansion limits
before hosted ingestion is approved.

## 7. Explicitly prohibited behavior

Portfolio ingestion must not execute trades, transmit orders, request
broker write authority, modify broker data, fabricate missing values,
infer unknown currencies silently, execute formulas or embedded code,
store real portfolio sources as fixtures, expose financial rows in logs,
or use production credentials in deterministic tests.

Parser output must not be presented as personalized financial advice.

## 8. Current security assumptions

The baseline assumes fixtures are synthetic and redacted, development is
local and read-only, no production broker connection exists, no production
user database exists, no hosted multi-user ingestion exists, and no durable
retention of real portfolio files has been approved.

Recommendations, broker write authority, and execution remain prohibited.

## 9. Verification requirements

Before a source parser is merged, verification must prove that its accepted
source type is named, malformed input is rejected, missing fields become
unknowns, values use decimal-safe handling, currencies and timestamps are
explicit, provenance is preserved, and the original source remains
unchanged.

Equivalent input must produce deterministic output. Tests must contain no
real account information, and every security and repository gate must pass.

## 10. Residual risks

This baseline does not eliminate local-machine compromise, unknown
dependency vulnerabilities, incorrect file selection, improperly redacted
future fixtures, source-format drift, infrastructure mistakes, or future
legal and regulatory obligations.

Residual risks must remain visible and must not be represented as solved.

## 11. Review triggers

Review is required when a source format is introduced, API ingestion is
proposed, real user data is processed, retention is introduced,
authentication or multi-user access is added, hosted ingestion is deployed,
broker write authority is proposed, a security incident occurs, or the
canonical portfolio contract changes materially.

Every review must preserve evidence of what changed and why.

## 12. Current decision

SEC-BASE-001 permits deterministic development using synthetic, redacted,
read-only portfolio information.

It does not approve production ingestion, hosted storage of real portfolio
files, multi-user access, broker write authority, order execution, or
personalized financial recommendations.

Those capabilities require separate security, privacy, legal, operational,
and product review.
