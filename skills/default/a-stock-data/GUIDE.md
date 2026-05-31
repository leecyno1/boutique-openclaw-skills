# a-stock-data 使用指南

## 1. 功能定位
- A 股全栈数据工具包，覆盖行情、研报、题材归因、北向资金、龙虎榜、解禁、两融、大宗交易、股东户数、分红、新闻、基础数据和公告。
- 默认档位：低档 / 标准组合推荐金融数据技能。
- 仓库目录：`skills/default/a-stock-data`
- 安装后目录：`~/.openclaw/skills/a-stock-data`

## 2. 使用前准备
```bash
pip install mootdx requests pandas stockstats
```

- 大多数数据源无需 API Key。
- 仅 iwencai 语义研报搜索需要 `IWENCAI_API_KEY`。
- `mootdx` 走通达信 TCP 行情源，国内网络环境更稳定。

## 3. 配置步骤
1. 安装依赖。
2. 如需 iwencai 语义搜索，配置：
   ```bash
   export IWENCAI_API_KEY="your_key_here"
   export IWENCAI_BASE_URL="https://openapi.iwencai.com"
   ```
3. 直接向 Agent 提问 A 股行情、估值、研报、题材、资金流、龙虎榜、解禁或公告相关问题。

## 4. 推荐提问方式
- 请用 a-stock-data 分析 600519 的估值、资金流和最新公告。
- 帮我对比 5 只半导体 A 股的 PE、PEG、研报覆盖和资金流。
- 今天 A 股强势题材和龙虎榜净买入最多的股票有哪些？

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/a-stock-data
python - <<'PY'
import requests, pandas, stockstats
print('a-stock-data dependencies ok')
PY
```

## 6. 参考资料
- 原生上游：https://github.com/simonlin1212/a-stock-data
- 本技能说明：`SKILL.md`
