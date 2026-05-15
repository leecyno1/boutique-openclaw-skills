---
name: planner-video-script
description: 视频脚本结构规划适配器。用于在 `target_media=video_script` 的前提下，基于已确认的 Content Brief、Material Pack 和 Media Plan，生成视频脚本的完整框架，包含开场钩子、核心论证段落、分镜建议、口播逻辑和结尾行动号召。
---

# Video Script Planner - 视频脚本结构规划

## 新定位

本 Skill 是 `video_script` 的媒介适配器。

它负责：
- 在视频脚本场景下
- 将 Brief / Material / Media Plan 转为视频脚本结构方案

它不再负责：
- 全局选题判断
- 全局媒介路由
- 完整的台词撰写（仅提供口播逻辑框架）

## 目标

把已确认的内容对象压缩成可拍、可演、可确认的视频脚本框架，包含视觉指示和口播节奏，减少后续制作返工。

---

## v1 输入契约

### 标准输入对象：Video Script Planning Request

```yaml
video_script_planning_request:
  request_id: string                    # 格式：video-script-{timestamp}-{uuid}
  content_brief:                        # 已确认的 Content Brief 对象
    brief_id: string
    core_judgment: string               # 核心判断
    target_audience: string             # 目标观众
    video_goal: string                  # 视频目标
    key_points: [string]                # 核心论点列表
    risk_boundaries: [string]           # 风险边界
  material_pack:                        # Material Pack 对象
    pack_id: string
    materials:
      - material_id: string
        type: "reference" | "quote" | "data" | "case_study" | "expert_view" | "visual_asset"
        title: string
        content: string
        source: string
        credibility: "high" | "medium" | "low"
        visual_potential: "high" | "medium" | "low"  # 视觉化潜力
    evidence_checklist: [string]        # 需要补充的证据
  media_plan:                           # 媒介计划
    target_media: "video_script"
    platform_constraints:
      duration_minutes: number          # 视频时长（分钟）
      scene_count: number               # 推荐场景数
      speaker_count: number             # 讲述人数
      background_music: boolean         # 是否需要背景音乐
      subtitle_required: boolean        # 是否需要字幕
      animation_required: boolean       # 是否需要动画
    distribution_strategy: string       # 分发策略
  target_media: "video_script"
  operator_note: string                 # 可选，操作员背景说明
  created_at: timestamp
```

### 示例

```yaml
video_script_planning_request:
  request_id: "video-script-20260315-abc123"
  content_brief:
    brief_id: "brief-ai-quant-001"
    core_judgment: "AI 在量化交易中已从理论进入实践，但仍需警惕过度拟合和黑箱风险"
    target_audience: "量化交易从业者、投资者、AI 研究者"
    video_goal: "通过案例展示 AI 量化的实际应用，同时提示风险"
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
        content: "该基金在 2024 年引入 AI 模型，收益率提升 15%..."
        source: "行业访谈"
        credibility: "high"
        visual_potential: "high"
      - material_id: "mat-002"
        type: "data"
        title: "AI 量化基金的收益分布"
        content: "2024 年 AI 量化基金平均收益 12%..."
        source: "公开数据"
        credibility: "high"
        visual_potential: "high"
  media_plan:
    target_media: "video_script"
    platform_constraints:
      duration_minutes: 8
      scene_count: 5
      speaker_count: 1
      background_music: true
      subtitle_required: true
      animation_required: false
    distribution_strategy: "YouTube、B站、小红书视频"
  target_media: "video_script"
  operator_note: "这是 AI 量化系列的第二期视频"
  created_at: "2026-03-15T09:43:00Z"
```

---

## v1 输出契约

### 输出对象：Video Script Structure

