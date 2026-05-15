"""
Dynamic Risk Assessment Algorithm for Content Brief

Evaluates content risk based on:
- Content type sensitivity
- Target audience vulnerability
- Platform policy constraints
- Claims credibility
- Data evidence quality
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class RiskAssessment:
    """Risk assessment result"""
    risk_level: RiskLevel
    total_score: int
    breakdown: Dict[str, int]  # Component scores
    risk_notes: List[str]  # Specific risk warnings
    improvement_suggestions: List[str]  # How to mitigate


class ContentTypeRiskEvaluator:
    """Evaluates content type sensitivity"""
    
    SENSITIVE_TYPES = {
        "financial": 20,      # Investment, trading, financial advice
        "medical": 20,        # Health, medical advice, treatments
        "educational": 15,    # Credentials, qualifications claims
        "legal": 20,          # Legal advice, compliance
        "political": 15,      # Political opinions, elections
        "religious": 10,      # Religious content
        "general": 0,         # News, entertainment, lifestyle
    }
    
    def evaluate(self, content_type: str) -> Tuple[int, str]:
        """
        Returns: (score, category)
        """
        content_type_lower = content_type.lower()
        for key, score in self.SENSITIVE_TYPES.items():
            if key in content_type_lower:
                return score, key
        return 0, "general"


class AudienceRiskEvaluator:
    """Evaluates target audience vulnerability"""
    
    VULNERABLE_AUDIENCES = {
        "minors": 15,           # Children, teenagers
        "elderly": 12,          # Senior citizens
        "low_literacy": 12,     # Limited education background
        "vulnerable_groups": 15, # Disabled, marginalized communities
        "general": 0,           # General adult audience
    }
    
    def evaluate(self, target_audience: List[str]) -> Tuple[int, List[str]]:
        """
        Returns: (max_score, matched_categories)
        """
        if not target_audience:
            return 0, []
        
        matched = []
        max_score = 0
        
        audience_str = " ".join(target_audience).lower()
        for key, score in self.VULNERABLE_AUDIENCES.items():
            if key in audience_str or any(key.replace("_", " ") in aud.lower() for aud in target_audience):
                matched.append(key)
                max_score = max(max_score, score)
        
        return max_score, matched


class MediaRiskEvaluator:
    """Evaluates platform policy constraints"""
    
    PLATFORM_RESTRICTIONS = {
        "wechat": 10,           # WeChat has strict content policies
        "douyin": 12,           # Douyin/TikTok algorithm sensitivity
        "xiaohongshu": 8,       # Xiaohongshu community guidelines
        "weibo": 10,            # Weibo political sensitivity
        "youtube": 5,           # YouTube relatively permissive
        "blog": 3,              # Personal blog minimal restrictions
        "general": 0,           # No specific platform
    }
    
    def evaluate(self, recommended_media: List[str]) -> Tuple[int, List[str]]:
        """
        Returns: (max_score, matched_platforms)
        """
        if not recommended_media:
            return 0, []
        
        matched = []
        max_score = 0
        
        for media in recommended_media:
            media_lower = media.lower()
            for platform, score in self.PLATFORM_RESTRICTIONS.items():
                if platform in media_lower:
                    matched.append(platform)
                    max_score = max(max_score, score)
        
        return max_score, matched


class ClaimsRiskEvaluator:
    """Evaluates claim credibility and over-promising"""
    
    RISKY_KEYWORDS = {
        "guarantee": 15,
        "cure": 15,
        "proven": 10,
        "100%": 15,
        "never": 10,
        "always": 10,
        "best": 8,
        "only": 8,
        "must": 8,
    }
    
    def evaluate(self, core_claim: Optional[str], core_tension: Optional[str]) -> Tuple[int, List[str]]:
        """
        Returns: (score, risky_keywords_found)
        """
        if not core_claim:
            return 0, []
        
        claim_text = (core_claim + " " + (core_tension or "")).lower()
        found_keywords = []
        score = 0
        
        for keyword, keyword_score in self.RISKY_KEYWORDS.items():
            if keyword in claim_text:
                found_keywords.append(keyword)
                score = max(score, keyword_score)
        
        return score, found_keywords


class DataRiskEvaluator:
    """Evaluates data evidence quality"""
    
    def evaluate(self, angle_candidates: List[Dict], evidence_provided: bool = False) -> Tuple[int, List[str]]:
        """
        Returns: (score, issues)
        """
        issues = []
        score = 0
        
        if not angle_candidates:
            issues.append("No angle candidates defined")
            score = 10
        else:
            # Check if angles have evidence_needed
            angles_without_evidence = 0
            for angle in angle_candidates:
                if isinstance(angle, dict):
                    evidence_needed = angle.get("evidence_needed", [])
                    if not evidence_needed:
                        angles_without_evidence += 1
            
            if angles_without_evidence == len(angle_candidates):
                issues.append("No evidence requirements specified for any angle")
                score = 10
            elif angles_without_evidence > 0:
                issues.append(f"{angles_without_evidence}/{len(angle_candidates)} angles lack evidence specification")
                score = 5
        
        if not evidence_provided:
            issues.append("No evidence sources provided yet")
            score = max(score, 5)
        
        return score, issues


class DynamicRiskAssessment:
    """Main risk assessment orchestrator"""
    
    def __init__(self):
        self.content_type_eval = ContentTypeRiskEvaluator()
        self.audience_eval = AudienceRiskEvaluator()
        self.media_eval = MediaRiskEvaluator()
        self.claims_eval = ClaimsRiskEvaluator()
        self.data_eval = DataRiskEvaluator()
    
    def assess(self, brief: Dict) -> RiskAssessment:
        """
        Main assessment method
        
        Args:
            brief: Content Brief object with fields:
                - content_type_intent
                - target_audience
                - recommended_media
                - core_claim
                - core_tension
                - angle_candidates
                - source_summary (optional)
        
        Returns:
            RiskAssessment with level, score, breakdown, notes, and suggestions
        """
        breakdown = {}
        risk_notes = []
        improvement_suggestions = []
        
        # 1. Content Type Risk
        content_type = brief.get("content_type_intent", "general")
        content_score, content_category = self.content_type_eval.evaluate(content_type)
        breakdown["content_type"] = content_score
        
        if content_score > 0:
            risk_notes.append(f"Sensitive content type: {content_category}")
            improvement_suggestions.append(f"Add disclaimers appropriate for {content_category} content")
        
        # 2. Audience Risk
        target_audience = brief.get("target_audience", [])
        audience_score, audience_categories = self.audience_eval.evaluate(target_audience)
        breakdown["audience"] = audience_score
        
        if audience_score > 0:
            risk_notes.append(f"Vulnerable audience detected: {', '.join(audience_categories)}")
            improvement_suggestions.append("Ensure content is age-appropriate and accessible")
        
        # 3. Media Risk
        recommended_media = brief.get("recommended_media", [])
        media_score, platforms = self.media_eval.evaluate(recommended_media)
        breakdown["media"] = media_score
        
        if media_score > 0:
            risk_notes.append(f"Platform policy constraints: {', '.join(platforms)}")
            improvement_suggestions.append(f"Review platform guidelines for {', '.join(set(platforms))}")
        
        # 4. Claims Risk
        core_claim = brief.get("core_claim")
        core_tension = brief.get("core_tension")
        claims_score, risky_keywords = self.claims_eval.evaluate(core_claim, core_tension)
        breakdown["claims"] = claims_score
        
        if claims_score > 0:
            risk_notes.append(f"Over-promising language detected: {', '.join(risky_keywords)}")
            improvement_suggestions.append("Soften absolute claims with qualifiers like 'may', 'can help', 'suggests'")
        
        # 5. Data Risk
        angle_candidates = brief.get("angle_candidates", [])
        source_summary = brief.get("source_summary", {})
        evidence_provided = bool(source_summary.get("representative_sources"))
        
        data_score, data_issues = self.data_eval.evaluate(angle_candidates, evidence_provided)
        breakdown["data"] = data_score
        
        if data_score > 0:
            for issue in data_issues:
                risk_notes.append(f"Data quality concern: {issue}")
            improvement_suggestions.append("Gather and cite authoritative sources before publishing")
        
        # Calculate total score and determine level
        total_score = sum(breakdown.values())
        risk_level = self._score_to_level(total_score)
        
        # Add general mitigation suggestions based on risk level
        if risk_level == RiskLevel.HIGH:
            improvement_suggestions.append("Consider legal/compliance review before publication")
        elif risk_level == RiskLevel.MEDIUM:
            improvement_suggestions.append("Review content with editorial team before publication")
        
        return RiskAssessment(
            risk_level=risk_level,
            total_score=total_score,
            breakdown=breakdown,
            risk_notes=risk_notes,
            improvement_suggestions=improvement_suggestions,
        )
    
    @staticmethod
    def _score_to_level(score: int) -> RiskLevel:
        """Convert numeric score to risk level"""
        if score >= 40:
            return RiskLevel.HIGH
        elif score >= 20:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW


def generate_risk_notes(assessment: RiskAssessment) -> List[str]:
    """
    Generate human-readable risk notes from assessment
    
    Returns list of formatted risk notes with suggestions
    """
    notes = []
    
    # Header
    notes.append(f"⚠️ Risk Level: {assessment.risk_level.value.upper()} (Score: {assessment.total_score}/70)")
    notes.append("")
    
    # Risk breakdown
    if assessment.risk_notes:
        notes.append("🔍 Identified Risks:")
        for note in assessment.risk_notes:
            notes.append(f"  • {note}")
        notes.append("")
    
    # Improvement suggestions
    if assessment.improvement_suggestions:
        notes.append("✅ Improvement Suggestions:")
        for suggestion in assessment.improvement_suggestions:
            notes.append(f"  • {suggestion}")
    
    return notes
