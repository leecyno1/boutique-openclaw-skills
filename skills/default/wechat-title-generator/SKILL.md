---
name: wechat-title-generator
description: Use when generating WeChat article title candidates from a brief, outline, or draft.
---

# Wechat Title Generator - v2 契约版本

## 新定位
本 Skill 是 `article_wechat` 的标题适配器。

它负责：
- 在文章主题与结构已经确认后
- 输出公众号标题候选与推荐版本

它不再负责：
- 全局主题判断
- 大纲生成
- 正文生成

---

## v2 输入契约

### 标准输入对象：Title Generation Request

```yaml
title_generation_request:
  request_id: string                    # 格式：title-{timestamp}-{uuid}
  content_brief:                        # 已确认的 Content Brief 对象
    brief_id: string
    core_judgment: string               # 核心判断
    target_audience: string             # 目标读者
    article_goal: string                # 文章目标
    key_points: [string]                # 核心论点列表
    risk_boundaries: [string]           # 风险边界
  article_source:                       # 文章来源（大纲或初稿）
    source_type: "outline" | "draft"
    source_id: string                   # outline_id 或 draft_id
    source_content: string              # 大纲摘要或初稿正文
  target_audience: string               # 目标读者（冗余字段，便于快速查阅）
  article_goal: string                  # 文章目标（冗余字段，便于快速查阅）
  style_dna:                            # 可选，文风 DNA
    dna_id: string
    tone: string
    vocabulary_level: string
  risk_boundaries: [string]             # 风险边界
  optional_constraints:                 # 可选的约束条件
    max_length: number                  # 标题最大字数，默认 30
    must_include_keywords: [string]     # 必须包含的关键词
    avoid_keywords: [string]            # 避免的关键词
    tone_preference: string             # 例如："激进" | "保守" | "平衡"
  operator_note: string                 # 可选，操作员背景说明
  created_at: timestamp
```

### 示例

```yaml
title_generation_request:
  request_id: "title-20260315-abc123"
  content_brief:
    brief_id: "brief-ai-quant-001"
    core_judgment: "AI 在量化交易中已从理论进入实践，但仍需警惕过度拟合和黑箱风险"
    target_audience: "量化交易从业者、投资者、AI 研究者"
    article_goal: "梳理 AI 量化的实际应用案例，提示风险和机会"
    key_points:
      - "AI 模型在特征工程中的优势"
      - "高频交易中的实际应用案例"
      - "过度拟合和风险控制的平衡"
    risk_boundaries:
      - "不能夸大 AI 的预测能力"
      - "必须提及监管风险"
  article_source:
    source_type: "draft"
    source_id: "draft-v1-20260315-001"
    source_content: "AI 在量化交易中已经不是未来式，而是现在式。2024 年，某头部量化基金引入 AI 模型后，收益率从 8% 跃升到 15%...（初稿正文）"
  target_audience: "量化交易从业者、投资者、AI 研究者"
  article_goal: "梳理 AI 量化的实际应用案例，提示风险和机会"
  style_dna:
    dna_id: "dna-lemon-001"
    tone: "理性、数据驱动、略带启发"
    vocabulary_level: "专业但易懂"
  risk_boundaries:
    - "不能夸大 AI 的预测能力"
    - "必须提及监管风险"
  optional_constraints:
    max_length: 30
    must_include_keywords:
      - "AI"
      - "量化"
    avoid_keywords:
      - "震撼"
      - "颠覆"
    tone_preference: "平衡"
  operator_note: "这是 AI 量化系列的第二篇，标题需要与第一篇形成递进关系。第一篇标题是'AI 量化交易的基础概念'。"
  created_at: "2026-03-15T09:43:00Z"
```

---

## v2 输出契约

### 输出对象：Title Generation Result

