---
name: planner-image-post
description: 图文卡片结构规划适配器。用于在 `target_media=image_post` 的前提下，基于已确认的 Content Brief、Material Pack 和 Media Plan，生成图文卡片的页面结构、内容分配、视觉指示和配图需求。
---

# Planner Image Post - 图文卡片结构规划

## 定位

本 Skill 是 `image_post` 的媒介适配器。

它负责：
- 在图文卡片场景下（小红书、微博、抖音等）
- 将 Brief / Material / Media Plan 转为图文卡片的页面结构方案
- 规划卡片页数、每页内容、视觉重点和配图需求

它不负责：
- 全局媒介选择
- 最终的设计稿生成
- 图片素材的实际制作

## 目标

将已确认的内容对象压缩成可执行的图文卡片框架，包括：
- 最优页数规划（3-8 页）
- 每页内容拆分（标题、文字、数据、视觉指示）
- 视觉重点标记（哪些内容需要配图）
- 配图需求生成（尺寸、风格、内容描述）

---

## 输入契约

### 标准输入对象：Image Post Planning Request

```yaml
image_post_planning_request:
  request_id: string                    # 格式：imgpost-{timestamp}-{uuid}
  content_brief:                        # 已确认的 Content Brief 对象
    brief_id: string
    working_title: string               # 工作标题
    core_claim: string                  # 核心观点
    content_goals: [string]             # 内容目标（增长、认知、转化等）
    target_audience: [string]           # 目标受众
    key_points: [string]                # 核心论点列表（3-5 个）
    risk_boundaries: [string]           # 风险边界
  material_pack:                        # Material Pack 对象
    pack_id: string
    materials:
      - material_id: string
        type: "reference" | "quote" | "data" | "case_study" | "expert_view" | "visual"
        title: string
        content: string
        source: string
        credibility: "high" | "medium" | "low"
    evidence_checklist: [string]        # 需要补充的证据
  media_plan:                           # 媒介计划
    target_media: "image_post"
    platform: "xiaohongshu" | "weibo" | "douyin" | "generic"  # 目标平台
    platform_constraints:
      image_ratio: string               # 图片比例（如 "3:4"）
      max_text_length: number           # 最大文字长度
      max_pages: number                 # 最大页数
      emoji_usage: "low" | "moderate" | "high"
    distribution_strategy: string       # 分发策略
  content_complexity: "simple" | "moderate" | "complex"  # 内容复杂度
  operator_note: string                 # 可选，操作员背景说明
  created_at: timestamp
```

### 示例

```yaml
image_post_planning_request:
  request_id: "imgpost-20260315-abc123"
  content_brief:
    brief_id: "brief-ai-quant-001"
    working_title: "AI 量化交易的 5 个陷阱"
    core_claim: "AI 在量化交易中很强大，但这 5 个陷阱会让你血本无归"
    content_goals: ["增长", "认知"]
    target_audience: ["量化交易从业者", "投资者"]
    key_points:
      - "过度拟合陷阱：历史数据不等于未来"
      - "黑箱风险：模型不可解释"
      - "数据质量陷阱：垃圾进垃圾出"
      - "监管风险：政策变化打破模型假设"
      - "心理陷阱：过度自信导致风险管理失效"
    risk_boundaries:
      - "不能夸大 AI 的预测能力"
      - "必须提及监管风险"
  material_pack:
    pack_id: "pack-ai-quant-001"
    materials:
      - material_id: "mat-001"
        type: "case_study"
        title: "某量化基金的失败案例"
        content: "该基金在 2024 年引入 AI 模型，收益率提升 15%，但在 2025 年初遭遇模型失效..."
        source: "行业访谈"
        credibility: "high"
      - material_id: "mat-002"
        type: "data"
        title: "AI 量化基金的收益分布"
        content: "2024 年 AI 量化基金平均收益 12%，但波动率也提升 20%..."
        source: "公开数据"
        credibility: "high"
  media_plan:
    target_media: "image_post"
    platform: "xiaohongshu"
    platform_constraints:
      image_ratio: "3:4"
      max_text_length: 400
      max_pages: 8
      emoji_usage: "moderate"
    distribution_strategy: "早晚高峰发布，配合话题标签"
  content_complexity: "moderate"
  created_at: "2026-03-15T12:00:00Z"
```

---

## 输出契约

### 单个 Image Post Structure 的结构

