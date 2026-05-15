# Model Usage 使用指南

## 1. 功能定位
- 按模型维度统计 Codex / Claude 的成本使用情况。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/model-usage`
- 安装后目录: `~/.openclaw/skills/model-usage`

## 2. 使用前准备
- `codexbar` CLI（目前更偏 macOS）

## 3. 配置步骤
1. 先确认 `codexbar cost --format json` 能输出。
2. 再用脚本做按模型汇总。

## 4. 推荐提问方式
- 请用 model-usage 统计最近使用最贵的模型。
- 请用 model-usage 输出 codex provider 的全部模型费用。

## 5. 手动验证
```bash
python3 skills/default/model-usage/scripts/model_usage.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/model-usage
- 本技能说明: `SKILL.md`
