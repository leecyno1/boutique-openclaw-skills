---
name: grok-imagine-1.0-video
description: 使用 grok-imagine-1.0-video 模型生成视频。用于高档默认技能包。
---

# Grok Imagine 1.0 Video

用于调用 `grok-imagine-1.0-video` 生成短视频。

## 前置环境变量

- `GROK_IMAGINE_API_KEY`
- `GROK_IMAGINE_BASE_URL`（示例：`https://api.x.ai` 或代理地址）
- `GROK_IMAGINE_MODEL`（默认：`grok-imagine-1.0-video`）

## 用法

```bash
python scripts/generate_video.py \
  --prompt "一段 6 秒的宇宙科幻镜头" \
  --output /tmp/grok-video.mp4
```

可选参数：

- `--endpoint /v1/videos/generations`

## 说明

- 该技能默认纳入高档规则（HIGH）技能包。
- 若服务商返回异步任务 id，请按服务商文档轮询任务状态。