```yaml
image_post_structure:
  structure_id: string                  # 格式：imgstruct-{timestamp}-{uuid}
  request_id: string                    # 关联的 request_id
  brief_id: string
  material_pack_id: string
  target_platform: string               # 目标平台
  
  # 页面规划
  page_plan:
    total_pages: number                 # 总页数（3-8）
    page_strategy: string               # 页数规划策略说明
    pages:
      - page_number: number
        page_type: "cover" | "content" | "data" | "cta" | "closing"
        title: string                   # 页面标题/主文案
        content: string                 # 页面正文（100-200 字）
        key_message: string             # 核心信息（一句话）
        visual_focus: string            # 视觉重点描述
        visual_elements:
          - type: "image" | "icon" | "chart" | "text_overlay"
            description: string
            position: "top" | "center" | "bottom" | "full"
        image_requirement:
          image_id: string              # 配图 ID
          description: string           # 配图描述（用于设计师）
          style: string                 # 风格指示（如 "现代简约"、"数据可视化"）
          ratio: string                 # 图片比例
          color_tone: string            # 色调建议
          content_focus: string         # 内容重点
        text_specs:
          font_size: string             # 字体大小建议
          font_weight: string           # 字体粗细
          text_color: string            # 文字颜色
          background_color: string      # 背景颜色
        cta_element: string             # 行动号召（如果有）
  
  # 整体视觉指示
  visual_guidelines:
    color_palette: [string]             # 推荐色板（3-5 个颜色）
    typography:
      headline_font: string
      body_font: string
      font_hierarchy: string            # 字体层级说明
    style_tone: string                  # 整体风格（如 "专业严肃"、"轻松活泼"）
    visual_metaphor: string             # 视觉隐喻（如 "陷阱"、"对比"）
  
  # 配图需求汇总
  image_requirements:
    total_images: number
    images:
      - image_id: string
        page_number: number
        description: string             # 详细描述
        style: string
        ratio: string
        priority: "high" | "medium" | "low"
        alternative_options: [string]   # 备选方案
  
  # 内容分配
  content_distribution:
    total_text_length: number           # 总文字数
    text_per_page: number               # 平均每页文字数
    key_points_distribution: object     # 核心论点分配到各页
    materials_used: [string]            # 使用的素材 ID
    materials_missing: [string]         # 缺失的素材
  
  # 排版建议
  layout_recommendations:
    grid_system: string                 # 网格系统（如 "3 列"、"2 列"）
    spacing_guidelines: string          # 间距建议
    alignment_rules: string             # 对齐规则
    white_space_strategy: string        # 留白策略
  
  # 质量检查
  quality_checklist:
    - "所有页面都有清晰的视觉��点"
    - "文字和图片比例均衡"
    - "核心论点都有对应的视觉支撑"
    - "配色方案一致"
    - "CTA 清晰明确"
  
  status: "planned"
  created_at: timestamp
  updated_at: timestamp
```

### 完整输出示例

