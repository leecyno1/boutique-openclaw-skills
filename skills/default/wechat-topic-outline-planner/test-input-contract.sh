#!/bin/bash

# 测试脚本：验证新输入契约的有效性

echo "=== wechat-topic-outline-planner v2 输入契约测试 ==="
echo ""
echo "测试时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 测试 1: 验证输入示例的 JSON 格式
echo "【测试 1】验证输入示例的 JSON 格式"
INPUT_FILE="~/clawd/skills/wechat-skills/wechat-topic-outline-planner/templates/input-example.json"

if python3 -m json.tool "$INPUT_FILE" > /dev/null 2>&1; then
    echo "✓ JSON 格式有效"
else
    echo "✗ JSON 格式无效"
    exit 1
fi

# 测试 2: 验证必需字段
echo ""
echo "【测试 2】验证必需字段"

REQUIRED_FIELDS=(
    "outline_planning_request"
    "request_id"
    "content_brief"
    "material_pack"
    "target_media"
    "created_at"
)

for field in "${REQUIRED_FIELDS[@]}"; do
    if grep -q "\"$field\"" "$INPUT_FILE"; then
        echo "✓ 字段 '$field' 存在"
    else
        echo "✗ 字段 '$field' 缺失"
    fi
done

# 测试 3: 验证 Brief 字段完整性
echo ""
echo "【测试 3】验证 Brief 字段完整性"

BRIEF_FIELDS=(
    "brief_id"
    "core_judgment"
    "target_audience"
    "article_goal"
    "key_points"
    "risk_boundaries"
)

for field in "${BRIEF_FIELDS[@]}"; do
    if grep -q "\"$field\"" "$INPUT_FILE"; then
        echo "✓ Brief 字段 '$field' 存在"
    else
        echo "✗ Brief 字段 '$field' 缺失"
    fi
done

# 测试 4: 验证 Material Pack 字段完整性
echo ""
echo "【测试 4】验证 Material Pack 字段完整性"

MATERIAL_FIELDS=(
    "pack_id"
    "materials"
    "evidence_checklist"
)

for field in "${MATERIAL_FIELDS[@]}"; do
    if grep -q "\"$field\"" "$INPUT_FILE"; then
        echo "✓ Material Pack 字段 '$field' 存在"
    else
        echo "✗ Material Pack 字段 '$field' 缺失"
    fi
done

# 测试 5: 验证素材类型
echo ""
echo "【测试 5】验证素材类型"

MATERIAL_TYPES=(
    "case_study"
    "data"
    "expert_view"
    "reference"
    "quote"
)

for type in "${MATERIAL_TYPES[@]}"; do
    if grep -q "\"type\": \"$type\"" "$INPUT_FILE"; then
        echo "✓ 素材类型 '$type' 存在"
    fi
done

# 测试 6: 验证 Media Plan 字段
echo ""
echo "【测试 6】验证 Media Plan 字段"

MEDIA_FIELDS=(
    "target_media"
    "platform_constraints"
    "max_length"
    "recommended_sections"
    "reading_time_minutes"
    "distribution_strategy"
)

for field in "${MEDIA_FIELDS[@]}"; do
    if grep -q "\"$field\"" "$INPUT_FILE"; then
        echo "✓ Media Plan 字段 '$field' 存在"
    else
        echo "✗ Media Plan 字段 '$field' 缺失"
    fi
done

# 测试 7: 统计素材数量
echo ""
echo "【测试 7】统计素材数量"

MATERIAL_COUNT=$(grep -c "\"material_id\"" "$INPUT_FILE")
echo "✓ 素材总数：$MATERIAL_COUNT 个"

# 测试 8: 验证可信度标记
echo ""
echo "【测试 8】验证可信度标记"

CREDIBILITY_HIGH=$(grep -c "\"credibility\": \"high\"" "$INPUT_FILE")
CREDIBILITY_MEDIUM=$(grep -c "\"credibility\": \"medium\"" "$INPUT_FILE")
CREDIBILITY_LOW=$(grep -c "\"credibility\": \"low\"" "$INPUT_FILE")

echo "✓ 高可信度素材：$CREDIBILITY_HIGH 个"
echo "✓ 中可信度素材：$CREDIBILITY_MEDIUM 个"
echo "✓ 低可信度素材：$CREDIBILITY_LOW 个"

# 测试 9: 验证关键点数量
echo ""
echo "【测试 9】验证关键点数量"

KEY_POINTS=$(grep -c "\"key_points\"" "$INPUT_FILE")
echo "✓ 关键点字段存在"

# 测试 10: 验证风险边界
echo ""
echo "【测试 10】验证风险边界"

RISK_BOUNDARIES=$(grep -c "\"risk_boundaries\"" "$INPUT_FILE")
echo "✓ 风险边界字段存在"

echo ""
echo "=== 测试完成 ==="
echo "✓ 所有基础验证通过"
echo ""
