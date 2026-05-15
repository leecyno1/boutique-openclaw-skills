---
name: dasheng-intake-brief-prod
description: Execute the reusable Dasheng production workflow for "rerun intake -> process ~1000-item draft in enhanced phase2 -> generate 8~10 detailed topic briefs (with derived topics + outlines)". Use when users ask to rerun采集+第二环节、生成详细Brief选题包、或复用同类选题生产流程。
---

# dasheng-intake-brief-prod

## Overview

Use this skill to run the stable production chain:
1) run or reuse latest intake data,
2) process intake topics with v8 phase2 contract (domain-first clustering),
3) output detailed brief assets (heat/evidence/suggestions/risk/next-actions),
4) generate `phase2-detailed-briefs.md` with 8~10 topics (each with derived topics + outline),
5) generate draft-stage longform articles via `dasheng-daily-draft`,
6) draft 后直接进入 rewrite（`dasheng-daily-final`），
7) rewrite 后进入素材合并环节（`dasheng-daily-material`，含补素材）。

## Workflow

### Step 1: Run pipeline

Default (rerun intake + phase2):

```bash
python3 /Users/lichengyin/clawd/skills/dasheng-intake-brief-prod/scripts/run_pipeline.py
```

Reuse existing intake file:

```bash
python3 /Users/lichengyin/clawd/skills/dasheng-intake-brief-prod/scripts/run_pipeline.py \
  --input-file /Users/lichengyin/clawd/memory/dasheng_v11_output_YYYYMMDD_HHMMSS.json
```

Run v8 detailed-brief mode (recommended, 8~10 topics):

```bash
python3 /Users/lichengyin/clawd/skills/dasheng-intake-brief-prod/scripts/run_pipeline.py \
  --input-file /Users/lichengyin/clawd/memory/dasheng_v11_output_YYYYMMDD_HHMMSS.json \
  --contract-version v8 \
  --cluster-target-min 8 \
  --cluster-target-max 10 \
  --max-clusters 10 \
  --top-n 10
```

Read JSON output and capture:
- `run_dir`
- `phase2_dir`
- `summary_file`
- `brief_file`
- `topn_file`
- `topic_index_file`
- `editorial_briefs_file`
- `stats`

### Step 2: Validate outputs

Must exist and be non-empty:
- `phase2-clusters-summary.json`
- `phase2-brief-library.md`
- `phase2-topn-for-confirmation.json`
- `phase2-topic-index.json`
- `phase2-editorial-briefs.json`
- `phase2-detailed-briefs.md`

Surface key numbers:
- total input topics
- classified count
- unmatched count
- cluster count
- TOP topics with heat

### Step 3: Publish review doc (optional)

When user asks to review in Feishu:
1. `feishu_doc action=create` with title `YYYY-MM-DD 第二环节详细 Brief（8~10选题）`
2. `feishu_doc action=write` with `phase2-detailed-briefs.md`（可选追加基础库 `phase2-brief-library.md`）
3. `feishu_doc action=read` and verify `block_count > 1`
4. return doc URL + revision_id + block_count

### Step 4: Optional Bitable sync

Only run when user explicitly requests.
Use `phase2-bitable-rows.json` with upsert strategy by `object_id/topic`.

### Step 5: Draft -> Rewrite -> Material（简化顺序）

When user confirms entering draft stage:
1. select confirmed topics (typically TOP3 or user-specified set)
2. generate draft files with `dasheng-daily-draft`
3. rewrite stage: run `dasheng-daily-final`
4. material merged stage: run `dasheng-daily-material`（含补素材）
5. publish to Feishu + sync SOP group with links and counts

## Format Lock

- Phase2 detailed brief output is format-locked for production.
- Default and expected shape: 8~10 topics; each topic includes core judgment + 3 derived topics + 5-section outline + 3 evidence items + max 3 next actions.
- Do not drift from this shape unless user explicitly requests a contract change.

## Output Contract

Always return:
- run id / run directory
- summary stats
- top topics + heat
- output file paths（必须含 `phase2-detailed-briefs.md`）
- Feishu review doc URL (if created)
- next step: TOP3 confirmation -> Outline -> Draft -> Rewrite(`dasheng-daily-final`) -> Material merged(`dasheng-daily-material`)

## Resources

- Pipeline runner: `scripts/run_pipeline.py`
- Data contract (v7): `references/workflow-contract.md`
- Data contract (v8 blueprint): `references/workflow-contract-v8.md`
- Architecture blueprint: `/Users/lichengyin/clawd/docs/phase2-v8-blueprint.md`
- Draft stage skill: `/Users/lichengyin/clawd/skills/dasheng-daily-draft/SKILL.md`
- Draft standard: `/Users/lichengyin/clawd/skills/dasheng-daily-draft/references/draft-standard-v1.md`
