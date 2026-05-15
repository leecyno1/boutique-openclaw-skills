#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${REMOTION_PROJECT_DIR:-/Users/lichengyin/clawd/remotion-video-starter}"
MODE="${1:-hello}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

cd "$PROJECT_DIR"

if [[ "$MODE" == "--xhs" || "$MODE" == "xhs" ]]; then
  OUT_NAME="${2:-xhs-remotion-rebuild-${TIMESTAMP}.mp4}"
  npx remotion render src/index.jsx XhsRemotionRebuild "out/$OUT_NAME"
  echo "OUTPUT=$PROJECT_DIR/out/$OUT_NAME"
  exit 0
fi

TITLE="${1:-Remotion + OpenClaw}"
OUT_NAME="${2:-generated-${TIMESTAMP}.mp4}"
npm run render:skill -- "$TITLE" "$OUT_NAME"
echo "OUTPUT=$PROJECT_DIR/out/$OUT_NAME"
