# LabPal Security Policy

## Project status

LabPal is currently a pre-release Understanding Platform under active
development.

No version is presently approved for production use with unrestricted real
financial data.

The `main` branch represents the currently supported development baseline.

| Version or branch | Supported |
|---|---|
| `main` | Yes |
| Active security milestone branches | During review only |
| Archived branches and legacy prototypes | No |
| Unreleased local experiments | No |

## Reporting a vulnerability

Please do not report security vulnerabilities through a public GitHub issue,
discussion, pull request, social-media post, or other public channel.

Use GitHub Private Vulnerability Reporting through:

1. Open the repository's **Security and quality** area.
2. Open **Advisories**.
3. Select **Report a vulnerability**.

If private vulnerability reporting is unavailable, contact the repository
maintainers privately and ask them to open a draft repository security
advisory before sharing sensitive details.

Do not include real portfolio exports, account identifiers, API credentials,
access tokens, private keys, personal information, or other restricted data in
a public report.

## Information to include

A useful report should include:

- a clear description of the vulnerability;
- the affected file, component, workflow, or boundary;
- reproducible steps using synthetic or redacted data;
- the possible security or privacy impact;
- whether the issue can expose, alter, destroy, or misrepresent data;
- suggested remediation, when known;
- confirmation that no real user's private data was accessed or retained.

## Response targets

LabPal will aim to:

- acknowledge a valid report within five business days;
- complete an initial assessment within ten business days;
- communicate whether the report is accepted, rejected, duplicated, or needs
  more information;
- coordinate remediation and disclosure according to the seriousness and
  complexity of the issue.

These are response targets rather than guaranteed resolution deadlines.

## Security scope

Security reports may include:

- exposure of secrets or credentials;
- unauthorized access to restricted data;
- accidental persistence of broker exports;
- unsafe portfolio-file handling;
- provenance tampering;
- path traversal or unintended file access;
- malicious or malformed input handling;
- sensitive-data exposure in logs or errors;
- dependency vulnerabilities;
- authentication or authorization failures;
- code execution or injection risks;
- bypass of read-only or non-execution boundaries;
- incorrect representation of unknown, unverified, or synthetic information.

## Out of scope

The following are normally outside the scope of this repository:

- attacks against brokers or other third-party services;
- social engineering;
- denial-of-service testing that harms availability;
- testing with another person's financial or personal data;
- public disclosure before maintainers have had a reasonable opportunity to
  investigate;
- findings that require disabling normal browser or operating-system security;
- speculative reports without a reproducible security impact.

## Research safety

Security research must:

- use synthetic or redacted data;
- avoid accessing data belonging to other people;
- avoid modifying or deleting data;
- avoid persistence after testing;
- avoid service disruption;
- stop immediately if restricted information is encountered;
- report the discovery privately without copying or distributing the data.

## LabPal security principles

LabPal's security posture is based on:

- privacy by default;
- local and minimal handling of restricted data;
- read-only portfolio ingestion;
- no broker execution authority;
- no hidden recommendations;
- deterministic verification;
- explicit provenance;
- honest preservation of unknowns;
- strict separation of synthetic and real data;
- no secrets or private portfolio exports in source control;
- evidence before claims of security or readiness.

## Disclosure

Please allow LabPal's maintainers to investigate and prepare a correction
before public disclosure.

The repository may credit responsible reporters when requested and when doing
so does not create additional security or privacy risk.
