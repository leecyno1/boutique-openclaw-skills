# Grok Imagine Video 使用指南

## 1. 功能定位
- 调用 `grok-imagine-1.0-video` 或兼容代理服务生成短视频。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/grok-imagine-1.0-video`
- 安装后目录: `~/.openclaw/skills/grok-imagine-1.0-video`

## 2. 使用前准备
- `GROK_IMAGINE_API_KEY`
- `GROK_IMAGINE_BASE_URL`
- `GROK_IMAGINE_MODEL`

## 3. 配置步骤
1. 建议把 3 个环境变量写入 `~/.openclaw/env`。
2. 如服务商不是 xAI 官方，务必核对路径与异步任务轮询方式。

## 4. 推荐提问方式
- 请用 grok-imagine-1.0-video 生成 6 秒产品展示视频。

## 5. 手动验证
```bash
python3 skills/default/grok-imagine-1.0-video/scripts/generate_video.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/grok-imagine-1.0-video
- 本技能说明: `SKILL.md`
