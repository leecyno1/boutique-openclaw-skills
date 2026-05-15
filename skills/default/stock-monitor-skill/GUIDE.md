# Stock Monitor 使用指南

## 1. 功能定位
- 股票监控预警系统，支持成本线、均线、RSI、量能、跳空和动态止盈。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/stock-monitor-skill`
- 安装后目录: `~/.openclaw/skills/stock-monitor-skill`

## 2. 使用前准备
- 建议安装 `akshare` 与默认 Python 运行依赖

## 3. 配置步骤
1. 先根据 README/SKILL 配置监控标的。
2. 后台常驻可执行 `./control.sh start`。

## 4. 推荐提问方式
- 请用 stock-monitor-skill 配置 600519 的预警规则。
- 请用 stock-monitor-skill 启动后台监控并查看状态。

## 5. 手动验证
```bash
bash skills/default/stock-monitor-skill/scripts/control.sh status
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/stock-monitor-skill
- 本技能说明: `SKILL.md`
