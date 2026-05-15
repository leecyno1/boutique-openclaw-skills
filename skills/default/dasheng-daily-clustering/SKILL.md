# dasheng-daily-clustering

大圣工作流第二环节（聚类 + 强化 Brief）。

## 功能
- 无缝接收 `dasheng-daily-intake` 产出的 `intake-records.json`（约 1000 条）
- 执行主题聚类与话题索引排序
- 计算多维热度（体量/跨平台/质量/稳定性）
- 生成强化版 Brief（证据链 + 撰写建议 + 风险提示 + 下一步动作）
- 产出可直接给编辑审核的 markdown 与结构化 JSON

## 触发方式
- 群内发送“下一步”
- 或直接调用 `dasheng-daily-phase2`

## 输出
- `phase2-clusters-summary.json`
- `phase2-topic-index.json`
- `phase2-editorial-briefs.json`
- `phase2-brief-library.md`
- `phase2-topn-for-confirmation.json`
- `phase2-bitable-rows.json`

## 下游衔接
- 默认进入 `dasheng-daily-material`（Task 1.3）
- Top N 选题从 `phase2-topn-for-confirmation.json` 读取

## 说明
本 skill 已升级为第二环节总入口，内部调用 `dasheng-daily-phase2` 的强化版实现。
