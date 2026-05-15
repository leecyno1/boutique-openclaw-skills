# dasheng-daily-phase2 使用指南

## 1. 功能定位
- 大圣自媒体工作流第二环节技能。接收 `dasheng-daily-intake` 底稿（intake-records 或 dasheng_v11 输出），执行 v8 语义聚类并产出 8~10 个可执行详细 Brief。用于“进入第二环节”“生成详细 Brief”“给下一阶段选题包（含衍生话题与大纲）”场景。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/dasheng-daily-phase2`
- 安装后目录: `~/.openclaw/skills/dasheng-daily-phase2`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 dasheng-daily-phase2 帮我处理当前任务。
- 如果 dasheng-daily-phase2 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/dasheng-daily-phase2
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
