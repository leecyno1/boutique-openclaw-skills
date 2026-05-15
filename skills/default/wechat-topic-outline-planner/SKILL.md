---
name: wechat-topic-outline-planner
description: Use when planning WeChat article outlines from confirmed briefs and materials.
---

# Wechat Topic Outline Planner - v2 契约版本

## 新定位
本 Skill 是 `article_wechat` 的媒介适配器。

它负责：
- 在公众号文章场景下
- 将 Brief / Material / Media Plan 转为文章结构方案

它不再负责：
- 全局选题判断
- 全局媒介路由
- 用裸主题直接承担完整策划中枢功能

## 目标
把已确认的内容对象压缩成可写、可证据化、可确认的公众号文章结构，减少后续初稿返工。

---

## v2 输入契约

### 标准输入对象：Outline Planning Request

```yaml
outline_planning_request:
  request_id: string                    # 格式：outline-{timestamp}-{uuid}
  content_brief:                        # 已确认的 Content Brief 对象
    brief_id: string
    core_judgment: string               # 核心判断
    target_audience: string             # 目标读者
    article_goal: string                # 文章目标
    key_points: [string]                # 核心论点列表
    risk_boundaries: [string]           # 风险边界
  material_pack:                        # Material Pack 对象
    pack_id: string
    materials:
      - material_id: string
        type: "reference" | "quote" | "data" | "case_study" | "expert_view"
        title: string
        content: string
        source: string
        credibility: "high" | "medium" | "low"
    evidence_checklist: [string]        # 需要补充的证据
  media_plan:                           # 可选，媒介计划
    target_media: "article_wechat"
    platform_constraints:
      max_length: number                # 字数限制
      recommended_sections: number      # 推荐章节数
      reading_time_minutes: number      # 目标阅读时间
    distribution_strategy: string       # 分发策略
  target_media: "article_wechat"
  operator_note: string                 # 可选，操作员背景说明
  created_at: timestamp
```

### 示例

```yaml
outline_planning_request:
  request_id: "outline-20260315-abc123"
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
  material_pack:
    pack_id: "pack-ai-quant-001"
    materials:
      - material_id: "mat-001"
        type: "case_study"
        title: "某量化基金的 AI 应用案例"
        content: "该基金在 2024 年引入 AI 模型，收益率提升 15%，但在 2025 年初遭遇模型失效..."
        source: "行业访谈"
        credibility: "high"
      - material_id: "mat-002"
        type: "data"
        title: "AI 量化基金的收益分布"
        content: "2024 年 AI 量化基金平均收益 12%，但波动率也提升 20%..."
        source: "公开数据"
        credibility: "high"
      - material_id: "mat-003"
        type: "expert_view"
        title: "某量化研究员的观点"
        content: "AI 不是银弹，关键是如何防止过度拟合..."
        source: "播客访谈"
        credibility: "medium"
    evidence_checklist:
      - "补充 2-3 个失败案例"
      - "补充监管政策背景"
  media_plan:
    target_media: "article_wechat"
    platform_constraints:
      max_length: 3000
      recommended_sections: 5
      reading_time_minutes: 8
    distribution_strategy: "周末深度分析，配合社群讨论"
  target_media: "article_wechat"
  operator_note: "这是 AI 量化系列的第二篇，需要与第一篇形成递进关系"
  created_at: "2026-03-15T09:43:00Z"
```

---

## v2 输出契约

### 输出对象：Outline Planning Result

