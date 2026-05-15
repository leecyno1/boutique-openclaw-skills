# Workflow Contract (Reusable Footage)

## 目标
将“选题内容”转成可复用的视频素材池，优先满足剪辑场景的 B-roll 与资料片诉求。

## 关键约束
- 登录站点默认走 CDP cookie 注入（`cookie_mode=cdp`）。
- Douyin 失败时走 CDP 解析流 + ffmpeg 合成回退。
- 自动锚点上限 `<=10`。
- 视频双链路：
  - `related`：上游证据链接线
  - `search`：网络检索线
- 搜索策略优先：`纪录片/资料片/历史影像/archive footage`。
- 搜索策略规避：`口播/访谈/对谈/podcast/reaction` 和大字幕倾向。

## 质量门槛（默认）
- `related_raw_videos >= 3`
- `search_raw_videos >= 3`
- `related_clips >= 3`
- `search_clips >= 5`

## 核心产物
- `manifest/report.json`
- `manifest/video-search-sources.json`
- `videos/related/raw`
- `videos/search/raw`
- `videos/related/clips`
- `videos/search/clips`

## 失败处理
- 若 `report.json` 缺失，视为执行失败。
- 若数量未达门槛，返回 `quality_summary.warnings` 并提示重跑。
