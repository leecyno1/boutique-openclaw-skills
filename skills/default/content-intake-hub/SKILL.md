---
name: content-intake-hub
description: 统一的内容入口 Skill。用于接收自动采集结果与人工命题输入，标准化为 Topic Intake Record，为后续 Brief 构建提供统一上游。适用于热点采集、人工提题、手工指定大纲意图、跨媒介内容任务发起。
---

# Content Intake Hub

## 目标
把自动采集与人工输入统一纳入同一种入口协议，减少后续工作流分叉。

## 支持的输入来源
1. 自动采集结果
2. 人工命题或选题想法
3. 人工指定的大纲意图
4. 指定某个内容要改编成另一种媒介

## 工作流
1. 识别输入来源：`auto` 或 `manual`
2. 提取主题、来源、媒介意图、优先级、已有素材线索
3. 标准化为 Topic Intake Record
4. 若输入明显属于同一已知主题，可附上已有 brief 或 cluster 引用
5. 输出结构化 intake 结果，交给 `content-brief-builder`

## 输出契约
1. `Intake Summary`
2. `Source Mode`
3. `Topic Intake Record`
4. `Next Recommended Step`

## 边界
- 不直接生成完整大纲
- 不直接写稿
- 不替代素材补全
- 不负责最终发布

## 参考
- `docs/content-brief-schema-v2.md`
- `docs/content-workflow-v2.md`
