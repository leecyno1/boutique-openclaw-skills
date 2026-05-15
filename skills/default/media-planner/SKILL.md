---
name: media-planner
description: 跨媒介规划 Skill。用于根据 Content Brief 和 Material Pack，为所有推荐媒介批量生成执行计划，如公众号文章大纲、视频脚本结构、图文拆页结构等。支持一鱼多吃的多媒介衍生。
---

# Media Planner - 批量生成版本

## 目标

让同一个 Brief 能够为所有推荐媒介批量生成不同的执行方案，实现真正的"一鱼多吃"。

## 核心改进

### v1.0 → v2.0 的变化

| 维度 | v1.0 | v2.0 |
|------|------|------|
| **生成范围** | 仅第一个推荐媒介 | 所有推荐媒介 |
| **媒介适配** | 硬编码逻辑 | 媒介适配器（可扩展） |
| **structure_type** | 固定值 | 根据媒介类型动态选择 |
| **大纲框架** | 通用框架 | 媒介特定框架 |
| **输出** | 单个 Media Plan | 多个 Media Plan（一个媒介一个） |

## 输入

```yaml
brief:
  brief_id: string
  working_title: string
  core_claim: string
  content_goals: array
  recommended_media: array  # 关键：所有推荐媒介
  target_audience: array
  
material_pack:
  material_pack_id: string
  resources: array
  evidence_list: array
  
operator_note: string (optional)
```

## 工作流

### Step 1: 验证 Brief 和推荐媒介

```
检查 Brief 是否有效
  ↓
检查 recommended_media 是否为空
  ↓
如果为空，返回错误
如果有效，继续
```

### Step 2: 遍历所有推荐媒介

```
for each media in recommended_media:
  ├─ 获取媒介配置（structure_type、production_params 等）
  ├─ 生成媒介特定的大纲框架
  ├─ 生成 Media Plan
  └─ 添加到输出列表
```

### Step 3: 为每个媒介生成 Media Plan

对于每个媒介，执行以下步骤：

#### 3.1 确定 structure_type

根据媒介类型和内容目标，选择合适的结构类型：

- **article_wechat**: argumentative / narrative
- **video_script**: narrative / interview
- **image_post**: comparative / data_driven
- **newsletter**: mixed
- **short_video**: narrative / instructional
- **slide_deck**: instructional / data_driven
- **podcast_script**: narrative / interview

#### 3.2 生成媒介特定的大纲

使用媒介适配器生成对应的大纲框架：

```python
outline = MediaTypeAdapter.generate_media_plan_outline(
    media_type=media,
    core_claim=brief.core_claim,
    content_goals=brief.content_goals
)
```

#### 3.3 填充 Media Plan 字段

```yaml
media_plan_id: mp_YYYYMMDD_序号_媒介类型
brief_id: {brief_id}
target_media: {media_type}
objective: {从 brief 推导}
structure_type: {媒介特定}
outline: {���介特定框架}
hook: {媒介特定的开篇 hook}
cta: {媒介特定的行动号召}
production_notes: {媒介特定的生产参数}
next_adapter: {媒介对应的下一个 skill}
status: planned
```

#### 3.4 生成媒介特定的 Hook 和 CTA

根据媒介类型生成不同风格的 Hook 和 CTA：

**article_wechat**:
- Hook: 长度 50-200 字，建立共鸣
- CTA: 邀请评论、分享、点赞

**video_script**:
- Hook: 3-5 秒的视觉冲击
- CTA: 邀请订阅、点赞、评论

**image_post**:
- Hook: 视觉冲击 + 短文案
- CTA: 邀请点赞、评论、转发

**newsletter**:
- Hook: 主题行 + 摘要
- CTA: 多个 CTA 按钮

## 输出契约

### 单个 Media Plan 的结构

```yaml
media_plan_id: string
brief_id: string
material_pack_id: string (optional)
target_media: enum
objective: enum
target_audience: array
structure_type: enum
outline: array
hook: string
cta: string
style_notes: object
production_notes: object
review_focus: array
status: enum
next_adapter: string
created_at: datetime
updated_at: datetime
```

### 批量输出结构

```yaml
brief_id: string
media_plans: array
  - media_plan_id: string
    target_media: string
    status: string
    next_adapter: string
  - ...
total_media_plans: integer
created_at: datetime
```

## 媒介适配逻辑

### 支持的媒介类型

| 媒介类型 | 主要结构 | 次要结构 | 下一个 Skill | 说明 |
|---------|--------|--------|------------|------|
| article_wechat | argumentative, narrative | data_driven, instructional | wechat-topic-outline-planner | 公众号文章 |
| video_script | narrative, interview | data_driven, instructional | video-script-generator | 视频脚本 |
| image_post | comparative, data_driven | narrative, instructional | image-post-planner | 图文内容 |
| newsletter | mixed, narrative | data_driven, instructional | newsletter-generator | 邮件通讯 |
| short_video | narrative, instructional | data_driven, comparative | short-video-generator | 短视频 |
| slide_deck | instructional, data_driven | comparative, argumentative | slide-deck-generator | 幻灯片 |
| podcast_script | narrative, interview | argumentative, instructional | podcast-script-generator | 播客脚本 |

### 媒介特定的生产参数

#### article_wechat
```yaml
word_count: "1500-2500字"
reading_time: "8-10分钟"
image_count: 3
image_specs: "800x600px, 高质量配图"
section_count: "4-6段"
```

#### video_script
```yaml
duration: "8-10分钟"
scene_count: 5
speaker_count: 1
background_music: true
subtitle_required: true
animation_required: false
```

