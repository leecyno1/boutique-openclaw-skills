#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/install-suite.sh <suite-id> [--dry-run]

Install a grouped skill suite from catalog/suites/<suite-id>.json.
Suites are domain packs kept separate from the no-duplicate standard bundle.
USAGE
}

if [[ $# -lt 1 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

SUITE_ID=""
DRY_RUN="false"
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="true" ;;
    --help|-h) usage; exit 0 ;;
    *)
      if [[ -z "$SUITE_ID" ]]; then
        SUITE_ID="$arg"
      else
        echo "[ERROR] unknown argument: $arg" >&2
        usage >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$SUITE_ID" ]]; then
  echo "[ERROR] missing suite id" >&2
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
SUITE_JSON="$REPO_ROOT/catalog/suites/$SUITE_ID.json"
SOURCE_DIR="$REPO_ROOT/skills/default"

if [[ ! -f "$SUITE_JSON" ]]; then
  echo "[ERROR] missing suite manifest: $SUITE_JSON" >&2
  exit 1
fi

readarray_output="$(python3 - <<'PY' "$SUITE_JSON"
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
skills = payload.get("skills", [])
if len(skills) != len(set(skills)):
    raise SystemExit("suite contains duplicate skills")
print(payload.get("title") or payload.get("id") or "suite")
print(",".join(payload.get("api_keys", []) or []))
print(",".join(payload.get("requires_tools", []) or []))
for skill in skills:
    print(skill)
PY
)"

SUITE_TITLE="$(printf '%s\n' "$readarray_output" | sed -n '1p')"
API_KEYS="$(printf '%s\n' "$readarray_output" | sed -n '2p')"
TOOLS="$(printf '%s\n' "$readarray_output" | sed -n '3p')"
mapfile -t SKILLS < <(printf '%s\n' "$readarray_output" | sed '1,3d')

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "[ERROR] suite '$SUITE_ID' has no skills" >&2
  exit 1
fi

echo "[INFO] Suite: $SUITE_TITLE ($SUITE_ID)"
echo "[INFO] Skills: ${#SKILLS[@]}"
echo "[INFO] Target: $TARGET"
if [[ -n "$API_KEYS" ]]; then
  echo "[INFO] API keys: $API_KEYS"
fi
if [[ -n "$TOOLS" ]]; then
  echo "[INFO] Tools: $TOOLS"
fi

if [[ "$DRY_RUN" != "true" ]]; then
  mkdir -p "$TARGET"
fi

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill"
  dst="$TARGET/$skill"
  if [[ ! -d "$src" ]]; then
    echo "[ERROR] missing local skill source: $skill" >&2
    exit 1
  fi
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] sync $src -> $dst"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "[INSTALL] $skill"
  fi
done

echo "[DONE] Suite '$SUITE_ID' processed."
