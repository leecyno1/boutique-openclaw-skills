---
name: wechat-draft-writer
description: Use when drafting WeChat articles from a confirmed brief, outline, and style DNA.
---

# Wechat Draft Writer - v2 契约版本

## 新定位
本 Skill 是 `article_wechat` 场景下的正文写作适配器。

它负责：
- 在结构已经确认的前提下
- 将 Brief / Material / confirmed outline 转为公众号初稿

它不再负责：
- 全局选题判断
- 全局大纲决策
- 标题决策

---

## v2 输入契约

### 标准输入对象：Draft Writing Request

```yaml
draft_writing_request:
  request_id: string                    # 格式：draft-{timestamp}-{uuid}
  confirmed_outline:                    # 已确认的大纲对象
    outline_id: string
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
    confirmation_status: "confirmed"    # 必须是 confirmed
  content_brief:                        # Content Brief 对象
    brief_id: string
    core_judgment: string
    target_audience: string
    article_goal: string
    key_points: [string]
    risk_boundaries: [string]
  material_pack:                        # Material Pack 对象
    pack_id: string
    materials:
      - material_id: string
        type: "reference" | "quote" | "data" | "case_study" | "expert_view"
        title: string
        content: string
        source: string
        credibility: "high" | "medium" | "low"
    evidence_checklist: [string]
  style_dna:                            # 文风 DNA 对象
    dna_id: string
    author_name: string
    tone: string                        # 例如："理性、启发、略带幽默"
    sentence_structure: string          # 例如："短句为主，偶尔长句"
    rhetorical_devices: [string]        # 例如：["类比", "排比", "反问"]
    vocabulary_level: string            # 例如："专业但易懂"
    paragraph_style: string             # 例如："1-3 句为主"
    taboo_patterns: [string]            # 禁用模式
  article_goal: string                  # 文章目标（冗余字段，便于快速查阅）
  media_plan:                           # 可选，媒介计划
    target_media: "article_wechat"
    platform_constraints:
      max_length: number
      recommended_sections: number
      reading_time_minutes: number
  operator_note: string                 # 可选，操作员背景说明
  created_at: timestamp
```

### 示例

```yaml
draft_writing_request:
  request_id: "draft-20260315-abc123"
  confirmed_outline:
    outline_id: "outline-primary-20260315-001"
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
    confirmation_status: "confirmed"
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
        content: "该基金在 2024 年引入 AI 模型，收益率提升 15%，但在 2025 年初遭遇模型失效，原因是过度拟合了 2023-2024 年的市场特征..."
        source: "行业访谈"
        credibility: "high"
      - material_id: "mat-002"
        type: "data"
        title: "AI 量化基金的收益分布"
        content: "2024 年 AI 量化基金平均收益 12%，但波动率也提升 20%。其中头部基金收益 25%，尾部基金亏损 5%..."
        source: "公开数据"
        credibility: "high"
      - material_id: "mat-003"
        type: "expert_view"
        title: "某量化研究员的观点"
        content: "AI 不是银弹，关键是如何防止过度拟合。我们的做法是：(1) 严格的交叉验证，(2) 定期的模型衰减检测，(3) 动态的特征更新..."
        source: "播客访谈"
        credibility: "medium"
    evidence_checklist:
      - "补充 2-3 个失败案例"
      - "补充监管政策背景"
  style_dna:
    dna_id: "dna-lemon-001"
    author_name: "lemon"
    tone: "理性、数据驱动、略带启发"
    sentence_structure: "短句为主，偶尔长句用于复杂论证"
    rhetorical_devices:
      - "类比"
      - "排比"
      - "反问"
      - "数据对比"
    vocabulary_level: "专业但易懂，避免过度学术化"
    paragraph_style: "1-3 句为主，段落间有明确的逻辑转接"
    taboo_patterns:
      - "避免使用破折号"
      - "避免过度修饰词"
      - "避免标题党式表达"
  article_goal: "梳理 AI 量化的实际应用案例，提示风险和机会"
  media_plan:
    target_media: "article_wechat"
    platform_constraints:
      max_length: 3000
      recommended_sections: 5
      reading_time_minutes: 8
  operator_note: "这是 AI 量化系列的第二篇，需要与第一篇形成递进关系。第一篇是基础概念，这篇是实践应用。"
  created_at: "2026-03-15T09:43:00Z"
```

---

## v2 输出契约

### 输出对象：Draft Writing Result