```yaml
video_script_structure:
  structure_id: string                  # 格式：video-struct-{timestamp}-{uuid}
  request_id: string                    # 关联的请求 ID
  input_digest:
    brief_summary: string               # Brief 摘要
    material_count: number
    visual_assets_count: number         # 可视化素材数
    evidence_gaps: [string]             # 证据缺口
  
  # 开场钩子（5-10 秒）
  hook:
    hook_id: string
    hook_type: "question" | "statement" | "visual" | "story"  # 钩子类型
    hook_text: string                   # 钩子文案（30-50 字）
    visual_suggestion: string           # 视觉建议
    duration_seconds: number            # 预计时长
    emotional_tone: string              # 情感基调
    why_this_hook: string               # 为什么选这个钩子
  
  # 核心论证段落（分段，每段 30-60 秒）
  sections:
    - section_id: string
      section_number: number
      section_title: string             # 段落标题
      section_objective: string         # 段落目标
      core_argument: string             # 核心论点
      duration_seconds: number          # 预计时长（30-60）
      
      # 口播逻辑
      narration:
        narration_id: string
        main_text: string               # 主要口播文案（100-150 字）
        key_phrases: [string]           # 关键短语（需要强调）
        pause_points: [string]          # 停顿点（用于呼吸和强调）
        tone: string                    # 语调建议（平稳、激昂、温和等）
        pacing: string                  # 节奏建议（快速、中等、缓慢）
      
      # 分镜建议
      shots:
        - shot_id: string
          shot_number: number
          shot_type: string             # 镜头类型（全景、中景、特写等）
          shot_description: string      # 镜头描述
          visual_elements: [string]     # 视觉元素（文字、图表、动画等）
          duration_seconds: number      # 镜头时长
          transition: string            # 转场方式
      
      # 证据支撑
      evidence:
        - evidence_id: string
          evidence_type: string         # 证据类型
          evidence_text: string         # 证据内容
          source: string                # 来源
          visual_format: string         # 视觉呈现方式
      
      # 转场逻辑
      transition_logic: string          # 到下一段的转场逻辑
  
  # 结尾行动号召（5-10 秒）
  cta:
    cta_id: string
    cta_type: "subscribe" | "like" | "comment" | "share" | "visit" | "multi"
    cta_text: string                    # CTA 文案（30-50 字）
    visual_suggestion: string           # 视觉建议
    duration_seconds: number            # 预计时长
    emotional_tone: string              # 情感基调
    call_to_action_buttons: [string]    # 行动按钮建议
  
  # 总体生产参数
  production_notes:
    total_duration_seconds: number      # 总时长（秒）
    total_duration_minutes: number      # 总时长（分钟）
    scene_count: number                 # 场景数
    speaker_count: number               # 讲述人数
    background_music_style: string      # 背景音乐风格建议
    subtitle_strategy: string           # 字幕策略
    animation_needs: [string]           # 动画需求
    color_palette: [string]             # 色彩建议
    visual_style: string                # 视觉风格建议
    equipment_needs: [string]           # 设备需求
  
  # 质量检查清单
  quality_checklist:
    - item: string
      status: "required" | "optional"
      description: string
  
  created_at: timestamp
  updated_at: timestamp
```

### 输出示例

