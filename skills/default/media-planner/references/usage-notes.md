# media-planner references

## 1. 输入模板

```yaml
brief:
material_pack:
target_media:
style_preference:
platform_constraints:
operator_note:
```

## 2. 输出模板（Media Plan）

```yaml
media_plan_id:
brief_ref:
material_pack_ref:
created_at:

target_media:
planning_summary:
structure_recommendation:
section_plan:
asset_usage_plan:
platform_constraints:
style_notes:
next_adapter:
```

## 3. 路由原则

- article_wechat → wechat-topic-outline-planner / wechat-draft-writer / wechat-title-generator
- video_script → 后续视频脚本 skill
- image_post → 后续图文 skill

## 4. 与旧链路衔接

- 旧 wechat-topic-outline-planner 从“全局 planner”降级为 article_wechat 适配器
- media-planner 才是跨媒介分流点

## 5. Feishu 落库建议

- 每个 Media Plan 单独一篇 Feishu Doc
- 标题建议：`[Media Plan] {brief primary topic} / {target_media}`
- Bitable 索引字段：
  - media_plan_id
  - brief_ref
  - target_media
  - next_adapter
  - status
  - doc_url
```
