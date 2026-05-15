#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险评估实现（简化版）
用于 dasheng-brief-builder
"""


class RiskAssessor:
    """风险评估器"""
    
    def __init__(self):
        self.sensitive_keywords = {
            'high': ['投资产品', '医疗', '健康建议', '法律建议', '必涨', '必跌'],
            'medium': ['投资', '政策', '经济', '建议'],
        }
    
    def assess_content_sensitivity(self, brief):
        """
        评估内容敏感性
        
        Args:
            brief: Content Brief
        
        Returns:
            sensitivity: 'low' | 'medium' | 'high'
        """
        topic = brief.get('topic_name', '').lower()
        judgment = brief.get('core_judgment', '').lower()
        text = topic + ' ' + judgment
        
        # 检查高敏感关键词
        for keyword in self.sensitive_keywords['high']:
            if keyword in text:
                return 'high'
        
        # 检查中敏感关键词
        for keyword in self.sensitive_keywords['medium']:
            if keyword in text:
                return 'medium'
        
        return 'low'
    
    def assess_evidence_quality(self, brief):
        """
        评估证据质量
        
        Args:
            brief: Content Brief
        
        Returns:
            quality: 'low' | 'medium' | 'high'
        """
        source_summary = brief.get('source_summary', {})
        
        # 检查来源数量
        representative_sources = source_summary.get('representative_sources', [])
        source_count = len(representative_sources)
        
        if source_count >= 3:
            return 'high'
        elif source_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def assess_platform_compliance(self, brief):
        """
        评估平台合规性
        
        Args:
            brief: Content Brief
        
        Returns:
            compliance: 'low' | 'medium' | 'high'
        """
        judgment = brief.get('core_judgment', '').lower()
        
        # 检查绝对化表述
        absolute_words = ['必', '一定', '肯定', '绝对', '100%', '保证']
        for word in absolute_words:
            if word in judgment:
                return 'low'
        
        # 检查虚假宣传词
        false_claim_words = ['最好', '最强', '无敌', '完美']
        for word in false_claim_words:
            if word in judgment:
                return 'medium'
        
        return 'high'
    
    def generate_risk_notes(self, sensitivity, quality, compliance):
        """
        生成风险说明
        
        Args:
            sensitivity: 内容敏感性
            quality: 证据质量
            compliance: 平台合规性
        
        Returns:
            risk_notes: 风险说明文本
        """
        notes = []
        
        if sensitivity == 'high':
            notes.append('内容涉及敏感话题，需要谨慎处理')
        elif sensitivity == 'medium':
            notes.append('内容涉及投资/政策等话题，需要添加免责声明')
        
        if quality == 'low':
            notes.append('证据不足，需要补充数据支撑')
        elif quality == 'medium':
            notes.append('证据相对充分，但可以进一步补强')
        
        if compliance == 'low':
            notes.append('存在平台政策风险，需要修改表述')
        elif compliance == 'medium':
            notes.append('需要标注信息来源和免责声明')
        
        return '；'.join(notes) if notes else '无风险'
    
    def generate_improvement_suggestions(self, sensitivity, quality, compliance):
        """
        生成改进建议
        
        Args:
            sensitivity: 内容敏感性
            quality: 证据质量
            compliance: 平台合规性
        
        Returns:
            suggestions: 改进建议列表
        """
        suggestions = []
        
        if quality == 'low':
            suggestions.append('补充最新的数据和案例')
            suggestions.append('引用权威来源（官方数据、研究报告等）')
        
        if compliance == 'low':
            suggestions.append('避免使用绝对化表述（必、一定、保证等）')
            suggestions.append('添加免责声明')
        elif compliance == 'medium':
            suggestions.append('标注信息来源')
            suggestions.append('添加"仅供参考"等免责语言')
        
        if sensitivity == 'high':
            suggestions.append('咨询法务或合规团队')
        
        return suggestions
    
    def assess(self, brief):
        """
        执行完整的风险评估
        
        Args:
            brief: Content Brief
        
        Returns:
            risk_assessment: 风险评估结果
        """
        sensitivity = self.assess_content_sensitivity(brief)
        quality = self.assess_evidence_quality(brief)
        compliance = self.assess_platform_compliance(brief)
        
        risk_assessment = {
            'content_sensitivity': sensitivity,
            'evidence_quality': quality,
            'platform_compliance': compliance,
            'risk_notes': self.generate_risk_notes(sensitivity, quality, compliance),
            'improvement_suggestions': self.generate_improvement_suggestions(sensitivity, quality, compliance),
        }
        
        return risk_assessment


# 测试
if __name__ == '__main__':
    assessor = RiskAssessor()
    
    # 示例 Brief
    sample_brief = {
        'topic_name': '黄金投资',
        'core_judgment': '黄金价格将继续上升，是投资的好机会',
        'source_summary': {
            'representative_sources': [
                {'url': 'https://example.com/1'},
                {'url': 'https://example.com/2'},
            ]
        }
    }
    
    risk_assessment = assessor.assess(sample_brief)
    print("风险评估结果：")
    for key, value in risk_assessment.items():
        print(f"  {key}: {value}")
