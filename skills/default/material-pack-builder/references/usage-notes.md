# material-pack-builder references

## 1. 输入模板

```yaml
brief:
existing_assets:
target_media:
operator_note:
```

## 2. 输出模板（Material Pack）

```yaml
material_pack_id:
brief_ref:
created_at:

evidence_requirements:
text_sources:
image_sources:
video_sources:
quotes:
data_points:
evidence_gaps:
screenshot_tasks:
clip_tasks:
next_step: media-planner
```

## 3. 核心原则

- 先补齐证据，再进入最终媒介规划
- 文本、图片、视频分开组织
- 缺口明确写出，不要假装素材已经充分

## 4. 与旧链路衔接

- 旧写稿流程中临时找图、临时找数据的动作，前置到 Material Pack
- 素材来源与证据说明集中沉淀，不再散落在聊天里

## 5. Feishu 落库建议

- 每个 Material Pack 单独一篇 Feishu Doc
- 标题建议：`[Material Pack] {brief primary topic}`
- Bitable 索引字段：
  - material_pack_id
  - brief_ref
  - coverage_status
  - evidence_gap_count
  - doc_url
```
