# xiaohongshu-ops 使用指南

## 1. 功能定位
- 小红书相关操作，覆盖账号定位、选题研究、内容生产、发布执行与复盘修复的小红书全链路运营技能。凡是小红书的浏览/搜索/发布/评论任务，默认必须使用 OpenClaw 内置浏览器流程并指定 profile=\"openclaw\"；除非用户明确要求，否则不要使用系统 open 或外部浏览器。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/xiaohongshu-ops`
- 安装后目录: `~/.openclaw/skills/xiaohongshu-ops`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 xiaohongshu-ops 帮我处理当前任务。
- 如果 xiaohongshu-ops 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/xiaohongshu-ops
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
