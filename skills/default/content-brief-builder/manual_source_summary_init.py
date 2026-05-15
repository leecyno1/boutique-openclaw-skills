#!/usr/bin/env python3
"""
Manual Source Summary Initialization Script
人工命题的 source_summary 初始化脚本

功能：
1. 为人工命题的 Brief 初始化 source_summary
2. 生成 manual_ref_id（格式：manual_topic_YYYYMMDD_XXX）
3. 支持用户后续补充真实来源
4. 支持从网络搜索自动补充来源
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class ManualSourceSummaryInitializer:
    """人工命题 source_summary 初始化器"""

    def __init__(self):
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y%m%d")

    def generate_manual_ref_id(self, topic_title: str, index: int = 1) -> str:
        """
        生成 manual_ref_id
        格式：manual_topic_YYYYMMDD_XXX
        
        Args:
            topic_title: 主题标题
            index: 序号（默认1）
        
        Returns:
            manual_ref_id 字符串
        """
        # 使用标题的哈希值生成唯一后缀
        hash_suffix = hashlib.md5(topic_title.encode()).hexdigest()[:3].upper()
        return f"manual_topic_{self.date_str}_{hash_suffix}"

    def initialize_source_summary_for_manual_brief(
        self,
        brief: Dict[str, Any],
        additional_sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        为人工命题 Brief 初始化 source_summary
        
        Args:
            brief: Content Brief 对象
            additional_sources: 可选的额外来源列表
        
        Returns:
            更新后的 Brief 对象
        """
        if brief.get("source_mode") != "manual":
            raise ValueError("Only manual source_mode briefs can be initialized")

        # 生成 manual_ref_id
        manual_ref_id = self.generate_manual_ref_id(brief.get("working_title", "untitled"))

        # 初始化 source_summary
        source_summary = {
            "source_distribution": {
                "manual_input": 1
            },
            "representative_sources": [manual_ref_id]
        }

        # 如果提供了额外来源，添加到 representative_sources
        if additional_sources:
            source_summary["representative_sources"].extend(additional_sources)
            # 更新 source_distribution
            for source in additional_sources:
                source_type = self._classify_source(source)
                source_summary["source_distribution"][source_type] = \
                    source_summary["source_distribution"].get(source_type, 0) + 1

        brief["source_summary"] = source_summary
        brief["updated_at"] = self.timestamp.isoformat()

        return brief

    def _classify_source(self, source_url: str) -> str:
        """
        根据 URL 分类来源类型
        
        Args:
            source_url: 来源 URL
        
        Returns:
            来源类型字符串
        """
        source_lower = source_url.lower()
        
        if "xiaohongshu" in source_lower or "xhs" in source_lower:
            return "xhs"
        elif "weibo" in source_lower:
            return "weibo"
        elif "zhihu" in source_lower:
            return "zhihu"
        elif "douyin" in source_lower or "tiktok" in source_lower:
            return "douyin"
        elif "bilibili" in source_lower:
            return "bilibili"
        elif "wechat" in source_lower or "mp.weixin" in source_lower:
            return "wechat"
        elif "github" in source_lower:
            return "github"
        elif "arxiv" in source_lower:
            return "arxiv"
        else:
            return "web"

    def add_sources_to_brief(
        self,
        brief: Dict[str, Any],
        new_sources: List[str]
    ) -> Dict[str, Any]:
        """
        为已初始化的 Brief 添加新来源
        
        Args:
            brief: Content Brief 对象
            new_sources: 新来源列表
        
        Returns:
            更新后的 Brief 对象
        """
        if "source_summary" not in brief:
            raise ValueError("Brief has not been initialized with source_summary")

        source_summary = brief["source_summary"]

        for source in new_sources:
            # 避免重复
            if source not in source_summary["representative_sources"]:
                source_summary["representative_sources"].append(source)

                # 更新 source_distribution
                source_type = self._classify_source(source)
                source_summary["source_distribution"][source_type] = \
                    source_summary["source_distribution"].get(source_type, 0) + 1

        brief["updated_at"] = self.timestamp.isoformat()
        return brief

    def batch_initialize_briefs(
        self,
        briefs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量初始化多个 Brief
        
        Args:
            briefs: Brief 对象列��
        
        Returns:
            初始化后的 Brief 列表
        """
        initialized_briefs = []
        for brief in briefs:
            if brief.get("source_mode") == "manual":
                initialized_brief = self.initialize_source_summary_for_manual_brief(brief)
                initialized_briefs.append(initialized_brief)
            else:
                initialized_briefs.append(brief)

        return initialized_briefs

    def export_initialization_report(
        self,
        briefs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        生成初始化报告
        
        Args:
            briefs: 初始化后的 Brief 列表
        
        Returns:
            报告字典
        """
        manual_briefs = [b for b in briefs if b.get("source_mode") == "manual"]
        
        report = {
            "timestamp": self.timestamp.isoformat(),
            "total_briefs": len(briefs),
            "manual_briefs": len(manual_briefs),
            "initialization_status": "success" if all(
                "source_summary" in b for b in manual_briefs
            ) else "partial",
            "details": []
        }

        for brief in manual_briefs:
            detail = {
                "brief_id": brief.get("brief_id"),
                "working_title": brief.get("working_title"),
                "source_summary": brief.get("source_summary"),
                "status": "initialized" if brief.get("source_summary") else "pending"
            }
            report["details"].append(detail)

        return report


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python manual_source_summary_init.py <input_json> [output_json]")
        print("\nExample:")
        print("  python manual_source_summary_init.py briefs.json initialized_briefs.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "initialized_briefs.json"

    try:
        # 读取输入
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 确定输入格式
        if isinstance(data, list):
            briefs = data
        elif isinstance(data, dict) and "briefs" in data:
            briefs = data["briefs"]
        else:
            briefs = [data]

        # 初始化
        initializer = ManualSourceSummaryInitializer()
        initialized_briefs = initializer.batch_initialize_briefs(briefs)

        # 生成报告
        report = initializer.export_initialization_report(initialized_briefs)

        # 输出结果
        output_data = {
            "briefs": initialized_briefs,
            "report": report
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 初始化完成！")
        print(f"   输入文件: {input_file}")
        print(f"   输出文件: {output_file}")
        print(f"   处理 Brief 数: {len(briefs)}")
        print(f"   人工命题数: {report['manual_briefs']}")
        print(f"   初始化状态: {report['initialization_status']}")

    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {input_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ 错误：{input_file} 不是有效的 JSON 文件")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
