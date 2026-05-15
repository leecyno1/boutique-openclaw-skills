"""
图文卡片结构生成器 - 根据 Brief + Material Pack 生成图文卡片的页面结构

支持功能：
- 页数规划（3-8 页）
- 内容分配
- 视觉指示生成
- 配图需求生成
- 平台特定的约束处理
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
import json
import uuid


class PageType(Enum):
    """页面类型"""
    COVER = "cover"  # 开篇
    CONTENT = "content"  # 内容
    DATA = "data"  # 数据展示
    CTA = "cta"  # 行动号召
    CLOSING = "closing"  # 结尾


class ContentComplexity(Enum):
    """内容复杂度"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


class Platform(Enum):
    """目标平台"""
    XIAOHONGSHU = "xiaohongshu"
    WEIBO = "weibo"
    DOUYIN = "douyin"
    GENERIC = "generic"


@dataclass
class ContentBrief:
    """内容简报"""
    brief_id: str
    working_title: str
    core_claim: str
    content_goals: List[str]
    target_audience: List[str]
    key_points: List[str]
    risk_boundaries: List[str] = field(default_factory=list)


@dataclass
class Material:
    """素材"""
    material_id: str
    type: str  # reference, quote, data, case_study, expert_view, visual
    title: str
    content: str
    source: str
    credibility: str  # high, medium, low


@dataclass
class MaterialPack:
    """素材包"""
    pack_id: str
    materials: List[Material]
    evidence_checklist: List[str] = field(default_factory=list)


@dataclass
class PlatformConstraints:
    """平台约束"""
    image_ratio: str
    max_text_length: int
    max_pages: int
    emoji_usage: str  # low, moderate, high


@dataclass
class MediaPlan:
    """媒介计划"""
    target_media: str
    platform: str
    platform_constraints: PlatformConstraints
    distribution_strategy: str


@dataclass
class ImageRequirement:
    """配图需求"""
    image_id: str
    page_number: int
    description: str
    style: str
    ratio: str
    priority: str  # high, medium, low
    color_tone: str
    content_focus: str
    alternative_options: List[str] = field(default_factory=list)


@dataclass
class TextSpecs:
    """文字规格"""
    font_size: str
    font_weight: str
    text_color: str
    background_color: str


@dataclass
class VisualElement:
    """视觉元素"""
    type: str  # image, icon, chart, text_overlay
    description: str
    position: str  # top, center, bottom, full


@dataclass
class PageContent:
    """页面内容"""
    page_number: int
    page_type: str
    title: str
    content: str
    key_message: str
    visual_focus: str
    visual_elements: List[VisualElement] = field(default_factory=list)
    image_requirement: Optional[ImageRequirement] = None
    text_specs: Optional[TextSpecs] = None
    cta_element: Optional[str] = None


@dataclass
class PagePlan:
    """页面规划"""
    total_pages: int
    page_strategy: str
    pages: List[PageContent] = field(default_factory=list)


@dataclass
class VisualGuidelines:
    """视觉指南"""
    color_palette: List[str]
    typography: Dict[str, str]
    style_tone: str
    visual_metaphor: str


@dataclass
class ImageRequirements:
    """配图需求汇总"""
    total_images: int
    images: List[ImageRequirement] = field(default_factory=list)


@dataclass
class ContentDistribution:
    """内容分配"""
    total_text_length: int
    text_per_page: int
    key_points_distribution: Dict[str, str]
    materials_used: List[str]
    materials_missing: List[str]


@dataclass
class LayoutRecommendations:
    """排版建议"""
    grid_system: str
    spacing_guidelines: str
    alignment_rules: str
    white_space_strategy: str


@dataclass
class ImagePostStructure:
    """图文卡片结构"""
    structure_id: str
    request_id: str
    brief_id: str
    material_pack_id: str
    target_platform: str
    page_plan: PagePlan
    visual_guidelines: VisualGuidelines
    image_requirements: ImageRequirements
    content_distribution: ContentDistribution
    layout_recommendations: LayoutRecommendations
    quality_checklist: List[str] = field(default_factory=list)
    status: str = "planned"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat() + "Z")