```yaml
draft_writing_result:
  result_id: string                     # 格式：draft-result-{timestamp}-{uuid}
  request_id: string                    # 关联的请求 ID
  style_dna_in_use:
    dna_id: string
    author_name: string
    tone: string
    key_characteristics: [string]       # 本稿中体现的文风特征
  draft_v1:
    draft_id: string                    # 格式：draft-v1-{uuid}
    title: string                       # 临时标题（最终标题由 title-generator 生成）
    content: string                     # 完整初稿正文
    word_count: number
    reading_time_minutes: number
    sections:
      - section_id: string
        section_number: number
        section_title: string
        section_content: string
        word_count: number
        evidence_used: [string]         # 使用的证据 ID
  style_adherence_notes:
    tone_adherence: string              # 文风贴合说明
    sentence_structure_adherence: string
    rhetorical_devices_used: [string]   # 实际使用的修辞手法
    vocabulary_adherence: string
    paragraph_style_adherence: string
  dna_compliance_report:
    compliance_score: number            # 0-100
    compliant_patterns: [string]        # 符合 DNA 的模式
    non_compliant_patterns: [string]    # 不符合 DNA 的模式
    violations: [string]                # 违反 DNA 的具体例子
  weak_sections_and_fix_suggestions:
    - section_id: string
      section_title: string
      weakness_description: string      # 弱点描述
      suggested_fix: string             # 修正建议
      priority: "high" | "medium" | "low"
  optional_alternative_lead:
    alternative_lead: string            # 可选的开头版本
    why_alternative: string             # 为什么提供这个替代版本
  evidence_usage_report:
    materials_used: number
    materials_unused: number
    unused_materials: [string]          # 未使用的材料 ID
    evidence_gaps_filled: [string]      # 填补的证据缺口
    evidence_gaps_remaining: [string]   # 仍然存在的证据缺口
  risk_boundary_compliance:
    boundaries_respected: boolean
    boundary_violations: [string]       # 如果有违反，列出具体例子
    risk_flags: [string]                # 需要编辑注意的风险点
  quality_checklist:
    - item: string
      status: "pass" | "warning" | "fail"
      notes: string
  operator_note: string
  created_at: timestamp
```

### 示例

