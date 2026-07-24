
That closes the trust-boundary diagram.

Then paste the missing sections **5 through 12** from the complete threat-model content supplied earlier:

```text
## 5. Threat actors
## 6. Primary threats and mitigations
## 7. Explicitly prohibited behavior
## 8. Current security assumptions
## 9. Verification requirements
## 10. Residual risks
## 11. Review triggers
## 12. Current decision# Portfolio Ingestion Threat Model

**Milestone:** SEC-BASE-001  
**Status:** Baseline security model  
**Scope:** Portfolio Understanding ingestion  
**Last reviewed:** 2026-07-24

## 1. Purpose

This document defines the baseline threat model for LabPal portfolio
ingestion.

The purpose of portfolio ingestion is to transform a user-supplied portfolio
source into LabPal's canonical portfolio snapshot without exposing private
financial information, fabricating missing information, modifying the source,
or enabling financial execution.

This threat model applies before implementation of PU-INGEST-001B and must be
reviewed whenever ingestion authority, supported source types, storage
behavior, or deployment architecture changes.

## 2. Security objectives

Portfolio ingestion must:

- remain read-only;
- preserve source provenance;
- preserve unknown or missing values explicitly;
- avoid exposing portfolio or account information;
- reject malformed or unsupported input safely;
- avoid logging sensitive source content;
- avoid committing real portfolio exports to the repository;
- avoid retaining source files without an explicit retention decision;
- avoid silently changing financial values;
- avoid enabling trading, order transmission, or portfolio execution;
- produce deterministic results for equivalent inputs.

## 3. Protected assets

The protected assets include:

### 3.1 Portfolio information

- security symbols and instrument names;
- quantities and position sizes;
- market values;
- average entry prices;
- cost basis;
- cash balances;
- portfolio totals;
- portfolio allocation and concentration;
- transaction or activity history when later supported.

### 3.2 Account and identity information

- broker account references;
- account numbers;
- user names;
- email addresses;
- residential addresses;
- tax identifiers;
- bank identifiers;
- broker-generated customer identifiers;
- filenames or metadata that reveal identity.

### 3.3 Authentication material

- API keys;
- access tokens;
- refresh tokens;
- session credentials;
- private keys;
- credential-bearing URLs;
- local environment files.

### 3.4 Integrity assets

- the original source artifact;
- source hashes;
- source row counts;
- timestamps;
- currency identifiers;
- canonical portfolio output;
- validation results;
- unknown-value records.

## 4. Trust boundaries

The ingestion path contains the following trust boundaries:

```text
Untrusted portfolio source
        |
        v
Input boundary and file validation
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
Validation and deterministic output
