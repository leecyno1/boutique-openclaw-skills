# content-brief-builder references

## 1. 输入模板

```yaml
intake_record:
raw_candidates:
account_positioning:
content_goal:
operator_note:
```

## 2. 输出模板（Content Brief）

```yaml
brief_id:
source_mode:
source_refs:
created_at:

primary_topic:
core_judgement:
core_conflict:
audience:
content_goal:
angle_candidates:
recommended_angle:
risk_boundary:
production_value_score:
recommended_media:
key_questions:
next_step: material-pack-builder
```

## 3. 判断准则

优先完成这几件事：
- 把主题说清楚
- 把为什么值得做说清楚
- 把最佳表达角度说清楚
- 把风险边界说清楚
- 把推荐媒介讲清楚

## 4. 与旧链路衔接

- 旧 dasheng 的“最终选题建议”迁移为 Brief 的 `recommended_angle + production_value_score`
- 旧 wechat planner 不再自己承担“是否值得写”的主判断

## 5. Feishu 落库建议

- 每个 Brief 单独一篇 Feishu Doc
- 标题建议：`[Brief] {primary_topic}`
- Bitable 只保留索引：
  - brief_id
  - primary_topic
  - recommended_media
  - production_value_score
  - status
  - doc_url
```
