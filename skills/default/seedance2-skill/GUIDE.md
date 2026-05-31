# seedance2-skill 使用指南

## 1. 功能定位
- Seedance 2.0 / 即梦视频生成提示词技能，用于撰写高质量文生视频、图生视频、视频延展、视频编辑、广告短片、短剧、AI MV 和科普视频提示词。
- 默认档位：高档专家技能；不进入标准组合，避免标准安装包变重。
- 仓库目录：`skills/default/seedance2-skill`
- 安装后目录：`~/.openclaw/skills/seedance2-skill`

## 2. 使用前准备
- 无本地运行依赖。
- 无强制 API Key。
- 需要用户自行在 Seedance 2.0 / 即梦平台使用生成出的提示词。

## 3. 配置步骤
1. 安装 skill 后，直接要求 Agent 生成 Seedance 2.0 视频提示词。
2. 如需中文提示词，可参考 `references/SKILL.zh.md`。
3. 如果使用图片、视频、音频素材，按 Seedance 的 `@Image1` / `@Video1` / `@Audio1` 引用方式说明素材角色。

## 4. 推荐提问方式
- 请用 seedance2-skill 帮我写一个 10 秒电商产品视频提示词。
- 根据这张图写一个 Seedance 2.0 图生视频 prompt，包含镜头运动和节奏分段。
- 帮我把这个视频延展成 15 秒短剧片段，保留人物动作和镜头语言。

## 5. 手动验证
```bash
ls -la ~/.openclaw/skills/seedance2-skill
```

## 6. 参考资料
- 原生上游：https://github.com/dexhunter/seedance2-skill
- 英文技能：`SKILL.md`
- 中文技能：`references/SKILL.zh.md`
