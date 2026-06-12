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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}"
SOURCE_DIR="$REPO_ROOT/skills/default"

mapfile -t SKILLS < <(python3 "$REPO_ROOT/scripts/catalog.py" "$PROFILE")

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "[ERROR] Profile '$PROFILE' resolved to empty skill list"
  exit 1
fi

echo "[INFO] Profile: $PROFILE"
echo "[INFO] Skills: ${#SKILLS[@]}"
echo "[INFO] Target: $TARGET"
printf ' - %s\n' "${SKILLS[@]}"

if [[ "$DRY_RUN" != "true" ]]; then
  mkdir -p "$TARGET"
fi

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill"
  dst="$TARGET/$skill"
  if [[ -d "$src" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "[DRY-RUN] sync $src -> $dst"
    else
      rm -rf "$dst"
      cp -R "$src" "$dst"
      echo "[INSTALL] $skill"
    fi
  else
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "[DRY-RUN] clawhub install $skill"
    else
      if ! command -v clawhub >/dev/null 2>&1; then
        echo "[ERROR] local source missing for '$skill' and clawhub is not installed" >&2
        echo "Install clawhub first: npm i -g clawhub" >&2
        exit 1
      fi
      echo "[INSTALL] $skill"
      clawhub install "$skill"
    fi
  fi
done

echo "[DONE] Profile '$PROFILE' processed."
