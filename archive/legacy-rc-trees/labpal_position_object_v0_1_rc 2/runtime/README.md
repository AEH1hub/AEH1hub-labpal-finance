# FI-001A-RC-B6 Minimal Runtime Harness

Run:

```bash
python runtime/labpal_rc_harness.py
```

The harness performs four operations:

1. Validates Position fixtures against the Position Object JSON Schema.
2. Validates claims and append-only events against their schemas.
3. Runs the first semantic guardrails against Position fixtures.
4. Derives a scoped Current Understanding for `CTX-RC-READINESS`.

The harness must not turn selection into verification, erase prior claims, average contradictory evidence, or hide mandatory contradiction event IDs.