```yaml
video_script_structure:
  structure_id: "video-struct-20260315-xyz789"
  request_id: "video-script-20260315-abc123"
  input_digest:
    brief_summary: "AI 在量化交易中的实际应用与风险"
    material_count: 5
    visual_assets_count: 3
    evidence_gaps: ["监管政策背景", "失败案例"]
  
  hook:
    hook_id: "hook-001"
    hook_type: "question"
    hook_text: "你知道吗？AI 已经在量化交易中赚到了真金白银，但也踩过不少坑。今天我们来看看那些真实的故事。"
    visual_suggestion: "屏幕上显示股票走势图，然后切换到 AI 芯片的特写"
    duration_seconds: 8
    emotional_tone: "好奇、引人入胜"
    why_this_hook: "用问句吸引注意力，同时暗示内容的实用性和风险性"
  
  sections:
    - section_id: "sec-001"
      section_number: 1
      section_title: "AI 模型在特征工程中的优势"
      section_objective: "解释 AI 如何改进传统量化模型"
      core_argument: "AI 能自动发现隐藏的市场规律，比人工特征工程快 10 倍"
      duration_seconds: 45
      
      narration:
        narration_id: "nar-001"
        main_text: "传统的量化交易依赖人工特征工程，需要交易员花费数周时间来发现市场规律。但 AI 模型可以在几小时内处理数百万条数据，自动发现那些人类容易忽视的模式。某量化基金的案例显示，引入 AI 后，模型的特征数量从 50 个增加到 500 个，而准确率提升了 15%。"
        key_phrases: ["自动发现", "数百万条数据", "准确率提升 15%"]
        pause_points: ["传统的量化交易依赖人工特征工程，", "需要交易员花费数周时间来发现市场规律。", "但 AI 模型可以在几小时内处理数百万条数据，"]
        tone: "平稳、专业"
        pacing: "中等"
      
      shots:
        - shot_id: "shot-001"
          shot_number: 1
          shot_type: "全景"
          shot_description: "展示交易员在办公室工作的场景"
          visual_elements: ["多屏显示器", "数据表格", "交易员思考的表情"]
          duration_seconds: 10
          transition: "淡入"
        
        - shot_id: "shot-002"
          shot_number: 2
          shot_type: "特写"
          shot_description: "展示 AI 模型处理���据的过程"
          visual_elements: ["数据流动画", "神经网络可视化", "进度条"]
          duration_seconds: 15
          transition: "切换"
        
        - shot_id: "shot-003"
          shot_number: 3
          shot_type: "中景"
          shot_description: "展示对比数据"
          visual_elements: ["柱状图对比", "数字增长动画", "百分比标注"]
          duration_seconds: 20
          transition: "淡出"
      
      evidence:
        - evidence_id: "ev-001"
          evidence_type: "case_study"
          evidence_text: "某量化基金在 2024 年引入 AI 模型，特征数量从 50 增加到 500，准确率提升 15%"
          source: "行业访谈"
          visual_format: "数据对比图表"
      
      transition_logic: "既然 AI 能改进特征工程，那它在实际交易中表现如何呢？"
    
    - section_id: "sec-002"
      section_number: 2
      section_title: "高频交易中的实际应用"
      section_objective: "展示 AI 在实际交易中的成果"
      core_argument: "AI 驱动的高频交易策略在 2024 年平均收益率达到 12%，超过传统策略"
      duration_seconds: 50
      
      narration:
        narration_id: "nar-002"
        main_text: "在高频交易领域，AI 的优势更加明显。一个典型的案例是，某基金使用 AI 模型进行微秒级的交易决策，在 2024 年全年的收益率达到 12%，而同期传统高频交易策略的平均收益率只有 8%。这 4% 的差异，在数十亿的资金规模上，意味着数亿元的额外收益。"
        key_phrases: ["微秒级决策", "收益率 12%", "超过传统策略 4%"]
        pause_points: ["在高频交易领域，", "AI 的优势更加明显。", "微秒级的交易决策，"]
        tone: "激昂、有说服力"
        pacing: "中等偏快"
      
      shots:
        - shot_id: "shot-004"
          shot_number: 4
          shot_type: "特写"
          shot_description: "展示交易数据实时更新"
          visual_elements: ["实时行情", "K线图", "数字滚动"]
          duration_seconds: 15
          transition: "切换"
        
        - shot_id: "shot-005"
          shot_number: 5
          shot_type: "中景"
          shot_description: "展示收益对比"
          visual_elements: ["折线图", "百分比增长", "对比标注"]
          duration_seconds: 20
          transition: "淡出"
        
        - shot_id: "shot-006"
          shot_number: 6
          shot_type: "全景"
          shot_description: "展示交易室的繁忙场景"
          visual_elements: ["多屏显示器", "团队协作", "紧张的氛围"]
          duration_seconds: 15
          transition: "切换"
      
      evidence:
        - evidence_id: "ev-002"
          evidence_type: "data"
          evidence_text: "AI 驱动的高频交易 2024 年收益率 12%，传统策略 8%"
          source: "公开数据"
          visual_format: "折线图对比"
      
      transition_logic: "但成功的背后，也隐藏着巨大的风险。"
    
    - section_id: "sec-003"
      section_number: 3
      section_title: "过度拟合与风险控制"
      section_objective: "警示 AI 模型的风险"
      core_argument: "过度拟合是 AI 量化交易最大的风险，需要严格的风险控制机制"
      duration_seconds: 55
      
      narration:
        narration_id: "nar-003"
        main_text: "但这里有个关键问题：AI 模型在历史数据上表现完美，不代表在未来市场中也能表现完美。这就是所谓的'过度拟合'。某基金在 2025 年初就遭遇了这个问题。他们的 AI 模型在 2024 年的回测中收益率高达 25%，但在真实交易中，仅仅一个月就亏损了 8%。原因很简单：模型学到的是历史数据中的噪声，而不是真正的市场规律。所以，风险控制不是可选项，而是必须项。"
        key_phrases: ["过度拟合", "回测 25%", "实际亏损 8%", "风险控制必须项"]
        pause_points: ["但这里有个关键问题：", "过度拟合。", "仅仅一个月就亏损了 8%。", "风险控制不是可选项，"]
        tone: "严肃、警示"
        pacing: "中等"
      
      shots:
        - shot_id: "shot-007"
          shot_number: 7
          shot_type: "特写"
          shot_description: "展示模型拟合曲线"
          visual_elements: ["完美拟合的曲线", "然后突然偏离", "对比动画"]
          duration_seconds: 15
          transition: "切换"
        
        - shot_id: "shot-008"
          shot_number: 8
          shot_type: "中景"
          shot_description: "展示亏损数据"
          visual_elements: ["下降的图表", "红色警告标志", "数字变化"]
          duration_seconds: 20
          transition: "淡出"
        
        - shot_id: "shot-009"
          shot_number: 9
          shot_type: "全景"
          shot_description: "展示风险控制面板"
          visual_elements: ["仪表盘", "风险指标", "控制按钮"]
          duration_seconds: 20
          transition: "切换"
      
      evidence:
        - evidence_id: "ev-003"
          evidence_type: "case_study"
          evidence_text: "某基金模型回测收益 25%，实际交易亏损 8%，典型的过度拟合案例"
          source: "行业访谈"
          visual_format: "对比图表"
      
      transition_logic: "那么，如何才能在 AI 的机遇和风险之间找到平衡呢？"
  
  cta:
    cta_id: "cta-001"
    cta_type: "multi"
    cta_text: "如果你也在探索 AI 量化的机遇和风险，欢迎订阅我们的频道，获取最新的行业洞察。同时，在评论区分享你的想法和经验。"
    visual_suggestion: "展示订阅按钮、点赞按钮、评论框，配合背景音乐"
    duration_seconds: 8
    emotional_tone: "邀请、友好"
    call_to_action_buttons: ["订阅", "点赞", "评论", "分享"]
  
  production_notes:
    total_duration_seconds: 206
    total_duration_minutes: 3.43
    scene_count: 9
    speaker_count: 1
    background_music_style: "现代、科技感、节奏感强"
    subtitle_strategy: "全程字幕，关键数字和概念加粗或高亮"
    animation_needs: ["数据流动画", "图表动画", "转场动画", "文字动画"]
    color_palette: ["深蓝", "科技绿", "金色", "白色"]
    visual_style: "现代科技风格，配合数据可视化"
    equipment_needs: ["4K 摄像机", "麦克风", "绿幕", "灯光"]
  
  quality_checklist:
    - item: "开场钩子是否能在 5-10 秒内吸引注意力"
      status: "required"
      description: "钩子必须在前 10 秒内建立观众的兴趣"
    
    - item: "每个段落是否有清晰的论点和证据支撑"
      status: "required"
      description: "每个段落必须有核心论点和至少一个证据"
    
    - item: "分镜建议是否可行"
      status: "required"
      description: "分镜建议必须考虑实际拍摄的可行性"
    
    - item: "口播逻辑是否流畅"
      status: "required"
      description: "口播文案必须自然流畅，避免生硬"
    
    - item: "CTA 是否清晰有力"
      status: "required"
      description: "CTA 必须明确指导观众的下一步行动"
    
    - item: "总时长是否符合媒介计划"
      status: "required"
      description: "总时长必须在媒介计划的范围内"
    
    - item: "视觉元素是否丰富"
      status: "optional"
      description: "建议使用多种视觉元素保持观众兴趣"
  
  created_at: "2026-03-15T10:30:00Z"
  updated_at: "2026-03-15T10:30:00Z"
```

