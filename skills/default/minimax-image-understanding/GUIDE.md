# MiniMax Understand Image 使用指南

## 1. 功能定位
- 优先用 MiniMax 做识图、OCR、截图理解与视觉分析。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/minimax-image-understanding`
- 安装后目录: `~/.openclaw/skills/minimax-image-understanding`

## 2. 使用前准备
- `MINIMAX_API_KEY` 或 `~/.openclaw/config/minimax.json`

## 3. 配置步骤
1. 确保 `~/.openclaw/config/minimax.json` 含有效 `api_key`。
2. 若无配置，可在当前 shell 导出 `MINIMAX_API_KEY`。
3. 本 skill 的脚本支持本地图片路径和远程 URL。

## 4. 推荐提问方式
- 请用 minimax-image-understanding 识别这张图里的错误信息。
- 请用 minimax-image-understanding 解释这个 UI 截图。

## 5. 手动验证
```bash
python3 skills/default/minimax-image-understanding/scripts/understand_image.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/minimax-image-understanding
- 本技能说明: `SKILL.md`
