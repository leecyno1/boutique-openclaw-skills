---
name: dasheng-xuanti
description: 内容采集适配器 Skill。用于从多平台采集热点内容、新闻、公众号文章与群分享链接，完成初步评分、归一化和候选主题整理，输出 Topic Intake Record，供 `content-intake-hub` 与 `content-brief-builder` 继续处理。
---

# Dasheng Xuanti - v2 契约版本

## 新定位

本 Skill 不再作为全链路内容中枢。

它的职责被收敛为：
- 多源内容采集
- 初步清洗、去重、评分
- 候选主题归一化
- 输出标准化上游对象：**Topic Intake Record**

它不再负责：
- 最终选题定稿
- 最终大纲生成
- 最终媒介路由
- 把"高分主题"直接当成最终内容任务单

---

## 目标

为 Content Workflow v2 提供稳定的自动采集上游供给层。

最终输出应进入：
- `content-intake-hub`
- 或直接供 `content-brief-builder` 消费

---

## 支持的数据源

### 1. 自媒体数据（MediaCrawler MCP - 端口 18081）
- 小红书 `xhs`
- 抖音 `douyin`
- B站 `bili`
- 微博 `wb`
- X/Twitter `x`

### 2. 新闻舆情（TrendRadar MCP）
- 最新新闻
- 热点趋势
- 关键词搜索

### 3. 公众号内容（WeMP RSS MCP）
- 订阅文章列表
- 文章详情

### 4. 飞书群聊分享
- 最近 24 小时的群分享链接

### 5. 网络热点搜索
- 使用 `web_search` 辅助分析评论与情绪

---

## v2 输入契约

### 标准输入对象：Collection Request

```yaml
collection_request:
  request_id: string                    # 唯一请求 ID，格式：dasheng-{timestamp}-{uuid}
  source_channels:                      # 采集源列表
    - channel: "xhs" | "douyin" | "bili" | "wb" | "x" | "news" | "wechat" | "feishu"
      enabled: boolean
      keywords: [string]                # 可选，��对该源的关键词
      time_range_hours: number          # 可选，默认 24
  collection_mode: "auto" | "manual"    # auto=定时采集，manual=按需采集
  priority_level: "high" | "normal" | "low"
  target_media: "article_wechat" | "article_xiaohongshu" | "video_douyin" | "all"
  operator_note: string                 # 可选，采集背景说明
  created_at: timestamp
```

---

## v2 输出契约

### 输出对象：Topic Intake Record（标准化主题记录）

本 Skill 的主要输出是 **Topic Intake Record**，这是内容中台的统一入口对象。

#### 完整字段定义

```yaml
topic_intake_record:
  # ============ 标识字段 ============
  intake_id: string                     # 格式：intake-{YYYYMMDD-HHMMSS}-{uuid}
  topic_id: string                      # 主题唯一标识，格式：topic-{hash}，用于去重
  
  # ============ 来源信息 ============
  source_mode: "auto" | "manual"        # auto=自动采集，manual=人工输入
  source_channel: string                # 采集源：xhs|douyin|bili|wb|x|news|wechat|feishu
  source_ref:
    url: string                         # 原始链接
    platform_id: string                 # 平台内容 ID（从 URL 提取）
    author: string                      # 原作者/账号
    published_at: string                # 发布时间（ISO 8601）
  
  # ============ 内容规范化 ============
  normalized_topic: string              # 规范化主题名（50-100 字）
  normalized_summary: string            # 规范化摘要（100-200 字）
  problem_statement: string             # 问题陈述：这个主题解决什么问题？
  media_intent: string                  # 媒介意图：适合什么媒介形式？
  
  # ============ Brief 候选字段 ============
  brief_candidate:
    core_judgment: string               # 核心判断（一句话观点）
    target_audience: string             # 目标读者
    article_goal: string                # 文章目标（增长/认知/转化等）
  
  # ============ 评分与优先级 ============
  priority: number                      # 优先级评分 0-100
  scoring_breakdown:
    platform_score: number              # 平台热度评分（基于互动数据）
    relevance_score: number             # 相关性评分（基于关键词匹配）
    freshness_score: number             # 时效性评分（基于发布时间）
    quality_score: number               # 内容质量评分（基于平台评级）
  
  # ============ 素材与证据 ============
  existing_assets:
    has_reference_material: boolean     # 是否有可复用素材
    material_summary: string            # 可复用素材线索
    evidence_hints: [string]            # 证据线索列表
  
  # ============ 元数据 ============
  operator_note: string                 # 可选，操作员备注
  next_step: string                     # 下一步：content-brief-builder|manual_review|archived
  created_at: string                    # 创建时间（ISO 8601）
  updated_at: string                    # 更新时间（ISO 8601）
```

