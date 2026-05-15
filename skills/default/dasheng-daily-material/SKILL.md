---
name: dasheng-daily-material
description: 素材合并环节默认技能（material+补素材已合并）。用于在 dasheng 工作流中于 rewrite 之后统一补齐视频、图片、图表、CSV、引用与证据清单；支持通过 run_id 自动回溯 ContentBrief。适用于“改写后补素材”“补齐素材包并做审计”的场景。
---

# Dasheng Daily Material

这是 rewrite 后的**素材合并统一入口**。

## 工作流位置（v4）
- intake -> phase2 -> outline -> draft -> rewrite(`dasheng-daily-final`) -> material（本 skill） -> postmortem

## 默认执行流
1. 读取 `content-briefs.json`（或仅传 `run_id` 自动从 manifest 回溯 `ContentBrief`）
2. 定位对应 `phase2-editorial-briefs.json`
3. 对每个选题 rank 调用 `scripts/run_topic_material_workflow_v2.py`
4. 使用统一视频策略：
   - 登录站点默认 `CDP cookies` 注入（9222）
   - Douyin 失败时 `CDP 解析流 + ffmpeg` 回退
   - 搜索优先 `纪录片/资料片/历史影像/archive footage`
   - 规避 `口播/访谈/podcast/对谈/大字幕`
5. 回写：
   - `material-packs.json`
   - `material-workflow-v2-results.json`
   - `run_manifest.json`
6. 输出下一步：`dasheng-daily-postmortem`

## 输出重点
- `manifest/report.json`：主结果计数与路径
- `manifest/video-search-sources.json`：检索 query 与选中源审计
- `material-packs.json`：素材合并环节最终结构化素材包
- `quality_summary`：素材质量阈值检查与告警

## 参考
- `references/merged-third-stage-analysis.md`
- `/Users/lichengyin/clawd/workflow-control/dasheng/config/workflow-v4.json`