```yaml
image_post_structure:
  structure_id: "imgstruct-20260315-xyz789"
  request_id: "imgpost-20260315-abc123"
  brief_id: "brief-ai-quant-001"
  material_pack_id: "pack-ai-quant-001"
  target_platform: "xiaohongshu"
  
  page_plan:
    total_pages: 5
    page_strategy: "采用对比型结构：第 1 页开篇吸引，第 2-5 页分别展示 5 个陷阱，每个陷阱配一个案例或数据"
    pages:
      - page_number: 1
        page_type: "cover"
        title: "AI 量化交易的 5 个陷阱"
        content: "你以为 AI 能帮你稳定赚钱？这 5 个陷阱会让你血本无归。"
        key_message: "AI 量化很强大，但陷阱更多"
        visual_focus: "大标题 + 警告符号 + 数字 5"
        visual_elements:
          - type: "text_overlay"
            description: "大号数字 '5' 作为背景"
            position: "center"
          - type: "icon"
            description: "警告符号"
            position: "top"
        image_requirement:
          image_id: "img-001"
          description: "AI 芯片与陷阱的对比图，暗示风险"
          style: "现代科技感，带警告色调"
          ratio: "3:4"
          color_tone: "深蓝 + 红色警告"
          content_focus: "AI 与风险的对立"
        text_specs:
          font_size: "48px"
          font_weight: "bold"
          text_color: "#FFFFFF"
          background_color: "transparent"
        cta_element: "往下滑看详情"
      
      - page_number: 2
        page_type: "content"
        title: "陷阱 1：过度拟合"
        content: "历史数据再完美，也不等于未来。某量化基金在 2024 年用 AI 模型拟合历史数据，收益率 15%，但 2025 年初直接爆炸。"
        key_message: "历史不会重复，只会押韵"
        visual_focus: "对比图：历史数据 vs 实际表现"
        visual_elements:
          - type: "chart"
            description: "两条曲线对比：完美拟合 vs 实际失效"
            position: "center"
        image_requirement:
          image_id: "img-002"
          description: "K 线图对比：历史拟合完美 vs 实际表现崩溃"
          style: "数据可视化，红绿对比"
          ratio: "3:4"
          color_tone: "绿色（历史）vs 红色（实际）"
          content_focus: "拟合与现实的巨大差异"
        text_specs:
          font_size: "32px"
          font_weight: "600"
          text_color: "#1A1A1A"
          background_color: "#F5F5F5"
      
      - page_number: 3
        page_type: "data"
        title: "陷阱 2：黑箱风险"
        content: "深度学习模型就像黑箱，你不知道它为什么做决策。当市场变化时，你无法快速调整。"
        key_message: "不可解释 = 不可控"
        visual_focus: "黑箱图示 + 问号"
        visual_elements:
          - type: "icon"
            description: "黑箱与问号"
            position: "center"
        image_requirement:
          image_id: "img-003"
          description: "黑箱示意图，内部充满问号和不确定性"
          style: "抽象简约"
          ratio: "3:4"
          color_tone: "黑色 + 金色问号"
          content_focus: "神秘与不确定"
      
      - page_number: 4
        page_type: "content"
        title: "陷阱 3-5：数据、监管、心理"
        content: "数据质量决定模型质量。监管政策变化会打破所有假设。过度自信是最大的敌人。"
        key_message: "三重风险叠加"
        visual_focus: "三个风险因素的并列展示"
        visual_elements:
          - type: "icon"
            description: "三个风险图标"
            position: "center"
        image_requirement:
          image_id: "img-004"
          description: "三个风险因素的图标组合"
          style: "现代扁平"
          ratio: "3:4"
          color_tone: "多色警告"
          content_focus: "风险的多维度"
      
      - page_number: 5
        page_type: "cta"
        title: "如何规避这些陷阱？"
        content: "1. 定期回测和压力测试 2. 保持模型可解释性 3. 严格的风险管理 4. 持续监测市场变化"
        key_message: "知道陷阱，才能避开陷阱"
        visual_focus: "清单式展示"
        visual_elements:
          - type: "text_overlay"
            description: "清单项目"
            position: "center"
        cta_element: "点赞 + 评论你的经历"
  
  visual_guidelines:
    color_palette: ["#1A1A1A", "#0066FF", "#FF3333", "#F5F5F5", "#FFD700"]
    typography:
      headline_font: "PingFang SC Bold"
      body_font: "PingFang SC Regular"
      font_hierarchy: "标题 48px > 副标题 32px > 正文 16px"
    style_tone: "专业严肃，带警告意味"
    visual_metaphor: "陷阱与对比"
  
  image_requirements:
    total_images: 4
    images:
      - image_id: "img-001"
        page_number: 1
        description: "AI 芯片与陷阱的对比图"
        style: "现代科技感"
        ratio: "3:4"
        priority: "high"
      - image_id: "img-002"
        page_number: 2
        description: "K 线图对比"
        style: "数据可视化"
        ratio: "3:4"
        priority: "high"
      - image_id: "img-003"
        page_number: 3
        description: "黑箱示意图"
        style: "抽象简约"
        ratio: "3:4"
        priority: "medium"
      - image_id: "img-004"
        page_number: 4
        description: "三个风险图标"
        style: "现代扁平"
        ratio: "3:4"
        priority: "medium"
  
  content_distribution:
    total_text_length: 450
    text_per_page: 90
    key_points_distribution:
      "过度拟合": "page 2"
      "黑箱风险": "page 3"
      "数据质量": "page 4"
      "监管风险": "page 4"
      "心理陷阱": "page 4"
    materials_used: ["mat-001", "mat-002"]
    materials_missing: ["更多失败案例", "监管政策变化的具体例子"]
  
  layout_recommendations:
    grid_system: "单列布局，全屏沉浸式"
    spacing_guidelines: "上下间距 20px，左右边距 16px"
    alignment_rules: "标题居中，正文左对齐"
    white_space_strategy: "充分留白，避免拥挤"
  
  quality_checklist:
    - "✓ 所有页面都有清晰的视觉焦点"
    - "✓ 文字和图片比例均衡"
    - "✓ 5 个核心论点都有对应的视觉支撑"
    - "✓ 配色方案一致（蓝色 + 红色警告）"
    - "✓ CTA 清晰明确"
  
  status: "planned"
  created_at: "2026-03-15T12:39:46Z"
  updated_at: "2026-03-15T12:39:46Z"
```

