#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skill-id> [optimizer-model] [target-model]" >&2
  exit 2
fi

SKILL_ID="$1"
OPTIMIZER_MODEL="${2:-${SKILLOPT_OPTIMIZER_MODEL:-}}"
TARGET_MODEL="${3:-${SKILLOPT_TARGET_MODEL:-$OPTIMIZER_MODEL}}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILLOPT_DIR="$ROOT_DIR/optimization/skillopt"
SKILL_PATH="$ROOT_DIR/skills/default/$SKILL_ID/SKILL.md"
SPLIT_DIR="$ROOT_DIR/optimization/datasets/skillopt/$SKILL_ID"
OUT_ROOT="$ROOT_DIR/optimization/skillopt-runs/$SKILL_ID"
READY_CHECK="$ROOT_DIR/optimization/scripts/check_skillopt_ready.py"

if [[ ! -f "$SKILL_PATH" ]]; then
  echo "Missing skill file: $SKILL_PATH" >&2
  exit 1
fi

for split in train val test; do
  if [[ ! -f "$SPLIT_DIR/$split/items.json" ]]; then
    echo "Missing dataset split: $SPLIT_DIR/$split/items.json" >&2
    exit 1
  fi
done

if [[ -z "$OPTIMIZER_MODEL" || -z "$TARGET_MODEL" ]]; then
  echo "Set SKILLOPT_OPTIMIZER_MODEL and SKILLOPT_TARGET_MODEL, or pass models as arguments." >&2
  exit 1
fi

SKILLOPT_OPTIMIZER_MODEL="$OPTIMIZER_MODEL" \
SKILLOPT_TARGET_MODEL="$TARGET_MODEL" \
python3 "$READY_CHECK" "$SKILL_ID" --require-models

cd "$SKILLOPT_DIR"
python scripts/train.py \
  --config configs/searchqa/default.yaml \
  --skill_init "$SKILL_PATH" \
  --split_dir "$SPLIT_DIR" \
  --out_root "$OUT_ROOT" \
  --optimizer_model "$OPTIMIZER_MODEL" \
  --target_model "$TARGET_MODEL"

echo "Best optimized skill: $OUT_ROOT/best_skill.md"
