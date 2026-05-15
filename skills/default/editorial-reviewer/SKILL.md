---
name: editorial-reviewer
description: 公众号终稿编辑复审适配器。用于对 Draft v1 进行结构、证据、语调的全面复审，输出结构化的修改建议。
---

# Editorial Reviewer - v1 契约版本

## 定位
本 Skill 是 `article_wechat` 场景下的编辑复审适配器。

它负责：
- 对已完成的 Draft v1 进行多维度复审
- 检查结构逻辑、证据风险、语调一致性
- 输出具体、可执行的修改建议

它不负责：
- 重写内容（只提建议）
- 改变文章核心观点
- 决策是否发布

---

## v1 输入契约

### 标准输入对象：Editorial Review Request

```yaml
editorial_review_request:
  request_id: string                    # 格式：review-{timestamp}-{uuid}
  draft_v1:                             # Draft v1 对象
    draft_id: string
    title: string
    full_content: string                # 完整初稿文本
    word_count: number
    created_at: timestamp
  confirmed_outline:                    # 原始确认大纲
    outline_id: string
    structure:
      - section_id: string
        section_number: number
        section_title: string
        section_objective: string
        core_argument: string
        evidence_required: [string]
  content_brief:                        # 原始 Content Brief
    brief_id: string
    core_judgment: string
    target_audience: string
    article_goal: string
    key_points: [string]
    risk_boundaries: [string]
  style_dna:                            # 文风 DNA
    dna_id: string
    author_name: string
    tone: string
    sentence_structure: string
    rhetorical_devices: [string]
    vocabulary_level: string
    paragraph_style: string
    taboo_patterns: [string]
  material_pack:                        # 原始 Material Pack（用于证据验证）
    pack_id: string
    materials:
      - material_id: string
        type: string
        title: string
        source: string
        credibility: string
  review_focus: [string]                # 可选，重点复审维度（默认全部）
  created_at: timestamp
```

---

## v1 输出契约

### 标准输出对象：Editorial Review Report

```yaml
editorial_review_report:
  report_id: string
  draft_id: string
  review_timestamp: timestamp
  
  # 1. 结构复审
  structural_review:
    overall_score: number               # 0-100
    status: "pass" | "needs_revision" | "critical"
    findings:
      - finding_id: string
        section_id: string
        severity: "critical" | "major" | "minor"
        issue_type: string              # 例如："逻辑断��"、"段落衔接弱"
        location: string                # 例如："第3段"
        description: string
        impact: string                  # 对读者理解的影响
        suggested_fix: string
    coherence_check:
      - section_id: string
        transition_quality: "smooth" | "abrupt" | "missing"
        transition_text: string
        suggestion: string
    argument_completeness:
      - section_id: string
        core_argument: string
        is_fully_supported: boolean
        missing_elements: [string]
  
  # 2. 证据风险检查
  evidence_risk_check:
    overall_score: number               # 0-100
    status: "pass" | "needs_revision" | "critical"
    findings:
      - finding_id: string
        section_id: string
        severity: "critical" | "major" | "minor"
        issue_type: string              # 例如："引用不准确"、"数据过时"、"来源可信度低"
        evidence_text: string
        source: string
        credibility_assessment: string
        risk_level: "high" | "medium" | "low"
        suggested_action: string        # 例如："补充来源"、"更新数据"、"删除"
    evidence_coverage:
      - section_id: string
        required_evidence: [string]
        provided_evidence: [string]
        coverage_rate: number           # 百分比
        missing_evidence: [string]
    source_credibility_summary:
      high_credibility_count: number
      medium_credibility_count: number
      low_credibility_count: number
      recommendations: [string]
  
  # 3. 语调一致性检查
  tone_consistency_check:
    overall_score: number               # 0-100
    status: "pass" | "needs_revision" | "critical"
    style_dna_adherence:
      tone_match: number                # 0-100
      sentence_structure_match: number  # 0-100
      vocabulary_match: number          # 0-100
      rhetorical_device_usage: [string] # 实际使用的修辞手法
      expected_devices: [string]        # 预期使用的修辞手法
    findings:
      - finding_id: string
        section_id: string
        severity: "critical" | "major" | "minor"
        issue_type: string              # 例如："语调不符"、"句式重复"、"词汇不当"
        location: string
        problematic_text: string
        reason: string
        suggested_revision: string
    audience_alignment:
      target_audience: string
      alignment_score: number           # 0-100
      issues: [string]
    consistency_violations:
      - violation_id: string
        pattern: string
        occurrences: number
        examples: [string]
        fix_suggestion: string
  
  # 4. 最终编辑建议
  final_edit_suggestions:
    priority_fixes:                     # 必须修改
      - fix_id: string
        priority: number                # 1-5，1 最高
        category: string                # 例如："结构"、"证据"、"语调"
        description: string
        location: string
        current_text: string
        suggested_text: string
        rationale: string
    optional_improvements:              # 可选优化
      - improvement_id: string
        category: string
        description: string
        location: string
        current_text: string
        suggested_text: string
        benefit: string
    readability_optimization:
      paragraph_length_issues: [string]
      formatting_suggestions: [string]
      scannability_score: number        # 0-100
    overall_recommendation: string      # 发布前是否需要修改
    estimated_revision_time: string     # 例如："30 分钟"
  
  # 5. 质量指标汇总
  quality_metrics:
    structural_integrity: number        # 0-100
    evidence_reliability: number        # 0-100
    style_consistency: number           # 0-100
    audience_fit: number                # 0-100
    readability: number                 # 0-100
    overall_quality_score: number       # 0-100
  
  # 6. 发布建议
  publication_readiness:
    ready_to_publish: boolean
    blockers: [string]                  # 发布前必须解决的问题
    warnings: [string]                  # 需要注意的问题
    next_steps: [string]
```

