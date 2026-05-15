# PDF 使用指南

## 1. 功能定位
- PDF 解析、表单填写、合并拆分与结构化提取。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/pdf`
- 安装后目录: `~/.openclaw/skills/pdf`

## 2. 使用前准备
- 依赖通常由安装脚本自动补齐；缺失时安装 `pypdf` / `pdf2image`。

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请用 pdf 填写这份 PDF 表单。
- 请用 pdf 把多个 PDF 合并并抽取第一页。

## 5. 手动验证
```bash
python3 skills/default/pdf/scripts/check_fillable_fields.py --help
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/pdf
- 本技能说明: `SKILL.md`
