---
name: dasheng-daily-draft
description: 大圣自媒体工作流初稿环节。接收已确认选题与大纲，按冻结标准生成可发布级公众号长稿。用于“进入初稿环节”“生成初稿”“写3篇长文（含数据/表格/来源）”等场景；默认执行 draft-standard-v2（每篇 >=5000 字，标准文章语体，不注入风格 DNA，证据仅来自底稿链接素材或外部公开数据源）。
---

# dasheng-daily-draft

## 目标

将已确认选题转为“可二改、可分发”的公众号初稿母版，并保持固定格式不漂移。

## 输入

优先输入：
- `dasheng-daily-outline` 产物（`outline-plans.json`）

兼容输入：
- 手工整理的 OutlinePlan JSON（包含标题、章节、子章节）

## 输出

默认输出到 run 目录 `artifacts/draft/`：
- `draft-packages.json`
- `draft-quality-report.json`

每篇稿件默认包含：
- 纯正文叙事（禁止内部流程话术）
- 标准文章语体（禁用风格 DNA 调整）
- 数据证据与论据链（仅使用底稿链接素材或外部公开数据）
- 关键数据表
- 策略与执行建议
- 数据与素材来源

## 固定标准（draft-standard-v2）

- 每篇字数：`>=5000`（按非空白字符计）
- 每篇必须有：`>=2` 张关键数据表
- 每篇必须有：`>=3` 条来源口径
- 每个 H2 章节正文段落：`<=5` 段
- 每篇必须有：数据证据 + 可执行建议
- 每篇必须通过“纯正文过滤”（禁用 `brief/run_id/提示词/模型参数/采集流程` 等内部词）
- 严禁把 intake/工作流内部统计（如热度、扩散、S/A占比）写入正文
- 数据、论据仅可来自：底稿链接素材或外部公开数据源（如 `akshare/tushare/新浪财经/人民网/CNN`）
- 禁止来源占位符（如 `example.com/source-pending`）
- 交付必须可追溯：本地稿件 + 飞书文档 + SOP 群报告

详细标准见：`references/draft-standard-v2.md`

## 生成提示词（固化）

本技能采用固定“写作提示词契约”，由代码和配置共同约束：
1. 标准文章语体（可直接用于公众号）
2. 论点-论据-论证闭环
3. 至少两张数据表支持关键结论
4. 段落长度可转写（后续文案/口播友好）
5. 自动写入转写策略：`rewrite_model_mode=bm`

## 防漂移规则

- 本技能处于格式冻结状态（`format_locked=true`）。
- 不允许修改以下字段：最小字数、纯正文约束、段落上限、表格/来源阈值、`rewrite_model_mode=bm`、`article_style_mode=standard_article`、`disable_style_dna=true`。
- 若用户明确要求改标准，先更新 `config.json` 与标准文档，再执行生成。

## 运行方式

```bash
node /Users/lichengyin/clawd/skills/dasheng-daily-draft/index.js \
  /path/to/outline-plans.json
```

可选参数（由上层调用传入）：
- `run_id`
- `min_chars`

## 交付约定

在需要对外交付时，按顺序执行：
1. 本地生成初稿 + 质量报告
2. 写入飞书（按篇/按包）
3. 同步 SOP 创作群
4. 回传“链接 + 字数 + 关键要点 + message_id”
