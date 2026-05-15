---
name: gemini-image-service
description: 使用 Gemini 第三方服务生成图片。读取 GEMINI_API_KEY/GEMINI_BASE_URL/GEMINI_IMAGE_MODEL。
---

# Gemini Image Service

用于图片生成场景，支持第三方代理地址与自定义模型名。

## 前置环境变量

- `GEMINI_API_KEY`
- `GEMINI_BASE_URL`（示例：`https://your-provider.example.com`）
- `GEMINI_IMAGE_MODEL`（示例：`gemini-2.5-flash-image-preview`）

## 用法

```bash
python scripts/generate_image.py \
  --prompt "一只赛博朋克风格的机械龙" \
  --output /tmp/gemini-image.png
```

可选参数：

- `--size 1024x1024`
- `--endpoint /v1/images/generations`

## 失败排查

1. 检查 `GEMINI_BASE_URL` 是否可访问。
2. 检查 `GEMINI_API_KEY` 是否有效。
3. 检查模型名是否为服务商支持的模型。
