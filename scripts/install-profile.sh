#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <profile-id> [--dry-run]"
  exit 1
fi

PROFILE="$1"
DRY_RUN="false"
if [[ "${2:-}" == "--dry-run" ]]; then
  DRY_RUN="true"
fi

if ! command -v clawhub >/dev/null 2>&1; then
  echo "[ERROR] clawhub not found. Install first: npm i -g clawhub"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

mapfile -t SKILLS < <(python3 "$REPO_ROOT/scripts/catalog.py" "$PROFILE")

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "[ERROR] Profile '$PROFILE' resolved to empty skill list"
  exit 1
fi

echo "[INFO] Profile: $PROFILE"
echo "[INFO] Skills: ${#SKILLS[@]}"
printf ' - %s\n' "${SKILLS[@]}"

for skill in "${SKILLS[@]}"; do
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] clawhub install $skill"
  else
    echo "[INSTALL] $skill"
    clawhub install "$skill"
  fi
done

echo "[DONE] Profile '$PROFILE' processed."
