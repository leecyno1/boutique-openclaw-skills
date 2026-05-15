# Media Planner 批量生成 - 实现指南

**版本**: v2.0  
**日期**: 2026-03-15  
**状态**: 已验证，可集成

---

## 概述

本指南说明如何将改造后的 media-planner（支持批量生成）集成到现有的内容中台工作流中。

## 核心改进

### 问题

当前 media-planner 只为 Brief 中的第一个推荐媒介生成 Media Plan，导致其他推荐媒介无法进入生产流程。

**示例**:
```
Brief 推荐媒介: [article_wechat, video_script, image_post]
当前生成: 仅 article_wechat 的 Media Plan
缺失: video_script 和 image_post 的 Media Plan
```

### 解决方案

改造 media-planner，使其能够：
1. 遍历 Brief 中的所有推荐媒介
2. 为每个媒介生成对应的 Media Plan
3. 每个 Media Plan 的 structure_type 根据媒介类型调整
4. 每个 Media Plan 的大纲框架是媒介特定的

**改进后**:
```
Brief 推荐媒介: [article_wechat, video_script, image_post]
改造后生成: 3 个 Media Plan
  ├─ article_wechat (structure_type: argumentative)
  ├─ video_script (structure_type: narrative)
  └─ image_post (structure_type: comparative)
```

## 文件清单

### 新增文件

1. **media_type_adapter.py** (19.8 KB)
   - 媒介类型配置和适配逻辑
   - 支持 7 种媒介类型
   - 媒介特定的大纲框架生成

2. **SKILL.md** (已更新)
   - 更新为 v2.0 版本
   - 说明批量生成逻辑
   - 媒介适配表和参数映射

3. **TEST_REPORT.md** (新增)
   - 完整的测试验证报告
   - 3 个测试场景（3媒介、4媒介、7媒介）
   - 性能和数据完整性验证

### 修改文件

- `SKILL.md` - 更新为 v2.0，说明批量生成

## 集成步骤

### Step 1: 部署媒介适配器

将 `media_type_adapter.py` 部署到 media-planner skill 目录：

```bash
cp media_type_adapter.py /path/to/skills/media-planner/
```

### Step 2: 更新 media-planner 的核心逻辑

在 media-planner 的主处理函数中，修改为批量生成逻辑：

```python
from media_type_adapter import MediaTypeAdapter

def generate_media_plans(brief, material_pack):
    """
    为 Brief 的所有推荐媒介批量生成 Media Plan
    """
    media_plans = []
    
    # 遍历所有推荐媒介
    for media_type in brief.recommended_media:
        # 获取媒介配置
        config = MediaTypeAdapter.get_config(media_type)
        if not config:
            continue
        
        # 确定 structure_type
        structure_type = MediaTypeAdapter.adapt_structure_type(
            media_type=media_type,
            content_goals=brief.content_goals,
            core_claim=brief.core_claim
        )
        
        # 生成媒介特定的大纲
        outline = MediaTypeAdapter.generate_media_plan_outline(
            media_type=media_type,
            core_claim=brief.core_claim,
            content_goals=brief.content_goals
        )
        
        # 生成 Media Plan
        media_plan = {
            "media_plan_id": generate_media_plan_id(media_type),
            "brief_id": brief.brief_id,
            "target_media": media_type,
            "objective": infer_objective(brief.content_goals),
            "structure_type": structure_type,
            "outline": outline,
            "hook": generate_hook(media_type, brief),
            "cta": generate_cta(media_type, brief),
            "production_notes": config.production_params,
            "next_adapter": config.next_adapter,
            "status": "planned",
            "created_at": datetime.now().isoformat()
        }
        
        media_plans.append(media_plan)
    
    return media_plans
```

### Step 3: 更新 Feishu 写入逻辑

修改 Feishu 写入，支持批量写入多个 Media Plan：

```python
def write_media_plans_to_feishu(media_plans, app_token, table_id):
    """
    将所有 Media Plan 写入 Feishu Bitable
    """
    for media_plan in media_plans:
        record = feishu_bitable.create_record(
            app_token=app_token,
            table_id=table_id,
            fields={
                "Media Plan ID": media_plan["media_plan_id"],
                "Brief ID": media_plan["brief_id"],
                "目标媒介": media_plan["target_media"],
                "内容结构": media_plan["structure_type"],
                "状态": media_plan["status"],
                "下一个Skill": media_plan["next_adapter"],
                "创建时间": media_plan["created_at"],
            }
        )
        print(f"✅ 已写入 {media_plan['target_media']} 的 Media Plan")
```

