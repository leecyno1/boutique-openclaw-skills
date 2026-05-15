# 输入契约迁移指南

## 概述

wechat-topic-outline-planner 已从 v1（裸主题输入）升级到 v2（Brief + Material + Media Plan 输入）。本指南说明如何迁移和使用新契约。

---

## v1 vs v2 对比

### v1 输入（旧格式）
```yaml
topic: "AI 在量化交易中的应用"
```

**问题：**
- 信息不足，无法生成高质量大纲
- 需要多轮交互补充背景、材料、约束
- 容易导致大纲与实际需求不匹配
- 返工率高

### v2 输入（新格式）
```yaml
outline_planning_request:
  content_brief: {...}      # 核心判断、目标、关键点、风险边界
  material_pack: {...}      # 已有素材、证据清单
  media_plan: {...}         # 平台约束、分发策略
```

**优势：**
- 信息完整，一次性输入所有必要上下文
- 大纲质量更高，返工率降低
- 支持多角度生成和对比
- 便于追踪和版本管理

---

## 迁移步骤

### 第 1 步：准备 Content Brief

从原有的主题和背景信息中提取：

| 字段 | 来源 | 示例 |
|------|------|------|
| `brief_id` | 自定义 ID | `brief-ai-quant-002` |
| `core_judgment` | 文章的核心观点 | "AI 在量化交易中已从理论进入实践，但仍需警惕过度拟合风险" |
| `target_audience` | 目标读者 | "量化交易从业者、投资者、AI 研究者" |
| `article_goal` | 文章要达成的目标 | "梳理实际应用案例，平衡机会与风险" |
| `key_points` | 核心论点列表 | ["AI 在特征工程中的优势", "过度拟合风险", "监管约束"] |
| `risk_boundaries` | 不能做的事 | ["不能夸大 AI 预测能力", "必须提及监管风险"] |

**检查清单：**
- [ ] Brief 中的 core_judgment 是一句话，清晰表达核心观点
- [ ] key_points 有 3-5 个，每个都是独立的��点
- [ ] risk_boundaries 明确列出了禁区和约束

### 第 2 步：整理 Material Pack

收集已有的素材和证据：

| 字段 | 说明 | 示例 |
|------|------|------|
| `pack_id` | 素材包 ID | `pack-ai-quant-002` |
| `materials` | 素材列表 | 见下表 |
| `evidence_checklist` | 缺失的证据 | ["补充失败案例", "补充国际对标"] |

**素材类型：**
- `case_study`: 真实案例
- `data`: 数据和统计
- `expert_view`: 专家观点
- `reference`: 学术或权威参考
- `quote`: 直接引用

**检查清单：**
- [ ] 每个素材都有 `material_id`、`type`、`title`、`content`、`source`、`credibility`
- [ ] `credibility` 标记为 high/medium/low
- [ ] `evidence_checklist` 列出了明显的缺口

### 第 3 步：定�� Media Plan

根据发布平台的约束：

| 字段 | 说明 | 示例 |
|------|------|------|
| `target_media` | 目标媒介 | `article_wechat` |
| `max_length` | 字数限制 | 3000-3500 |
| `recommended_sections` | 推荐章节数 | 5 |
| `reading_time_minutes` | 目标阅读时间 | 8-10 分钟 |
| `distribution_strategy` | 分发策略 | "周末深度分析，配合社群讨论" |

**检查清单：**
- [ ] `max_length` 根据平台特性设定（微信公众号通常 2500-4000）
- [ ] `recommended_sections` 与字数和阅读时间匹配
- [ ] `distribution_strategy` 明确了发布时机和配套策略

### 第 4 步：组装完整请求

```json
{
  "outline_planning_request": {
    "request_id": "outline-{timestamp}-{uuid}",
    "content_brief": {...},
    "material_pack": {...},
    "media_plan": {...},
    "target_media": "article_wechat",
    "operator_note": "可选的背景说明",
    "created_at": "ISO 8601 timestamp"
  }
}
```

