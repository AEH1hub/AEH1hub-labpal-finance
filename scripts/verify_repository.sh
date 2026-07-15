#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1
  pwd
)"

cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python}"
RUFF_BIN="${RUFF_BIN:-ruff}"

CURRENT_GATE="initialization"

report_failure() {
  local exit_code=$?

  echo
  echo "LABPAL REPOSITORY VERIFICATION: FAIL"
  echo "Failed gate: ${CURRENT_GATE}"
  echo "Exit code: ${exit_code}"

  exit "$exit_code"
}

trap report_failure ERR

run_gate() {
  local gate_name="$1"

  shift

  CURRENT_GATE="$gate_name"

  echo
  echo "============================================================"
  echo "Gate: ${gate_name}"
  echo "============================================================"

  "$@"

  echo "Result: PASS"
}

run_gate \
  "Dependency integrity" \
  "$PYTHON_BIN" -m pip check

run_gate \
  "Duplicate dictionary-key integrity" \
  "$RUFF_BIN" check \
    --select F601 \
    runtime

CURRENT_GATE="Python compilation"

echo
echo "============================================================"
echo "Gate: Python compilation"
echo "============================================================"

while IFS= read -r -d '' python_file; do
  "$PYTHON_BIN" -m py_compile "$python_file"
done < <(
  find runtime \
    -maxdepth 1 \
    -type f \
    -name '*.py' \
    -print0
)

echo "Result: PASS"

run_gate \
  "LU-UX-001 Understanding Experience harness" \
  "$PYTHON_BIN" -m runtime.understanding_experience_harness

run_gate \
  "LU-001 Understanding Platform harness" \
  "$PYTHON_BIN" -m runtime.understanding_api_harness

run_gate \
  "FI-REAS-001 Unified Reasoning Pipeline harness" \
  "$PYTHON_BIN" -m runtime.unified_reasoning_pipeline_harness

run_gate \
  "FI-001A-RC-B6 harness" \
  "$PYTHON_BIN" runtime/labpal_rc_harness.py

run_gate \
  "FI-ASK-001 Research Question harness" \
  "$PYTHON_BIN" runtime/research_question_harness.py

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  run_gate \
    "Git whitespace integrity" \
    git diff --check
else
  echo
  echo "Gate: Git whitespace integrity"
  echo "Result: SKIPPED — not inside a Git worktree"
fi

echo
echo "============================================================"
echo "LABPAL REPOSITORY VERIFICATION: PASS"
echo "All required deterministic gates passed."
echo "============================================================"
