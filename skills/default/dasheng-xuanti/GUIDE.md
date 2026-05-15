# dasheng-xuanti 使用指南

## 1. 功能定位
- 内容采集适配器 Skill。用于从多平台采集热点内容、新闻、公众号文章与群分享链接，完成初步评分、归一化和候选主题整理，输出 Topic Intake Record，供 `content-intake-hub` 与 `content-brief-builder` 继续处理。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/dasheng-xuanti`
- 安装后目录: `~/.openclaw/skills/dasheng-xuanti`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 dasheng-xuanti 帮我处理当前任务。
- 如果 dasheng-xuanti 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/dasheng-xuanti
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
