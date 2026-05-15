# dasheng-daily-material 使用指南

## 1. 功能定位
- 素材合并环节默认技能（material+补素材已合并）。用于在 dasheng 工作流中于 rewrite 之后统一补齐视频、图片、图表、CSV、引用与证据清单；支持通过 run_id 自动回溯 ContentBrief。适用于“改写后补素材”“补齐素材包并做审计”的场景。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/dasheng-daily-material`
- 安装后目录: `~/.openclaw/skills/dasheng-daily-material`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 dasheng-daily-material 帮我处理当前任务。
- 如果 dasheng-daily-material 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/dasheng-daily-material
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