---

## 与 planner-article-wechat 的差异

| 维度 | 公众号文章 | 视频脚本 |
|------|---------|--------|
| **时间维度** | 静态阅读，读者自主控制节奏 | 动态播放，时间线固定 |
| **信息密度** | 高（1500-2500 字） | 中等（口播 + 视觉） |
| **论证方式** | 文字论证为主 | 视觉 + 口播结合 |
| **开场** | 引言段落（100-200 字） | 钩子（5-10 秒） |
| **段落结构** | 逻辑递进 | 时间递进 + 视觉递进 |
| **证据呈现** | 引用、数据、案例 | 图表、动画、视频片段 |
| **结尾** | 总结 + 号召 | CTA（5-10 秒） |
| **下游 Skill** | wechat-topic-outline-planner | video-script-generator |

---

## 使用流程

### 输入来源

1. **Content Brief** - 已确认的内容方向
2. **Material Pack** - 收集的素材和证据
3. **Media Plan** - 媒介计划（包含时长、场景数等约束）

### 处理步骤

1. **验证输入** - 检查 Brief、Material、Media Plan 的完整性
2. **分析视频需求** - 根据时长和场景数规划段落
3. **生成开场钩子** - 创建 5-10 秒的吸引力钩子
4. **拆分核心论证** - 根据时长将论点分段（每段 30-60 秒）
5. **设计分镜** - 为每个段落建议镜头和视觉元素
6. **优化口播逻辑** - 设计节奏、停顿、强调点
7. **设计 CTA** - 创建清晰的行动号召
8. **生成生产参数** - 汇总所有生产需求

