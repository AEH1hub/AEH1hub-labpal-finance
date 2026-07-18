# LU-LIVE-002 — API and Experience Integration Specification

## Status

Implementation milestone.

## Purpose

Connect the existing LU-LIVE-001 preserved-provider orchestration to the
existing LU-001 API and LU-UX-001 browser experience without duplicating
the reasoning engine, browser, or provider adapter.

## Integration path

Preserved normalized provider evidence
→ LU-LIVE-001
→ LU-001 API
→ LU-UX-001 browser

## Initial supported request

- Provider: Alpha Vantage
- Symbol: IBM
- Evidence mode: PRESERVED_PROVIDER_EVIDENCE
- Source: committed preserved provider fixture
- Network provider request: prohibited in this initial integration slice

## Required behavior

1. Validate provider, symbol, and evidence mode.
2. Load the preserved normalized provider record.
3. Reject symbol or provider mismatch.
4. Invoke LU-LIVE-001 without mutating evidence.
5. Preserve provenance, freshness, unknowns, limitations, Decision State,
   Review State, and history.
6. Return a browser-safe JSON response.
7. Never expose provider credentials.
8. Never silently fall back to mock evidence.
9. Preserve research-only authority boundaries.

## Browser behavior

The existing four deterministic scenarios remain available.

A separate preserved-provider control must allow the user to request the
IBM integration result and display:

- provider;
- requested and returned symbol;
- evidence identifier;
- retrieved timestamp;
- canonical freshness;
- Current Understanding;
- unknowns;
- limitations;
- Decision State;
- Review State;
- visible preserved-response notice.

## Prohibited behavior

LU-LIVE-002 does not:

- make provider requests from the browser;
- expose API credentials;
- provide investment recommendations;
- execute trades;
- add authentication;
- add persistence;
- claim production readiness.

## Verification requirements

- valid preserved IBM request;
- missing symbol rejection;
- unsupported provider rejection;
- unsupported symbol rejection;
- invalid evidence mode rejection;
- mock evidence rejection;
- API key absence;
- no silent mock fallback;
- Decision and Review state parity;
- old browser scenarios remain functional;
- preserved-provider result renders visibly;
- full repository verification passes.
