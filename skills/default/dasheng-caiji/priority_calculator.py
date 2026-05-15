#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority 计算公式实现
用于 dasheng-caiji
"""

def calculate_priority(platform_score, quality_score, freshness_score, relevance_score):
    """
    计算最终优先级
    
    Args:
        platform_score: 互动数据评分 0-100
        quality_score: 平台评级 0-100
        freshness_score: 时效性评分 0-100
        relevance_score: 关键词匹配评分 0-100
    
    Returns:
        priority: 最终优先级 0-100
    """
    priority = (
        platform_score * 0.4 +
        quality_score * 0.35 +
        freshness_score * 0.15 +
        relevance_score * 0.1
    )
    return min(100, max(0, priority))


def calculate_platform_score(like_count, collect_count, share_count, comment_count, max_interaction=100000):
    """
    计算互动数据评分
    
    Args:
        like_count: 赞数
        collect_count: 收藏数
        share_count: 分享数
        comment_count: 评论数
        max_interaction: 最大互动数（用于归一化）
    
    Returns:
        platform_score: 0-100
    """
    total_interaction = (
        like_count * 0.25 +
        collect_count * 0.35 +
        share_count * 0.25 +
        comment_count * 0.15
    )
    platform_score = min(100, (total_interaction / max_interaction) * 100)
    return platform_score


def calculate_quality_score(rating):
    """
    计算平台评级分数
    
    Args:
        rating: 评级 'S', 'A', 'B', 'C'
    
    Returns:
        quality_score: 0-100
    """
    rating_map = {
        'S': 95,
        'A': 85,
        'B': 60,
        'C': 35,
    }
    return rating_map.get(rating, 0)


def calculate_freshness_score(hours_ago):
    """
    计算时效性评分
    
    Args:
        hours_ago: 发布距离现在的小时数
    
    Returns:
        freshness_score: 0-100
    """
    if hours_ago <= 6:
        return 100
    elif hours_ago <= 24:
        return 80
    elif hours_ago <= 72:
        return 60
    else:
        return 30


def calculate_relevance_score(title, summary, keywords):
    """
    计算关键词匹配评分
    
    Args:
        title: 标题
        summary: 摘要
        keywords: 关键词列表
    
    Returns:
        relevance_score: 0-100
    """
    if not keywords:
        return 0
    
    text = (title + summary).lower()
    matched_keywords = sum(1 for kw in keywords if kw.lower() in text)
    relevance_score = (matched_keywords / len(keywords)) * 100
    return min(100, relevance_score)


# 测试
if __name__ == '__main__':
    # 示例 1：高质量内容
    ps = calculate_platform_score(40100, 27000, 19700, 5000)
    qs = calculate_quality_score('S')
    fs = calculate_freshness_score(2)
    rs = calculate_relevance_score(
        '神秘的数字7，藏着中国四十年的财富周期规律！',
        '康波周期理论分析',
        ['康波', '周期', '财富']
    )
    priority = calculate_priority(ps, qs, fs, rs)
    print(f"示例 1（高质量）：priority={priority:.1f}")
    
    # 示例 2：低质量内容
    ps = calculate_platform_score(100, 50, 30, 10)
    qs = calculate_quality_score('C')
    fs = calculate_freshness_score(120)
    rs = calculate_relevance_score('随机内容', '无关摘要', ['康波'])
    priority = calculate_priority(ps, qs, fs, rs)
    print(f"示例 2（低质量）：priority={priority:.1f}")