class ImagePostStructureGenerator:
    """图文卡片结构生成器"""

    def __init__(self):
        self.platform_configs = self._init_platform_configs()

    def _init_platform_configs(self) -> Dict[str, Dict[str, Any]]:
        """初始化平台配置"""
        return {
            "xiaohongshu": {
                "image_ratio": "3:4",
                "max_text_length": 400,
                "emoji_usage": "moderate",
                "style_tone": "轻松活泼，视觉优先",
            },
            "weibo": {
                "image_ratio": "1:1 or 16:9",
                "max_text_length": 280,
                "emoji_usage": "high",
                "style_tone": "快速传播，话题驱动",
            },
            "douyin": {
                "image_ratio": "9:16",
                "max_text_length": 150,
                "emoji_usage": "high",
                "style_tone": "视觉冲击，快节奏",
            },
            "generic": {
                "image_ratio": "3:4",
                "max_text_length": 400,
                "emoji_usage": "moderate",
                "style_tone": "通用风格",
            },
        }

    def generate(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        media_plan: MediaPlan,
        content_complexity: str,
        request_id: str,
        operator_note: Optional[str] = None,
    ) -> ImagePostStructure:
        """生成图文卡片结构"""

        # 1. 规划页数
        total_pages = self._plan_page_count(
            content_complexity, len(brief.key_points), len(material_pack.materials)
        )

        # 2. 生成页面内容
        pages = self._generate_pages(
            brief, material_pack, total_pages, media_plan.platform_constraints
        )

        # 3. 生成视觉指南
        visual_guidelines = self._generate_visual_guidelines(brief, media_plan.platform)

        # 4. 生成配图需求
        image_requirements = self._generate_image_requirements(pages, media_plan.platform)

        # 5. 生成内容分配
        content_distribution = self._generate_content_distribution(
            brief, material_pack, pages
        )

        # 6. 生成排版建议
        layout_recommendations = self._generate_layout_recommendations(media_plan.platform)

        # 7. 生成质量检查清单
        quality_checklist = self._generate_quality_checklist(pages, brief)

        # 8. 组装最终结构
        structure = ImagePostStructure(
            structure_id=f"imgstruct-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            request_id=request_id,
            brief_id=brief.brief_id,
            material_pack_id=material_pack.pack_id,
            target_platform=media_plan.platform,
            page_plan=PagePlan(
                total_pages=total_pages,
                page_strategy=self._generate_page_strategy(
                    content_complexity, len(brief.key_points), total_pages
                ),
                pages=pages,
            ),
            visual_guidelines=visual_guidelines,
            image_requirements=image_requirements,
            content_distribution=content_distribution,
            layout_recommendations=layout_recommendations,
            quality_checklist=quality_checklist,
        )

        return structure

    def _plan_page_count(
        self, complexity: str, key_points_count: int, material_count: int
    ) -> int:
        """规划页数"""
        if complexity == "simple":
            base_pages = 3
        elif complexity == "moderate":
            base_pages = 5
        else:  # complex
            base_pages = 7

        # 根据核心论点数调整
        if key_points_count > 5:
            base_pages += 1
        if key_points_count > 8:
            base_pages += 1

        # 确保在 3-8 范围内
        return max(3, min(8, base_pages))

    def _generate_pages(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        total_pages: int,
        platform_constraints: PlatformConstraints,
    ) -> List[PageContent]:
        """生成页面内容"""
        pages = []

        # 第 1 页：开篇
        pages.append(
            self._generate_cover_page(brief, material_pack, platform_constraints)
        )

        # 第 2 到 n-1 页：内容
        content_pages_count = total_pages - 2
        key_points_per_page = max(
            1, len(brief.key_points) // content_pages_count
        )

        for i in range(content_pages_count):
            start_idx = i * key_points_per_page
            end_idx = (
                start_idx + key_points_per_page
                if i < content_pages_count - 1
                else len(brief.key_points)
            )
            page_key_points = brief.key_points[start_idx:end_idx]

            pages.append(
                self._generate_content_page(
                    brief,
                    material_pack,
                    page_key_points,
                    i + 2,
                    platform_constraints,
                )
            )

        # 最后一页：行动号召
        pages.append(
            self._generate_cta_page(brief, material_pack, total_pages, platform_constraints)
        )

        return pages

    def _generate_cover_page(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        platform_constraints: PlatformConstraints,
    ) -> PageContent:
        """生成开篇页"""
        return PageContent(
            page_number=1,
            page_type=PageType.COVER.value,
            title=brief.working_title,
            content=brief.core_claim,
            key_message=brief.core_claim,
            visual_focus="大标题 + 核心观点 + 视觉冲击",
            visual_elements=[
                VisualElement(
                    type="text_overlay",
                    description="大号标题作为背景",
                    position="center",
                ),
                VisualElement(
                    type="image",
                    description="主视觉配图",
                    position="full",
                ),
            ],
            image_requirement=ImageRequirement(
                image_id="img-001",
                page_number=1,
                description=f"开篇配图：{brief.working_title}",
                style="视觉冲击，吸引注意力",
                ratio=platform_constraints.image_ratio,
                priority="high",
                color_tone="鲜艳、对比强烈",
                content_focus="核心观点的视觉表达",
            ),
            text_specs=TextSpecs(
                font_size="48px",
                font_weight="bold",
                text_color="#FFFFFF",
                background_color="transparent",
            ),
            cta_element="往下滑看详情",
        )

    def _generate_content_page(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        page_key_points: List[str],
        page_number: int,
        platform_constraints: PlatformConstraints,
    ) -> PageContent:
        """生成内容页"""
        key_point = page_key_points[0] if page_key_points else ""

        # 查找对应的素材
        matching_material = self._find_matching_material(key_point, material_pack)

        visual_focus = self._determine_visual_focus(matching_material)

        return PageContent(
            page_number=page_number,
            page_type=PageType.CONTENT.value,
            title=key_point,
            content=self._generate_page_content(key_point, matching_material),
            key_message=key_point,
            visual_focus=visual_focus,
            visual_elements=[
                VisualElement(
                    type="image",
                    description="内容配图",
                    position="center",
                ),
            ],
            image_requirement=ImageRequirement(
                image_id=f"img-{str(page_number).zfill(3)}",
                page_number=page_number,
                description=f"页面 {page_number} 配图：{key_point}",
                style=self._determine_image_style(matching_material),
                ratio=platform_constraints.image_ratio,
                priority="high" if page_number <= 3 else "medium",
                color_tone="与整体风格一致",
                content_focus=key_point,
            ),
            text_specs=TextSpecs(
                font_size="32px",
                font_weight="600",
                text_color="#1A1A1A",
                background_color="#F5F5F5",
            ),
        )

    def _generate_cta_page(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        total_pages: int,
        platform_constraints: PlatformConstraints,
    ) -> PageContent:
        """生成行动号召页"""
        return PageContent(
            page_number=total_pages,
            page_type=PageType.CTA.value,
            title="总结与行动号召",
            content="感谢阅读！如果有帮助，请点赞、评论、转发。",
            key_message="知道陷阱，才能避开陷阱",
            visual_focus="清单式展示或总结图",
            visual_elements=[
                VisualElement(
                    type="text_overlay",
                    description="清单项目或总结",
                    position="center",
                ),
            ],
            image_requirement=ImageRequirement(
                image_id=f"img-{str(total_pages).zfill(3)}",
                page_number=total_pages,
                description="结尾配图：总结与号召",
                style="温暖、鼓励性",
                ratio=platform_constraints.image_ratio,
                priority="medium",
                color_tone="积极向上",
                content_focus="行动号召",
            ),
            text_specs=TextSpecs(
                font_size="28px",
                font_weight="600",
                text_color="#FFFFFF",
                background_color="#0066FF",
            ),
            cta_element="点赞 + 评论 + 转发",
        )

    def _find_matching_material(
        self, key_point: str, material_pack: MaterialPack
    ) -> Optional[Material]:
        """查找匹配的素材"""
        for material in material_pack.materials:
            if key_point.lower() in material.title.lower() or key_point.lower() in material.content.lower():
                return material
        return material_pack.materials[0] if material_pack.materials else None

    def _determine_visual_focus(self, material: Optional[Material]) -> str:
        """确定视觉重点"""
        if not material:
            return "通用配图"

        if material.type == "data":
            return "数据可视化（图表、数字）"
        elif material.type == "case_study":
            return "对比图或流程图"
        elif material.type == "quote":
            return "引用框或强调文字"
        elif material.type == "expert_view":
            return "人物肖像或采访场景"
        else:
            return "通用配图"

    def _determine_image_style(self, material: Optional[Material]) -> str:
        """确定图片风格"""
        if not material:
            return "现代简约"

        if material.type == "data":
            return "数据可视化"
        elif material.type == "case_study":
            return "对比或流程图"
        elif material.type == "quote":
            return "排版设计"
        else:
            return "现代简约"

    def _generate_page_content(
        self, key_point: str, material: Optional[Material]
    ) -> str:
        """生成页面内容"""
        if material:
            return f"{key_point}\n\n{material.content[:150]}..."
        return key_point

    def _generate_page_strategy(
        self, complexity: str, key_points_count: int, total_pages: int
    ) -> str:
        """生成页面策略说明"""
        if complexity == "simple":
            return f"采用简洁型结构：第 1 页开篇，第 2-{total_pages-1} 页分别展示核心论点，最后一页行动号召"
        elif complexity == "moderate":
            return f"采用对比型结构：第 1 页开篇吸引，第 2-{total_pages-1} 页分别展示 {key_points_count} 个核心论点，每个论点配一个案例或数据，最后一页总结与号召"
        else:
            return f"采用深度型结构：第 1 页开篇，第 2-{total_pages-2} 页深度展开 {key_points_count} 个核心论点，第 {total_pages-1} 页补充信息，最后一页行动号召"

    def _generate_visual_guidelines(
        self, brief: ContentBrief, platform: str
    ) -> VisualGuidelines:
        """生成视觉指南"""
        platform_config = self.platform_configs.get(platform, self.platform_configs["generic"])

        return VisualGuidelines(
            color_palette=["#1A1A1A", "#0066FF", "#FF3333", "#F5F5F5", "#FFD700"],
            typography={
                "headline_font": "PingFang SC Bold",
                "body_font": "PingFang SC Regular",
                "font_hierarchy": "标题 48px > 副标题 32px > 正文 16px",
            },
            style_tone=platform_config["style_tone"],
            visual_metaphor=self._extract_visual_metaphor(brief.core_claim),
        )

    def _extract_visual_metaphor(self, core_claim: str) -> str:
        """提取视觉隐喻"""
        keywords = ["陷阱", "对比", "增长", "下降", "循环", "连接"]
        for keyword in keywords:
            if keyword in core_claim:
                return keyword
        return "通用"

    def _generate_image_requirements(
        self, pages: List[PageContent], platform: str
    ) -> ImageRequirements:
        """生成配图需求"""
        images = []
        for page in pages:
            if page.image_requirement:
                images.append(page.image_requirement)

        return ImageRequirements(
            total_images=len(images),
            images=images,
        )

    def _generate_content_distribution(
        self,
        brief: ContentBrief,
        material_pack: MaterialPack,
        pages: List[PageContent],
    ) -> ContentDistribution:
        """生成内容分配"""
        total_text_length = sum(len(page.content) for page in pages)
        text_per_page = total_text_length // len(pages) if pages else 0

        key_points_distribution = {}
        for i, key_point in enumerate(brief.key_points):
            page_idx = min(i + 1, len(pages) - 1)
            key_points_distribution[key_point] = f"page {page_idx + 1}"

        materials_used = [m.material_id for m in material_pack.materials]
        materials_missing = material_pack.evidence_checklist

        return ContentDistribution(
            total_text_length=total_text_length,
            text_per_page=text_per_page,
            key_points_distribution=key_points_distribution,
            materials_used=materials_used,
            materials_missing=materials_missing,
        )

    def _generate_layout_recommendations(self, platform: str) -> LayoutRecommendations:
        """生成排版建议"""
        if platform == "douyin":
            return LayoutRecommendations(
                grid_system="全屏竖屏，9:16 比例",
                spacing_guidelines="上下间距 16px，左右边距 12px",
                alignment_rules="标题居中，正文左对齐",
                white_space_strategy="充分留白，避免拥挤",
            )
        else:
            return LayoutRecommendations(
                grid_system="单列布局，全屏沉浸式",
                spacing_guidelines="上下间距 20px，左右边距 16px",
                alignment_rules="标题居中，正文左对齐",
                white_space_strategy="充分留白，避免拥挤",
            )

    def _generate_quality_checklist(
        self, pages: List[PageContent], brief: ContentBrief
    ) -> List[str]:
        """生成质量检查清单"""
        checklist = [
            "✓ 所有页面都有清晰的视觉焦点",
            "✓ 文字和图片比例均衡",
            f"✓ {len(brief.key_points)} 个核心论点都有对应的视觉支撑",
            "✓ 配色方案一致",
            "✓ CTA 清晰明确",
        ]
        return checklist


