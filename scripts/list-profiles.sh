#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for f in "$REPO_ROOT"/profiles/*.json; do
  python3 - <<'PY' "$f"
import json,sys
p=sys.argv[1]
d=json.load(open(p,'r',encoding='utf-8'))
print(f"{d['id']}: {d['title']}")
PY
done
