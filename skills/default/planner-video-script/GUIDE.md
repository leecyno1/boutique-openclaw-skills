# planner-video-script 使用指南

## 1. 功能定位
- 视频脚本结构规划适配器。用于在 `target_media=video_script` 的前提下，基于已确认的 Content Brief、Material Pack 和 Media Plan，生成视频脚本的完整框架，包含开场钩子、核心论证段落、分镜建议、口播逻辑和结尾行动号召。
- 默认档位: 仅全量默认包/手动同步
- 仓库目录: `skills/default/planner-video-script`
- 安装后目录: `~/.openclaw/skills/planner-video-script`

## 2. 使用前准备
- 无强制 API Key；按 skill 自身依赖运行。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请使用 planner-video-script 帮我处理当前任务。
- 如果 planner-video-script 需要额外配置，请先告诉我缺少什么。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/planner-video-script
```

## 6. 参考资料
- 上游来源: 见 docs/upstream-sources.md
- 本技能说明: `SKILL.md`
