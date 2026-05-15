# 大圣-选题工作流

## 概述
自动采集自媒体热门内容，生成选题建议，同步飞书表格。

## 数据源

### 1. 自媒体数据（端口 5173）
| 平台 | platform | 说明 |
|------|----------|------|
| 小红书 | `xhs` | 热门笔记 |
| 抖音 | `douyin` | 热门视频 |
| 微博 | `wb` | 热搜话题 |
| B站 | `bili` | 热门视频 |

### 2. 公众号（端口 8001）
- 需先登录：`/api/v1/wx/auth/login`
- 公众号列表：`/api/v1/wx/mps`

### 3. 飞书群
- 监控分享链接

## 工作流程

### 1. 数据采集
```python
# 拉取各平台数据
platforms = ["xhs", "douyin", "wb", "bili"]
for p in platforms:
    url = f"http://127.0.0.1:5173/api/data/latest?platform={p}&limit=300"
```

### 2. 筛选排序
- 按 `liked_count` 降序
- 筛选热度 > 1000

### 3. 生成选题
- 母题：高热度内容
- 子题：延伸角度（2-3个/母题）

### 4. 输出
- 写入飞书表格
- 关联源笔记链接

## 采集中间表字段
| 字段 | 说明 |
|------|------|
| 平台 | xhs/douyin/wb/bili |
| 标题 | 原始标题 |
| 热度 | liked_count |
| 作者 | author_name |
| 链接 | 原始URL |
| 采集时间 | fetched_at |

## 使用方法
```bash
# 手动执行
python3 /Users/lichengyin/clawd/scripts/dasheng_xuanti.py

# 定时任务（每天10:00）
crontab -l | grep dasheng
```
