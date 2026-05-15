#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚类算法实现（纯 Python，无外部依赖）
用于 dasheng-clustering
"""

import json
import re
from collections import Counter
from datetime import datetime
import uuid
import math


class TopicClusterer:
    """话题聚类器（纯 Python 实现）"""
    
    def __init__(self, min_cluster_size=3, max_clusters=20, similarity_threshold=0.5):
        self.min_cluster_size = min_cluster_size
        self.max_clusters = max_clusters
        self.similarity_threshold = similarity_threshold
        self.stop_words = self._load_stop_words()
    
    def _load_stop_words(self):
        """加载停用词"""
        stop_words = {
            '的', '了', '和', '是', '在', '有', '一', '个', '这', '那',
            '我', '你', '他', '她', '它', '们', '我们', '你们', '他们',
            '不', '没', '没有', '很', '太', '非常', '真', '就', '也',
            '还', '又', '再', '更', '最', '比', '被', '把', '给',
            '向', '对', '从', '到', '为', '以', '用', '通过', '经过',
            '但', '可是', '然而', '虽然', '因为', '所以', '如果', '那么',
            '或', '及', '与', '而', '且', '或者', '以及', '等等',
        }
        return stop_words
    
    def _extract_keywords(self, text):
        """提取关键词（字符级 n-gram）"""
        text = text.lower()
        keywords = set()
        
        # 提取 2-3 字符的 n-gram
        for i in range(len(text) - 1):
            if text[i:i+2] not in self.stop_words:
                keywords.add(text[i:i+2])
        
        for i in range(len(text) - 2):
            if text[i:i+3] not in self.stop_words:
                keywords.add(text[i:i+3])
        
        return keywords
    
    def _calculate_similarity(self, text1, text2):
        """计算两个文本的相似度（Jaccard 相似度）"""
        keywords1 = self._extract_keywords(text1)
        keywords2 = self._extract_keywords(text2)
        
        if not keywords1 or not keywords2:
            return 0
        
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        
        return intersection / union if union > 0 else 0
    
    def _preprocess_texts(self, intake_records):
        """预处理文本"""
        texts = []
        for record in intake_records:
            text = record.get('normalized_topic', '') + ' ' + record.get('normalized_summary', '')
            texts.append(text)
        return texts
    
    def cluster(self, intake_records):
        """
        执行聚类（基于相似度的贪心聚类）
        
        Args:
            intake_records: Topic Intake Record 列表
        
        Returns:
            clusters: 聚类结果 {cluster_id: [intake_record, ...]}
        """
        if len(intake_records) < self.min_cluster_size:
            cluster_id = f'cluster-{datetime.now().strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex[:8]}'
            return {cluster_id: intake_records}
        
        # 预处理文本
        texts = self._preprocess_texts(intake_records)
        
        # 计算相似度矩阵
        n = len(texts)
        similarity_matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                sim = self._calculate_similarity(texts[i], texts[j])
                similarity_matrix[i][j] = sim
                similarity_matrix[j][i] = sim
        
        # 贪心聚类：从最相似的对开始合并
        clusters = [[i] for i in range(n)]  # 初始化：每个记录单独成簇
        
        # 迭代合并相似的簇
        iteration = 0
        while len(clusters) > 1 and iteration < 100:
            iteration += 1
            
            # 找到最相似的两个簇
            max_sim = -1
            merge_i, merge_j = -1, -1
            
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    # 计算簇间相似度（取平均）
                    sim_sum = 0
                    count = 0
                    for idx_i in clusters[i]:
                        for idx_j in clusters[j]:
                            sim_sum += similarity_matrix[idx_i][idx_j]
                            count += 1
                    
                    avg_sim = sim_sum / count if count > 0 else 0
                    
                    if avg_sim > max_sim:
                        max_sim = avg_sim
                        merge_i, merge_j = i, j
            
            # 如果最大相似度低于阈值，停止合并
            if max_sim < self.similarity_threshold:
                break
            
            # 合并簇
            clusters[merge_i].extend(clusters[merge_j])
            clusters.pop(merge_j)
            
            # 限制簇数
            if len(clusters) <= self.max_clusters:
                break
        
        # 过滤小簇，组织结果
        result_clusters = {}
        for cluster_indices in clusters:
            if len(cluster_indices) >= self.min_cluster_size:
                cluster_id = f'cluster-{datetime.now().strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex[:8]}'
                cluster_records = [intake_records[i] for i in cluster_indices]
                result_clusters[cluster_id] = cluster_records
        
        # 如果没有有效的簇，返回所有记录作为一个簇
        if not result_clusters:
            cluster_id = f'cluster-{datetime.now().strftime("%Y%m%d-%H%M%S")}-{uuid.uuid4().hex[:8]}'
            result_clusters[cluster_id] = intake_records
        
        return result_clusters
    
    def name_cluster(self, cluster_records):
        """
        为簇自动命名
        
        Args:
            cluster_records: 簇内的 Intake Record 列表
        
        Returns:
            cluster_name: 簇名称
        """
        # 提取所有关键词
        all_keywords = []
        for record in cluster_records:
            text = record.get('normalized_topic', '') + ' ' + record.get('normalized_summary', '')
            keywords = self._extract_keywords(text)
            all_keywords.extend(keywords)
        
        # 计算关键词频率
        keyword_freq = Counter(all_keywords)
        
        # 选择频率最高的 1-2 个关键词
        top_keywords = [kw for kw, _ in keyword_freq.most_common(2)]
        
        if top_keywords:
            cluster_name = ''.join(top_keywords)
        else:
            cluster_name = f'话题簇-{len(cluster_records)}条'
        
        return cluster_name
    
    def generate_cluster_summary(self, cluster_records, cluster_name):
        """
        生成簇摘要
        
        Args:
            cluster_records: 簇内的 Intake Record 列表
            cluster_name: 簇名称
        
        Returns:
            summary: 簇摘要
        """
        # 计算平均优先级
        avg_priority = sum(r.get('priority', 0) for r in cluster_records) / len(cluster_records)
        
        # 计算平台分布
        platform_dist = Counter(r.get('source_channel', '未知') for r in cluster_records)
        
        # 计算质量分布
        quality_dist = Counter(r.get('scoring_breakdown', {}).get('quality_score', 0) for r in cluster_records)
        
        # 提取推荐角度
        recommended_angles = []
        for record in cluster_records[:3]:  # 取前 3 条
            summary = record.get('normalized_summary', '')
            if summary:
                recommended_angles.append(summary[:30])
        
        summary = {
            'cluster_name': cluster_name,
            'cluster_size': len(cluster_records),
            'avg_priority': avg_priority,
            'platform_distribution': dict(platform_dist),
            'quality_distribution': dict(quality_dist),
            'recommended_angles': recommended_angles,
        }
        
        return summary


# 测试
if __name__ == '__main__':
    # 示例数据
    sample_records = [
        {
            'intake_id': 'intake-001',
            'normalized_topic': '美伊战争升级',
            'normalized_summary': '伊朗对美国发动导弹攻击',
            'priority': 85,
            'source_channel': 'douyin',
            'scoring_breakdown': {'quality_score': 95}
        },
        {
            'intake_id': 'intake-002',
            'normalized_topic': '伊朗战争影响',
            'normalized_summary': '中东局势紧张，黄金价格上升',
            'priority': 80,
            'source_channel': 'douyin',
            'scoring_breakdown': {'quality_score': 85}
        },
        {
            'intake_id': 'intake-003',
            'normalized_topic': '康波周期理论',
            'normalized_summary': '中国四十年财富周期规律',
            'priority': 90,
            'source_channel': 'douyin',
            'scoring_breakdown': {'quality_score': 95}
        },
    ]
    
    clusterer = TopicClusterer()
    clusters = clusterer.cluster(sample_records)
    
    print(f"聚类完成：{len(clusters)} 个簇")
    for cluster_id, records in clusters.items():
        cluster_name = clusterer.name_cluster(records)
        summary = clusterer.generate_cluster_summary(records, cluster_name)
        print(f"\n{cluster_name}：{len(records)} 条")
        print(f"  平均优先级：{summary['avg_priority']:.1f}")
        print(f"  平台分布：{summary['platform_distribution']}")