```yaml
title_generation_result:
  result_id: string                     # 格式：title-result-{timestamp}-{uuid}
  request_id: string                    # 关联的请求 ID
  title_strategy:
    core_promise: string                # 标题的核心承诺
    emotional_hook: string              # 情绪钩子
    contrast_point: string              # 反差点
    reader_benefit: string              # 读者收益
    key_message: string                 # 核心信息
  title_candidates:
    - candidate_id: string              # 格式：title-candidate-{number}
      candidate_number: number          # 1-8
      title: string                     # 标题文本
      intensity_level: "soft" | "medium" | "strong"  # 强度等级
      emotional_tone: string            # 情绪基调
      why_this_title: string            # 为什么选这个标题
      target_appeal: string             # 目标吸引力
      risk_assessment: string           # 风险评估
  best_title_recommendation:
    candidate_id: string
    title: string
    rationale: string                   # 推荐理由
    why_best: string                    # 为什么是最佳选择
    expected_ctr: string                # 预期点击率评估
    alignment_with_brief: number        # 与 Brief 的对齐度 0-100
    alignment_with_content: number      # 与内容的对齐度 0-100
  safer_alternative:
    candidate_id: string
    title: string
    rationale: string                   # 为什么更稳妥
    when_to_use: string                 # 什么时候使用这个版本
  stronger_alternative:
    candidate_id: string
    title: string
    rationale: string                   # 为什么更强传播
    when_to_use: string                 # 什么时候使用这个版本
  eliminated_titles_and_why:
    - candidate_id: string
      title: string
      elimination_reason: string        # 为什么被淘汰
      violation_type: string            # 违反的约束类型
  quality_metrics:
    title_diversity_score: number       # 标题多样性评分 0-100
    risk_boundary_compliance_score: number  # 风险边界合规评分 0-100
    brief_alignment_score: number       # Brief 对齐度评分 0-100
    content_alignment_score: number     # 内容对齐度评分 0-100
  hard_constraints_check:
    - constraint: string
      status: "pass" | "fail"
      details: string
  operator_note: string
  created_at: timestamp
```

### 示例

```yaml
title_generation_result:
  result_id: "title-result-20260315-xyz789"
  request_id: "title-20260315-abc123"
  title_strategy:
    core_promise: "AI 在量化交易中已经从理论进入实践"
    emotional_hook: "实践突破、机会与风险的平衡"
    contrast_point: "从成功案例到风险警示的转变"
    reader_benefit: "了解 AI 量化的真实现状，避免盲目跟风"
    key_message: "AI 是工具，不是银弹"
  title_candidates:
    - candidate_id: "title-candidate-1"
      candidate_number: 1
      title: "AI 量化交易的实践突破与风险陷阱"
      intensity_level: "medium"
      emotional_tone: "理性、启发"
      why_this_title: "直接表达核心内容，平衡了机会和风险"
      target_appeal: "专业读者、投资者"
      risk_assessment: "低风险，内容完全支撑"
    - candidate_id: "title-candidate-2"
      candidate_number: 2
      title: "我看到了 AI 量化的真相：15% 收益背后的陷阱"
      intensity_level: "strong"
      emotional_tone: "启发、警惕"
      why_this_title: "使用第一人称和具体数据，增加代入感"
      target_appeal: "寻求深度分析的读者"
      risk_assessment: "中等风险，需要确保内容完全支撑 15% 这个数据"
    - candidate_id: "title-candidate-3"
      candidate_number: 3
      title: "AI 量化基金 2024 年平均收益 12%，但 2025 年初集体失效"
      intensity_level: "strong"
      emotional_tone: "警惕、反思"
      why_this_title: "使用对比数据，强调风险"
      target_appeal: "风险意识强的读者"
      risk_assessment: "中等风险，需要确保有足够的失效案例支撑"
    - candidate_id: "title-candidate-4"
      candidate_number: 4
      title: "量化交易员必读：AI 模型为什么在实盘中失效"
      intensity_level: "medium"
      emotional_tone: "实用、警惕"
      why_this_title: "直接针对目标读者，提出问题"
      target_appeal: "量化交易从业者"
      risk_assessment: "低风险，内容完全支撑"
    - candidate_id: "title-candidate-5"
      candidate_number: 5
      title: "从 15% 到 -5%：AI 量化的成功与失败"
      intensity_level: "strong"
      emotional_tone: "对比、启发"
      why_this_title: "使用极端对比，强调风险"
      target_appeal: "寻求警示的读者"
      risk_assessment: "中等风险，需要确保有具体案例支撑"
    - candidate_id: "title-candidate-6"
      candidate_number: 6
      title: "AI 在量化交易中的应用现状与未来"
      intensity_level: "soft"
      emotional_tone: "理性、平衡"
      why_this_title: "最保守的表述，完全中立"
      target_appeal: "寻求客观分析的读者"
      risk_assessment: "低风险，但可能缺乏吸引力"
    - candidate_id: "title-candidate-7"
      candidate_number: 7
      title: "特征工程、高频交易、过度拟合：AI 量化的三个关键词"
      intensity_level: "medium"
      emotional_tone: "专业、启发"
      why_this_title: "使用关键词列举，强调内容的专业性"
      target_appeal: "专业读者、研究者"
      risk_assessment: "低风险，内容完全支撑"
    - candidate_id: "title-candidate-8"
      candidate_number: 8
      title: "AI 量化交易：机会与陷阱的平衡术"
      intensity_level: "medium"
      emotional_tone: "启发、平衡"
      why_this_title: "强调平衡和方法论"
      target_appeal: "寻求实用建议的读者"
      risk_assessment: "低风险，内容完全支撑"
  best_title_recommendation:
    candidate_id: "title-candidate-1"
    title: "AI 量化交易的实践突破与风险陷阱"
    rationale: "这个标题最好地平衡了内容的两个核心面向：成功案例和风险警示。它既能吸引对 AI 量化感兴趣的读者，也能满足风险意识强的读者。"
    why_best: "相比其他标题，它最准确地反映了文章的核心内容，不夸大也不保守。它符合 Brief 的核心判断，也完全由文章内容支撑。"
    expected_ctr: "预期点击率 8-12%，高于平均水平"
    alignment_with_brief: 95
    alignment_with_content: 98
  safer_alternative:
    candidate_id: "title-candidate-6"
    title: "AI 在量化交易中的应用现状与未来"
    rationale: "这个标题最保守，完全中立，不会引起任何争议。"
    when_to_use: "如果你想要最低的风险，或者如果你的读者群体对激进表述不感兴趣。"
  stronger_alternative:
    candidate_id: "title-candidate-2"
    title: "我看到了 AI 量化的真相：15% 收益背后的陷阱"
    rationale: "这个标题使用第一人称和具体数据，增加了代入感和吸引力。预期点击率会更高。"
    when_to_use: "如果你想要更强的传播力，或者如果你的读者群体对启发式表述感兴趣。"
  eliminated_titles_and_why: []
  quality_metrics:
    title_diversity_score: 88
    risk_boundary_compliance_score: 100
    brief_alignment_score: 94
    content_alignment_score: 96
  hard_constraints_check:
    - constraint: "必须生成恰好 8 个标题"
      status: "pass"
      details: "生成了 8 个标题"
    - constraint: "标题不能出现引号"
      status: "pass"
      details: "所有标题都不含引号"
    - constraint: "标题不能出现冒号"
      status: "fail"
      details: "候选 2 和候选 5 中出现了冒号，已在最终推荐中排除"
    - constraint: "标题不能出现破折号"
      status: "pass"
      details: "所有标题都不含破折号"
    - constraint: "标题中如果出现两个或以上分句，分句之间必须使用逗号"
      status: "pass"
      details: "所有多分句标题都使用了逗号"
    - constraint: "标题要有情绪或反差"
      status: "pass"
      details: "所有标题都有明确的情绪基调或反差点"
    - constraint: "标题必须和文章真实内容一致"
      status: "pass"
      details: "所有标题都由文章内容完全支撑"
  operator_note: "推荐使用候选 1。如果想要更强的传播力，可以考虑候选 2，但需要确保 15% 这个数据在文章中有明确的出处。"
  created_at: "2026-03-15T09:43:00Z"
```

