# Gemini Image Service 使用指南

## 1. 功能定位
- 通过 Gemini 兼容服务生成图片，支持第三方代理地址与自定义模型名。
- 默认档位: 扩展档默认安装
- 仓库目录: `skills/default/gemini-image-service`
- 安装后目录: `~/.openclaw/skills/gemini-image-service`

## 2. 使用前准备
- `GEMINI_API_KEY`
- `GEMINI_BASE_URL`
- `GEMINI_IMAGE_MODEL`

## 3. 配置步骤
1. 推荐写入 `~/.openclaw/skills/gemini-image-service/service.env`。
2. 也可以写入 `~/.openclaw/env`，但服务 env 优先更清晰。
3. 配置后用 `python3 scripts/generate_image.py --prompt "测试" --output /tmp/gemini.png` 验证。

## 4. 推荐提问方式
- 请用 gemini-image-service 生成一张产品海报。
- 请用 gemini-image-service 按第三方地址生成 1:1 方图。

## 5. 手动验证
```bash
python3 skills/default/gemini-image-service/scripts/generate_image.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/gemini-image-service
- 本技能说明: `SKILL.md`
