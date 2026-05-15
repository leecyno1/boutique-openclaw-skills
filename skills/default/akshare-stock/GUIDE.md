# AkShare Stock 使用指南

## 1. 功能定位
- A 股行情、财务、板块、资金流向等数据分析。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/akshare-stock`
- 安装后目录: `~/.openclaw/skills/akshare-stock`

## 2. 使用前准备
- Python 依赖 `akshare`

## 3. 配置步骤
1. 执行 `pip install akshare`。
2. 若要长期使用，建议安装到 OpenClaw 运行环境同一 Python。

## 4. 推荐提问方式
- 请用 akshare-stock 查询 600519 最近 3 个月日线。
- 请用 akshare-stock 分析半导体板块近 20 日资金流向。

## 5. 手动验证
```bash
python3 -c "import akshare; print(akshare.__version__)"
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/akshare-stock
- 本技能说明: `SKILL.md`
