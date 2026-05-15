---
name: dasheng-daily-phase2
description: 大圣自媒体工作流第二环节技能。接收 `dasheng-daily-intake` 底稿（intake-records 或 dasheng_v11 输出），执行 v8 语义聚类并产出 8~10 个可执行详细 Brief。用于“进入第二环节”“生成详细 Brief”“给下一阶段选题包（含衍生话题与大纲）”场景。
---

# dasheng-daily-phase2

## 目标

把第一环节底稿转换为“可直接指导下一阶段选题”的标准交付：

1. 8~10 个选题（去噪后）
2. 每个选题的详细 Brief
3. 每个选题的衍生话题（3条）
4. 每个选题的写作大纲（5段）
5. 关键证据 + 下一阶段动作

## 输入

优先输入：
- `dasheng-daily-intake` 运行产物中的 `intake-records.json`

兼容输入：
- `memory/dasheng_v11_output_*.json`

## 输出（默认目录：`artifacts/phase2/`）

基础产物：
- `phase2-clusters-summary.json`
- `phase2-topic-index.json`
- `phase2-editorial-briefs.json`
- `phase2-brief-library.md`
- `phase2-topn-for-confirmation.json`

新增核心产物：
- `phase2-detailed-briefs.md`（8~10个选题详细版）

## 执行方式

自动衔接 intake 最新 run：

```bash
node /Users/lichengyin/clawd/skills/dasheng-daily-phase2/index.js
```

指定输入文件：

```bash
node /Users/lichengyin/clawd/skills/dasheng-daily-phase2/index.js /path/to/input.json
```

## 固定参数（本 skill 默认）

- `cluster_mode = semantic`
- `contract_version = v8`
- `cluster_target_min = 8`
- `cluster_target_max = 10`
- `max_clusters = 10`
- `top_n = 10`

## 最终文档格式（固定）

`phase2-detailed-briefs.md` 中每个选题固定包含：

1. 核心判断
2. 价值判断（热度/扩散/SA占比）
3. 衍生话题（3条）
4. 写作大纲（5段）
5. 关键证据（3条）
6. 下一阶段动作（最多3条）

## 格式冻结规则（防漂移）

- 第二环节交付格式视为“冻结契约”，默认不得变更。
- 未经用户明确指令，不允许修改以下硬约束：
  - 选题数：`8~10`
  - 衍生话题：`3` 条
  - 大纲：`5` 段
  - 关键证据：`3` 条
  - 下一阶段动作：最多 `3` 条
- 如需调整格式，必须先得到用户确认，再更新 `config.json + workflow contract`。

## 在大圣工作流中的位置

- 第一环节：`dasheng-daily-intake`
- 第二环节：`dasheng-daily-phase2`（本 skill）
- 下一环节：`dasheng-daily-outline`

本 skill 完成后，`next_step` 固定推进到 `dasheng-daily-outline`。
