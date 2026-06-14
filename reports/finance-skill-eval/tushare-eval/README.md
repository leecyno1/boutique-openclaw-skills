# Tushare Finance Skill Evaluation

本目录保存金融 skills 的 Tushare 数据接口评测结果。

## 安全运行方式

不要把 Tushare token 写入仓库文件、脚本或命令历史。请在本机终端临时设置环境变量后运行：

```bash
./scripts/run-tushare-eval.sh
```

也可以手动临时设置环境变量后运行：

```bash
export TUSHARE_TOKEN="你的 Tushare token"
python3 scripts/evaluate_finance_tushare.py
unset TUSHARE_TOKEN
```

脚本只读取 `TUSHARE_TOKEN` 环境变量，不会保存或展示 token。推荐使用 `run-tushare-eval.sh`，它会隐藏输入，避免 token 进入命令历史。

## 输出文件

- `tushare-finance-skill-evaluation.html`：面向人工浏览的 HTML 评测报告。
- `tushare-finance-skill-evaluation.json`：机器可读的完整评测结果。

## 当前状态

如果报告显示 `Tushare 连通 = 否`，说明生成报告时当前 shell 没有设置 `TUSHARE_TOKEN`。设置环境变量后重新运行脚本即可生成实测版。
