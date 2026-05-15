# XLSX 使用指南

## 1. 功能定位
- 表格读写、公式处理、分析和导出。
- 默认档位: 基础档默认安装
- 仓库目录: `skills/default/xlsx`
- 安装后目录: `~/.openclaw/skills/xlsx`

## 2. 使用前准备
- Python 依赖 `openpyxl`

## 3. 配置步骤
1. 通常无需额外配置。若运行时报缺依赖，再按 `SKILL.md` 补装。

## 4. 推荐提问方式
- 请用 xlsx 读取这个 Excel 并统计每列汇总。
- 请用 xlsx 生成一个带公式的财务表。

## 5. 手动验证
```bash
python3 -c "import openpyxl; print(openpyxl.__version__)"
```

## 6. 参考资料
- 上游来源: ~/.codex/skills/xlsx
- 本技能说明: `SKILL.md`
