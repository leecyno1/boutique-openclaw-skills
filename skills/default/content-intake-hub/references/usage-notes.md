# content-intake-hub references

## 1. 标准输入模板

```yaml
source_mode: auto | manual
source_channel:
source_ref:
created_at:
priority:

topic_seed:
summary:
media_intent:
existing_assets:
operator_note:
```

## 2. 标准输出模板（Topic Intake Record）

```yaml
intake_id:
source_mode:
source_channel:
source_ref:
created_at:

normalized_topic:
normalized_summary:
problem_statement:
intent_type:
media_intent:
priority:

candidate_brief_ref:
cluster_ref:
existing_assets:
operator_note:
next_step: content-brief-builder
```

## 3. 与旧链路衔接

- dasheng-xuanti 输出的热点/候选主题，先映射成 Topic Intake Record
- 人工在飞书/聊天中给出的选题想法，也统一落成 Topic Intake Record
- 后续一律不直接把“原始采集结果”喂给写稿 skill

## 4. Feishu 落库建议

- 主体内容：优先写入 Feishu Doc
- 索引字段：写入 Bitable
- Bitable 建议字段：
  - intake_id
  - source_mode
  - normalized_topic
  - media_intent
  - priority
  - brief_status
  - brief_doc_url
  - created_at
```
