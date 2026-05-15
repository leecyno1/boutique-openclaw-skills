"""
Integration example: Using Dynamic Risk Assessment in content-brief-builder workflow

This script demonstrates how to integrate the risk assessment algorithm
into the Brief generation process.
"""

from risk_assessment_algorithm import DynamicRiskAssessment, generate_risk_notes, RiskLevel
from typing import Dict, List
import json


class ContentBriefBuilderWithRiskAssessment:
    """Enhanced Content Brief Builder with dynamic risk assessment"""
    
    def __init__(self):
        self.risk_assessor = DynamicRiskAssessment()
    
    def build_brief(self, intake_data: Dict) -> Dict:
        """
        Build a Content Brief with integrated risk assessment
        
        Args:
            intake_data: Topic Intake Record with:
                - working_title
                - content_type_intent
                - target_audience
                - core_claim
                - core_tension
                - angle_candidates
                - recommended_media
                - source_summary (optional)
        
        Returns:
            Complete Content Brief with risk assessment
        """
        
        # Step 1: Normalize input
        brief = self._normalize_intake(intake_data)
        
        # Step 2: Perform dynamic risk assessment
        risk_assessment = self.risk_assessor.assess(brief)
        
        # Step 3: Generate risk notes
        risk_notes_formatted = generate_risk_notes(risk_assessment)
        
        # Step 4: Integrate risk assessment into brief
        brief["risk_assessment"] = {
            "risk_level": risk_assessment.risk_level.value,
            "risk_score": risk_assessment.total_score,
            "risk_breakdown": risk_assessment.breakdown,
            "risk_notes": risk_assessment.risk_notes,
            "improvement_suggestions": risk_assessment.improvement_suggestions,
            "risk_notes_formatted": risk_notes_formatted,
        }
        
        # Step 5: Determine publication readiness
        brief["publication_readiness"] = self._determine_readiness(risk_assessment)
        
        # Step 6: Add workflow recommendations
        brief["next_steps"] = self._recommend_next_steps(risk_assessment)
        
        return brief
    
    def _normalize_intake(self, intake_data: Dict) -> Dict:
        """Normalize intake data to Brief format"""
        return {
            "brief_id": intake_data.get("brief_id", f"brief_{id(intake_data)}"),
            "working_title": intake_data.get("working_title", ""),
            "content_type_intent": intake_data.get("content_type_intent", "general"),
            "target_audience": intake_data.get("target_audience", []),
            "core_claim": intake_data.get("core_claim"),
            "core_tension": intake_data.get("core_tension"),
            "angle_candidates": intake_data.get("angle_candidates", []),
            "recommended_media": intake_data.get("recommended_media", []),
            "source_summary": intake_data.get("source_summary", {}),
        }
    
    def _determine_readiness(self, assessment) -> Dict:
        """Determine publication readiness based on risk level"""
        readiness_map = {
            RiskLevel.LOW: {
                "status": "ready_to_publish",
                "required_review": "none",
                "estimated_time_to_publish": "immediate",
                "notes": "Content is low-risk and can proceed directly to publication"
            },
            RiskLevel.MEDIUM: {
                "status": "needs_editorial_review",
                "required_review": "editorial_team",
                "estimated_time_to_publish": "1-2 days",
                "notes": "Content requires editorial team review before publication"
            },
            RiskLevel.HIGH: {
                "status": "needs_compliance_review",
                "required_review": "legal_compliance",
                "estimated_time_to_publish": "3-5 days",
                "notes": "Content requires legal/compliance review before publication decision"
            }
        }
        return readiness_map[assessment.risk_level]
    
    def _recommend_next_steps(self, assessment) -> List[str]:
        """Recommend next steps based on risk assessment"""
        steps = []
        
        if assessment.risk_level == RiskLevel.LOW:
            steps = [
                "1. Proceed to material-pack-builder for evidence gathering",
                "2. Assign to content writer for draft generation",
                "3. Schedule for publication"
            ]
        elif assessment.risk_level == RiskLevel.MEDIUM:
            steps = [
                "1. Address improvement suggestions from risk assessment",
                "2. Submit to editorial team for review",
                "3. Gather additional evidence as recommended",
                "4. Proceed to material-pack-builder after approval",
                "5. Assign to content writer for draft generation"
            ]
        else:  # HIGH
            steps = [
                "1. URGENT: Address all improvement suggestions",
                "2. Consult with legal/compliance team",
                "3. Consider major content revisions",
                "4. Resubmit for risk assessment after changes",
                "5. Only proceed if risk level improves to MEDIUM or LOW"
            ]
        
        return steps