def generate_image_post_structure(
    brief_dict: Dict[str, Any],
    material_pack_dict: Dict[str, Any],
    media_plan_dict: Dict[str, Any],
    content_complexity: str,
    request_id: str,
    operator_note: Optional[str] = None,
) -> Dict[str, Any]:
    """
    生成图文卡片结构的便捷函数

    Args:
        brief_dict: Content Brief 字典
        material_pack_dict: Material Pack 字典
        media_plan_dict: Media Plan 字典
        content_complexity: 内容复杂度
        request_id: 请求 ID
        operator_note: 操作员备注

    Returns:
        图文卡片结构字典
    """
    # 构建对象
    brief = ContentBrief(**brief_dict)

    materials = [Material(**m) for m in material_pack_dict.get("materials", [])]
    material_pack = MaterialPack(
        pack_id=material_pack_dict["pack_id"],
        materials=materials,
        evidence_checklist=material_pack_dict.get("evidence_checklist", []),
    )

    platform_constraints = PlatformConstraints(
        **media_plan_dict["platform_constraints"]
    )
    media_plan = MediaPlan(
        target_media=media_plan_dict["target_media"],
        platform=media_plan_dict["platform"],
        platform_constraints=platform_constraints,
        distribution_strategy=media_plan_dict["distribution_strategy"],
    )

    # 生成结构
    generator = ImagePostStructureGenerator()
    structure = generator.generate(
        brief=brief,
        material_pack=material_pack,
        media_plan=media_plan,
        content_complexity=content_complexity,
        request_id=request_id,
        operator_note=operator_note,
    )

    # 转换为字典
    return asdict(structure)