#### image_post
```yaml
image_count: 5
text_length: "200-400字"
hashtag_count: 5
platform_specific:
  xiaohongshu:
    image_ratio: "3:4"
    emoji_usage: "moderate"
  weibo:
    image_ratio: "1:1 or 16:9"
    emoji_usage: "high"
```

#### newsletter
```yaml
word_count: "800-1200字"
section_count: 3
reading_time: "5-7分钟"
cta_count: 2
image_count: 2
```

## 使用示例

### 输入

```json
{
  "brief": {
    "brief_id": "brief-20260315-001",
    "working_title": "AI时代的职业转型指南",
    "core_claim": "AI不会替代人类，而是改变工作方式",
    "content_goals": ["增长", "认知"],
    "recommended_media": ["article_wechat", "video_script", "image_post"],
    "target_audience": ["职场人士", "学生", "创业者"]
  },
  "material_pack": {
    "material_pack_id": "mp-pack-20260315-001",
    "resources": ["小红书原文", "行业报告", "案例研究"],
    "evidence_list": ["1928赞", "高互动评论", "相关话题聚集"]
  }
}
```

### 输出

```json
{
  "brief_id": "brief-20260315-001",
  "media_plans": [
    {
      "media_plan_id": "mp-20260315-001-article_wechat",
      "target_media": "article_wechat",
      "structure_type": "argumentative",
      "outline": [
        {
          "section_number": 1,
          "section_title": "开篇：焦虑的根源",
          "purpose": "建立共鸣，引出问题",
          "key_points": ["AI发展速度超预期", "职场人士的真实焦虑"],
          "content_length": "300-400字"
        },
        ...
      ],
      "hook": "你的工作会被AI替代吗？1928个赞的讨论背后，是职场人士的真实焦虑。",
      "cta": "评论区分享你的职业转型故事。",
      "production_notes": {
        "word_count": "1500-2500字",
        "reading_time": "8-10分钟",
        "image_count": 3
      },
      "next_adapter": "wechat-topic-outline-planner",
      "status": "planned"
    },
    {
      "media_plan_id": "mp-20260315-001-video_script",
      "target_media": "video_script",
      "structure_type": "narrative",
      "outline": [
        {
          "section_number": 1,
          "section_title": "开场（Hook）",
          "purpose": "吸引观众，建立期待",
          "key_points": ["问题提出", "视觉冲击"],
          "content_length": "30-60秒"
        },
        ...
      ],
      "hook": "【AI时代职业焦虑】你是否担心自己的工作被替代？",
      "cta": "点赞、评论、订阅，分享你的职业转型故事。",
      "production_notes": {
        "duration": "8-10分钟",
        "scene_count": 5,
        "subtitle_required": true
      },
      "next_adapter": "video-script-generator",
      "status": "planned"
    },
    {
      "media_plan_id": "mp-20260315-001-image_post",
      "target_media": "image_post",
      "structure_type": "comparative",
      "outline": [
        {
          "section_number": 1,
          "section_title": "封面图 + 标题",
          "purpose": "吸引点击",
          "key_points": ["视觉冲击", "标题吸引力"],
          "content_length": "标题 20-30字"
        },
        ...
      ],
      "hook": "AI时代职业转型：从焦虑到机遇",
      "cta": "点赞、评论、转发，分享你的想法。",
      "production_notes": {
        "image_count": 5,
        "text_length": "200-400字",
        "hashtag_count": 5
      },
      "next_adapter": "image-post-planner",
      "status": "planned"
    }
  ],
  "total_media_plans": 3,
  "created_at": "2026-03-15T12:39:46Z"
}
```

## 边界

- 不直接生成最终正文或视频台词全文
- 不直接发布
- 不替代素材补全
- 仅为推荐媒介生成 Media Plan（不生成未推荐的媒介）

## 参考

- `media_type_adapter.py` - 媒介适配逻辑
- `docs/media-plan-schema-v3.md` - Media Plan 数据结构
- `docs/content-brief-schema-v2.md` - Content Brief 数据结构
- `docs/content-workflow-v2.md` - 完整工作流

## 集成指南

### 与 Feishu Bitable 的集成

每个 Media Plan 应写入 Feishu Bitable：

```python
for media_plan in media_plans:
    feishu_bitable.create_record(
        app_token=app_token,
        table_id=table_id,
        fields={
            "Media Plan ID": media_plan.media_plan_id,
            "Brief ID": media_plan.brief_id,
            "目标媒介": media_plan.target_media,
            "内容结构": media_plan.structure_type,
            "状态": media_plan.status,
            "下一个Skill": media_plan.next_adapter,
            "创建时间": media_plan.created_at,
        }
    )
```

### 与下游 Skill 的集成

每个 Media Plan 包含 `next_adapter` 字段，指向下一个处理 Skill：

```
media_plan (status=planned)
  ├─ article_wechat → wechat-topic-outline-planner
  ├─ video_script → video-script-generator
  ├─ image_post → image-post-planner
  ├─ newsletter → newsletter-generator
  ├─ short_video → short-video-generator
  ├─ slide_deck → slide-deck-generator
  └─ podcast_script → podcast-script-generator
```

## 版本历史

### v2.0 (2026-03-15)
- ✅ 支持批量生成所有推荐媒介的 Media Plan
- ✅ 引入媒介适配器（media_type_adapter.py）
- ✅ 媒介特定的 structure_type 和大纲框架
- ✅ 媒介特定的 Hook 和 CTA 生成
- ✅ 完整的生产参数映射

### v1.0 (2026-03-14)
- 仅为第一个推荐媒介生成 Media Plan
- 通用的大纲框架
- 硬编码的 structure_type
