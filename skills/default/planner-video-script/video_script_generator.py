"""
视频脚本生成器 - 根据 Brief + Material + Media Plan 生成视频脚本框架

支持的功能：
- 开场钩子生成（5-10 秒）
- 核心论证段落拆分（每段 30-60 秒）
- 分镜建议生成
- 口播逻辑优化
- 结尾行动号召生成
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import json
import uuid


class HookType(Enum):
    """钩子类型"""
    QUESTION = "question"  # 问句
    STATEMENT = "statement"  # 陈述
    VISUAL = "visual"  # 视觉冲击
    STORY = "story"  # 故事开场


class ShotType(Enum):
    """镜头类型"""
    WIDE = "全景"
    MEDIUM = "中景"
    CLOSE_UP = "特写"
    EXTREME_CLOSE_UP = "极特写"
    AERIAL = "航拍"
    POV = "主观视角"


class CTAType(Enum):
    """行动号召类型"""
    SUBSCRIBE = "subscribe"
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    VISIT = "visit"
    MULTI = "multi"


@dataclass
class Hook:
    """开场钩子"""
    hook_id: str
    hook_type: str
    hook_text: str
    visual_suggestion: str
    duration_seconds: int
    emotional_tone: str
    why_this_hook: str


@dataclass
class Narration:
    """口播逻辑"""
    narration_id: str
    main_text: str
    key_phrases: List[str]
    pause_points: List[str]
    tone: str
    pacing: str


@dataclass
class Shot:
    """镜头"""
    shot_id: str
    shot_number: int
    shot_type: str
    shot_description: str
    visual_elements: List[str]
    duration_seconds: int
    transition: str


@dataclass
class Evidence:
    """证据"""
    evidence_id: str
    evidence_type: str
    evidence_text: str
    source: str
    visual_format: str


@dataclass
class Section:
    """视频段落"""
    section_id: str
    section_number: int
    section_title: str
    section_objective: str
    core_argument: str
    duration_seconds: int
    narration: Narration
    shots: List[Shot]
    evidence: List[Evidence]
    transition_logic: str


@dataclass
class CTA:
    """行动号召"""
    cta_id: str
    cta_type: str
    cta_text: str
    visual_suggestion: str
    duration_seconds: int
    emotional_tone: str
    call_to_action_buttons: List[str]


@dataclass
class ProductionNotes:
    """生产参数"""
    total_duration_seconds: int
    total_duration_minutes: float
    scene_count: int
    speaker_count: int
    background_music_style: str
    subtitle_strategy: str
    animation_needs: List[str]
    color_palette: List[str]
    visual_style: str
    equipment_needs: List[str]


@dataclass
class QualityCheckItem:
    """质量检查项"""
    item: str
    status: str
    description: str


@dataclass
class VideoScriptStructure:
    """视频脚本结构"""
    structure_id: str
    request_id: str
    brief_summary: str
    material_count: int
    visual_assets_count: int
    evidence_gaps: List[str]
    hook: Hook
    sections: List[Section]
    cta: CTA
    production_notes: ProductionNotes
    quality_checklist: List[QualityCheckItem]
    created_at: str
    updated_at: str


class VideoScriptGenerator:
    """视频脚本生成器"""

    def __init__(self):
        self.hook_templates = {
            "question": [
                "你知道吗？{key_insight}",
                "有没有想过，{key_insight}？",
                "你是否遇到过这样的问题：{key_insight}？",
            ],
            "statement": [
                "{key_insight}，这是一个你必须知道的事实。",
                "{key_insight}，而大多数人还不知道。",
                "{key_insight}，这改变了一切。",
            ],
            "story": [
                "让我给你讲一个真实的故事。{key_insight}",
                "这是一个发生在{context}的故事。{key_insight}",
            ],
        }

    def generate_video_script_structure(
        self,
        request_id: str,
        brief: Dict[str, Any],
        material_pack: Dict[str, Any],
        media_plan: Dict[str, Any],
        operator_note: Optional[str] = None,
    ) -> VideoScriptStructure:
        """
        生成完整的视频脚本框架

        Args:
            request_id: 请求 ID
            brief: Content Brief 对象
            material_pack: Material Pack 对象
            media_plan: Media Plan 对象
            operator_note: 操作员备注

        Returns:
            VideoScriptStructure 对象
        """

        # 1. 验证输入
        self._validate_inputs(brief, material_pack, media_plan)

        # 2. 生成开场钩子
        hook = self._generate_hook(brief, material_pack)

        # 3. 计算段落数和时长
        total_duration = media_plan.get("platform_constraints", {}).get(
            "duration_minutes", 8
        )
        hook_duration = hook.duration_seconds / 60
        cta_duration = 0.15  # 假设 CTA 占 9 秒
        available_duration = total_duration - hook_duration - cta_duration

        # 4. 生成核心论证段落
        sections = self._generate_sections(
            brief, material_pack, media_plan, available_duration
        )

        # 5. 生成结尾 CTA
        cta = self._generate_cta(brief, material_pack)

        # 6. 生成生产参数
        production_notes = self._generate_production_notes(
            hook, sections, cta, media_plan
        )

        # 7. 生成质量检查清单
        quality_checklist = self._generate_quality_checklist()

        # 8. 组装最终结构
        structure = VideoScriptStructure(
            structure_id=f"video-struct-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            request_id=request_id,
            brief_summary=brief.get("core_judgment", ""),
            material_count=len(material_pack.get("materials", [])),
            visual_assets_count=self._count_visual_assets(material_pack),
            evidence_gaps=material_pack.get("evidence_checklist", []),
            hook=hook,
            sections=sections,
            cta=cta,
            production_notes=production_notes,
            quality_checklist=quality_checklist,
            created_at=datetime.now().isoformat() + "Z",
            updated_at=datetime.now().isoformat() + "Z",
        )

        return structure

    def _validate_inputs(
        self, brief: Dict, material_pack: Dict, media_plan: Dict
    ) -> None:
        """验证输入的完整性"""
        if not brief.get("brief_id"):
            raise ValueError("Brief 必须包含 brief_id")
        if not brief.get("core_judgment"):
            raise ValueError("Brief 必须包含 core_judgment")
        if not material_pack.get("pack_id"):
            raise ValueError("Material Pack 必须包含 pack_id")
        if not media_plan.get("target_media") == "video_script":
            raise ValueError("Media Plan 的 target_media 必须是 video_script")

    def _generate_hook(self, brief: Dict, material_pack: Dict) -> Hook:
        """生成开场钩子"""
        core_judgment = brief.get("core_judgment", "")
        key_points = brief.get("key_points", [])

        # 选择钩子类型
        hook_type = "question"  # 默认使用问句
        if "故事" in core_judgment or "案例" in core_judgment:
            hook_type = "story"

        # 生成钩子文案
        hook_text = self._generate_hook_text(hook_type, core_judgment, key_points)

        return Hook(
            hook_id=f"hook-{str(uuid.uuid4())[:8]}",
            hook_type=hook_type,
            hook_text=hook_text,
            visual_suggestion="屏幕上显示关键视觉元素，然后切换到主题",
            duration_seconds=8,
            emotional_tone="好奇、引人入胜",
            why_this_hook="用问句或故事吸引注意力，同时暗示内容的核心价值",
        )

    def _generate_hook_text(
        self, hook_type: str, core_judgment: str, key_points: List[str]
    ) -> str:
        """生成钩子文案"""
        if hook_type == "question":
            return f"你知道吗？{core_judgment}今天我们来看看这背后的故事。"
        elif hook_type == "story":
            return f"让我给你讲一个真实的故事。{core_judgment}"
        else:
            return f"{core_judgment}这是你必须知道的。"

    def _generate_sections(
        self,
        brief: Dict,
        material_pack: Dict,
        media_plan: Dict,
        available_duration: float,
    ) -> List[Section]:
        """生成核心论证段落"""
        key_points = brief.get("key_points", [])
        materials = material_pack.get("materials", [])

        # 计算每个段落的时长
        section_count = min(len(key_points), 3)  # 最多 3 个段落
        duration_per_section = (available_duration * 60) / section_count

        sections = []
        for i, key_point in enumerate(key_points[:section_count]):
            section = self._generate_single_section(
                i + 1,
                key_point,
                materials,
                int(duration_per_section),
            )
            sections.append(section)

        return sections

    def _generate_single_section(
        self,
        section_number: int,
        key_point: str,
        materials: List[Dict],
        duration_seconds: int,
    ) -> Section:
        """生成单个段落"""
        section_id = f"sec-{str(uuid.uuid4())[:8]}"

        # 生成口播逻辑
        narration = self._generate_narration(key_point, materials)

        # 生成分镜建议
        shots = self._generate_shots(section_number, duration_seconds)

        # 生成证据
        evidence = self._generate_evidence(materials)

        return Section(
            section_id=section_id,
            section_number=section_number,
            section_title=key_point,
            section_objective=f"解释和论证：{key_point}",
            core_argument=key_point,
            duration_seconds=duration_seconds,
            narration=narration,
            shots=shots,
            evidence=evidence,
            transition_logic=self._generate_transition_logic(section_number),
        )

    def _generate_narration(
        self, key_point: str, materials: List[Dict]
    ) -> Narration:
        """生成口播逻辑"""
        # 从素材中提取相关内容
        relevant_material = next(
            (m for m in materials if m.get("type") in ["case_study", "data"]),
            None,
        )

        main_text = f"{key_point}。"
        if relevant_material:
            main_text += f"根据{relevant_material.get('source', '数据')}，{relevant_material.get('content', '')}。"

        return Narration(
            narration_id=f"nar-{str(uuid.uuid4())[:8]}",
            main_text=main_text,
            key_phrases=[key_point],
            pause_points=[key_point + "。"],
            tone="平稳、专业",
            pacing="中等",
        )

    def _generate_shots(self, section_number: int, duration_seconds: int) -> List[Shot]:
        """生成分镜建议"""
        shot_types = ["全景", "中景", "特写"]
        shots = []

        # 根据时长分配镜头
        shot_count = min(3, max(1, duration_seconds // 20))
        duration_per_shot = duration_seconds // shot_count

        for i in range(shot_count):
            shot = Shot(
                shot_id=f"shot-{str(uuid.uuid4())[:8]}",
                shot_number=i + 1,
                shot_type=shot_types[i % len(shot_types)],
                shot_description=f"展示第 {section_number} 段的关键内容",
                visual_elements=["数据可视化", "文字标注", "动画效果"],
                duration_seconds=duration_per_shot,
                transition="切换" if i < shot_count - 1 else "淡出",
            )
            shots.append(shot)

        return shots

    def _generate_evidence(self, materials: List[Dict]) -> List[Evidence]:
        """生成证据"""
        evidence_list = []

        for material in materials[:2]:  # 最多使用 2 个素材
            evidence = Evidence(
                evidence_id=f"ev-{str(uuid.uuid4())[:8]}",
                evidence_type=material.get("type", "reference"),
                evidence_text=material.get("content", ""),
                source=material.get("source", ""),
                visual_format="数据图表或文字标注",
            )
            evidence_list.append(evidence)

        return evidence_list

    def _generate_transition_logic(self, section_number: int) -> str:
        """生成转场逻辑"""
        transitions = [
            "既然我们了解了这一点，那么接下来的问题是什么呢？",
            "但这还不是全部。还有更重要的一点需要注意。",
            "综合以上分析，我们可以得出什么结论呢？",
        ]
        return transitions[section_number % len(transitions)]

    def _generate_cta(self, brief: Dict, material_pack: Dict) -> CTA:
        """生成结尾行动号召"""
        return CTA(
            cta_id=f"cta-{str(uuid.uuid4())[:8]}",
            cta_type="multi",
            cta_text="如果你觉得这个内容有价值，欢迎订阅我们的频道，获取更多深度洞察。同时，在评论区分享你的想法。",
            visual_suggestion="展示订阅按钮、点赞按钮、评论框",
            duration_seconds=8,
            emotional_tone="邀请、友好",
            call_to_action_buttons=["订阅", "点赞", "评论", "分享"],
        )

    def _generate_production_notes(
        self, hook: Hook, sections: List[Section], cta: CTA, media_plan: Dict
    ) -> ProductionNotes:
        """生成生产参数"""
        total_seconds = (
            hook.duration_seconds
            + sum(s.duration_seconds for s in sections)
            + cta.duration_seconds
        )

        return ProductionNotes(
            total_duration_seconds=total_seconds,
            total_duration_minutes=round(total_seconds / 60, 2),
            scene_count=len(sections) * 3,
            speaker_count=1,
            background_music_style="现代、科技感、节奏感强",
            subtitle_strategy="全程字幕，关键数字和概念加粗或高亮",
            animation_needs=["数据流动画", "图表动画", "转场动画", "文字动画"],
            color_palette=["深蓝", "科技绿", "金色", "白色"],
            visual_style="现代科技风格，配合数据可视化",
            equipment_needs=["4K 摄像机", "麦克风", "绿幕", "灯光"],
        )

    def _generate_quality_checklist(self) -> List[QualityCheckItem]:
        """生成质量检查清单"""
        return [
            QualityCheckItem(
                item="开场钩子是否能在 5-10 秒内吸引注意力",
                status="required",
                description="钩子必须在前 10 秒内建立观众的兴趣",
            ),
            QualityCheckItem(
                item="每个段落是否有清晰的论点和证据支撑",
                status="required",
                description="每个段落必须有核心论点和至少一个证据",
            ),
            QualityCheckItem(
                item="分镜建议是否可行",
                status="required",
                description="分镜建议必须考虑实际拍摄的可行性",
            ),
            QualityCheckItem(
                item="口播逻辑是否流畅",
                status="required",
                description="口播文案必须自然流畅，避免生硬",
            ),
            QualityCheckItem(
                item="CTA 是否清晰有力",
                status="required",
                description="CTA 必须明确指导观众的下一步行动",
            ),
            QualityCheckItem(
                item="总时长是否符合媒介计划",
                status="required",
                description="总时长必须在媒介计划的范围内",
            ),
        ]

    def _count_visual_assets(self, material_pack: Dict) -> int:
        """计算可视化素材数"""
        materials = material_pack.get("materials", [])
        return sum(
            1
            for m in materials
            if m.get("visual_potential") == "high"
            or m.get("type") in ["data", "case_study"]
        )

    def to_dict(self, structure: VideoScriptStructure) -> Dict:
        """将结构转换为字典"""
        return {
            "structure_id": structure.structure_id,
            "request_id": structure.request_id,
            "input_digest": {
                "brief_summary": structure.brief_summary,
                "material_count": structure.material_count,
                "visual_assets_count": structure.visual_assets_count,
                "evidence_gaps": structure.evidence_gaps,
            },
            "hook": asdict(structure.hook),
            "sections": [asdict(s) for s in structure.sections],
            "cta": asdict(structure.cta),
            "production_notes": asdict(structure.production_notes),
            "quality_checklist": [asdict(q) for q in structure.quality_checklist],
            "created_at": structure.created_at,
            "updated_at": structure.updated_at,
        }

    def to_json(self, structure: VideoScriptStructure) -> str:
        """将结构转换为 JSON"""
        return json.dumps(self.to_dict(structure), ensure_ascii=False, indent=2)


# 使用示例
if __name__ == "__main__":
    generator = VideoScriptGenerator()

    # 示例输入
    brief = {
        "brief_id": "brief-ai-quant-001",
        "core_judgment": "AI 在量化交易中已从理论进入实践，但仍需警惕过度拟合和黑箱风险",
        "target_audience": "量化交易从业者、投资者、AI 研究者",
        "video_goal": "通过案例展示 AI 量化的实际应用，同时提示风险",
        "key_points": [
            "AI 模型在特征工程中的优势",
            "高频交易中的实际应用案例",
            "过度拟合与风险控制",
        ],
        "risk_boundaries": ["不能夸大 AI 的预测能力", "必须提及监管风险"],
    }

    material_pack = {
        "pack_id": "pack-ai-quant-001",
        "materials": [
            {
                "material_id": "mat-001",
                "type": "case_study",
                "title": "某量化基金的 AI 应用案例",
                "content": "该基金在 2024 年引入 AI 模型，收益率提升 15%",
                "source": "行业访谈",
                "credibility": "high",
                "visual_potential": "high",
            },
            {
                "material_id": "mat-002",
                "type": "data",
                "title": "AI 量化基金的收益分布",
                "content": "2024 年 AI 量化基金平均收益 12%，波动率提升 20%",
                "source": "公开数据",
                "credibility": "high",
                "visual_potential": "high",
            },
        ],
        "evidence_checklist": ["补充失败案例", "补充监管政策背景"],
    }

    media_plan = {
        "target_media": "video_script",
        "platform_constraints": {
            "duration_minutes": 8,
            "scene_count": 5,
            "speaker_count": 1,
            "background_music": True,
            "subtitle_required": True,
            "animation_required": False,
        },
        "distribution_strategy": "YouTube、B站、小红书视频",
    }

    # 生成视频脚本框架
    structure = generator.generate_video_script_structure(
        request_id="video-script-20260315-abc123",
        brief=brief,
        material_pack=material_pack,
        media_plan=media_plan,
    )

    # 输出为 JSON
    print(generator.to_json(structure))
