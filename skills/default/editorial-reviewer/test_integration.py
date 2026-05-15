#!/usr/bin/env python3
"""
Editorial Reviewer Integration Test
快速验证规则引擎对真实 Draft 的复审效果
"""

import sys
sys.path.insert(0, '/Users/lichengyin/clawd/skills/wechat-skills/editorial-reviewer')

from review_rules_engine import EditorialReviewer, Severity

# 真实 Draft 数据
draft_v1 = {
    "draft_id": "draft-20260315-us-iran-001",
    "title": "美伊局势输赢判断",
    "full_content": """老朋友们知道，我以前聊任何话题，几乎不提"赢"和"输"。

因为只要是博弈，必然有利益损失，也必然有利益获取——单纯说谁赢了谁输了，其实没什么意义。

但今天想斗胆跟大家分享这个话题，有两个原因：

第一，最近相关的内容太多了。几乎每一天都有人说"这边赢了"、"那边输了"、"美帝已经完蛋了"、"伊朗已经扛不住了"。

没有标准，凭情绪下判断，毫无价值。

第二，美、以、伊三方心里各有所想。拿到想要的就是赢，没拿到就是输。标准不一样，结论自然不一样。

所以，不带情绪，我们来认真拆解一下。

几个前提先说清楚：

1. 不能有情绪——"我希望谁赢"、"我想谁输"，不在讨论范围
2. 不预测具体怎么打——真消息假消息满天飞，我们不在一线，很难判断
3. 只看各方目标——谁达成了目标，谁就是赢

还有一点：伊昨天表态"绝不投降"，美也放话"绝不允许拥有核武器"。这件事，短期内不会完。

好，这些说清楚了，我们入题。

以色列：目标最清晰的一个

把以色列先摘出来，因为它的目标非常直接：

完全不能留。

不管是核武器、远程导弹、杀伤性武器，还是把这个地方彻底摧毁��都在所不辞。

目标极其清晰，结果导向极其明确。

所以对以色列来说判断标准很简单：只要伊朗还有核能力、还有能威胁到它的远程导弹，这场战争它就输了。

美国：真正复杂的博弈

美国到底想要什么？

两个核心：

第一，石油。

第二，霍尔木兹海峡控制权。

石油美元的命根子

稍微梳理一下过去这一年多特政府在这条线上的动作：

最早出访中东，答应给对方更多武器和芯片，换回石油美元进一步绑定
邀请中亚五国到白宫，能源合作+关键矿产
中亚最大国家哈萨克斯坦签署亚伯拉罕协议
委内瑞拉出口的石油必须先过美账户，用美元结算

看石油储量分布：

中东阿拉伯国家��50%
委内瑞拉：18%
伊朗：12%
俄罗斯：5-6%
中亚：3%

合计超过90%。

为什么是现在？

三个条件缺一不可：

1. 石油美元确实在受挑战——如果36%的石油都在非美元体系流通，霸权根基会动摇
2. 伊经济确实在下滑——工资从200美元跌到70-100美元，汇率1:190万里亚尔，提供了可趁之机
3. 俄被俄乌冲突牵制——如果俄乌结束，这条条件就不存在了

怎么定义美的输赢？

注意，是他自己的标准，不是我们的。

核心判断：

最后谈判桌上，伊是否同意回到美元结算体系？

如果同意——美实质上赢了。
如果不同意——美输了。

至于中间飞机掉了、航母可能受损、通胀飙升、民意不满……都是过程。

最终只看结果。

霍尔木兹海峡：第二战场

这件事难度极大，但美在推进：

国家开发金融公司DSC和财政部、军方已达成共识，要对海峡船只保险进行兜底
全球最大险企安达保险正式加入

如果最后在谈判桌上，关于海峡实现了保险、共治、合资公司、利益分润……美就又赢一分。

没有？在这件事上就是输。

中间可能发生的"赢中的输"

一个补充点：

美并不希望炸毁伊的基础设施。

不想激起民怨
不想战后自己出更多钱重建

如果炸了石油设施、电力设施——

就算最后回到美元结算，这个烂摊子也会让美付出更大代价。

算赢中之输。

伊朗：与美相对应

伊的输赢跟美正好对应：

领土主权完整
经济、金融、贸易正常运行
未来不被美控制
战争损失的赔偿

核心就一条：不被美元体系绑架。

我的结论

说几点我的理解：

第一，4月2日之前是关键窗口。

之前特说"四周"，这两天说"两周"。他希望在一些重要事件前拿出突破性成果。

第二，只看最核心的利益线。

什么飞机掉了、谁谁又挨炸了、中间死了多少人……这些都是舆论战的一部分。

最后一条最重要：

赢，不代表对。

就算美达成了所有目标，也不代表他的做法是对的。这是两码事。""",
    "word_count": 2800
}

