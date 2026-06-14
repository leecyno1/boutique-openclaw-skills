#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -z "${TUSHARE_TOKEN:-}" ]]; then
  if [[ -t 0 ]]; then
    printf 'Enter TUSHARE_TOKEN (input hidden): ' >&2
    stty -echo
    read -r TUSHARE_TOKEN
    stty echo
    printf '\n' >&2
  else
    read -r TUSHARE_TOKEN
  fi
  export TUSHARE_TOKEN
fi

python3 "$REPO_ROOT/scripts/evaluate_finance_tushare.py"
unset TUSHARE_TOKEN