---

## 工作流

### 输入阶段
1. 接收 Editorial Review Request
2. 验证所有必需字段完整
3. 加载 Style DNA、Content Brief、Material Pack

### 复审阶段
1. **结构复审**（10+ 条规则）
   - 检查逻辑流畅性
   - 验证段落衔接
   - 确认论证完整性
   - 检查过渡句质量

2. **证据风险检查**（8+ 条规则）
   - 验证引用准确性
   - 检查数据有效性
   - 评估来源可信度
   - 检查证据覆盖率

3. **语调一致性检查**（6+ 条规则）
   - 对比 Style DNA
   - 检查修辞手法使用
   - 验证目标受众匹配
   - 检查表达准确性

### 输出阶段
1. 生成结构化复审报告
2. 输出优先级修改建议
3. 提供发布建议

---

## 示例

### 输入示例

```yaml
editorial_review_request:
  request_id: "review-20260315-us-iran-001"
  draft_v1:
    draft_id: "draft-20260315-us-iran-001"
    title: "美伊局势输赢判断"
    full_content: "[完整初稿文本]"
    word_count: 2800
  confirmed_outline:
    outline_id: "outline-us-iran-001"
    structure:
      - section_id: "sec-001"
        section_number: 1
        section_title: "为什么要讨论输赢"
        section_objective: "建立讨论框架"
        core_argument: "没有标准的输赢判断毫无价值"
        evidence_required: ["最近舆论现象", "三方不同目标"]
  content_brief:
    brief_id: "brief-us-iran-001"
    core_judgment: "美伊冲突的输赢取决于各方是否达成自身目标"
    target_audience: "关注国际政治的投资者和分析师"
    article_goal: "理性分析美伊冲突的实质和各方目标"
    key_points:
      - "以色列目标最清晰"
      - "美国核心是石油美元"
      - "伊朗目标是经济独立"
    risk_boundaries:
      - "不能预测具体军事行动"
      - "不能表达政治立场"
  style_dna:
    dna_id: "dna-lemon-001"
    author_name: "柠檬博士"
    tone: "理性、启发、略带幽默"
    sentence_structure: "短句为主，偶尔长句"
    rhetorical_devices: ["类比", "排比", "反问"]
    vocabulary_level: "专业但易懂"
    paragraph_style: "1-3 句为主"
    taboo_patterns: ["绝对化表述", "情绪化词汇"]
```

### 输出示例

```yaml
editorial_review_report:
  report_id: "report-20260315-us-iran-001"
  draft_id: "draft-20260315-us-iran-001"
  
  structural_review:
    overall_score: 82
    status: "needs_revision"
    findings:
      - finding_id: "struct-001"
        section_id: "sec-004"
        severity: "major"
        issue_type: "逻辑断层"
        location: "第 4 段"
        description: "从'美国目标'突然跳到'霍尔木兹海峡'，缺少过渡"
        impact: "读者可能不理解两者的关联"
        suggested_fix: "添加过渡句：'除了石油美元，美还关注海峡控制权'"
  
  evidence_risk_check:
    overall_score: 75
    status: "needs_revision"
    findings:
      - finding_id: "evid-001"
        section_id: "sec-003"
        severity: "major"
        issue_type: "数据过时"
        evidence_text: "工资从 200 美元跌到 70-100 美元"
        source: "未标注"
        credibility_assessment: "来源不明确"
        risk_level: "high"
        suggested_action: "补充数据来源和时间戳"
  
  tone_consistency_check:
    overall_score: 88
    status: "pass"
    style_dna_adherence:
      tone_match: 90
      sentence_structure_match: 85
      vocabulary_match: 88
    findings: []
  
  final_edit_suggestions:
    priority_fixes:
      - fix_id: "fix-001"
        priority: 1
        category: "结构"
        description: "添加过渡句连接第 3 和第 4 段"
        location: "第 3 段末尾"
        suggested_text: "除了石油美元，美还关注另一个战略要点：霍尔木兹海峡。"
      - fix_id: "fix-002"
        priority: 2
        category: "证据"
        description: "补充伊朗经济数据的来源"
        location: "第 3 段"
        suggested_text: "[补充：数据来源为 IMF 2025 年报告]"
    optional_improvements:
      - improvement_id: "imp-001"
        category: "语调"
        description: "第 5 段的反问句可以更有力"
        current_text: "美国到底想要什么？"
        suggested_text: "美国到底想要什么？这个问题的答案，决定了整场博弈的走向。"
  
  quality_metrics:
    structural_integrity: 82
    evidence_reliability: 75
    style_consistency: 88
    audience_fit: 85
    readability: 90
    overall_quality_score: 82
  
  publication_readiness:
    ready_to_publish: false
    blockers:
      - "补充伊朗经济数据的来源"
      - "添加第 3-4 段的过渡句"
    warnings:
      - "第 6 段的表述可能过于绝对"
    next_steps:
      - "修改优先级 1 的问题"
      - "补充证据来源"
      - "再次复审"
```

---

## Guardrails
- 不改写内容，只提建议
- 基于 Style DNA 进行语调检查
- 基于 Material Pack 进行证据验证
- 基于 Content Brief 的 risk_boundaries 进行风险检查
- 所有建议必须具体、可执行
- 优先级排序基于对读者理解和信息准确性的影响
- 不做政治判断，只检查逻辑和证据

---

## 参考
- `wechat-draft-writer/SKILL.md`
- `wechat-style-profiler/SKILL.md`
- `content-brief-builder/SKILL.md`
