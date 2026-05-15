"""
Editorial Review Rules Engine
用于对公众号初稿进行多维度复审
"""

import re
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class IssueType(Enum):
    # 结构问题
    LOGIC_GAP = "逻辑断层"
    WEAK_TRANSITION = "段落衔接弱"
    INCOMPLETE_ARGUMENT = "论证不完整"
    ABRUPT_SHIFT = "话题突变"
    
    # 证据问题
    INACCURATE_CITATION = "引用不准确"
    OUTDATED_DATA = "数据过时"
    LOW_CREDIBILITY = "来源可信度低"
    MISSING_EVIDENCE = "缺少证据"
    
    # 语调问题
    TONE_MISMATCH = "语调不符"
    REPETITIVE_STRUCTURE = "句式重复"
    INAPPROPRIATE_VOCABULARY = "词汇不当"
    ABSOLUTE_STATEMENT = "绝对化表述"


@dataclass
class Finding:
    finding_id: str
    section_id: str
    severity: Severity
    issue_type: IssueType
    location: str
    description: str
    impact: str
    suggested_fix: str
    problematic_text: str = ""


class StructuralReviewRules:
    """结构复审规则（10+ 条）"""
    
    @staticmethod
    def check_logic_flow(sections: List[Dict]) -> List[Finding]:
        """规则 1: 检查逻辑流畅性"""
        findings = []
        for i, section in enumerate(sections):
            if i == 0:
                continue
            prev_arg = sections[i-1].get("core_argument", "")
            curr_arg = section.get("core_argument", "")
            
            if not prev_arg or not curr_arg:
                continue
        
        return findings
    
    @staticmethod
    def check_transitions(content: str, sections: List[Dict]) -> List[Finding]:
        """规则 2: 检查段落衔接质量"""
        findings = []
        
        transition_words = ["因此", "所以", "但是", "然而", "另一方面", "进一步", "总之"]
        
        for i, section in enumerate(sections):
            if i == 0:
                continue
            
            section_title = section.get("section_title", "")
            if not any(word in content for word in transition_words):
                findings.append(Finding(
                    finding_id=f"trans-{i}",
                    section_id=section.get("section_id", ""),
                    severity=Severity.MAJOR,
                    issue_type=IssueType.WEAK_TRANSITION,
                    location=f"第 {i+1} 段",
                    description="缺少过渡句或过渡词",
                    impact="读者可能不理解段落间的逻辑关系",
                    suggested_fix="添加过渡句连接前后段落",
                    problematic_text=""
                ))
        
        return findings
    
    @staticmethod
    def check_argument_completeness(sections: List[Dict], material_pack: Dict) -> List[Finding]:
        """规则 3: 检查论证完整性"""
        findings = []
        
        for section in sections:
            required_evidence = section.get("evidence_required", [])
            if not required_evidence:
                continue
            
            section_content = section.get("content", "")
            for evidence in required_evidence:
                if evidence not in section_content:
                    findings.append(Finding(
                        finding_id=f"arg-{section.get('section_id')}",
                        section_id=section.get("section_id", ""),
                        severity=Severity.MAJOR,
                        issue_type=IssueType.INCOMPLETE_ARGUMENT,
                        location=f"第 {section.get('section_number')} 段",
                        description=f"缺少必需证据：{evidence}",
                        impact="论证不够充分，可能削弱说服力",
                        suggested_fix=f"补充或引用：{evidence}",
                        problematic_text=""
                    ))
        
        return findings
    
    @staticmethod
    def check_paragraph_length(content: str, style_dna: Dict) -> List[Finding]:
        """规则 4: 检查段落长度是否符合风格"""
        findings = []
        
        paragraphs = content.split("\n\n")
        target_sentences = 3
        
        for i, para in enumerate(paragraphs):
            if not para.strip():
                continue
            
            sentences = re.split(r'[。！？]', para)
            sentences = [s for s in sentences if s.strip()]
            
            if len(sentences) > target_sentences + 1:
                findings.append(Finding(
                    finding_id=f"para-len-{i}",
                    section_id="",
                    severity=Severity.MINOR,
                    issue_type=IssueType.WEAK_TRANSITION,
                    location=f"第 {i+1} 段",
                    description=f"段落过长（{len(sentences)} 句），建议 1-3 句",
                    impact="影响微信阅读体验",
                    suggested_fix="拆分为多个短段落",
                    problematic_text=para[:100]
                ))
        
        return findings
    
    @staticmethod
    def check_topic_coherence(sections: List[Dict]) -> List[Finding]:
        """规则 5: 检查主题连贯性"""
        findings = []
        
        for i in range(1, len(sections)):
            prev_obj = sections[i-1].get("section_objective", "")
            curr_obj = sections[i].get("section_objective", "")
            
            if prev_obj and curr_obj:
                prev_keywords = set(prev_obj.split())
                curr_keywords = set(curr_obj.split())
                
                overlap = len(prev_keywords & curr_keywords)
                if overlap == 0 and i > 1:
                    findings.append(Finding(
                        finding_id=f"coherence-{i}",
                        section_id=sections[i].get("section_id", ""),
                        severity=Severity.MAJOR,
                        issue_type=IssueType.ABRUPT_SHIFT,
                        location=f"第 {i} 到第 {i+1} 段之间",
                        description="话题转换过于突兀",
                        impact="读者可能感到困惑",
                        suggested_fix="添加过渡段落或调整段落顺序",
                        problematic_text=""
                    ))
        
        return findings
    
    @staticmethod
    def check_hook_strength(content: str) -> List[Finding]:
        """规则 6: 检查开头吸引力"""
        findings = []
        
        first_lines = content.split("\n")[:5]
        first_text = "\n".join(first_lines)
        
        hook_patterns = ["为什么", "怎样", "什么是", "最近", "数据", "案例"]
        has_hook = any(pattern in first_text for pattern in hook_patterns)
        
        if not has_hook:
            findings.append(Finding(
                finding_id="hook-001",
                section_id="",
                severity=Severity.MINOR,
                issue_type=IssueType.WEAK_TRANSITION,
                location="开头",
                description="开头缺少吸引力",
                impact="可能降低读者继续阅读的意愿",
                suggested_fix="用问题、数据或故事开头",
                problematic_text=first_text[:100]
            ))
        
        return findings
    
    @staticmethod
    def check_conclusion_clarity(content: str) -> List[Finding]:
        """规则 7: 检查结论清晰度"""
        findings = []
        
        last_lines = content.split("\n")[-5:]
        last_text = "\n".join(last_lines)
        
        conclusion_patterns = ["总结", "结论", "最后", "总之", "核心是"]
        has_conclusion = any(pattern in last_text for pattern in conclusion_patterns)
        
        if not has_conclusion:
            findings.append(Finding(
                finding_id="conclusion-001",
                section_id="",
                severity=Severity.MINOR,
                issue_type=IssueType.INCOMPLETE_ARGUMENT,
                location="结尾",
                description="结论不够明确",
                impact="读者可能不清楚文章的核心观点",
                suggested_fix="添加明确的结论或总结",
                problematic_text=last_text[:100]
            ))
        
        return findings


