# DOCX 使用指南

## 1. 功能定位
- 创建、编辑、批注 Word 文档，并尽量保持格式。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/docx`
- 安装后目录: `~/.openclaw/skills/docx`

## 2. 使用前准备
- Python 依赖通常由安装脚本补齐；缺失时补 `python-docx`。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请用 docx 生成一份会议纪要 Word。
- 请在现有 docx 文件中加入批注并保持排版。

## 5. 手动验证
```bash
python3 -c "import docx; print(docx.__version__)"
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/docx
- 本技能说明: `SKILL.md`