```yaml
outline_planning_result:
  result_id: string                     # 格式：outline-result-{timestamp}-{uuid}
  request_id: string                    # 关联的请求 ID
  input_digest:
    brief_summary: string               # Brief 摘要
    material_count: number
    evidence_gaps: [string]             # 证据缺口
  topic_angles:                         # 2-3 个表达角度
    - angle_id: string
      angle_name: string                # 角度名称
      angle_description: string         # 角度描述
      why_this_angle: string            # 为什么选这个角度
      target_emotion: string            # 目标情绪
      key_message: string               # 核心信息
  recommended_angle:
    angle_id: string
    angle_name: string
    rationale: string                   # 推荐理由
    why_better_than_others: string      # 相比其他角度的优势
  primary_outline:
    outline_id: string                  # 格式：outline-primary-{uuid}
    angle_id: string                    # 使用的角度 ID
    structure:
      - section_id: string
        section_number: number
        section_title: string           # 章节标题（陈述句）
        section_objective: string       # 章节目标
        core_argument: string           # 核心论点
        evidence_required: [string]     # 需要的证据
        transition_logic: string        # 转场逻辑
        estimated_words: number
    total_estimated_words: number
    reading_time_minutes: number
  backup_outline:
    outline_id: string                  # 格式：outline-backup-{uuid}
    angle_id: string
    structure:
      - section_id: string
        section_number: number
        section_title: string
        section_objective: string
        core_argument: string
        evidence_required: [string]
        transition_logic: string
        estimated_words: number
    total_estimated_words: number
    reading_time_minutes: number
  evidence_checklist:
    - evidence_id: string
      evidence_type: "reference" | "quote" | "data" | "case_study" | "expert_view"
      evidence_description: string
      required_for_sections: [string]   # 哪些章节需要
      status: "available" | "gap" | "optional"
      source_hint: string               # 来源提示
  quality_metrics:
    angle_diversity_score: number       # 角度多样性评分 0-100
    structure_coherence_score: number   # 结构连贯性评分 0-100
    evidence_coverage_score: number     # 证据覆盖度评分 0-100
  waiting_for_confirmation:
    confirmation_required: boolean
    confirmation_items:
      - "确认推荐角度是否合适"
      - "确认主大纲的章节划分"
      - "确认是否需要补充证据"
  operator_note: string
  created_at: timestamp
```

### 示例