if __name__ == "__main__":
    # 示例使用
    brief_dict = {
        "brief_id": "brief-ai-quant-001",
        "working_title": "AI 量化交易的 5 个陷阱",
        "core_claim": "AI 在量化交易中很强大，但这 5 个陷阱会让你血本无归",
        "content_goals": ["增长", "认知"],
        "target_audience": ["量化交易从业者", "投资者"],
        "key_points": [
            "过度拟合陷阱：历史数据不等于未来",
            "黑箱风险：模型不可解释",
            "数据质量陷阱：垃圾进垃圾出",
            "监管风险：政策变化打破模型假设",
            "心理陷阱：过度自信导致风险管理失效",
        ],
        "risk_boundaries": [
            "不能夸大 AI 的预测能力",
            "必须提及监管风险",
        ],
    }

    material_pack_dict = {
        "pack_id": "pack-ai-quant-001",
        "materials": [
            {
                "material_id": "mat-001",
                "type": "case_study",
                "title": "某量化基金的失败案例",
                "content": "该基金在 2024 年引入 AI 模型，收益率提升 15%，但在 2025 年初遭遇模型失效...",
                "source": "行业访谈",
                "credibility": "high",
            },
            {
                "material_id": "mat-002",
                "type": "data",
                "title": "AI 量化基金的收益分布",
                "content": "2024 年 AI 量化基金平均收益 12%，但波动率也提升 20%...",
                "source": "公开数据",
                "credibility": "high",
            },
        ],
        "evidence_checklist": ["更多失败案例", "监管政策变化的具体例子"],
    }

    media_plan_dict = {
        "target_media": "image_post",
        "platform": "xiaohongshu",
        "platform_constraints": {
            "image_ratio": "3:4",
            "max_text_length": 400,
            "max_pages": 8,
            "emoji_usage": "moderate",
        },
        "distribution_strategy": "早晚高峰发布，配合话题标签",
    }

    result = generate_image_post_structure(
        brief_dict=brief_dict,
        material_pack_dict=material_pack_dict,
        media_plan_dict=media_plan_dict,
        content_complexity="moderate",
        request_id="imgpost-20260315-abc123",
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