### Step 4: 更新工作流路由

在 content-workflow-v2 中，更新 media-planner 的输出路由：

```yaml
# 原来的路由（仅第一个媒介）
media-planner:
  input: brief + material_pack
  output: media_plan (单个)
  next: 
    - article_wechat → wechat-topic-outline-planner

# 改造后的路由（所有媒介）
media-planner:
  input: brief + material_pack
  output: media_plans (多个)
  next:
    - article_wechat → wechat-topic-outline-planner
    - video_script → video-script-generator
    - image_post → image-post-planner
    - newsletter → newsletter-generator
    - short_video → short-video-generator
    - slide_deck → slide-deck-generator
    - podcast_script → podcast-script-generator
```

### Step 5: 测试验证

运行测试报告中的 3 个场景，验证批量生成功能：

```bash
# 场景 1: 三媒介批量生成
python test_scenario_1.py

# 场景 2: 四媒介批量生成
python test_scenario_2.py

# 场景 3: 七媒介完整覆盖
python test_scenario_3.py
```

## 媒介适配表

### 支持的媒介类型

| 媒介类型 | 主要结构 | 次要结构 | 下一个 Skill | 生产参数 |
|---------|--------|--------|------------|--------|
| article_wechat | argumentative | narrative | wechat-topic-outline-planner | 1500-2500字，3张图 |
| video_script | narrative | interview | video-script-generator | 8-10分钟，5场景 |
| image_post | comparative | data_driven | image-post-planner | 5张图，200-400字 |
| newsletter | mixed | narrative | newsletter-generator | 800-1200字，2个CTA |
| short_video | narrative | instructional | short-video-generator | 30-60秒，3场景 |
| slide_deck | instructional | data_driven | slide-deck-generator | 15-20张，10张图 |
| podcast_script | narrative | interview | podcast-script-generator | 20-30分钟，4段 |

### 媒介特定的大纲框架

#### article_wechat (5段)
1. 开篇：建立共鸣
2. 核心论证：阐述观点
3. 深度分析：提供洞察
4. 行动指南：提供建议
5. 结尾：强化观点

#### video_script (5段)
1. 开场（Hook）：吸引观众
2. 背景介绍：提供上下文
3. 核心内容：传递信息
4. 互动环节：增加参与感
5. 结尾（CTA）：行动号召

#### image_post (5段)
1. 封面图 + 标题：吸引点击
2. 问题陈述：建立共鸣
3. 对比/数据展示：提供证据
4. 核心观点：传递信息
5. 行动号召：驱动互动

#### newsletter (4段)
1. 主题行 + 摘要：吸引打开
2. 核心内容：传递信息
3. 推荐阅读：提供延伸
4. 行动号召：驱动转化

#### short_video (3段)
1. Hook（3秒）：停留用户
2. 核心内容（20-40秒）：传递信息
3. 结尾（10-20秒）：行动号召

#### slide_deck (5段)
1. 标题页：介绍主题
2. 问题陈述：建立背景
3. 核心内容：传递信息
4. 行动方案：提供建议
5. 结尾页：总结互动

#### podcast_script (5段)
1. 开场（1分钟）：欢迎听众
2. 背景介绍（3-5分钟）：提供上下文
3. 核心讨论（12-18分钟）：深度对话
4. 听众互动（2-3分钟）：回答问题
5. 结尾（1分钟）：总结告别

## 性能指标

### 批量生成性能

- **3 媒介**: <100ms
- **4 媒介**: <150ms
- **7 媒介**: <250ms
- **平均单个**: <40ms

### ��扩展性

- 支持最多 7 种媒介类型
- 可轻松扩展到更多媒介类型
- 性能线性增长

## 数据流示例

### 输入

```json
{
  "brief": {
    "brief_id": "brief-20260315-001",
    "working_title": "AI时代的职业转型指南",
    "core_claim": "AI不会替代人类，而是改变工作方式",
    "content_goals": ["增长", "认知"],
    "recommended_media": ["article_wechat", "video_script", "image_post"]
  },
  "material_pack": {
    "material_pack_id": "mp-pack-20260315-001",
    "resources": ["小红书原文", "行业报告"]
  }
}
```

