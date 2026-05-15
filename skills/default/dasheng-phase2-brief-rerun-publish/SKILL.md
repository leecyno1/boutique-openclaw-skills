---
name: dasheng-phase2-brief-rerun-publish
description: Re-run Dasheng phase2 brief workflow, merge a user-specified backup topic into a 10-topic package, enforce full detailed briefs for all topics, publish full正文 to Feishu doc, and notify SOP group. Use when users ask “并入重跑brief”、“10个题都要详细brief”、“写入文档并发送到群”.
---

# dasheng-phase2-brief-rerun-publish

## Inputs

- `run_id`（required），例如：`daily-intake-20260326-074911`
- `intake_file`（required），例如：`/Users/lichengyin/clawd/logs/<run_id>/intake-records.json`
- `extra_topic`（optional），例如：`高市早苗与日本极右势力`
- `doc_token`（optional，若不传则新建文档）
- `sop_chat_id`（optional，默认：`oc_975d43c5704bf8c755bb9e32bf7c3922`）

## Hard Rules

1. `brief` 大纲必须由大模型推理生成，不允许硬编码模板句。
2. 最终必须是 `10` 个题，每题都要完整包含：
   - 核心判断
   - 衍生话题（3条）
   - 大纲（5段）
   - 关键证据（3条）
   - 下一阶段动作（最多3条）
3. 飞书发布必须先写入、再回读校验；校验未过不得宣称完成。
4. 发群消息必须用 `message.action=send` + `card`（Feishu 纯文本发送常见 400）。

## Workflow

### Step 1: 重跑 phase2

```bash
node /Users/lichengyin/clawd/skills/dasheng-daily-phase2/index.js <intake_file>
```

记录输出中的：
- `output_dir`
- `detailed_brief_file`
- `detailed_topics`

### Step 2: 合并备选题并产出 10 题版

1. 若用户要求并入备选题：
   - 从 `intake-records.json` 按关键词检索证据（优先跨平台）。
   - 用大模型生成该备选题 5 段大纲（禁止模板复读）。
   - 追加为 `## 10. ...`，写入：
     - `artifacts/phase2/phase2-detailed-briefs-10topics-with-<slug>.md`
     - 同步复制到 `/Users/lichengyin/clawd/logs/<run_id>/`
2. 若原始产物已是 10 题，直接进入校验。

### Step 3: 结构校验（必须通过）

运行快速校验：

```bash
python3 - <<'PY'
from pathlib import Path
import re
p = Path('<10-topic-markdown-file>')
t = p.read_text(encoding='utf-8')
sections = len(re.findall(r'^##\s+\d+\.\s+', t, flags=re.M))
outline = len(re.findall(r'^###\s+大纲$', t, flags=re.M))
evidence = len(re.findall(r'^###\s+关键证据$', t, flags=re.M))
next_actions = len(re.findall(r'^###\s+下一阶段动作$', t, flags=re.M))
ok = sections == 10 and outline >= 10 and evidence >= 10 and next_actions >= 10
print({'sections': sections, 'outline': outline, 'evidence': evidence, 'next_actions': next_actions, 'ok': ok})
if not ok:
    raise SystemExit(1)
PY
```

### Step 4: 飞书写入（正文全量）

1. `feishu_doc.create`（无 `doc_token` 时）
2. `feishu_doc.write` 覆盖写入完整 Markdown
3. 若超长导致写入不完整：分块 `append` 直到写完
4. `feishu_doc.read` 回读校验：
   - `block_count >= 200`（10题正文通常显著高于此值）
   - 内容包含 `10. 地缘与国际关系·`（或目标第10题标题）
   - 能看到每题的 `大纲 / 关键证据 / 下一阶段动作`

### Step 5: 发送 SOP 群通知

使用 `message.send` + `card`，内容至少包括：
- `run_id`
- 文档链接
- 已并入备选题名称
- 校验结果（如 `block_count` / `revision_id`）

返回 `messageId` 作为发送凭据。

## Failure Handling

- phase2 失败：直接返回错误输出，不进入发布。
- 10题校验失败：停止并报告缺失项，不发群。
- 飞书回读失败：重写一次；仍失败则标记 blocked 并给出具体失败点。
- 群发送失败：保留文档链接并报告错误码，不伪造“已发送”。

## Output Contract

完成时必须返回：
- `run_id`
- 10题文件路径（runtime + logs）
- Feishu 文档 URL + `revision_id` + `block_count`
- SOP 群消息 `messageId`
- 并入题名称与校验结果