```yaml
draft_writing_result:
  result_id: "draft-result-20260315-xyz789"
  request_id: "draft-20260315-abc123"
  style_dna_in_use:
    dna_id: "dna-lemon-001"
    author_name: "lemon"
    tone: "理性、数据驱动、略带启发"
    key_characteristics:
      - "短句为主，便于移动阅读"
      - "使用数据对比强化论点"
      - "类比和反问增加互动感"
      - "避免过度修饰，保持专业感"
  draft_v1:
    draft_id: "draft-v1-20260315-001"
    title: "AI 量化交易的实践突破与风险陷阱"
    content: |
      AI 在量化交易中已经不是未来式，而是现在式。

      2024 年，某头部量化基金引入 AI 模型后，收益率从 8% 跃升到 15%。这不是个案。根据公开数据，2024 年 AI 量化基金的平均收益达到 12%，远超传统量化基金的 6%。

      但这个数字背后，隐藏着一个更复杂的故事。

      ## AI 量化从实验室走向交易所

      AI 在量化中的应用，经历了三个阶段。

      第一阶段是学术验证。2015-2018 年，AI 模型在历史数据上表现惊人，但实盘效果平平。原因很简单：过度拟合。

      第二阶段是工程优化。2018-2022 年，量化团队开始认真对待 AI 的工程问题。他们引入了交叉验证、特征衰减检测、动态模型更新等方法。效果开始显现。

      第三阶段是规模应用。2023 年至今，AI 量化已经成为头部基金的标配。不用 AI，反而成了异类。

      这个转变的关键，是从"AI 能做什么"转向"AI 在这个场景下怎么不失效"。

      ## 特征工程：AI 的第一个突破口

      传统量化交易中，特征工程是最耗时的工作。分析师需要手工设计数百个特征，然后通过回测筛选。这个过程既慢又容易遗漏。

      AI 改变了这一点。

      某基金的做法是：用 AI 自动生成候选特征，然后用严格的交叉验证筛选。结果是，他们在相同的计算资源下，特征数量从 200 个增加到 2000 个，而过度拟合的风险反而下降了。

      为什么？因为 AI 生成的特征更多样化，而严格的交叉验证能有效过滤掉虚假特征。

      这就是 AI 在量化中的第一个真正突破：不是��代人类的判断，而是扩展人类的能力。

      ## 高频交易中的 AI 实战

      高频交易是 AI 量化最成熟的应用场景。

      在这个场景中，AI 的优势是明显的：(1) 处理高维数据的能力，(2) 实时决策的速度，(3) 模式识别的准确性。

      某头部高频交易基金的数据显示，引入 AI 后，他们的夏普比率从 1.2 提升到 1.8，最大回撤从 8% 降低到 5%。这不是小幅改进，这是质的飞跃。

      但这个成功的背后，是什么？

      是严格的风险管理。这家基金对 AI 模型的要求是：(1) 必须能解释，(2) 必须有衰减检测，(3) 必须有实时风险限制。

      换句话说，他们用 AI，但不盲目信任 AI。

      ## 过度拟合：AI 量化的隐形杀手

      这是最容易被忽视的风险。

      2025 年初，某基金的 AI 模型在实盘中突然失效。回测收益 25%，实盘亏损 5%。原因是什么？过度拟合。

      这个基金的模型在 2023-2024 年的数据上训练得太好了，以至于完全适应了那个特定的市场环境。当市场环境改变时，模型就失效了。

      这个案例告诉我们：回测好不等于实盘好。

      如何防止过度拟合？某量化研究员的建议是：(1) 严格的交叉验证，(2) 定期的模型衰减检测，(3) 动态的特征更新。简单说，就是不要让模型"记住"历史，而是让它"理解"规律。

      ## AI 量化的未来：机会与挑战

      AI 在量化中的应用才刚刚开始。

      机会在于：AI 能处理的数据维度和复杂度远超人类，这意味着还有大量的"信息金矿"等待挖掘。

      挑战在于：监管部门对 AI 量化的态度正在收紧。黑箱决策、系统性风险、市场操纵等问题都在监管的视野中。

      未来的 AI 量化，必须在创新和风险之间找到平衡。这不是技术问题，而是管理问题。

      那些能做到"用 AI，但不盲目信任 AI"的基金，才是真正的赢家。
    word_count: 1850
    reading_time_minutes: 6
    sections:
      - section_id: "sec-001"
        section_number: 1
        section_title: "AI 量化从实验室走向交易所"
        section_content: "AI 在量化中的应用，经历了三个阶段。第一阶段是学术验证...（内容同上）"
        word_count: 320
        evidence_used: ["mat-001", "mat-002"]
      - section_id: "sec-002"
        section_number: 2
        section_title: "特征工程：AI 的第一个突破口"
        section_content: "传统量化交易中，特征工程是最耗时的工作...（内容同上）"
        word_count: 380
        evidence_used: ["mat-001"]
      - section_id: "sec-003"
        section_number: 3
        section_title: "高频交易中的 AI 实战"
        section_content: "高频交易是 AI 量化最成熟的应用场景...（内容同上）"
        word_count: 420
        evidence_used: ["mat-001", "mat-003"]
      - section_id: "sec-004"
        section_number: 4
        section_title: "过度拟合：AI 量化的隐形杀手"
        section_content: "这是最容易被忽视的风险...（内容同上）"
        word_count: 350
        evidence_used: ["mat-001", "mat-003"]
      - section_id: "sec-005"
        section_number: 5
        section_title: "AI 量化的未来：机会与挑战"
        section_content: "AI 在量化中的应用才刚刚开始...（内容同上）"
        word_count: 380
        evidence_used: ["mat-003"]
  style_adherence_notes:
    tone_adherence: "全文保持理性、数据驱动的基调。使用具体数据（15%、12%、1.8 等）强化论点，避免空泛表述。"
    sentence_structure_adherence: "短句为主（平均 15 字），复杂论证时使用长句。例如：'这个转变的关键，是从 AI 能做什么转向 AI 在这个场景下怎么不失效。'"
    rhetorical_devices_used:
      - "类比：AI 在量化中的应用与工程优化的类比"
      - "排比：三个阶段的并列描述"
      - "反问：'为什么？因为 AI 生成的特征更多样化'"
      - "数据对比：回测 vs 实盘、传统 vs AI"
    vocabulary_adherence: "使用专业术语（特征工程、交叉验证、夏普比率）但配以解释，确保易懂。避免过度学术化。"
    paragraph_style_adherence: "段落长度 1-3 句，段落间有明确的逻辑转接。例如：'但这个数字背后，隐藏着一个更复杂的故事。'"
  dna_compliance_report:
    compliance_score: 92
    compliant_patterns:
      - "短句为主，便于移动阅读"
      - "数据对比强化论点"
      - "类比和反问增加互动感"
      - "避免过度修饰，保持专业感"
      - "段落间逻辑清晰"
    non_compliant_patterns: []
    violations: []
  weak_sections_and_fix_suggestions:
    - section_id: "sec-004"
      section_title: "过度拟合：AI 量化的隐形杀手"
      weakness_description: "失败案例的具体细节不足，读者可能不够理解为什么会失效"
      suggested_fix: "补充更多关于模型衰减检测的具体方法，或者补充另一个失败案例"
      priority: "medium"
    - section_id: "sec-005"
      section_title: "AI 量化的未来：机会与挑战"
      weakness_description: "监管风险的具体政策背景不足，显得有些抽象"
      suggested_fix: "补充最近的监管政策案例，例如某国对 AI 交易的限制措施"
      priority: "medium"
  optional_alternative_lead: |
    2024 年，某头部量化基金的 AI 模型在实盘中创造了 15% 的收益。但在 2025 年初，同一个模型突然失效，亏损 5%。这个故事告诉我们：AI 在量化中既是机会，也是陷阱。
  why_alternative: "这个开头更直接地切入风险主题，适合想要强调风险的版本。原开头更平衡，适合当前的版本。"
  evidence_usage_report:
    materials_used: 3
    materials_unused: 0
    unused_materials: []
    evidence_gaps_filled:
      - "AI 量化的三个阶段"
      - "特征工程的改进"
      - "高频交易的实际效果"
    evidence_gaps_remaining:
      - "更多失败案例"
      - "最新监管政策背景"
  risk_boundary_compliance:
    boundaries_respected: true
    boundary_violations: []
    risk_flags:
      - "第 4 节关于过度拟合的讨论可以更深入"
      - "第 5 节关于监管风险的讨论需要补充具体政策"
  quality_checklist:
    - item: "是否避免了夸大 AI 的预测能力"
      status: "pass"
      notes: "全文强调 AI 的局限性和风险"
    - item: "是否提及了监管风险"
      status: "warning"
      notes: "提及了，但不够具体，建议补充政策案例"
    - item: "是否符合文风 DNA"
      status: "pass"
      notes: "短句、数据对比、类比等都得到了很好的体现"
    - item: "是否避免了破折号"
      status: "pass"
      notes: "全文未使用破折号"
    - item: "是否避免了标题党式表达"
      status: "pass"
      notes: "标题和内容一致，没有虚假承诺"
    - item: "段落长度是否符合移动阅读习惯"
      status: "pass"
      notes: "段落长度 1-3 句，适合移动阅读"
  operator_note: "初稿质量较高，DNA 贴合度 92%。建议的修改方向：(1) 补充更多失败案例，(2) 补充最新监管政策。这两个修改可以在编辑阶段完成，不需要重写。"
  created_at: "2026-03-15T09:43:00Z"
```