```yaml
outline_planning_result:
  result_id: "outline-result-20260315-xyz789"
  request_id: "outline-20260315-abc123"
  input_digest:
    brief_summary: "AI 在量化交易中已从理论进入实践，需要梳理应用案例和风险"
    material_count: 3
    evidence_gaps:
      - "失败案例不足"
      - "监管政策背景需要补充"
  topic_angles:
    - angle_id: "angle-001"
      angle_name: "AI 量化的实践突破"
      angle_description: "从成功案例出发，展示 AI 在量化中的实际应用价值"
      why_this_angle: "符合读者的学习需求，容易产生共鸣"
      target_emotion: "启发、兴奋"
      key_message: "AI 不是理论，已���在真实交易中创造价值"
    - angle_id: "angle-002"
      angle_name: "AI 量化的风险陷阱"
      angle_description: "从失败案例和风险出发，警示过度拟合和黑箱问题"
      why_this_angle: "提供对立视角，增加文章深度"
      target_emotion: "警惕、理性"
      key_message: "AI 是工具，不是银弹，需要严格的风险管理"
    - angle_id: "angle-003"
      angle_name: "AI 量化的未来路径"
      angle_description: "从现状分析推向未来展望，讨论 AI 量化的发展方向"
      why_this_angle: "前瞻性强，但需要更多专家观点支撑"
      target_emotion: "思考、期待"
      key_message: "AI 量化的未来取决于如何平衡创新和风险"
  recommended_angle:
    angle_id: "angle-001"
    angle_name: "AI 量化的实践突破"
    rationale: "这个角度最符合当前的材料储备和读者需求"
    why_better_than_others: "相比纯风险角度，更容易吸引读者；相比未来展望，更有现实支撑"
  primary_outline:
    outline_id: "outline-primary-20260315-001"
    angle_id: "angle-001"
    structure:
      - section_id: "sec-001"
        section_number: 1
        section_title: "AI 量化从实验室走向交易所"
        section_objective: "建立读者对 AI 量化现状的认知"
        core_argument: "AI 在量化交易中已经从理论验证进入实际应用阶段"
        evidence_required:
          - "某量化基金的 AI 应用案例"
          - "行业数据：AI 量化基金的规模和收益"
        transition_logic: "从宏观现象引入具体案例"
        estimated_words: 400
      - section_id: "sec-002"
        section_number: 2
        section_title: "特征工程：AI 的第一个突破口"
        section_objective: "说明 AI 在量化中的具体应用方式"
        core_argument: "AI 在特征工程中的优势是量化交易的第一个突破口"
        evidence_required:
          - "特征工程的传统方法 vs AI 方法对比"
          - "实际案例中的特征工程改进"
        transition_logic: "从宏观应用深入到具体技术"
        estimated_words: 600
      - section_id: "sec-003"
        section_number: 3
        section_title: "高频交易中的 AI 实战"
        section_objective: "展示 AI 在高频交易中的实际效果"
        core_argument: "高频交易是 AI 量化最成熟的应用场景"
        evidence_required:
          - "高频交易基金的 AI 应用案例"
          - "收益率和风险指标对比"
        transition_logic: "从特征工程进入具体交易场景"
        estimated_words: 700
      - section_id: "sec-004"
        section_number: 4
        section_title: "过度拟合：AI 量化的隐形杀手"
        section_objective: "提示 AI 应用中的核心风险"
        core_argument: "过度拟合是 AI 量化最常见的失败原因"
        evidence_required:
          - "失败案例：模型在回测中表现好，实盘失效"
          - "过度拟合的识别方法"
        transition_logic: "从成功案例转向风险提示"
        estimated_words: 500
      - section_id: "sec-005"
        section_number: 5
        section_title: "AI 量化的未来：机会与挑战"
        section_objective: "总结并展望"
        core_argument: "AI 量化的未来取决于如何在创新和风险之间找到平衡"
        evidence_required:
          - "专家观点：AI 量化的发展方向"
          - "监管政策背景"
        transition_logic: "从风险提示升华到未来展望"
        estimated_words: 400
    total_estimated_words: 2600
    reading_time_minutes: 7
  backup_outline:
    outline_id: "outline-backup-20260315-001"
    angle_id: "angle-002"
    structure:
      - section_id: "sec-b01"
        section_number: 1
        section_title: "AI 量化的三大风险陷阱"
        section_objective: "快速建立风险意识"
        core_argument: "AI 量化存在过度拟合、黑箱决策和监管风险三大陷阱"
        evidence_required:
          - "失败案例"
          - "风险分类框架"
        transition_logic: "直接切入风险主题"
        estimated_words: 600
      - section_id: "sec-b02"
        section_number: 2
        section_title: "过度拟合：为什么回测好用不了"
        section_objective: "深入讲解最常见的失败原因"
        core_argument: "过度拟合是 AI 模型在量化中最常见的失败原因"
        evidence_required:
          - "具体失败案例"
          - "过度拟合的识别和防止方法"
        transition_logic: "从风险分类深入到具体案例"
        estimated_words: 700
      - section_id: "sec-b03"
        section_number: 3
        section_title: "黑箱决策：AI 能否被信任"
        section_objective: "讨论 AI 透明性问题"
        core_argument: "AI 的黑箱特性与量化交易的风险管理需求存在矛盾"
        evidence_required:
          - "黑箱问题的具体表现"
          - "行业的解决方案探索"
        transition_logic: "从技术风险升级到管理风险"
        estimated_words: 500
      - section_id: "sec-b04"
        section_number: 4
        section_title: "监管风险：AI 量化的合规底线"
        section_objective: "提示政策风险"
        core_argument: "监管部门对 AI 量化的态度正在收紧"
        evidence_required:
          - "最新监管政策"
          - "行业合规案例"
        transition_logic: "从技术和管理风险升级到政策风险"
        estimated_words: 400
      - section_id: "sec-b05"
        section_number: 5
        section_title: "如何在风险中寻找机会"
        section_objective: "提供建设性建议"
        core_argument: "理解风险的本质，才能更好地把握 AI 量化的机会"
        evidence_required:
          - "风险管理的最佳实践"
          - "专家建议"
        transition_logic: "从风险警示转向建设性建议"
        estimated_words: 400
    total_estimated_words: 2600
    reading_time_minutes: 7
  evidence_checklist:
    - evidence_id: "ev-001"
      evidence_type: "case_study"
      evidence_description: "某量化基金的 AI 应用案例"
      required_for_sections: ["sec-001", "sec-003"]
      status: "available"
      source_hint: "已有材料"
    - evidence_id: "ev-002"
      evidence_type: "data"
      evidence_description: "AI 量化基金的收益分布和风险指标"
      required_for_sections: ["sec-001", "sec-003"]
      status: "available"
      source_hint: "已有材料"
    - evidence_id: "ev-003"
      evidence_type: "case_study"
      evidence_description: "失败案例：模型失效的具体情况"
      required_for_sections: ["sec-004", "sec-b02"]
      status: "gap"
      source_hint: "需要补充"
    - evidence_id: "ev-004"
      evidence_type: "reference"
      evidence_description: "过度拟合的识别和防止方法"
      required_for_sections: ["sec-004", "sec-b02"]
      status: "gap"
      source_hint: "需要补充"
    - evidence_id: "ev-005"
      evidence_type: "expert_view"
      evidence_description: "专家观点：AI 量化的发展方向"
      required_for_sections: ["sec-005"]
      status: "available"
      source_hint: "已有材料"
    - evidence_id: "ev-006"
      evidence_type: "reference"
      evidence_description: "最新监管政策"
      required_for_sections: ["sec-005", "sec-b04"]
      status: "gap"
      source_hint: "需要补充"
  quality_metrics:
    angle_diversity_score: 85
    structure_coherence_score: 88
    evidence_coverage_score: 72
  waiting_for_confirmation:
    confirmation_required: true
    confirmation_items:
      - "确认推荐角度（AI 量化的实践突破）是否合适"
      - "确认主大纲的 5 个章节划分是否满足需求"
      - "确认是否需要补充失败案例和监管政策背景"
      - "确认备选大纲（风险陷阱角度）是否需要采用"
  operator_note: "主大纲侧重正面案例和启发，备选大纲侧重风险警示。建议先用主大纲，如果需要更强的风险提示，可以切换到备选大纲。"
  created_at: "2026-03-15T09:43:00Z"
```