---

## 工作流

1. 先提炼文章承诺、情绪点、反差点和读者收益。
2. 以 Brief 的核心判断和文章实际内容为标题边界。
3. 使用 `references/title-rubric.md` 生成 8 个标题，覆盖不同力度层级。
4. 筛除违反硬约束的标题。
5. 对保留标题逐项评分，并推荐 1 个最佳标题。
6. 同时给出 1 个更稳妥版本和 1 个更强传播版本。

---

## 输出契约总结

| 字段 | 说明 |
|------|------|
| title_strategy | 标题策略，包括核心承诺、情绪钩子等 |
| title_candidates | 8 个标题候选，每个都有完整的分析 |
| best_title_recommendation | 最佳标题推荐及其理由 |
| safer_alternative | 更稳妥的版本 |
| stronger_alternative | 更强传播的版本 |
| eliminated_titles_and_why | 被淘汰的标题及其原因 |
| quality_metrics | 质量评分 |
| hard_constraints_check | 硬约束检查 |

---

## 硬约束
- 必须生成恰好 8 个标题。
- 标题不能出现引号。
- 标题不能出现冒号。
- 标题不能出现破折号。
- 标题中如果出现两个或以上分句，分句之间必须使用逗号。
- 标题要有情绪或反差。
- 可以适度夸张，允许使用高情绪表达，比如"这是我读过最好的一篇文章""我看到了新世界的大门""我被震到了"这一类强感受句式。
- 夸张必须仍然和正文内容一致，不能靠编造收益或虚构结果制造点击。
- 标题必须和文章真实内容一致。

---

## 边界
- 不写大纲，不写正文。
- 如果主题还没定，先交给 `wechat-topic-outline-planner`。

---

## 参考文件
- `references/title-rubric.md`
- `docs/task001-task003-integration-v1.md`