#### 字段映射规则

| dasheng 字段 | Intake Record 字段 | 转换逻辑 |
|-------------|------------------|--------|
| `platform` | `source_channel` | 平台名映射为标准代码（xhs/douyin/bili/wb/x/news/wechat） |
| `url` | `source_ref.url` | 直接复制 |
| `title` | `normalized_topic` | 清理特殊字符，保留原意 |
| `create_time` | `source_ref.published_at` | 转换为 ISO 8601 格式 |
| `score` | `priority` | 基于 dasheng 评分和其他因素重新计算 |
| `rating` | `scoring_breakdown.quality_score` | A→85, B→60, C→35, S→95 |
| `like_count` | 计入 `platform_score` | 权重 25% |
| `collect_count` | 计入 `platform_score` | 权重 35% |
| `share_count` | 计入 `platform_score` | 权重 25% |
| `comment_count` | 计入 `platform_score` | 权重 25% |

#### 优先级与下一步处理

- **priority >= 70**：高优先级，自动进入 `content-brief-builder`
- **50 <= priority < 70**：中优先级，进入 `content-brief-builder`
- **priority < 50**：低优先级，标记为 `manual_review`

#### 完整示例

```json
{
  "intake_id": "intake-20260315-123816-5f73858d-aab8-4363-91b3-4f827f9673eb",
  "topic_id": "topic-24f84cb17143",
  "source_mode": "auto",
  "source_channel": "douyin",
  "source_ref": {
    "url": "https://www.douyin.com/video/7414903239449054499",
    "platform_id": "7414903239449054499",
    "author": "内容创作者",
    "published_at": "2024-09-16T00:12:02Z"
  },
  "normalized_topic": "市场同质化严重，产品该如何突围？卖情绪价值",
  "normalized_summary": "市场同质化严重，产品该如何突围？被卖产品，卖情绪价值！在这个焦虑的时代，人们更愿意为情绪买单，有情怀、有共鸣、有情感寄托的产品不仅仅是具备了实用功能，更具备内核价值。",
  "problem_statement": "读者需要了解：如何通过情绪价值实现产品差异化",
  "media_intent": "短视频脚本、抖音文案、微信视频号",
  "brief_candidate": {
    "core_judgment": "在同质化市场中，卖情绪价值比卖产品功能更有竞争力",
    "target_audience": "产品经理、营销人员、创业者",
    "article_goal": "转化"
  },
  "priority": 86,
  "scoring_breakdown": {
    "platform_score": 100,
    "relevance_score": 100,
    "freshness_score": 50,
    "quality_score": 95
  },
  "existing_assets": {
    "has_reference_material": true,
    "material_summary": "原始链接包含完整案例和观点",
    "evidence_hints": ["情绪价值", "产品差异化", "市场同质化"]
  },
  "operator_note": "自动采集自抖音，原始评分 90.18",
  "next_step": "content-brief-builder",
  "created_at": "2026-03-15T12:38:16Z",
  "updated_at": "2026-03-15T12:38:16Z"
}
```

---

## 适配脚本

为了将 dasheng 采集结果自动转换为 Topic Intake Record，提供了专用的适配脚本。

### 脚本位置

`scripts/dasheng_to_intake_adapter.py`

### 使用方法

```bash
python scripts/dasheng_to_intake_adapter.py <input_json> [output_json]
```

### 示例

```bash
# 转换 dasheng 采集结果
python scripts/dasheng_to_intake_adapter.py dasheng_output.json intake_records.json

# 输出示例
=== 转换统计 ===
输入: 1000 条
输出: 994 条
去重: 6 条
错误: 0 条

优先级分布:
  高 (>=70): 172
  中 (50-70): 217
  低 (<50): 605

下一步处理:
  content-brief-builder: 389
  manual_review: 605
```

### 脚本功能