---

## 工作流

1. 先读取 Brief，明确主题定义、核心判断、核心冲突与推荐角度。
2. 再读取 Material Pack，识别已有证据、素材缺口和可复用信息。
3. 如已提供 Media Plan，优先对齐其中的结构建议。
4. 使用 `references/topic-evaluation-rubric.md` 生成 2-3 个文章表达角度。
5. 推荐 1 个主角度，并说明为什么比其他角度更值得写。
6. 基于主角度产出 1 套主大纲和 1 套备选大纲，使用 `references/outline-patterns.md`。
7. 对每个大纲补齐 section objective、核心论点、证据需求、转场逻辑。
8. 停在确认环节，等待用户明确确认，不写正文。

---

## 输出契约总结

| 字段 | 说明 |
|------|------|
| input_digest | 输入摘要，快速回顾 Brief 和 Material |
| topic_angles | 2-3 个表达角度，每个都有完整的描述和理由 |
| recommended_angle | 推荐角度及其理由 |
| primary_outline | 主大纲，基于推荐角度 |
| backup_outline | 备选大纲，基于另一个角度 |
| evidence_checklist | 证据清单，标记哪些已有、哪些缺失 |
| quality_metrics | 质量评分 |
| waiting_for_confirmation | 确认项清单 |

---

## 质量标准
- 角度之间必须真正不同，而不是同义改写。
- 大纲必须能直接交给写稿技能，不允许只有标题没有论点。
- 每个 section 只承担一个核心结论。
- 结论必须能回到 Brief 的目标，不做纯展示型结构。

---

## 边界
- 不写完整初稿。
- 不负责最终标题优化，标题交给 `wechat-title-generator`。
- 如果结构前提未满足，优先回退到 Brief 层，而不是硬写大纲。

---

## 参考文件
- `references/topic-evaluation-rubric.md`
- `references/outline-patterns.md`
- `docs/task001-task003-integration-v1.md`
