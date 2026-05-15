# Workflow Contract

> Note: this is the legacy v7 contract. For current production (domain-first + 8~10 detailed topics), use `workflow-contract-v8.md`.

## Input

- Collector script: `/Users/lichengyin/clawd/scripts/dasheng_skill_v11.py`
- Phase2 script: `/Users/lichengyin/clawd/scripts/phase2_rebuilder.py`
- Topic spec: `/Users/lichengyin/clawd/configs/phase2/topic_specs.v1.json`

## Run Output Layout

`/Users/lichengyin/clawd/logs/daily-intake-YYYYMMDD-HHMMSS/`

- `intake-output-v11.json`
- `workflow-report.json`
- `phase2-prod-v7/`
  - `phase2-clusters-summary.json`
  - `phase2-brief-library.md`
  - `phase2-topn-for-confirmation.json`
  - `phase2-topic-index.json`
  - `phase2-editorial-briefs.json`
  - `phase2-bitable-rows.json`
  - `phase2-sync-contract.json`
  - `phase2-unmatched.json`

## Processing Scope

- Default processes **all intake topics** (~1000 draft items) for clustering.
- Optional `--sa-only` limits to S/A when explicitly needed.

## Review Publish Standard

When publishing for review:

1. Create a new Feishu doc.
2. Write full `phase2-brief-library.md`.
3. Read back and verify `block_count > 1`.
4. Return doc URL + key stats + block validation.

## Quality Gate

- Intake step must provide a valid JSON input.
- Phase2 step must produce all v6 outputs listed above.
- Summary must include non-empty `stats` and `clusters`.
- Brief must include heat analysis + evidence chain + editorial suggestions.