1. **字段映射**：自动将 dasheng 字段映射到 Topic Intake Record 标准字段
2. **去重**：基于 `topic_id`（platform + url 的 hash）去除重复项
3. **评分计算**：
   - 平台热度评分：基于互动数据（收藏×35% + 分享×25% + 互动×25% + 时效×15%）
   - 相关性评分：基于 dasheng 原始评分
   - 时效性评分：基于发布时间与当前时间的差距
   - 质量评分：基于 dasheng 的 rating（A/B/C/S）
4. **优先级计算**：加权平均（平台×35% + 相关×25% + 时效×25% + 质量×15%）
5. **验证**：检查所有必填字段和格式
6. **统计**：生成详细的转换统计报告

### 输出格式

脚本输出 JSON 文件，包含：

```json
{
  "timestamp": "2026-03-15T12:38:16Z",
  "total_input": 1000,
  "total_output": 994,
  "duplicates_removed": 6,
  "validation_errors": 0,
  "records": [
    { /* Topic Intake Record */ },
    ...
  ],
  "errors": [],
  "stats": {
    "by_source_channel": { "xhs": 100, "douyin": 100, ... },
    "by_priority_level": { "high": 172, "medium": 217, "low": 605 },
    "by_next_step": { "content-brief-builder": 389, "manual_review": 605 }
  }
}
```

---

## 与 Bitable 集成

### 推荐的 Bitable 配置

```
表名：Topic Intake Records
字段：
  - intake_id (文本，主键)
  - topic_id (文本，用于去重)
  - source_channel (单选：xhs/douyin/bili/wb/x/news/wechat)
  - topic (文本，100字)
  - summary (长文本，200字)
  - priority (数字，0-100)
  - source_url (URL)
  - published_at (日期时间)
  - next_step (单选：content-brief-builder/manual_review/archived)
  - created_at (日期时间)
  - updated_at (日期时间)
```

### 字段映射

| Topic Intake Record 字段 | Bitable 字段 | 类型 | 说明 |
|------------------------|------------|------|------|
| `intake_id` | intake_id | 文本 | 唯一标识 |
| `topic_id` | topic_id | 文本 | 去重用 |
| `source_channel` | source_channel | 单选 | xhs/douyin/bili/wb/x/news/wechat |
| `normalized_topic` | topic | 文本 | 主题名 |
| `normalized_summary` | summary | 长文本 | 摘要 |
| `priority` | priority | 数字 | 优先级 0-100 |
| `source_ref.url` | source_url | URL | 原始链接 |
| `source_ref.published_at` | published_at | 日期时间 | 发布时间 |
| `next_step` | next_step | 单选 | content-brief-builder/manual_review |
| `created_at` | created_at | 日期时间 | 创建时间 |

---

## 工作流集成

### 完整流程

```
dasheng-xuanti 采集
    ↓
dasheng_to_intake_adapter.py 转换
    ↓
Topic Intake Record 输出
    ↓
写入 Bitable（可选）
    ↓
content-brief-builder 消费
    ↓
Content Brief 生成
```

### 使用场景

**场景 1：自动采集流程**
```
定时任务 → dasheng-xuanti 采集 → 适配脚本转换 → 写入 Bitable → Brief 构建
```

**场景 2：手工指定主题**
```
用户输入 → 手工创建 Topic Intake Record → 直接进入 Brief 构建
```

**场景 3：批量审核**
```
dasheng 采集 → 适配脚本转换 → Bitable 审核 → 标记为 content-brief-builder → Brief 构建
```

---

## 与旧链路的迁移关系

### 旧链路
采集 → 评分 → 最终选题 → 飞书表格

### 新链路
采集 → 评分 → intake record → brief-builder → material → media

迁移原则：
- 保留采集能力
- 保留评分能力
- 剥离最终策划职责
- 剥离最终输出职责

---

## 边界

- 不直接写公众号大纲
- 不直接写初稿
- 不直接生成标题
- 不直接把表格中的一行当作最终内容对象

---

## 飞书落库建议

- 原始采集数据：本地 JSON / 调试快照
- 正式内容对象：交给 Brief Doc + Bitable Index
- 本 Skill 若写表格，仅可写"采集快照 / 候选池"，不作为最终任务单主存储

---

## 参考

- `docs/content-workflow-v2.md`
- `docs/content-migration-roadmap-v1.md`
- `docs/task001-task003-integration-v1.md`
- `docs/task001-intake-mapping-v1.md`
- `docs/topic-intake-record-schema-v1.md`
- `skills/content-intake-hub/references/usage-notes.md`