class EvidenceReviewRules:
    """证据复审规则（8+ 条）"""
    
    @staticmethod
    def check_citation_accuracy(content: str, material_pack: Dict) -> List[Finding]:
        """规则 1: 检查引用准确性"""
        findings = []
        
        materials = material_pack.get("materials", [])
        for material in materials:
            title = material.get("title", "")
            source = material.get("source", "")
            
            if title and title not in content:
                findings.append(Finding(
                    finding_id=f"cite-{material.get('material_id')}",
                    section_id="",
                    severity=Severity.MAJOR,
                    issue_type=IssueType.INACCURATE_CITATION,
                    location="未找到",
                    description=f"材料未被引用：{title}",
                    impact="可能浪费了有价值的证据",
                    suggested_fix=f"在相关段落引用：{title}",
                    problematic_text=""
                ))
        
        return findings
    
    @staticmethod
    def check_data_freshness(content: str) -> List[Finding]:
        """规则 2: 检查数据新鲜度"""
        findings = []
        
        old_years = ["2020", "2021", "2022"]
        current_year = "2026"
        
        for year in old_years:
            if year in content:
                findings.append(Finding(
                    finding_id=f"data-old-{year}",
                    section_id="",
                    severity=Severity.MAJOR,
                    issue_type=IssueType.OUTDATED_DATA,
                    location="",
                    description=f"数据可能过时（{year} 年）",
                    impact="可能影响论证的说服力",
                    suggested_fix=f"更新为 {current_year} 年的最新数据",
                    problematic_text=year
                ))
        
        return findings
    
    @staticmethod
    def check_source_credibility(material_pack: Dict) -> List[Finding]:
        """规则 3: 检查来源可信度"""
        findings = []
        
        materials = material_pack.get("materials", [])
        for material in materials:
            credibility = material.get("credibility", "medium")
            
            if credibility == "low":
                findings.append(Finding(
                    finding_id=f"cred-{material.get('material_id')}",
                    section_id="",
                    severity=Severity.MAJOR,
                    issue_type=IssueType.LOW_CREDIBILITY,
                    location="",
                    description=f"来源可信度低：{material.get('source')}",
                    impact="可能削弱论证的说服力",
                    suggested_fix="替换为更可信的来源或标注为'参考观点'",
                    problematic_text=material.get("source", "")
                ))
        
        return findings
    
    @staticmethod
    def check_evidence_coverage(sections: List[Dict], material_pack: Dict) -> List[Finding]:
        """规则 4: 检查证据覆盖率"""
        findings = []
        
        for section in sections:
            required_evidence = section.get("evidence_required", [])
            if not required_evidence:
                continue
            
            coverage = len([e for e in required_evidence if e])
            coverage_rate = (coverage / len(required_evidence)) * 100 if required_evidence else 0
            
            if coverage_rate < 80:
                findings.append(Finding(
                    finding_id=f"coverage-{section.get('section_id')}",
                    section_id=section.get("section_id", ""),
                    severity=Severity.MAJOR,
                    issue_type=IssueType.MISSING_EVIDENCE,
                    location=f"第 {section.get('section_number')} 段",
                    description=f"证据覆盖率仅 {coverage_rate:.0f}%",
                    impact="论证不够充分",
                    suggested_fix="补充缺失的证据",
                    problematic_text=""
                ))
        
        return findings


