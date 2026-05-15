---
name: reusable-footage-material
description: 聚焦视频素材质量的执行技能。用于单独验证或调优“资料片/纪录片/archive footage 优先、规避口播/访谈/大字幕”的视频检索策略；适合做单点质量测试或素材风格优化，不作为 dasheng 第三环节的默认统一入口。
---

# Reusable Footage Material

这是一个 **视频质量调优 / 独立执行** skill。

## 用途
- 单独跑一次非口播素材流
- 验证 query、来源、质量阈值是否合理
- 快速审查 `video-search-sources.json` 与 `quality_summary`

## 默认边界
- 不负责第三环节的主流程统一入口语义
- 不负责替代 `dasheng-daily-material` 的 manifest / next_step 链路

## 默认执行入口
第三环节实际执行请优先使用：`dasheng-daily-material`

## 参考
- `references/workflow-contract.md`
