# dasheng-daily-draft 使用指南

## 1. 功能定位
- 大圣自媒体工作流初稿环节。接收已确认选题与大纲，按冻结标准生成可发布级公众号长稿。用于“进入初稿环节”“生成初稿”“写3篇长文（含数据/表格/来源）”等场景；默认执行 draft-standard-v2（每篇 >=5000 字，标准文章语体，不注入风格 DNA，证据仅来自底稿链接素材或外部公开数据源）。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/dasheng-daily-draft`
- 安装后目录: `~/.openclaw/skills/dasheng-daily-draft`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 dasheng-daily-draft 帮我处理当前任务。
- 如果 dasheng-daily-draft 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/dasheng-daily-draft
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
