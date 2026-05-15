# content-brief-builder 使用指南

## 1. 功能定位
- 内容中台核心 Skill。用于把自动采集结果聚类归并，或把人工命题结构化整理，生成统一的 Content Brief。适用于话题策划、内容任务单生成、推荐媒介判断、生产价值评分，以及将 Brief 写入飞书文档。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/content-brief-builder`
- 安装后目录: `~/.openclaw/skills/content-brief-builder`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 content-brief-builder 帮我处理当前任务。
- 如果 content-brief-builder 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/content-brief-builder
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