### 处理流程

```
输入 Brief
  ↓
验证 recommended_media
  ↓
遍历媒介列表
  ├─ article_wechat
  │  ├─ 获取配置 (structure_type: argumentative)
  │  ├─ 生成大纲 (5段框架)
  │  └─ 生成 Media Plan
  ├─ video_script
  │  ├─ 获取配置 (structure_type: narrative)
  │  ├─ 生成大纲 (5段框架)
  │  └─ 生成 Media Plan
  └─ image_post
     ├─ 获取配置 (structure_type: comparative)
     ├─ 生成大纲 (5段框架)
     └─ 生成 Media Plan
  ↓
输出 3 个 Media Plan
  ↓
写入 Feishu Bitable
  ↓
路由到下游 Skill
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
      "next_adapter": "wechat-topic-outline-planner",
      "status": "planned"
    },
    {
      "media_plan_id": "mp-20260315-001-video_script",
      "target_media": "video_script",
      "structure_type": "narrative",
      "next_adapter": "video-script-generator",
      "status": "planned"
    },
    {
      "media_plan_id": "mp-20260315-001-image_post",
      "target_media": "image_post",
      "structure_type": "comparative",
      "next_adapter": "image-post-planner",
      "status": "planned"
    }
  ],
  "total_media_plans": 3
}
```

## 常见问题

### Q1: 如果 Brief 中没有推荐媒介怎么办？

**A**: 系统会返回错误，提示需要先在 Brief 中指定推荐媒介。

```python
if not brief.recommended_media:
    raise ValueError("Brief 必须包含至少一个推荐媒介")
```

### Q2: 如果推荐了不支持的媒介类型怎么办？

**A**: 系统会跳过不支持的媒介类型，仅为支��的媒介生成 Media Plan。

```python
for media_type in brief.recommended_media:
    config = MediaTypeAdapter.get_config(media_type)
    if not config:
        print(f"⚠️ 不支持的媒介类型: {media_type}，已跳过")
        continue
```

### Q3: 如何添加新的媒介类型？

**A**: 在 `media_type_adapter.py` 中添加新的媒介配置：

```python
MEDIA_CONFIGS["new_media_type"] = MediaTypeConfig(
    media_type=MediaType.NEW_MEDIA_TYPE,
    primary_structure_types=[...],
    secondary_structure_types=[...],
    production_params={...},
    next_adapter="new-adapter-skill",
    description="新媒介类型描述"
)
```

### Q4: 性能如何？能否支持更多媒介？

**A**: 当前性能满足要求，平均每个媒介 <40ms。理论上可支持 20+ 媒介，但建议保持在 7-10 个以内。

### Q5: 如何与现有的 wechat-topic-outline-planner 兼容？

**A**: 改造后的 media-planner 为 article_wechat 生成的 Media Plan 与现有的 wechat-topic-outline-planner 完全兼容，可以直接作为输入。

## 验收清单

- [ ] 部署 media_type_adapter.py
- [ ] 更新 media-planner 核心逻辑
- [ ] 更新 Feishu 写入逻辑
- [ ] 更新工作流路由
- [ ] 运行 3 个测试场景
- [ ] 验证所有 Media Plan 都正确生成
- [ ] 验证 Feishu Bitable 写入成功
- [ ] 验证下游 Skill 路由正确
- [ ] 性能测试通过
- [ ] 文档更新完成

## 下一步

1. **集成到生产环境**: 部署改造后的 media-planner
2. **监控和优化**: 监控批量生成的性能和质量
3. **用户反馈**: 收集实际使用中的反馈
4. **持续改进**: 根据反馈优化媒介适配逻辑
5. **扩展媒介**: 根据需求添加新的媒介类型

## 参考资源

- `media_type_adapter.py` - 媒介适配器实现
- `SKILL.md` - 更新后的 Skill 文档
- `TEST_REPORT.md` - 完整的测试验证报告
- `docs/media-plan-schema-v3.md` - Media Plan 数据结构
- `docs/content-workflow-v2.md` - 完整工作流

