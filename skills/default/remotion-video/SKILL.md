---
name: remotion-video
description: Remotion executable workflow for title-card videos and XHS-style dynamic chart videos. Merged with remotion-best-practices knowledge rules.
---

# Remotion Video Skill

This skill renders MP4 videos using a local Remotion project.
It is merged with the official knowledge skill:
- `/Users/lichengyin/.agents/skills/remotion-best-practices/SKILL.md`

When generating chart-heavy videos, follow these rule files first:
- `rules/charts.md`
- `rules/animations.md`
- `rules/timing.md`
- `rules/transitions.md`
- `rules/ffmpeg.md` (if source trimming / frame extraction is needed)

## Project Path
- Default project: `/Users/lichengyin/clawd/remotion-video-starter`
- Override with env var: `REMOTION_PROJECT_DIR`

## Commands

### 1) Preview in Remotion Studio
```bash
cd /Users/lichengyin/clawd/remotion-video-starter
npm run dev
```

### 2) Render title-card video (HelloWorld)
```bash
cd /Users/lichengyin/clawd/remotion-video-starter
npm run render
```

### 3) Render XHS-style dynamic chart rebuild
```bash
cd /Users/lichengyin/clawd/remotion-video-starter
npm run render:xhs
```

### 4) Render with helper script (two modes)
```bash
# Title-card mode
/Users/lichengyin/.openclaw/skills/remotion-video/render.sh "你的标题" "your-file.mp4"

# XHS rebuild mode
/Users/lichengyin/.openclaw/skills/remotion-video/render.sh --xhs "xhs-rebuild.mp4"
```

Output path:
- `/Users/lichengyin/clawd/remotion-video-starter/out/<file>.mp4`

## Usage Rules
- Keep title concise (recommended <= 24 chars for single line).
- If user requests multiple variants, render multiple files with different names.
- Return final output file path(s) after rendering.
- For chart replication tasks, use composition `XhsRemotionRebuild` in `src/XhsRemotionRebuild.jsx`.
