# LabPal Data Classification

**Milestone:** SEC-BASE-001  
**Status:** Development baseline

## Purpose

This policy defines how LabPal classifies and handles information.

Classification is determined by the potential harm caused by unauthorized
disclosure, modification, loss, or misrepresentation.

## PUBLIC

Information intentionally suitable for public repository use.

Examples:

- README files;
- published architecture documents;
- schemas;
- source code without secrets;
- synthetic fixtures;
- redacted examples;
- public security policy;
- deterministic verification reports containing no private data.

Requirements:

- must contain no credentials;
- must contain no real account identifiers;
- synthetic information must be clearly identifiable;
- mock or unverified evidence must remain labeled.

## INTERNAL

Information intended for maintainers and controlled project operations.

Examples:

- unfinished roadmaps;
- internal review notes;
- non-sensitive development reports;
- security implementation planning;
- operational checklists.

Requirements:

- review before publication;
- remove unnecessary personal information;
- never use INTERNAL as a substitute for protecting restricted data.

## CONFIDENTIAL

Information that could expose financial structure, project operations, or
non-public user context.

Examples:

- redacted portfolio summaries derived from real sources;
- non-public product research;
- detailed security findings;
- internal incident records;
- unreleased validation observations.

Requirements:

- collect only when necessary;
- minimize fields;
- redact identifiers;
- restrict access;
- do not commit unless explicitly approved and safely transformed.

## RESTRICTED

Information that must never enter the public repository.

Examples:

- real broker exports;
- account statements;
- account numbers;
- API keys;
- access or refresh tokens;
- passwords;
- private keys and certificates;
- authentication cookies;
- names linked to private financial holdings;
- addresses, identification documents, or tax identifiers;
- unredacted vulnerability evidence;
- production secrets;
- raw private logs.

Requirements:

- local or approved protected storage only;
- never commit to Git;
- never place in fixtures;
- never print in logs;
- never include in screenshots or public reports;
- delete safely when no longer required;
- rotate or revoke immediately if exposed.

## Portfolio-ingestion rule

Before a real portfolio source is processed:

1. classify it as RESTRICTED;
2. confirm that its location is ignored by Git;
3. avoid copying it into repository fixtures;
4. calculate provenance without publishing its contents;
5. redact account identity before canonical exposure;
6. preserve unknowns rather than inferring private or missing information.

## Synthetic fixture rule

Repository fixtures must be:

- intentionally synthetic;
- free of real account identifiers;
- free of credentials;
- marked as fixture, mock, synthetic, or redacted;
- safe to publish;
- deterministic.

## Escalation

When classification is uncertain, use the more restrictive classification
until the uncertainty is resolved.
