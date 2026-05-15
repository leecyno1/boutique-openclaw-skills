# Workflow Contract v8 (Domain-first Topic Clustering + Detailed Brief)

## Input

- Collector output: `intake-output-v11.json` (or equivalent `items[]` JSON)
- Phase2 engine: `scripts/phase2_rebuilder.py` (v8 mode)
- Domain config: `configs/phase2/domain_taxonomy.v8.json`
- Detailed brief builder: `skills/dasheng-daily-phase2/scripts/build_detailed_brief.py`

## Runtime Output Layout

`/Users/lichengyin/clawd/logs/daily-intake-YYYYMMDD-HHMMSS/phase2-prod-v8/`

Required artifacts:
- `phase2-domain-map.json`
- `phase2-topic-clusters.json`
- `phase2-cluster-audit.json`
- `phase2-brief-cards.md`
- `phase2-topn-for-confirmation.json`
- `phase2-rejects.json`
- `phase2-bitable-rows.json`
- `phase2-sync-contract.json`
- `phase2-editorial-briefs.json`
- `phase2-detailed-briefs.md`  ← 第二环节最终交付文档

## Processing Logic

1. Normalize + dedupe + noise filtering
2. Domain routing (soft assignment)
3. In-domain clustering
4. Cluster audit (purity/consistency/noise/platform-bias)
5. Split/merge and reject
6. Parent-child naming
7. Ranking with domain balance
8. Brief card generation (`phase2-editorial-briefs.json`)
9. Detailed brief rendering (8~10 topics, each with derived topics + outline)

## Quality Gate (hard)

- Phase2 clusters count in `[8, 10]`
- Detailed brief selected topics in `[8, 10]`
- Domain coverage `>= 5`
- Noise clusters not included in final selected topics
- Parent-child duplication not shown as flat duplicates
- Every selected topic contains:
  - 核心判断
  - 衍生话题（3）
  - 写作大纲（5段）
  - 关键证据（3）
  - 下一阶段动作（<=3）

## Review Publish Standard

When publishing to Feishu:
1. Create doc
2. Write `phase2-detailed-briefs.md`
3. Read back and verify `block_count > 1`
4. Return URL + revision_id + block_count + key stats

## Draft Stage Contract (locked)

When entering draft stage (after topic confirmation), use `dasheng-daily-draft` with `draft-standard-v1`.

Hard requirements per article:
- length `>=3000` non-whitespace chars
- include `核心结论` / `关键数据与证据` / `关键数据表` / `策略与执行建议` / `数据与素材来源`
- at least `1` key data table
- at least `3` source bullets
- output quality report artifact: `draft-quality-report.json`

Delivery requirements:
- local draft files persisted
- Feishu docs written and non-empty
- SOP group synced with links + counts + message id

## Bitable Standard

Use `phase2-bitable-rows.json` as source for upsert by `object_id/topic_cluster`.
Do not sync unless user explicitly requests.

## Drift Control (Format Freeze)

- This contract is the production baseline and is treated as format-locked.
- Do not change second-phase output shape unless user explicitly asks.
- Frozen fields for each selected topic:
  - 核心判断（1）
  - 衍生话题（3）
  - 写作大纲（5段）
  - 关键证据（3）
  - 下一阶段动作（<=3）
- Any future format change must update both:
  1. `skills/dasheng-daily-phase2/config.json`
  2. this contract file (`workflow-contract-v8.md`)
- Draft stage is also locked by `draft-standard-v1`; any change must update:
  1. `skills/dasheng-daily-draft/config.json`
  2. `skills/dasheng-daily-draft/references/draft-standard-v1.md`

## Backward Compatibility

- Keep v7 artifacts for rollback
- v8 is new subdir `phase2-prod-v8`
- preserve previous CLI options where possible