# Example usage
def example_workflow():
    """Demonstrate the workflow with different risk profiles"""
    
    builder = ContentBriefBuilderWithRiskAssessment()
    
    # Example 1: Low-risk content
    low_risk_intake = {
        "brief_id": "brief_001",
        "working_title": "春季居家整理指南",
        "content_type_intent": "article",
        "target_audience": ["general_adults", "homemakers"],
        "core_claim": "通过简单的整理方法改善居家环境",
        "core_tension": "忙碌生活中如何找到整理时间",
        "angle_candidates": [
            {
                "angle_name": "15分钟快速整理法",
                "evidence_needed": ["整理师访谈", "用户案例"]
            }
        ],
        "recommended_media": ["article_wechat", "image_post"],
        "source_summary": {
            "representative_sources": ["整理师博客"]
        }
    }
    
    print("=" * 80)
    print("EXAMPLE 1: Low-Risk Content")
    print("=" * 80)
    brief_1 = builder.build_brief(low_risk_intake)
    print_brief_summary(brief_1)
    
    # Example 2: Medium-risk content
    medium_risk_intake = {
        "brief_id": "brief_002",
        "working_title": "2026年基金投资策略",
        "content_type_intent": "article",
        "target_audience": ["young_professionals", "investors"],
        "core_claim": "通过科学选基能获得稳定收益",
        "core_tension": "市场波动下如何选择基金",
        "angle_candidates": [
            {
                "angle_name": "基金类型对比分析",
                "evidence_needed": ["历史收益数据", "基金经理背景"]
            }
        ],
        "recommended_media": ["article_wechat", "video_script"],
        "source_summary": {}
    }
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Medium-Risk Content")
    print("=" * 80)
    brief_2 = builder.build_brief(medium_risk_intake)
    print_brief_summary(brief_2)
    
    # Example 3: High-risk content
    high_risk_intake = {
        "brief_id": "brief_003",
        "working_title": "某草本配方能治疗糖尿病",
        "content_type_intent": "article",
        "target_audience": ["elderly", "patients"],
        "core_claim": "这个配方能100%治愈糖尿病，已被证明有效",
        "core_tension": "传统医学vs现代医学的对比",
        "angle_candidates": [
            {
                "angle_name": "古方新用",
                "evidence_needed": []
            }
        ],
        "recommended_media": ["article_wechat", "douyin"],
        "source_summary": {}
    }
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: High-Risk Content")
    print("=" * 80)
    brief_3 = builder.build_brief(high_risk_intake)
    print_brief_summary(brief_3)


def print_brief_summary(brief: Dict):
    """Pretty print brief summary with risk assessment"""
    print(f"\n📋 Brief: {brief['working_title']}")
    print(f"   ID: {brief['brief_id']}")
    print(f"   Type: {brief['content_type_intent']}")
    print(f"   Audience: {', '.join(brief['target_audience'])}")
    
    risk = brief["risk_assessment"]
    print(f"\n⚠️  Risk Assessment:")
    print(f"   Level: {risk['risk_level'].upper()}")
    print(f"   Score: {risk['risk_score']}/70")
    print(f"   Breakdown: {risk['risk_breakdown']}")
    
    if risk["risk_notes"]:
        print(f"\n   Risks:")
        for note in risk["risk_notes"]:
            print(f"     • {note}")
    
    if risk["improvement_suggestions"]:
        print(f"\n   Improvements:")
        for suggestion in risk["improvement_suggestions"]:
            print(f"     • {suggestion}")
    
    readiness = brief["publication_readiness"]
    print(f"\n📊 Publication Readiness:")
    print(f"   Status: {readiness['status']}")
    print(f"   Required Review: {readiness['required_review']}")
    print(f"   Time to Publish: {readiness['estimated_time_to_publish']}")
    print(f"   Notes: {readiness['notes']}")
    
    print(f"\n📝 Next Steps:")
    for step in brief["next_steps"]:
        print(f"   {step}")


if __name__ == "__main__":
    example_workflow()