---

## 使用示例

### 场景 1：从旧格式迁移

**旧输入：**
```
主题：AI 在量化交易中的应用
背景：这是系列文章的第二篇
已有素材：某基金案例、行业数据、专家观点
```

**新输入：**
```json
{
  "outline_planning_request": {
    "request_id": "outline-20260315-ai-quant-002",
    "content_brief": {
      "brief_id": "brief-ai-quant-002",
      "core_judgment": "AI 在量化交易中已从理论进入实践，但仍需警惕过度拟合风险",
      "target_audience": "量化交易从业者、投资者、AI 研究者",
      "article_goal": "梳理实际应用案例，平衡机会与风险",
      "key_points": [
        "AI 在特征工程中的优势",
        "实际应用案例对比",
        "过度拟合风险防控",
        "监管环境约束"
      ],
      "risk_boundaries": [
        "不能夸大 AI 预测能力",
        "必须提及监管风险"
      ]
    },
    "material_pack": {
      "pack_id": "pack-ai-quant-002",
      "materials": [
        {
          "material_id": "mat-001",
          "type": "case_study",
          "title": "某头部量化基金的 AI 应用案例",
          "content": "...",
          "source": "行业访谈",
          "credibility": "high"
        }
      ],
      "evidence_checklist": [
        "补充失败案例",
        "补充国际对标"
      ]
    },
    "media_plan": {
      "target_media": "article_wechat",
      "platform_constraints": {
        "max_length": 3500,
        "recommended_sections": 5,
        "reading_time_minutes": 10
      },
      "distribution_strategy": "周末深度分析"
    },
    "target_media": "article_wechat",
    "operator_note": "系列文章第二篇，需与第一篇形成递进",
    "created_at": "2026-03-15T12:00:00Z"
  }
}
```

---

## 常见问题

### Q1: 如果我还没有完整的 Material Pack 怎么办？

**A:** 可以先提交已有的素材，在 `evidence_checklist` 中明确列出缺失项。系统会识别缺口并提示补充。

### Q2: Media Plan 是必须的吗？

**A:** 不是必须的，但强烈推荐。如果不提供，系统会使用默认的微信公众号约束（3000 字，5 个章节，8 分钟阅读时间）。

### Q3: 如何处理多个角度的需求？

**A:** 在 `operator_note` 中明确说明需要的角度数量和侧重点。系统会生成 2-3 个不同角度的大纲供选择。

### Q4: 旧格式的输入还能用吗？

**A:** 不能。v2 是完全的契约升级。如果收到旧格式输入，系统会返回错误并提示使用新格式。

---

## 质量检查清单

在提交输入前，请确认：

- [ ] Brief 中的 core_judgment 清晰、具体、可论证
- [ ] key_points 有 3-5 个，互相独立，不重复
- [ ] risk_boundaries 明确列出了禁区
- [ ] 每个素材都有完整的元数据（ID、类型、来源、可信度）
- [ ] evidence_checklist 列出了明显的缺口
- [ ] Media Plan 的约束与文章目标匹配
- [ ] operator_note 提供了必要的背景信息

---

## 输出质量对比

### v1 输出（旧格式）
- 大纲结构简单，通常只有标题
- 缺少论点支撑和证据需求
- 需要多轮修改和确认
- 返工率 40-60%

### v2 输出（新格式）
- 大纲结构完整，包含论点、证据、转场逻辑
- 提供 2-3 个不同角度的选择
- 一次性输出主大纲和备选大纲
- 返工率 10-20%

---

## 后续步骤

1. 使用新格式提交输入
2. 获取 2-3 个角度的大纲
3. 选择主大纲或备选大纲
4. 将大纲交给 `wechat-draft-writer` 进行初稿写作
5. 根据初稿反馈调整大纲（如需要）

---

## 支持

如有问题，请参考：
- `templates/input-example.json` - 完整的输入示例
- `SKILL.md` - 详细的契约定义
- `references/` - 参考文件和评估标准