---

## 工作流

1. Require confirmed outline, Content Brief, Material Pack, Style DNA card, and article goal.
2. 如果用户还没有个人 Style DNA，先调用 `wechat-style-profiler` 生成。
3. 将个人 Style DNA 复制到 `wechat-draft-writer/references/author-style-dna.md`。
4. 在开写前明确声明当前使用的 Style DNA 文件或作者画像名称。
5. Digest source material, separating hard facts from personal 观点、原话和待验证信息。
6. 以 Brief 的核心判断与 Material Pack 的证据清单作为写作硬边界。
7. 为每个 section 生成内部写作 brief，不对外输出新的大纲版本。
8. 按 section 写出 `Draft v1`，执行 `references/draft-dna-enforcement.md` 的硬约束。
9. 跑 `references/draft-quality-checklist.md` 自检。
10. 返回初稿、文风贴合说明、风险点和可修正建议。

---

## 输出契约总结

| 字段 | 说明 |
|------|------|
| style_dna_in_use | 使用的文风 DNA 及其特征 |
| draft_v1 | 完整初稿，包括分章节内容 |
| style_adherence_notes | 文风贴合说明 |
| dna_compliance_report | DNA 合规报告，包括评分和违反情况 |
| weak_sections_and_fix_suggestions | 弱点章节和修正建议 |
| optional_alternative_lead | 可选的开头版本 |
| evidence_usage_report | 证据使用报告 |
| risk_boundary_compliance | 风险边界合规情况 |
| quality_checklist | 质量检查清单 |

---

## Guardrails
- Avoid inventing facts; mark any uncertain claim with `[待补充证据]`.
- Distinguish source types explicitly: `参考资料` facts vs `语音底稿` personal expression.
- Keep paragraph granularity suitable for WeChat mobile reading.
- Preserve the user's habitual rhetorical devices from the Style DNA card.
- If no personal Style DNA is provided, hand off to `wechat-style-profiler` first.
- Prefer loading DNA from `wechat-draft-writer/references/author-style-dna.md`.
- The default DNA template is only a temporary fallback for demo/testing, not for final publish drafts.
- Must explicitly tell the user which DNA file or author profile is being used before presenting the draft.
- Keep paragraph length within 1-3 sentences unless explicitly requested.
- Do not use em dashes.
- If hard-fail pattern is detected, rewrite before returning output.
- If outline is not confirmed, hand off to `wechat-topic-outline-planner` instead of drafting.

---

## 参考
- `docs/task001-task003-integration-v1.md`
