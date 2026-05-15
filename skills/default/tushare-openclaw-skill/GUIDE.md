# tushare-openclaw-skill 使用指南

## 1. 功能定位
- Tushare Pro 金融数据 API 查询助手。用于帮助用户查询中国股票、基金、期货、债券等金融数据。当用户需要获取股票行情、财务数据、基础信息、宏观经济数据时使用此 skill。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/tushare-openclaw-skill`
- 安装后目录: `~/.openclaw/skills/tushare-openclaw-skill`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 tushare-openclaw-skill 帮我处理当前任务。
- 如果 tushare-openclaw-skill 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/tushare-openclaw-skill
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