---

## 核心算法

### 1. 页数规划算法

```
输入：content_complexity, key_points_count, material_count
输出：optimal_page_count

if content_complexity == "simple":
    base_pages = 3
elif content_complexity == "moderate":
    base_pages = 5
else:  # complex
    base_pages = 7

# 根据核心论点数调整
if key_points_count > 5:
    base_pages += 1
if key_points_count > 8:
    base_pages += 1

# 确保在 3-8 范围内
optimal_page_count = max(3, min(8, base_pages))
```

### 2. 内容分配算法

```
输入：key_points, total_pages, materials
输出：page_content_map

# 第 1 页：开篇（Cover）
page_1 = {
    type: "cover",
    content: "标题 + 核心观点 + 吸引力"
}

# 第 2 到 n-1 页：内容（Content）
content_pages = total_pages - 2
points_per_page = ceil(key_points / content_pages)

for i in range(content_pages):
    page = {
        type: "content",
        key_points: key_points[i*points_per_page:(i+1)*points_per_page],
        visual_focus: "对应的视觉重点",
        image: "配图"
    }

# 最后一页：行动号召（CTA）
page_n = {
    type: "cta",
    content: "总结 + 行动号召"
}
```

### 3. 视觉重点标记算法

```
输入：page_content, material_pack
输出：visual_focus_list

for each key_point in page_content:
    # 查找对应的素材
    matching_material = find_material(key_point)
    
    if matching_material.type == "data":
        visual_focus = "数据可视化（图表、数字）"
    elif matching_material.type == "case_study":
        visual_focus = "对比图或流程图"
    elif matching_material.type == "quote":
        visual_focus = "引用框或强调文字"
    else:
        visual_focus = "通用配图"
    
    visual_focus_list.append(visual_focus)
```

---

## 与其他 Planner 的差异

| 维度 | Wechat Topic Outline | Image Post Planner | Video Script Planner |
|------|---------------------|-------------------|----------------------|
| **输出单位** | 文章大纲（段落） | 卡片页面（页数） | 视频场景（镜头） |
| **信息密度** | 高（1500-2500 字） | 中（200-400 字） | 低（视觉为主） |
| **视觉指示** | 配图位置 | 详细的视觉指示 + 配图需求 | 镜头、场景、特效 |
| **排版重点** | 段落结构、引用标注 | 页面布局、色彩、字体 | 镜头语言、转场 |
| **核心输出** | 文章结构 | 页面结构 + 视觉指示 | 脚本 + 制作指南 |

---

## 使用流程

### 1. 接收输入

```python
request = ImagePostPlanningRequest(
    content_brief=brief,
    material_pack=material_pack,
    media_plan=media_plan,
    content_complexity="moderate"
)
```

### 2. 验证输入

```python
validator = ImagePostValidator()
validator.validate_brief(request.content_brief)
validator.validate_material_pack(request.material_pack)
validator.validate_media_plan(request.media_plan)
```

### 3. 生成页面结构

```python
generator = ImagePostStructureGenerator()
structure = generator.generate(request)
```

### 4. 输出结果

```python
output = {
    "structure_id": structure.structure_id,
    "page_plan": structure.page_plan,
    "visual_guidelines": structure.visual_guidelines,
    "image_requirements": structure.image_requirements,
    "status": "planned"
}
```

---

## 集成指南

### 与 Feishu Bitable 的集成

```python
for structure in image_post_structures:
    feishu_bitable.create_record(
        app_token=app_token,
        table_id=table_id,
        fields={
            "Structure ID": structure.structure_id,
            "Brief ID": structure.brief_id,
            "总页数": structure.page_plan.total_pages,
            "目标平台": structure.target_platform,
            "配图数": len(structure.image_requirements.images),
            "状态": structure.status,
            "创建时间": structure.created_at,
        }
    )
```

### 与下游 Skill 的集成

```
image_post_structure (status=planned)
  ├─ 下一步：image-post-generator（生成最终卡片）
  ├─ 或：design-system（设计稿生成）
  └─ 或：content-writer（文案优化）
```

---

## 版本历史

### v1.0 (2026-03-15)
- ✅ 支持 3-8 页的图文卡片结构规划
- ✅ 页数规划算法（基于内容复杂度）
- ✅ 每页内容拆分和视觉指示
- ✅ 配图需求生成
- ✅ 平台特定的约束处理（小红书、微博等）
- ✅ 完整的输入/输出契约