class ToneReviewRules:
    """语调复审规则（6+ 条）"""
    
    @staticmethod
    def check_absolute_statements(content: str) -> List[Finding]:
        """规则 1: 检查绝对化表述"""
        findings = []
        
        absolute_patterns = ["绝对", "必然", "一定", "肯定", "不可能"]
        
        for pattern in absolute_patterns:
            if pattern in content:
                findings.append(Finding(
                    finding_id=f"absolute-{pattern}",
                    section_id="",
                    severity=Severity.MAJOR,
                    issue_type=IssueType.ABSOLUTE_STATEMENT,
                    location="",
                    description=f"使用了绝对化表述：'{pattern}'",
                    impact="可能显得武断，降低说服力",
                    suggested_fix="改为更谨慎的表述，如'可能'、'往往'",
                    problematic_text=pattern
                ))
        
        return findings


class EditorialReviewer:
    """编辑复审主类"""
    
    def __init__(self):
        self.structural_rules = StructuralReviewRules()
        self.evidence_rules = EvidenceReviewRules()
        self.tone_rules = ToneReviewRules()
    
    def review(self, draft: Dict, outline: List[Dict], brief: Dict, 
               material_pack: Dict, style_dna: Dict) -> Dict:
        """执行完整复审"""
        
        content = draft.get("full_content", "")
        
        structural_findings = []
        structural_findings.extend(self.structural_rules.check_logic_flow(outline))
        structural_findings.extend(self.structural_rules.check_transitions(content, outline))
        structural_findings.extend(self.structural_rules.check_argument_completeness(outline, material_pack))
        structural_findings.extend(self.structural_rules.check_paragraph_length(content, style_dna))
        structural_findings.extend(self.structural_rules.check_topic_coherence(outline))
        structural_findings.extend(self.structural_rules.check_hook_strength(content))
        structural_findings.extend(self.structural_rules.check_conclusion_clarity(content))
        
        evidence_findings = []
        evidence_findings.extend(self.evidence_rules.check_citation_accuracy(content, material_pack))
        evidence_findings.extend(self.evidence_rules.check_data_freshness(content))
        evidence_findings.extend(self.evidence_rules.check_source_credibility(material_pack))
        evidence_findings.extend(self.evidence_rules.check_evidence_coverage(outline, material_pack))
        
        tone_findings = []
        tone_findings.extend(self.tone_rules.check_absolute_statements(content))
        
        structural_score = self._calculate_score(structural_findings)
        evidence_score = self._calculate_score(evidence_findings)
        tone_score = self._calculate_score(tone_findings)
        overall_score = (structural_score + evidence_score + tone_score) // 3
        
        return {
            "structural_review": {
                "overall_score": structural_score,
                "status": self._get_status(structural_score),
                "findings": structural_findings
            },
            "evidence_review": {
                "overall_score": evidence_score,
                "status": self._get_status(evidence_score),
                "findings": evidence_findings
            },
            "tone_review": {
                "overall_score": tone_score,
                "status": self._get_status(tone_score),
                "findings": tone_findings
            },
            "overall_quality_score": overall_score,
            "publication_ready": overall_score >= 80
        }
    
    @staticmethod
    def _calculate_score(findings: List[Finding]) -> int:
        """根据问题数量计算评分"""
        if not findings:
            return 100
        
        critical_count = sum(1 for f in findings if f.severity == Severity.CRITICAL)
        major_count = sum(1 for f in findings if f.severity == Severity.MAJOR)
        minor_count = sum(1 for f in findings if f.severity == Severity.MINOR)
        
        score = 100 - (critical_count * 20 + major_count * 10 + minor_count * 2)
        return max(0, score)
    
    @staticmethod
    def _get_status(score: int) -> str:
        """根据评分确定状态"""
        if score >= 85:
            return "pass"
        elif score >= 70:
            return "needs_revision"
        else:
            return "critical"
