# 使用条件索引

| 使用条件 | 数量 |
|---|---:|
| `api-key` | 55 |
| `browser-required` | 10 |
| `direct` | 120 |
| `mcp-required` | 4 |

## api-key

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `github` | `GH_TOKEN`, `GITHUB_TOKEN` | `gh` | `medium` |
| `agentmail-mcp` | `AGENTMAIL_API_KEY` | `mcp` | `medium` |
| `agentmail-toolkit` | `AGENTMAIL_API_KEY`, `OPENAI_API_KEY` | 无 | `medium` |
| `baoyu-image-gen` | `ARK_API_KEY`, `AZURE_OPENAI_API_KEY`, `BIGMODEL_API_KEY`, `DASHSCOPE_API_KEY`, `GOOGLE_API_KEY`, `MINIMAX_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `REPLICATE_API_TOKEN`, `ZAI_API_KEY` | 无 | `medium` |
| `dual-axis-skill-reviewer` | `OPENAI_API_KEY` | 无 | `medium` |
| `funda-data` | `FUNDA_API_KEY` | `python` | `medium` |
| `lark-calendar` | `FEISHU_APP_SECRET` | 无 | `medium` |
| `minimax-web-search` | `MINIMAX_API_KEY` | `browser`, `mcp` | `medium` |
| `openclaw-stock-data-skill` | `STOCK_API_KEY` | `python` | `medium` |
| `paperless-docs` | `PAPERLESS_TOKEN` | 无 | `medium` |
| `paperless-ngx-tools` | `PAPERLESS_TOKEN` | 无 | `medium` |
| `tavily-search` | `OPENAI_API_KEY`, `TAVILY_API_KEY` | `browser`, `python` | `medium` |
| `tushare-openclaw-skill` | `TUSHARE_TOKEN` | 无 | `medium` |
| `agentmail-cli` | `AGENTMAIL_API_KEY` | `browser` | `medium` |
| `alphaear-sentiment` | `OPENAI_API_KEY` | `python` | `medium` |
| `baoyu-post-to-wechat` | `ACCESS_TOKEN`, `WECHAT_AI_TOOLS_APP_SECRET`, `WECHAT_APP_SECRET`, `WECHAT_BAOYU_APP_SECRET` | 无 | `medium` |
| `canslim-screener` | `FMP_API_KEY` | `python` | `medium` |
| `dividend-growth-pullback-screener` | `FINVIZ_API_KEY`, `FMP_API_KEY` | `python` | `medium` |
| `downtrend-duration-analyzer` | `FMP_API_KEY` | 无 | `medium` |
| `earnings-calendar` | `FMP_API_KEY` | `browser`, `python` | `medium` |
| `earnings-trade-analyzer` | `FMP_API_KEY` | `node`, `python` | `medium` |
| `economic-calendar-fetcher` | `FMP_API_KEY` | `python` | `medium` |
| `edge-hint-extractor` | `OPENAI_API_KEY` | `node` | `medium` |
| `exposure-coach` | `FMP_API_KEY` | 无 | `medium` |
| `finance-sentiment` | `ADANOS_API_KEY` | `python` | `medium` |
| `finviz-screener` | `FINVIZ_API_KEY` | `python` | `medium` |
| `ftd-detector` | `FMP_API_KEY` | 无 | `medium` |
| `gemini-image-service` | `GEMINI_API_KEY` | 无 | `medium` |
| `ibd-distribution-day-monitor` | `FMP_API_KEY` | 无 | `medium` |
| `inference-skills` | `OPENAI_API_KEY` | 无 | `medium` |
| `institutional-flow-tracker` | `FMP_API_KEY` | `python` | `medium` |
| `kanchi-dividend-sop` | `FMP_API_KEY` | `python` | `medium` |
| `macro-regime-detector` | `FMP_API_KEY` | 无 | `medium` |
| `market-top-detector` | `FMP_API_KEY` | `python` | `medium` |
| `minimax-image-understanding` | `MINIMAX_API_KEY` | 无 | `medium` |
| `options-strategy-advisor` | `FMP_API_KEY` | 无 | `medium` |
| `oracle` | `OPENAI_API_KEY` | `browser` | `medium` |
| `pair-trade-screener` | `FMP_API_KEY` | `python` | `medium` |
| `parabolic-short-trade-planner` | `ALPACA_API_KEY`, `FMP_API_KEY` | 无 | `medium` |
| `pead-screener` | `FMP_API_KEY` | `python` | `medium` |
| `signal-postmortem` | `FMP_API_KEY` | 无 | `medium` |
| `stock-daily-analysis-skill` | `OPENAI_API_KEY` | `python` | `medium` |
| `theme-detector` | `FINVIZ_API_KEY`, `FMP_API_KEY` | 无 | `medium` |
| `value-dividend-screener` | `FINVIZ_API_KEY`, `FMP_API_KEY` | `python` | `medium` |
| `vcp-screener` | `FMP_API_KEY` | `python` | `medium` |
| `agentmail` | `AGENTMAIL_API_KEY` | `browser` | `medium` |
| `ai-image-generation` | `GEMINI_API_KEY`, `OPENAI_API_KEY` | 无 | `medium` |
| `fullstack-dev` | `JWT_SECRET` | `node` | `medium` |
| `media-downloader` | `PEXELS_API_KEY` | 无 | `medium` |
| `minimax-multimodal-toolkit` | `MINIMAX_API_KEY` | `browser`, `ffmpeg` | `medium` |
| `notebooklm-skill` | `GEMINI_API_KEY` | `browser` | `medium` |
| `vision-analysis` | `MINIMAX_API_KEY` | 无 | `medium` |
| `gif-sticker-maker` | `MINIMAX_API_KEY` | `ffmpeg` | `medium` |
| `baoyu-danger-x-to-markdown` | `X_AUTH_TOKEN` | 无 | `high` |
| `baoyu-danger-gemini-web` | `GEMINI_API_KEY` | `browser` | `high` |

## browser-required

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `agent-browser` | 无 | `browser`, `python` | `medium` |
| `url-to-markdown` | 无 | `browser` | `medium` |
| `baoyu-url-to-markdown` | 无 | `browser` | `medium` |
| `openclaw-cron-setup` | 无 | `browser` | `medium` |
| `alphaear-search` | 无 | `browser`, `python` | `medium` |
| `baoyu-compress-image` | 无 | `browser` | `medium` |
| `baoyu-post-to-weibo` | 无 | `browser`, `ffmpeg` | `medium` |
| `baoyu-post-to-x` | 无 | `browser`, `ffmpeg` | `medium` |
| `market-news-analyst` | 无 | `browser`, `node`, `python` | `medium` |
| `web-search` | 无 | `browser`, `ffmpeg` | `medium` |

## direct

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `brainstorming` | 无 | 无 | `low` |
| `find-skills` | 无 | 无 | `low` |
| `model-usage` | 无 | `python` | `low` |
| `planning-with-files` | 无 | 无 | `low` |
| `skill-creator` | 无 | 无 | `low` |
| `skill-security-auditor` | 无 | `python` | `low` |
| `skill-vetter` | 无 | 无 | `low` |
| `subagent-driven-development` | 无 | 无 | `low` |
| `task` | 无 | 无 | `low` |
| `todo` | 无 | `python` | `low` |
| `using-superpowers` | 无 | 无 | `low` |
| `verification-before-completion` | 无 | 无 | `low` |
| `weather` | 无 | 无 | `low` |
| `writing-skills` | 无 | 无 | `low` |
| `animation` | 无 | 无 | `low` |
| `backtest-expert` | 无 | 无 | `low` |
| `baoyu-youtube-transcript` | 无 | `ffmpeg`, `python` | `low` |
| `data-analyst` | 无 | `python` | `low` |
| `discord-reader` | 无 | 无 | `low` |
| `edge-concept-synthesizer` | 无 | 无 | `low` |
| `edge-pipeline-orchestrator` | 无 | 无 | `low` |
| `edge-signal-aggregator` | 无 | `python` | `low` |
| `edge-strategy-designer` | 无 | 无 | `low` |
| `generative-ui` | 无 | 无 | `low` |
| `linkedin-reader` | 无 | 无 | `low` |
| `multi-search-engine` | 无 | 无 | `low` |
| `nano-pdf` | 无 | 无 | `low` |
| `openclaw-stock-kb` | 无 | `python` | `low` |
| `opencli-reader` | 无 | 无 | `low` |
| `proactive-agent` | 无 | 无 | `low` |
| `reflection` | 无 | 无 | `low` |
| `seedance2-skill` | 无 | 无 | `low` |
| `self-improving-agent-cn` | 无 | 无 | `low` |
| `skill-designer` | 无 | 无 | `low` |
| `skill-integration-tester` | 无 | `python` | `low` |
| `strategy-pivot-designer` | 无 | 无 | `low` |
| `telegram-reader` | 无 | 无 | `low` |
| `twitter-reader` | 无 | 无 | `low` |
| `writing-plans` | 无 | 无 | `low` |
| `yc-reader` | 无 | 无 | `low` |
| `a-stock-data` | 无 | `python` | `medium` |
| `akshare-stock` | 无 | `python` | `medium` |
| `yfinance-data` | 无 | `python` | `medium` |
| `baoyu-article-illustrator` | 无 | 无 | `low` |
| `baoyu-comic` | 无 | 无 | `low` |
| `baoyu-cover-image` | 无 | 无 | `low` |
| `baoyu-format-markdown` | 无 | 无 | `low` |
| `baoyu-infographic` | 无 | 无 | `low` |
| `baoyu-markdown-to-html` | 无 | 无 | `low` |
| `baoyu-skills` | 无 | 无 | `low` |
| `baoyu-slide-deck` | 无 | 无 | `low` |
| `baoyu-translate` | 无 | 无 | `low` |
| `baoyu-xhs-images` | 无 | 无 | `low` |
| `capability-evolver` | 无 | 无 | `low` |
| `edge-strategy-reviewer` | 无 | 无 | `low` |
| `estimate-analysis` | 无 | 无 | `low` |
| `hormuz-strait` | 无 | 无 | `low` |
| `scenario-analyzer` | 无 | 无 | `low` |
| `sepa-strategy` | 无 | 无 | `low` |
| `skill-idea-miner` | 无 | 无 | `low` |
| `startup-analysis` | 无 | 无 | `low` |
| `android-native-dev` | 无 | 无 | `low` |
| `flutter-dev` | 无 | 无 | `low` |
| `frontend-dev` | 无 | `node` | `low` |
| `ios-application-dev` | 无 | 无 | `low` |
| `minimax-docx` | 无 | 无 | `low` |
| `minimax-pdf` | 无 | 无 | `low` |
| `minimax-xlsx` | 无 | `node`, `python` | `low` |
| `pptx-generator` | 无 | `node` | `low` |
| `react-native-dev` | 无 | `node` | `low` |
| `shader-dev` | 无 | 无 | `low` |
| `social-content` | 无 | `ffmpeg` | `low` |
| `alphaear-deepear-lite` | 无 | `python` | `medium` |
| `alphaear-logic-visualizer` | 无 | `python` | `medium` |
| `alphaear-news` | 无 | `python` | `medium` |
| `alphaear-predictor` | 无 | `python` | `medium` |
| `alphaear-reporter` | 无 | `python` | `medium` |
| `alphaear-signal-tracker` | 无 | `python` | `medium` |
| `alphaear-stock` | 无 | `python` | `medium` |
| `breadth-chart-analyst` | 无 | `python` | `medium` |
| `breakout-trade-planner` | 无 | 无 | `medium` |
| `company-valuation` | 无 | 无 | `medium` |
| `data-quality-checker` | 无 | `python` | `medium` |
| `earnings-preview` | 无 | 无 | `medium` |
| `earnings-recap` | 无 | 无 | `medium` |
| `edge-candidate-agent` | 无 | `python` | `medium` |
| `etf-premium` | 无 | 无 | `medium` |
| `finance-skill-creator` | 无 | `python` | `medium` |
| `kanchi-dividend-review-monitor` | 无 | 无 | `medium` |
| `kanchi-dividend-us-tax-accounting` | 无 | 无 | `medium` |
| `market-breadth-analyzer` | 无 | `python` | `medium` |
| `market-environment-analysis` | 无 | `python` | `medium` |
| `options-payoff` | 无 | 无 | `medium` |
| `policy-monitor` | 无 | 无 | `medium` |
| `position-sizer` | 无 | `python` | `medium` |
| `pybroker-backtest-skill` | 无 | 无 | `medium` |
| `saas-valuation-compression` | 无 | 无 | `medium` |
| `sector-analyst` | 无 | `python` | `medium` |
| `stanley-druckenmiller-investment` | 无 | 无 | `medium` |
| `stock-analysis` | 无 | `node`, `python` | `medium` |
| `stock-correlation` | 无 | `python` | `medium` |
| `stock-liquidity` | 无 | `python` | `medium` |
| `stock-monitor-skill` | 无 | `python` | `medium` |
| `technical-analyst` | 无 | `python` | `medium` |
| `trade-hypothesis-ideator` | 无 | 无 | `medium` |
| `trader-memory-core` | 无 | 无 | `medium` |
| `uptrend-analyzer` | 无 | `python` | `medium` |
| `us-market-bubble-detector` | 无 | `python` | `medium` |
| `us-stock-analysis` | 无 | `python` | `medium` |
| `content-strategy` | 无 | 无 | `medium` |
| `buddy-sings` | 无 | 无 | `low` |
| `codex-responses-tooling` | 无 | 无 | `low` |
| `minimax-music-gen` | 无 | `ffmpeg` | `low` |
| `minimax-music-playlist` | 无 | `ffmpeg` | `low` |
| `marketingskills` | 无 | 无 | `medium` |
| `docx` | 无 | 无 | `low` |
| `pdf` | 无 | 无 | `low` |
| `pptx` | 无 | `node` | `low` |
| `shell` | 无 | 无 | `high` |
| `xlsx` | 无 | `node`, `python` | `low` |

## mcp-required

| Skill | API Key | Tools | 风险 |
|---|---|---|---|
| `chrome-devtools-mcp` | 无 | `browser`, `mcp` | `medium` |
| `mcp-builder` | 无 | `mcp` | `medium` |
| `news-radar` | 无 | `mcp`, `python` | `medium` |
| `portfolio-manager` | 无 | `mcp`, `python` | `medium` |
