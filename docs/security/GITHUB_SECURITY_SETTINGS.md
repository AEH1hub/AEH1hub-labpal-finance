# GitHub Security Settings

**Milestone:** SEC-BASE-001
**Status:** Required configuration and verification record
**Scope:** LabPal repository security

## 1. Purpose

This document records the GitHub security controls required for LabPal.

A control must not be represented as enabled merely because it appears in
documentation. Its actual state must be confirmed through GitHub settings, API
evidence, workflow evidence, or another preserved verification record.

## 2. Confirmed repository controls

The repository contains:

- a GitHub Actions repository-verification workflow;
- verification on pull requests targeting `main`;
- verification on pushes to `main`;
- read-only workflow content permissions;
- Dependabot configuration for Python;
- Dependabot configuration for GitHub Actions;
- a deterministic SEC-BASE security gate;
- integration of that gate into repository verification.

## 3. Controls requiring confirmation

The following controls remain explicit unknowns until GitHub settings or API
evidence confirms them:

- dependency graph;
- Dependabot alerts;
- Dependabot security updates;
- private vulnerability reporting;
- secret scanning;
- push protection;
- branch protection for `main`;
- required status checks;
- required pull-request reviews;
- protection against force pushes;
- protection against branch deletion.

## 4. Required main-branch policy

Before external beta or production use, `main` should require:

- changes through pull requests;
- passing LabPal Repository Verification;
- resolved review conversations;
- no force pushes;
- no branch deletion;
- review of security-sensitive dependency changes.

## 5. Evidence rule

Documentation is not proof that a GitHub-hosted control is enabled.

A hosted control remains unverified until its state is confirmed and preserved
as reviewable evidence.

## 6. Current decision

SEC-BASE-001 establishes the required repository security posture without
claiming that every GitHub-hosted control is currently enabled.
