---
name: dasheng-clustering
description: 内容聚类 Skill。用于将多条 Topic Intake Record 按真实话题进行聚类分析，识别主要话题簇（如美伊战争、康波周期等），输出 Topic Cluster，供 dasheng-brief-builder 生成 Content Brief。
---

# Dasheng Clustering - 聚类层 v1

## 定位

本 Skill 职责单一：**Topic Intake Record 聚类 → 识别真实话题簇**

不负责：
- 采集
- Brief 生成
- 最终选题定稿

---

## 输入契约

### Clustering Request

```yaml
clustering_request:
  request_id: string                    # 格式：cluster-{timestamp}-{uuid}
  intake_records: [Topic Intake Record] # 待聚类的 Intake Record 列表
  clustering_mode: "semantic" | "keyword"  # 聚类模式
  min_cluster_size: number              # 最小簇大小，默认 3
  max_clusters: number                  # 最大簇数，默认 20
  created_at: timestamp
```

---

## 输出契约

### Topic Cluster（话题簇）

```yaml
topic_cluster:
  # ============ 标识字段 ============
  cluster_id: string                    # 格式：cluster-{YYYYMMDD-HHMMSS}-{uuid}
  cluster_name: string                  # 真实话题名（美伊战争、康波周期等）
  
  # ============ 簇内容 ============
  intake_records: [Topic Intake Record] # 簇内所有 Intake Record
  cluster_size: number                  # 簇内 Intake Record 数量
  
  # ============ 簇级统计 ============
  cluster_stats:
    avg_priority: number                # 平均优先级
    platform_distribution:              # 平台分布
      douyin: number
      xhs: number
      bili: number
      wb: number
      x: number
    quality_breakdown:                  # 质量分布
      s_level: number                   # S 级数量
      a_level: number                   # A 级数量
      b_level: number                   # B 级数量
  
  # ============ 簇摘要 ============
  cluster_summary:
    core_topic: string                  # 核心话题（一句话）
    why_matters: string                 # 为什么这个话题值得写
    recommended_angles: [string]        # 推荐的写作角度（3-5 个）
  
  # ============ 元数据 ============
  created_at: string                    # 创建时间（ISO 8601）
```

---

## 聚类算法

### 算法流程

```
1. 关键词提取
   ├─ 从 normalized_topic 和 normalized_summary 提取关键词
   ├─ 使用 jieba 进行中文分词
   └─ 过滤停用词

2. 相似度计算
   ├─ 使用 TF-IDF 向量化
   ├─ 计算余弦相似度矩阵
   └─ 相似度阈值：0.6

3. 聚类方法
   ├─ 使用 DBSCAN（自动确定簇数）
   ├─ eps=0.4, min_samples=3
   └─ 或使用 K-Means（指定簇数）

4. 后处理
   ├─ 合并相似度 > 0.8 的小簇
   ├─ 删除大小 < min_cluster_size 的孤立簇
   └─ 为每个簇自动命名（基于高频关键词）

5. 簇验证
   ├─ 检查簇内相似度（应 > 0.6）
   ├─ 检查簇间相似度（应 < 0.4）
   └─ 输出聚类质量报告
```

### 簇自动命名规则

```
1. 提取簇内所有 Intake Record 的关键词
2. 计算关键词频率
3. 选择频率最高的 1-2 个关键词作为簇名
4. 如果关键词过于通用，使用人工定义的话题词典

示例：
- 关键词：伊朗、美国、战争、中东 → 簇名：美伊战争
- 关键词：康波、周期、财富、规律 → 簇名：康波周期
- 关键词：恒生、科技、下跌、投资 → 簇名：恒生科技
```

---

## 工作流

1. 接收 Clustering Request（包含 N 条 Intake Record）
2. 提取关键词
3. 计算相似度矩阵
4. 执行聚类算法
5. 后处理（合并、删除、命名）
6. 生成 Topic Cluster 列表
7. 输出到 dasheng-brief-builder

---

## 边界

- 不进行采集
- 不生成 Brief
- 不生成最终选题定稿
- 不直接写飞书表格

---

## 参考

- `docs/content-workflow-v3.md`
- `scripts/clustering_algorithm.py` - 聚类算法实现
- `scripts/topic_naming.py` - 簇自动命名实现
