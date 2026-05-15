# Media Planner v2.0 - 快速参考

**版本**: v2.0 (批量生成)  
**日期**: 2026-03-15  
**状态**: ✅ 已验证

---

## 核心改进一览

| 维度 | v1.0 | v2.0 |
|------|------|------|
| 生成范围 | 仅第一个媒介 | **所有推荐媒介** ✅ |
| 输出数量 | 1 个 Media Plan | **N 个 Media Plan** ✅ |
| 媒介适配 | 硬编码 | **媒介适配器** ✅ |
| structure_type | 固定 | **动态选择** ✅ |
| 大纲框架 | 通用 | **媒介特定** ✅ |
| 生产参数 | 基础 | **完整媒介特定** ✅ |

---

## 支持的媒介类型

```
✅ article_wechat      → argumentative/narrative
✅ video_script        → narrative/interview
✅ image_post          → comparative/data_driven
✅ newsletter          → mixed
✅ short_video         → narrative/instructional
✅ slide_deck          → instructional/data_driven
✅ podcast_script      → narrative/interview
```

---

## 使用流程

### 输入
```json
{
  "brief": {
    "recommended_media": ["article_wechat", "video_script", "image_post"]
  }
}
```

### 处理
```
遍历 recommended_media
  ├─ 获取媒介配置
  ├─ 确定 structure_type
  ├─ 生成媒介特定大纲
  └─ 生成 Media Plan
```

### 输出
```json
{
  "media_plans": [
    { "target_media": "article_wechat", "structure_type": "argumentative" },
    { "target_media": "video_script", "structure_type": "narrative" },
    { "target_media": "image_post", "structure_type": "comparative" }
  ]
}
```

---

## 媒介特定的大纲框架

### article_wechat (5段)
```
1️⃣ 开篇：建立共鸣 (300-400字)
2️⃣ 核心论证：阐述观点 (800-1000字)
3️⃣ 深度分析：提供洞察 (600-800字)
4️⃣ 行���指南：提供建议 (400-500字)
5️⃣ 结尾：强化观点 (200-300字)
```

### video_script (5段)
```
1️⃣ 开场 Hook (30-60秒)
2️⃣ 背景介绍 (1-2分钟)
3️⃣ 核心内容 (4-5分钟)
4️⃣ 互动环节 (1-2分钟)
5️⃣ 结尾 CTA (30-60秒)
```

### image_post (5段)
```
1️⃣ 封面图 + 标题 (20-30字)
2️⃣ 问题陈述 (50-80字)
3️⃣ 对比/数据展示 (配图为主)
4️⃣ 核心观点 (50-80字)
5️⃣ 行动号召 (30-50字)
```

### newsletter (4段)
```
1️⃣ 主题行 + 摘要 (主题行50字，摘要100字)
2️⃣ 核心内容 (400-600字)
3️⃣ 推荐阅读 (3-5个推荐)
4️⃣ 行动号召 (2个CTA按钮)
```

### short_video (3段)
```
1️⃣ Hook (3秒)
2️⃣ 核心内容 (20-40秒)
3️��� 结尾 (10-20秒)
```

### slide_deck (5段)
```
1️⃣ 标题页 (1张)
2️⃣ 问题陈述 (2-3张)
3️⃣ 核心内容 (8-10张)
4️⃣ 行动方案 (3-4张)
5️⃣ 结尾页 (1张)
```

### podcast_script (5段)
```
1️⃣ 开场 (1分钟)
2️⃣ 背景介绍 (3-5分钟)
3️⃣ 核心讨论 (12-18分钟)
4️⃣ 听众互动 (2-3分钟)
5️⃣ 结尾 (1分钟)
```

---

## 生产参数速查表

| 媒介 | 字数/时长 | 配图/场景 | 其他 |
|-----|---------|---------|------|
| article_wechat | 1500-2500字 | 3张 | 8-10分钟阅读 |
| video_script | 8-10分钟 | 5场景 | 需字幕 |
| image_post | 200-400字 | 5张 | 5个标签 |
| newsletter | 800-1200字 | 2张 | 2个CTA |
| short_video | 30-60秒 | 3场景 | 快节奏 |
| slide_deck | 15-20张 | 10张 | 3个图表 |
| podcast_script | 20-30分钟 | - | 4段 |

---

## 下一个 Skill 路由

```
article_wechat    → wechat-topic-outline-planner
video_script      → video-script-generator
image_post        → image-post-planner
newsletter        → newsletter-generator
short_video       → short-video-generator
slide_deck        → slide-deck-generator
podcast_script    → podcast-script-generator
```

---

## 测试场景

### 场景 1: 三媒介 ✅
```
输入: [article_wechat, video_script, image_post]
输出: 3 个 Media Plan
耗时: <100ms
```

### 场景 2: 四媒介 ✅
```
输入: [article_wechat, video_script, image_post, newsletter]
输出: 4 个 Media Plan
耗时: <150ms
```

### 场景 3: 七媒介 ✅
```
输入: [article_wechat, video_script, image_post, newsletter, short_video, slide_deck, podcast_script]
输出: 7 个 Media Plan
耗时: <250ms
```

---

## 性能指标

- **平均单个**: <40ms
- **3 媒介**: <100ms
- **7 媒介**: <250ms
- **可扩展性**: 线性增长

---

## 文件清单

```
skills/media-planner/
├── SKILL.md                    (更新为 v2.0)
├── media_type_adapter.py       (新增 - 19.8 KB)
├── TEST_REPORT.md              (新增 - 完整测试)
├── IMPLEMENTATION_GUIDE.md     (新增 - 集成指南)
├── QUICK_REFERENCE.md          (本文件)
└── references/
    └── usage-notes.md          (保持不变)
```

---

## 集成检查清单

- [ ] 部署 media_type_adapter.py
- [ ] 更新 media-planner 核心逻辑为批量生成
- [ ] 更新 Feishu 写入支持多个 Media Plan
- [ ] 更新工作流路由
- [ ] 运行测试验证
- [ ] 性能测试通过
- [ ] 文档更新完成

---

## 常见问题

**Q: 如果 Brief 没有推荐媒介？**  
A: 返回错误，提示需要指定推荐媒介

**Q: 如果推荐了���支持的媒介？**  
A: 跳过不支持的媒介，仅为支持的媒介生成

**Q: 如何添加新媒介？**  
A: 在 media_type_adapter.py 中添加新配置

**Q: 性能如何？**  
A: 平均 <40ms/个，支持 7+ 媒介

---

## 验收标准

✅ Brief 的所有推荐媒介都能生成对应的 Media Plan  
✅ 每个 Media Plan 的 structure_type 根据媒介类型调整  
✅ 每个 Media Plan 的大纲框架是媒介特定的  
✅ 所有生产参数完整且媒介特定  
✅ 性能满足要求  
✅ 数据完整性验证通过  

---

## 下一步

1. 集成到生产环境
2. 监控性能和质量
3. 收集用户反馈
4. 持续优化

---

**状态**: ✅ 已验证，可集成  
**版本**: v2.0  
**日期**: 2026-03-15
