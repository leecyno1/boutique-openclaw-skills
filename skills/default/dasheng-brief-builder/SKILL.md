---
name: dasheng-brief-builder
description: 内容 Brief 生成 Skill。用于将 Topic Cluster 或单条 Topic Intake Record 转化为可复用、可跨媒介消费的 Content Brief。包含风险评估、生产价值评分、媒介推荐等功能。
---

# Dasheng Brief Builder - Brief 生成层 v3

## 定位

本 Skill 职责单一：**Topic Cluster/Intake Record → Content Brief**

不负责：
- 采集
- 聚类
- 最终选题定稿
- 素材补全
- 初稿生成

---

## 输入契约

### Brief Request

```yaml
brief_request:
  request_id: string                    # 格式：brief-{timestamp}-{uuid}
  input_type: "cluster" | "intake"      # 输入类型
  input_data: Topic Cluster | Topic Intake Record
  account_positioning: string           # 可选，账号定位
  content_goal: string                  # 可选，内容目标
  created_at: timestamp
```

---

## 输出契约

### Content Brief（内容 Brief）

```yaml
content_brief:
  # ============ 标识字段 ============
  brief_id: string                      # 格式：brief-{YYYYMMDD-HHMMSS}-{uuid}
  
  # ============ 话题信息 ============
  topic_name: string                    # 话题名称
  core_judgment: string                 # 核心判断（一句话观点）
  
  # ============ 内容策略 ============
  target_audience: string               # 目标受众
  article_goal: string                  # 文章目标（增长/认知/转化等）
  angle_candidates: [string]            # 可写角度（3-5 个）
  recommended_angle: string             # 推荐角度
  
  # ============ 媒介推荐 ============
  recommended_media: [string]           # 推荐媒介（article/video/infographic/mixed）
  platform_adaptation:                  # 平台适配性
    douyin: "high" | "medium" | "low"
    xhs: "high" | "medium" | "low"
    bili: "high" | "medium" | "low"
    wb: "high" | "medium" | "low"
    x: "high" | "medium" | "low"
  
  # ============ 风险评估（简化版） ============
  risk_assessment:
    content_sensitivity: "low" | "medium" | "high"  # 内容敏感性
    evidence_quality: "low" | "medium" | "high"     # 证据质量
    platform_compliance: "low" | "medium" | "high"  # 平台合规性
    risk_notes: string                  # 风险说明
    improvement_suggestions: [string]   # 改进建议
  
  # ============ 生产价值评分（简化版） ============
  production_value_score: number        # 0-100
  score_breakdown:
    content_depth: number               # 内容深度（角度数量）
    media_diversity: number             # 媒介多样性
    audience_reach: number              # 受众覆盖面
  
  # ============ 来源信息 ============
  source_summary:
    source_mode: "auto" | "manual" | "clustered"
    cluster_id: string                  # 如果是聚类模式
    cluster_size: number                # 簇内 Intake Record 数量
    platform_distribution:              # 平台分布
      douyin: number
      xhs: number
      ...
    representative_sources:             # TOP 3 参考选题
      - intake_id: string
        url: string
        title: string
  
  # ============ 元数据 ============
  next_step: string                     # material-pack-builder|media-planner|archived
  created_at: string                    # 创建时间（ISO 8601）
```

---

## 风险评估（简化版）

### 3 个核心维度

#### 1. content_sensitivity（内容敏感性）
```
评估内容是否涉及敏感话题（财务建议、医疗建议等）

low：
  - 一般商业观察
  - 国际新闻评论
  - 技术趋势分析

medium：
  - 投资建议（但不涉及具体产品）
  - 政策解读
  - 经济分析

high：
  - 具体投资产品推荐
  - 医疗/健康建议
  - 法律建议
```

#### 2. evidence_quality（证据质量）
```
评估内容的数据和证据是否充分

low：
  - 缺少数据支撑
  - 数据过时（> 3 个月）
  - 来源不明确

medium：
  - 有部分数据支撑
  - 数据相对新鲜（1-3 个月）
  - 来源可追溯

high：
  - 充分的数据支撑
  - 数据最新（< 1 个月）
  - 来源权威可信
```

#### 3. platform_compliance（平台合规性）
```
评估内容是否符合平台政策

low：
  - 违反平台金融内容政策
  - 包含虚假宣传
  - 包含绝对化表述（必涨/必跌）

medium：
  - 需要添加免责声明
  - 需要标注信息来源
  - 需要避免某些表述

high：
  - 完全符合平台政策
  - 无需特殊处理
```

---

## 生产价值评分（简化版）

### 3 个核心维度

```
production_value_score = (
  content_depth * 0.4 +       # 内容深度（角度数量）
  media_diversity * 0.3 +     # 媒介多样性
  audience_reach * 0.3        # 受众覆盖面
)
```

#### content_depth（内容深度）
```
基于角度数量：
- 1 个角度：30 分
- 2 个角度：50 分
- 3 个角度：70 分
- 4 个角度：85 分
- 5+ 个角度：100 分
```

#### media_diversity（媒介多样性）
```
基于推荐媒介数量：
- 1 种媒介：30 分
- 2 种媒介：60 分
- 3+ 种媒介：100 分
```

#### audience_reach（受众覆盖面）
```
基于目标受众数量和平台适配性：
- 1 个受众，1 个平台：30 分
- 2 个受众，2 个平台：60 分
- 3+ 个受众，3+ 个平台：100 分
```

---

## 工作流

### 聚类模式（输入：Topic Cluster）
1. 接收 Topic Cluster
2. 提炼核心判断和目标受众
3. 生成可写角度（基于簇内 Intake Record 的多样性）
4. 推荐媒介（基于平台分布）
5. 执行风险评估
6. 计算生产价值评分
7. 生成 Content Brief

### 单条模式（输入：Topic Intake Record）
1. 接收 Topic Intake Record
2. 提炼核心判断和目标受众
3. 生成可写角度（基于 brief_hints）
4. 推荐媒介（基于 source_channel）
5. 执行风险评估
6. 计算生产价值评分
7. 生成 Content Brief

---

## 边界

- 不进行采集
- 不进行聚类
- 不直接补全素材
- 不直接生成初稿
- 不直接生成标题
- 不直接写飞书表格

---

## 参考

- `docs/content-workflow-v3.md`
- `scripts/risk_assessment.py` - 风险评估实现
- `scripts/production_value_scorer.py` - 生产价值评分实现