### 输出交付

生成完整的 `video_script_structure` 对象，包含：
- 开场钩子
- 3-5 个核心论证段落
- 每个段落的分镜建议
- 口播逻辑和节奏
- 结尾 CTA
- 生产参数和质量检查清单

---

## 集成指南

### 与 Feishu Bitable 的集成

每个 Video Script Structure 应写入 Feishu Bitable：

```python
feishu_bitable.create_record(
    app_token=app_token,
    table_id=table_id,
    fields={
        "Script Structure ID": structure.structure_id,
        "Request ID": structure.request_id,
        "Brief ID": structure.input_digest.brief_id,
        "总时长（分钟）": structure.production_notes.total_duration_minutes,
        "场景数": structure.production_notes.scene_count,
        "状态": "planned",
        "下一个Skill": "video-script-generator",
        "创建时间": structure.created_at,
    }
)
```

### 与下游 Skill 的集成

Video Script Structure 的输出应传递给 `video-script-generator`：

```
video_script_structure (status=planned)
  └─ video-script-generator (生成完整台词和制作指南)
```

---

## 版本历史

### v1.0 (2026-03-15)
- ✅ 支持从 Brief + Material + Media Plan 生成视频脚本框架
- ✅ 包含开场钩子、核心论证段落、分镜建议、口播逻辑、CTA
- ✅ 完整的生产参数和质量检查清单
- ✅ 与 planner-article-wechat 的差异对标
