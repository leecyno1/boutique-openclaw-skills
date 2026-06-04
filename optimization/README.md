# Skill Optimization Module

This directory contains the optional optimization layer for improving repository skills with external evaluators.

## Modules

- `skillopt/` — vendored source snapshot of [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt), MIT licensed.
- `datasets/skillopt/` — local benchmark splits used to optimize selected skills.
- `skillopt-runs/` — generated training/evaluation outputs. This directory is intentionally ignored by git.

## When to Use

Use SkillOpt when a skill needs measurable improvement against repeatable examples, such as QA accuracy, spreadsheet reasoning, document QA, coding task execution, or domain-specific answer quality.

Do not use it for routine README edits or simple metadata/tag maintenance.

For repository policy, candidate selection, quality gates, and recommended first targets, see [`docs/SKILLOPT_USAGE.md`](../docs/SKILLOPT_USAGE.md).

## Workflow

1. Pick one target skill from `skills/default/<skill-id>/SKILL.md`.
2. Build a small task set with `train/`, `val/`, and `test/` splits under `optimization/datasets/skillopt/<skill-id>/`.
3. Run SkillOpt against that split and the target skill as `skill_init`.
4. Inspect `optimization/skillopt-runs/<skill-id>/best_skill.md`.
5. Manually review the diff before copying improvements back to `skills/default/<skill-id>/SKILL.md`.
6. Regenerate the catalog and docs after accepting an optimized skill.

## Quick Start

```bash
cd optimization/skillopt
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

For OpenAI-compatible endpoints, export credentials before training:

```bash
export AZURE_OPENAI_ENDPOINT="https://api.openai.com/v1"
export AZURE_OPENAI_API_KEY="sk-..."
export AZURE_OPENAI_AUTH_MODE="openai_compatible"
```

Example SearchQA-style run from the repository root:

```bash
python3 optimization/scripts/create_skillopt_dataset.py <skill-id> --template qa
export SKILLOPT_OPTIMIZER_MODEL=<optimizer-model>
export SKILLOPT_TARGET_MODEL=<target-model>
python3 optimization/scripts/check_skillopt_ready.py <skill-id> --require-models
./optimization/scripts/run_skillopt_searchqa.sh <skill-id>
python3 optimization/scripts/review_skillopt_candidate.py <skill-id>
```

Equivalent direct command:

```bash
cd optimization/skillopt
python scripts/train.py \
  --config configs/searchqa/default.yaml \
  --skill_init ../../skills/default/<skill-id>/SKILL.md \
  --split_dir ../datasets/skillopt/<skill-id> \
  --out_root ../skillopt-runs/<skill-id> \
  --optimizer_model <optimizer-model> \
  --target_model <target-model>
```

Expected output:

- `optimization/skillopt-runs/<skill-id>/best_skill.md`
- `optimization/skillopt-runs/<skill-id>/history.json`
- `optimization/skillopt-runs/<skill-id>/summary.json`

## Dataset Shape

For SearchQA-style optimization, create:

```text
optimization/datasets/skillopt/<skill-id>/
  train/items.json
  val/items.json
  test/items.json
```

Each `items.json` is a JSON array:

```json
[
  {
    "id": "case-001",
    "question": "What should the skill do in this scenario?",
    "context": "Ground-truth reference material or task context.",
    "answers": ["Expected concise answer"]
  }
]
```

## Safety Rules

- Treat `best_skill.md` as a candidate, not an automatic replacement.
- Preserve upstream origin metadata and license files when optimizing imported skills.
- Keep benchmark data free of secrets, private customer data, and API keys.
- Do not commit `skillopt-runs/`, virtual environments, or downloaded benchmark datasets.
- If optimization changes behavior materially, update the skill guide and catalog tags.

## Updating SkillOpt

To refresh the vendored source snapshot:

```bash
rm -rf optimization/skillopt
git clone --depth 1 https://github.com/microsoft/SkillOpt.git optimization/skillopt
rm -rf optimization/skillopt/.git
```

Then re-check this README and any local run scripts against upstream CLI changes.
