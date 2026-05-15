---
name: content-brief-builder
description: 内容中台核心 Skill。用于把自动采集结果聚类归并，或把人工命题结构化整理，生成统一的 Content Brief。适用于话题策划、内容任务单生成、推荐媒介判断、生产价值评分，以及将 Brief 写入飞书文档。
---

# Content Brief Builder

## 目标
将原始主题输入转化为可复用、可跨媒介消费的 Content Brief。

## 输入
1. Topic Intake Record
2. 可选的原始采集记录集合
3. 可选的账号定位 / 内容目标
4. 可选的人工补充说明

## 工作流
1. 若输入来自自动采集，先进行聚类、归并、去重。
2. 若输入来自人工命题，先整理主题、意图、受众、内容目标。
3. 统一提炼：主题定义、核心判断、核心冲突、角度候选、风险边界。
4. **动态风险评估**（已实现）：
   - 分析内容类型敏感性（教育/财务/医疗等 +20分）
   - 评估目标受众脆弱性（未成年人/特殊群体 +15分）
   - 检查媒介平台政策限制（+10分）
   - 识别声明中的绝对化表述（过度承诺/虚假宣传 +15分）
   - 评估数据证据质量（缺少证据/过时数据 +10分）
   - 生成动态 `risk_notes` 和改进建议
5. **动态计算 `production_value_score`**（新增，使用 `scoring_algorithm.py`）：
   - 基础分：50 分
   - 角度数量奖励：每个角度 +10 分（最多 +30）
   - 媒介数量奖励：每个媒介 +5 分（最多 +25）
   - 复杂度奖励：low +0, medium +10, high +15
   - 风险惩罚：low -0, medium -5, high -15
   - 目标受众奖励：每个受众 +3 分（最多 +15）
   - 最终评分范围：0-100
6. 给出推荐媒介类型：文章、视频、图文或混合。
7. **初始化 `source_summary`**（已实现）
   - 自动采集模式：从 intake_refs 提取来源分布
   - 人工命题模式：初始化为 `{ "manual_input": 1 }` + 生成 manual_ref_id
8. 生成 Content Brief，并建议写入飞书文档保存为长期资产。

## 输出契约
1. `Brief Summary`
2. `Angle Candidates`
3. `Recommended Angle`
4. `Production Value Score`（动态计算，0-100）
5. `Recommended Media`
6. `Risk Assessment`（包含 risk_notes 和改进建议）
7. `Content Brief`（含完整的 source_summary）
8. `Next Recommended Step`

## 生产价值评分算法

### 评分公式

```
最终评分 = 基础分 + 角度奖励 + 媒介奖励 + 复杂度奖励 + 受众奖励 - 风险惩罚
```

### 评分组件详解

| 组件 | 基础值 | 规则 | 最大值 |
|------|-------|------|-------|
| 基础分 | 50 | 固定 | 50 |
| 角度奖励 | - | 每个角度 +10 | +30 |
| 媒介奖励 | - | 每个媒介 +5 | +25 |
| 复杂度奖励 | - | low +0, medium +10, high +15 | +15 |
| 受众奖励 | - | 每个受众 +3 | +15 |
| 风险惩罚 | - | low -0, medium -5, high -15 | -15 |

### 评分示例

**低复杂度内容**（1 角度，1 媒介，低风险，1 受众）
```
50 + 10 + 5 + 0 + 3 - 0 = 68/100
```

**高复杂度内容**（3 角度，3 媒介，高风险，3 受众）
```
50 + 30 + 15 + 15 + 9 - 15 = 104 → 100/100（截断）
```

## source_summary 初始化规则

### 自动采集模式（source_mode: 'auto'）
```yaml
source_summary:
  source_distribution:
    xhs: 2          # 来自小红书的采集数
    weibo: 1        # 来自微博的采集数
    ...
  representative_sources:
    - "https://www.xiaohongshu.com/explore/..."
    - "https://weibo.com/..."
```

### 人工命题模式（source_mode: 'manual'）
```yaml
source_summary:
  source_distribution:
    manual_input: 1
  representative_sources:
    - "manual_topic_20260315_001"  # 格式：manual_topic_YYYYMMDD_XXX
```

## 人工命题后续补充流程

用户可通过以下方式补充真实来源：

1. **Web Search Integration**
   - 调用 web_search 自动补充相关来源
   - 更新 source_distribution 和 representative_sources

2. **Manual Source Addition**
   - 提供接口让用户添加真实 URL
   - 支持批量导入来源列表

3. **Source Verification**
   - 验证来源的有效性和相关性
   - 更新 Brief 的 source_summary

## 边界
- 不直接补全全部素材
- 不直接写完整大纲
- 不直接生成正文
- source_summary 初始化后，用户可自主补充真实来源

## 集成指南

### Python 集成

```python
from scoring_algorithm import ProductionValueScorer, calculate_production_value_score

# 方式 1: 使用便捷函数
brief = {
    'angle_candidates': [...],
    'recommended_media': [...],
    'complexity': 'high',
    'risk_level': 'medium',
    'target_audience': [...],
}
score = calculate_production_value_score(brief)

# 方式 2: 使用 Scorer 类获取详细信息
scorer = ProductionValueScorer()
breakdown = scorer.score_from_brief(brief)
print(f"评分: {breakdown.final_score}")
print(f"详细: {breakdown.to_dict()}")
```

### 集成到 Brief 生成流程

1. 在 Brief 生成完成后，调用 `calculate_production_value_score(brief)`
2. 将返回的评分赋值给 `brief['production_value_score']`
3. 将 Brief 写入飞书文档时，包含该评分

## 参考
- `docs/content-brief-schema-v2.md`
- `docs/content-workflow-v2.md`
- `scoring_algorithm.py` - 生产价值评分算法实现
- `SCORING_TEST_REPORT.md` - 评分算法测试报告
- `risk_assessment_algorithm.py` - 风险评估算法实现
- `TEST_REPORT.md` - 风险评估测试报告