# 大纲数据
outline = [
    {
        "section_id": "sec-001",
        "section_number": 1,
        "section_title": "为什么要讨论输赢",
        "section_objective": "建立讨论框架",
        "core_argument": "没有标准的输赢判断毫无价值",
        "evidence_required": ["最近舆论现象", "三方不同目标"]
    },
    {
        "section_id": "sec-002",
        "section_number": 2,
        "section_title": "几个前提先说清楚",
        "section_objective": "设定讨论边界",
        "core_argument": "讨论需要三个前提",
        "evidence_required": ["不能有情绪", "不预测具体"]
    },
    {
        "section_id": "sec-003",
        "section_number": 3,
        "section_title": "以色列：目标最清晰的一个",
        "section_objective": "分析以色列目标",
        "core_argument": "以色列目标极其清晰",
        "evidence_required": ["以色列目标", "判断标准"]
    },
    {
        "section_id": "sec-004",
        "section_number": 4,
        "section_title": "美国：真正复杂的博弈",
        "section_objective": "分析美国目标",
        "core_argument": "美国有两个核心目标",
        "evidence_required": ["石油美元", "海峡控制权"]
    }
]

# Content Brief
brief = {
    "brief_id": "brief-us-iran-001",
    "core_judgment": "美伊冲突的输赢取决于各方是否达成自身目标",
    "target_audience": "关注国际政治的投资者和分析师",
    "article_goal": "理性分析美伊冲突的实质和各方目标",
    "key_points": [
        "以色列目标最清晰",
        "美国核心是石油美元",
        "伊朗目标是经济独立"
    ],
    "risk_boundaries": [
        "不能预测具体军事行动",
        "不能表达政治立场"
    ]
}

# Material Pack
material_pack = {
    "pack_id": "pack-us-iran-001",
    "materials": [
        {
            "material_id": "mat-001",
            "type": "data",
            "title": "石油储量分布",
            "source": "BP 能源统计",
            "credibility": "high"
        },
        {
            "material_id": "mat-002",
            "type": "reference",
            "title": "伊朗经济数据",
            "source": "IMF 报告",
            "credibility": "high"
        },
        {
            "material_id": "mat-003",
            "type": "case_study",
            "title": "美国中东政策",
            "source": "新闻报道",
            "credibility": "medium"
        }
    ]
}

# Style DNA
style_dna = {
    "dna_id": "dna-lemon-001",
    "author_name": "柠檬博士",
    "tone": "理性、启发、略带幽默",
    "sentence_structure": "短句为主，偶尔长句",
    "rhetorical_devices": ["类比", "排比", "反问"],
    "vocabulary_level": "专业但易懂",
    "paragraph_style": "1-3 句为主",
    "taboo_patterns": ["绝对化表述", "情绪化词汇"]
}

# 运行复审
print("=" * 80)
print("Editorial Reviewer Integration Test")
print("=" * 80)
print()

reviewer = EditorialReviewer()
result = reviewer.review(draft_v1, outline, brief, material_pack, style_dna)

print(f"总体质量评分: {result['overall_quality_score']}/100")
print(f"发布就绪: {'✅ 是' if result['publication_ready'] else '❌ 否'}")
print()

# 结构复审结果
print("【结构复审】")
print(f"评分: {result['structural_review']['overall_score']}/100")
print(f"状态: {result['structural_review']['status']}")
print(f"问题数: {len(result['structural_review']['findings'])}")
for finding in result['structural_review']['findings']:
    print(f"  - [{finding.severity.value}] {finding.issue_type.value}: {finding.description}")
print()

# 证据复审结果
print("【证据复审】")
print(f"评分: {result['evidence_review']['overall_score']}/100")
print(f"状态: {result['evidence_review']['status']}")
print(f"问题数: {len(result['evidence_review']['findings'])}")
for finding in result['evidence_review']['findings']:
    print(f"  - [{finding.severity.value}] {finding.issue_type.value}: {finding.description}")
print()

# 语调复审结果
print("【语调复审】")
print(f"评分: {result['tone_review']['overall_score']}/100")
print(f"状态: {result['tone_review']['status']}")
print(f"问题数: {len(result['tone_review']['findings'])}")
for finding in result['tone_review']['findings']:
    print(f"  - [{finding.severity.value}] {finding.issue_type.value}: {finding.description}")
print()

print("=" * 80)
print("测试完成")
print("=" * 80)
