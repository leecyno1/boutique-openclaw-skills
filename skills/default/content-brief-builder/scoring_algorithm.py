"""
Dynamic Production Value Scoring Algorithm for Content Brief

Evaluates content production value based on:
- Base score: 50 points
- Angle quantity reward: +10 per angle (max +30)
- Media quantity reward: +5 per media (max +25)
- Complexity reward: low +0, medium +10, high +15
- Risk penalty: low -0, medium -5, high -15
- Target audience reward: +3 per audience (max +15)

Final score range: 0-100
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ComplexityLevel(Enum):
    """Content complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ScoringBreakdown:
    """Detailed scoring breakdown"""
    base_score: int
    angle_reward: int
    media_reward: int
    complexity_reward: int
    risk_penalty: int
    audience_reward: int
    final_score: int
    
    def to_dict(self) -> Dict:
        return {
            "base_score": self.base_score,
            "angle_reward": self.angle_reward,
            "media_reward": self.media_reward,
            "complexity_reward": self.complexity_reward,
            "risk_penalty": self.risk_penalty,
            "audience_reward": self.audience_reward,
            "final_score": self.final_score,
        }


class ProductionValueScorer:
    """Calculates dynamic production value score for Content Brief"""
    
    # Scoring constants
    BASE_SCORE = 50
    ANGLE_REWARD_PER_ITEM = 10
    ANGLE_REWARD_MAX = 30
    MEDIA_REWARD_PER_ITEM = 5
    MEDIA_REWARD_MAX = 25
    AUDIENCE_REWARD_PER_ITEM = 3
    AUDIENCE_REWARD_MAX = 15
    
    COMPLEXITY_REWARDS = {
        ComplexityLevel.LOW: 0,
        ComplexityLevel.MEDIUM: 10,
        ComplexityLevel.HIGH: 15,
    }
    
    RISK_PENALTIES = {
        RiskLevel.LOW: 0,
        RiskLevel.MEDIUM: 5,
        RiskLevel.HIGH: 15,
    }
    
    def score(
        self,
        angle_count: int,
        media_count: int,
        complexity: str,
        risk_level: str,
        audience_count: int,
    ) -> ScoringBreakdown:
        """
        Calculate production value score for a Brief.
        
        Args:
            angle_count: Number of angle candidates
            media_count: Number of recommended media types
            complexity: Complexity level ('low', 'medium', 'high')
            risk_level: Risk level ('low', 'medium', 'high')
            audience_count: Number of target audiences
            
        Returns:
            ScoringBreakdown with detailed scoring information
        """
        
        # Validate inputs
        angle_count = max(0, angle_count)
        media_count = max(0, media_count)
        audience_count = max(0, audience_count)
        
        # Parse complexity level
        try:
            complexity_enum = ComplexityLevel(complexity.lower())
        except ValueError:
            complexity_enum = ComplexityLevel.LOW
        
        # Parse risk level
        try:
            risk_enum = RiskLevel(risk_level.lower())
        except ValueError:
            risk_enum = RiskLevel.LOW
        
        # Calculate components
        base = self.BASE_SCORE
        
        # Angle reward (capped at max)
        angle_reward = min(
            angle_count * self.ANGLE_REWARD_PER_ITEM,
            self.ANGLE_REWARD_MAX
        )
        
        # Media reward (capped at max)
        media_reward = min(
            media_count * self.MEDIA_REWARD_PER_ITEM,
            self.MEDIA_REWARD_MAX
        )
        
        # Complexity reward
        complexity_reward = self.COMPLEXITY_REWARDS[complexity_enum]
        
        # Risk penalty
        risk_penalty = self.RISK_PENALTIES[risk_enum]
        
        # Audience reward (capped at max)
        audience_reward = min(
            audience_count * self.AUDIENCE_REWARD_PER_ITEM,
            self.AUDIENCE_REWARD_MAX
        )
        
        # Calculate final score (0-100 range)
        final_score = (
            base
            + angle_reward
            + media_reward
            + complexity_reward
            + audience_reward
            - risk_penalty
        )
        
        # Clamp to 0-100 range
        final_score = max(0, min(100, final_score))
        
        return ScoringBreakdown(
            base_score=base,
            angle_reward=angle_reward,
            media_reward=media_reward,
            complexity_reward=complexity_reward,
            risk_penalty=risk_penalty,
            audience_reward=audience_reward,
            final_score=final_score,
        )
    
    def score_from_brief(self, brief: Dict) -> ScoringBreakdown:
        """
        Calculate production value score from a Brief object.
        
        Args:
            brief: Content Brief dictionary with required fields
            
        Returns:
            ScoringBreakdown with detailed scoring information
        """
        
        # Extract fields from brief
        angle_count = len(brief.get("angle_candidates", []))
        media_count = len(brief.get("recommended_media", []))
        complexity = brief.get("complexity", "low")
        risk_level = brief.get("risk_level", "low")
        audience_count = len(brief.get("target_audience", []))
        
        return self.score(
            angle_count=angle_count,
            media_count=media_count,
            complexity=complexity,
            risk_level=risk_level,
            audience_count=audience_count,
        )


def calculate_production_value_score(brief: Dict) -> int:
    """
    Convenience function to calculate production value score.
    
    Args:
        brief: Content Brief dictionary
        
    Returns:
        Production value score (0-100)
    """
    scorer = ProductionValueScorer()
    breakdown = scorer.score_from_brief(brief)
    return breakdown.final_score
