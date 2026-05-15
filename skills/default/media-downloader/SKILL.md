---
name: media-downloader
description: |-
  Use when downloading or finding images, videos, clips, or media assets.
  智能媒体下载器。根据用户描述自动搜索和下载图片、视频片段，支持视频自动剪辑。
  Smart media downloader. Automatically search and download images/video clips based on user description, with auto-trimming support.
  触发方式 Triggers: "下载图片", "找视频", "download media", "download images", "find video", "/media"
---

# 🎬 Media Downloader / 智能媒体下载器

只需告诉我你想要什么，我就会帮你找到并下载相关的图片和视频！

Just tell me what you want, and I'll find and download relevant images and videos for you!

---

## 🚀 我能帮你做什么？/ What Can I Do?

| 你说... / You say... | 我会... / I will... |
|---------------------|---------------------|
| "下载一些可爱的猫咪图片" | 搜索并下载 5 张猫咪图片 |
| "Download sunset photos" | Search and download sunset images |
| "找一段海浪的视频，15秒左右" | 下载一段 15 秒的海浪视频 |
| "Get me a 30-second cooking video" | Download a trimmed cooking clip |
| "下载这个 YouTube 视频的 1:30-2:00" | 下载并自动剪辑指定片段 |

---

## ✨ 功能特点 / Features

- 🖼️ **图片下载** - 从专业图库搜索高清图片
- 🎬 **视频素材** - 获取免费商用视频片段
- 📺 **YouTube 下载** - 支持下载和剪辑
- ✂️ **智能剪辑** - 自动裁剪到你需要的长度
- 🌍 **中英双语** - 支持中文和英文指令

---

## 📋 Skill 执行逻辑 / Skill Execution Logic

### 🔑 API Key 按需配置 / On-Demand API Key Configuration

**重要**：不要在用户安装时就要求配置 API Key！按以下逻辑处理：

1. **用户下载 YouTube 视频时**：直接执行，不需要任何 API Key
2. **用户首次下载图片时**：
   - 检查 `PEXELS_API_KEY` 环境变量是否存在
   - 如果不存在，引导用户配置：
     ```
     检测到你还没有配置图库 API Key。下载图片需要一个免费的 API Key。

     请按以下步骤操作：
     1. 打开 https://www.pexels.com，点击 Join 注册（支持 Google/Apple 一键注册）
     2. 注册后访问 https://www.pexels.com/api/，点击 Your API Key
     3. 复制显示的密钥，粘贴给我
     ```
   - 用户提供 API Key 后，帮用户保存到系统环境变量：
     ```bash
     echo 'export PEXELS_API_KEY="用户的密钥"' >> ~/.zshrc && source ~/.zshrc
     ```
   - 然后继续完成图片下载任务

### 🎬 YouTube 下载优先 / YouTube First

当用户说「下载视频」但没有指定来源时，优先推荐 YouTube：
- YouTube 不需要 API Key
- 内容更丰富
- 支持时间段裁剪

---

## 💬 使用示例 / Examples

### 下载图片 / Download Images

```
"帮我下载 5 张星空的图片"
"Download 10 coffee shop photos"
"找一些适合做壁纸的风景图"
```

### 下载视频素材 / Download Video Clips

```
"下载一段城市夜景的视频，30秒以内"
"Find me a 15-second ocean wave video"
"找一些适合做背景的自然风光视频"
```

### YouTube 下载与剪辑 / YouTube Download & Trim

```
"下载这个视频：https://youtube.com/watch?v=xxx"
"下载这个 YouTube 视频的第 2 分钟到第 3 分钟"
"只下载这个视频的音频"
```

---

## 📁 下载位置 / Download Location

所有文件默认保存在：

```
~/.claude/skills/media-downloader/downloads/
```

---

## ❓ 常见问题 / FAQ

### Q: 为什么搜索图片没有结果？
A: 请确认已配置 API Key。运行 `status` 命令检查配置状态。

### Q: YouTube 视频下载失败？
A: YouTube 下载不需要 API Key，但需要安装 yt-dlp。运行 `pip install yt-dlp` 安装。

### Q: 视频剪辑功能不工作？
A: 需要安装 ffmpeg。macOS 用户运行 `brew install ffmpeg`。

### Q: 这些图片/视频可以商用吗？
A: Pexels、Pixabay、Unsplash 的素材都可以免费商用，无需署名（但署名是一种礼貌）。

---

## 🛠️ CLI 命令参考 / CLI Reference

供高级用户直接使用命令行：

```bash
# 检查配置状态
media_cli.py status

# 下载图片
media_cli.py image "关键词" -n 数量 -o 输出目录

# 下载视频素材
media_cli.py video "关键词" -d 最大时长 -n 数量

# 下载 YouTube 视频
media_cli.py youtube "URL" --start 开始秒数 --end 结束秒数

# 搜索媒体（不下载）
media_cli.py search "关键词" --type image/video/all

# 剪辑本地视频
media_cli.py trim 输入文件 --start 开始 --end 结束
```

---

## 📦 支持的素材来源 / Supported Sources

| 来源 Source | 类型 Type | 特点 Features |
|-------------|-----------|---------------|
| Pexels | 图片 + 视频 | 高质量，更新快 |
| Pixabay | 图片 + 视频 | 数量多，种类全 |
| Unsplash | 图片 | 艺术感强，适合壁纸 |
| YouTube | 视频 | 内容丰富，支持剪辑 |

---

🎬 **开始使用吧！直接告诉我你想要什么图片或视频！**

🎬 **Start using! Just tell me what images or videos you want!**
