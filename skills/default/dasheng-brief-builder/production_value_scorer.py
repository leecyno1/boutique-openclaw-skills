#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产价值评分实现（简化版）
用于 dasheng-brief-builder
"""


class ProductionValueScorer:
    """生产价值评分器"""
    
    def score_content_depth(self, angle_count):
        """
        评分内容深度（基于角度数量）
        
        Args:
            angle_count: 角度数量
        
        Returns:
            score: 0-100
        """
        if angle_count <= 0:
            return 0
        elif angle_count == 1:
            return 30
        elif angle_count == 2:
            return 50
        elif angle_count == 3:
            return 70
        elif angle_count == 4:
            return 85
        else:  # 5+
            return 100
    
    def score_media_diversity(self, media_count):
        """
        评分媒介多样性（基于推荐媒介数量）
        
        Args:
            media_count: 推荐媒介数量
        
        Returns:
            score: 0-100
        """
        if media_count <= 0:
            return 0
        elif media_count == 1:
            return 30
        elif media_count == 2:
            return 60
        else:  # 3+
            return 100
    
    def score_audience_reach(self, audience_count, platform_count):
        """
        评分受众覆盖面（基于受众数量和平台数量）
        
        Args:
            audience_count: 目标受众数量
            platform_count: 适配平台数量
        
        Returns:
            score: 0-100
        """
        total_reach = audience_count + platform_count
        
        if total_reach <= 1:
            return 30
        elif total_reach <= 3:
            return 60
        else:  # 4+
            return 100
    
    def calculate_production_value_score(self, brief):
        """
        计算生产价值评分
        
        Args:
            brief: Content Brief
        
        Returns:
            score: 0-100
        """
        # 提取数据
        angle_candidates = brief.get('angle_candidates', [])
        recommended_media = brief.get('recommended_media', [])
        platform_adaptation = brief.get('platform_adaptation', {})
        
        angle_count = len(angle_candidates)
        media_count = len(recommended_media)
        
        # 计算平台适配数（high 或 medium 的平台数）
        platform_count = sum(
            1 for v in platform_adaptation.values()
            if v in ['high', 'medium']
        )
        
        # 计算受众数（假设每个角度对应一个受众）
        audience_count = min(angle_count, 3)
        
        # 评分各维度
        content_depth_score = self.score_content_depth(angle_count)
        media_diversity_score = self.score_media_diversity(media_count)
        audience_reach_score = self.score_audience_reach(audience_count, platform_count)
        
        # 加权计算
        production_value_score = (
            content_depth_score * 0.4 +
            media_diversity_score * 0.3 +
            audience_reach_score * 0.3
        )
        
        return {
            'production_value_score': min(100, max(0, production_value_score)),
            'score_breakdown': {
                'content_depth': content_depth_score,
                'media_diversity': media_diversity_score,
                'audience_reach': audience_reach_score,
            }
        }


# 测试
if __name__ == '__main__':
    scorer = ProductionValueScorer()
    
    # 示例 Brief
    sample_brief = {
        'angle_candidates': [
            '康波周期的历史规律与预测',
            '康波周期与个人财富的关系',
            '如何在周期中把握机会',
        ],
        'recommended_media': ['article', 'video'],
        'platform_adaptation': {
            'douyin': 'high',
            'xhs': 'medium',
            'bili': 'low',
            'wb': 'low',
            'x': 'low',
        }
    }
    
    result = scorer.calculate_production_value_score(sample_brief)
    print("生产价值评分结果：")
    print(f"  总分：{result['production_value_score']:.1f}")
    print(f"  内容深度：{result['score_breakdown']['content_depth']:.1f}")
    print(f"  媒介多样性：{result['score_breakdown']['media_diversity']:.1f}")
    print(f"  受众覆盖面：{result['score_breakdown']['audience_reach']:.1f}")
