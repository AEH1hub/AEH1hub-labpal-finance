#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1
  pwd
)"

cd "$ROOT_DIR"

required_files=(
  ".gitignore"
  ".github/dependabot.yml"
  "SECURITY.md"
  "docs/security/DATA_CLASSIFICATION.md"
  "docs/security/GITHUB_SECURITY_SETTINGS.md"
  "docs/security/SEC-BASE-001_PORTFOLIO_DATA_PROTECTION.md"
  "docs/security/THREAT_MODEL_PORTFOLIO_INGESTION.md"
)

for required_file in "${required_files[@]}"; do
  if [[ ! -f "$required_file" ]]; then
    echo "Missing required security file: $required_file"
    exit 1
  fi
done

python3 - <<'PY'
from pathlib import Path
import re

path = Path("docs/security/THREAT_MODEL_PORTFOLIO_INGESTION.md")
text = path.read_text(encoding="utf-8")

if not text.startswith("# Portfolio Ingestion Threat Model"):
    raise SystemExit("Threat model has an invalid document opening.")

prohibited_fragments = [
    "That closes the trust-boundary diagram",
    "Then paste the missing sections",
    "supplied earlier",
    "## 12. Current decision#",
]

for fragment in prohibited_fragments:
    if fragment in text:
        raise SystemExit(
            f"Threat model contains prohibited conversational text: {fragment}"
        )

headings = [
    "## 1. Purpose",
    "## 2. Security objectives",
    "## 3. Protected assets",
    "## 4. Trust boundaries",
    "## 5. Threat actors",
    "## 6. Primary threats and mitigations",
    "## 7. Explicitly prohibited behavior",
    "## 8. Current security assumptions",
    "## 9. Verification requirements",
    "## 10. Residual risks",
    "## 11. Review triggers",
    "## 12. Current decision",
]

for index, heading in enumerate(headings):
    if text.count(heading) != 1:
        raise SystemExit(
            f"Threat-model heading must occur exactly once: {heading}"
        )

    start = text.index(heading) + len(heading)
    end = (
        text.index(headings[index + 1])
        if index + 1 < len(headings)
        else len(text)
    )
    body = text[start:end]
    substantive = re.sub(r"[\s#`*_|-]", "", body)

    if len(substantive) < 80:
        raise SystemExit(
            f"Threat-model section has insufficient content: {heading}"
        )

if text.count("```") % 2 != 0:
    raise SystemExit("Threat model contains an unclosed Markdown code fence.")

for number in range(1, 13):
    threat_id = f"T-{number:03d}"
    if threat_id not in text:
        raise SystemExit(f"Missing required threat identifier: {threat_id}")

print("Threat-model semantic structure: PASS")
PY

ignore_candidates=(
  ".env"
  ".env.local"
  ".private/founder.csv"
  "private/founder.csv"
  "imports/private/founder.csv"
  "exports/private/founder.csv"
  "reports/private/founder.log"
  "broker-exports/ibkr.csv"
  "portfolio-exports/founder.csv"
  "account-statements/statement.pdf"
  "founder-broker-export.csv"
  "founder-portfolio-export.csv"
  "portfolio.sqlite"
  "private.pem"
)

for candidate in "${ignore_candidates[@]}"; do
  if ! git check-ignore -q --no-index "$candidate"; then
    echo "Sensitive path is not ignored: $candidate"
    exit 1
  fi
done

tracked_restricted="$(
  git ls-files |
    grep -Ev '(^|/)\.env\.example$' |
    grep -Ei \
      '\.(pem|key|p12|pfx|sqlite|sqlite3|db|log)$|(^|/)\.env($|\.)|broker-export.*\.csv$|portfolio-export.*\.csv$|account-statement.*\.(csv|pdf)$' \
    || true
)"

if [[ -n "$tracked_restricted" ]]; then
  echo "Restricted tracked files detected:"
  printf '%s\n' "$tracked_restricted"
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
import json
import re

dependabot = Path(".github/dependabot.yml").read_text(encoding="utf-8")

for ecosystem in ("pip", "github-actions"):
    pattern = rf'package-ecosystem:\s*["\']?{re.escape(ecosystem)}["\']?'
    if not re.search(pattern, dependabot):
        raise SystemExit(f"Dependabot ecosystem missing: {ecosystem}")

fixture = json.loads(
    Path(
        "fixtures/portfolio-ingestion/"
        "founder-portfolio-expected.fixture.json"
    ).read_text(encoding="utf-8")
)

account_reference = fixture["source"]["account_reference"]

if not account_reference.startswith("ACCOUNT-REDACTED"):
    raise SystemExit("Founder fixture account reference is not redacted.")

if fixture["source"]["read_only"] is not True:
    raise SystemExit("Founder fixture must remain read-only.")

print("Dependabot and synthetic fixture checks: PASS")
PY

echo "SEC-BASE-001 security baseline: PASS"
