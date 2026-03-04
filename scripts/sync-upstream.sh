#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORT_DIR="$REPO_ROOT/reports"
mkdir -p "$REPORT_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$REPORT_DIR/sync-$TS.log"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "[ERROR] clawhub not found" | tee -a "$LOG"
  exit 1
fi

mapfile -t SKILLS < <(python3 - <<'PY'
import json
from pathlib import Path
p=Path('/Users/lichengyin/Desktop/Projects/boutique-openclaw-skills/catalog/skills.json')
data=json.loads(p.read_text(encoding='utf-8'))
seen=[]
for s in data.get('skills',[]):
    name=s['skill']
    if name not in seen:
        seen.append(name)
for name in seen:
    print(name)
PY
)

echo "[INFO] sync start $TS" | tee -a "$LOG"
for skill in "${SKILLS[@]}"; do
  echo "[SYNC] $skill" | tee -a "$LOG"
  if clawhub update "$skill" >>"$LOG" 2>&1; then
    echo "[OK] $skill" | tee -a "$LOG"
  else
    echo "[WARN] update failed: $skill" | tee -a "$LOG"
  fi
done

echo "[INFO] running audit" | tee -a "$LOG"
python3 "$REPO_ROOT/scripts/audit_skills.py" --report "$REPORT_DIR/audit-$TS.md" --json "$REPORT_DIR/audit-$TS.json" | tee -a "$LOG"

echo "[DONE] sync + audit complete" | tee -a "$LOG"
