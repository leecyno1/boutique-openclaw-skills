"""
媒介类型适配器 - 根据媒介类型生成对应的 structure_type 和执行参数

支持的媒介类型：
- article_wechat: 公众号文章
- video_script: 视频脚本
- image_post: 图文（小红书、微博等）
- newsletter: 邮件通讯
- short_video: 短视频（抖音、快手等）
- slide_deck: 幻灯片演讲
- podcast_script: 播客脚本
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MediaType(Enum):
    """支持的媒介类型"""
    ARTICLE_WECHAT = "article_wechat"
    VIDEO_SCRIPT = "video_script"
    IMAGE_POST = "image_post"
    NEWSLETTER = "newsletter"
    SHORT_VIDEO = "short_video"
    SLIDE_DECK = "slide_deck"
    PODCAST_SCRIPT = "podcast_script"


class StructureType(Enum):
    """内容结构类型"""
    NARRATIVE = "narrative"  # 叙事型（讲故事）
    ARGUMENTATIVE = "argumentative"  # 论证型（摆事实、讲道理）
    DATA_DRIVEN = "data_driven"  # 数据型（数据分析、可视化）
    COMPARATIVE = "comparative"  # 对比型（对比分析）
    INSTRUCTIONAL = "instructional"  # 教学型（教程、指南）
    INTERVIEW = "interview"  # 访谈型（采访、对话）
    MIXED = "mixed"  # 混合型（多种结构结合）


@dataclass
class MediaTypeConfig:
    """媒介类型配置"""
    media_type: MediaType
    primary_structure_types: List[StructureType]
    secondary_structure_types: List[StructureType]
    production_params: Dict[str, Any]
    next_adapter: str
    description: str


class MediaTypeAdapter:
    """媒介类型适配器 - 为不同媒介生成对应的规划参数"""

    # 媒介类型配置映射表
    MEDIA_CONFIGS: Dict[str, MediaTypeConfig] = {
        "article_wechat": MediaTypeConfig(
            media_type=MediaType.ARTICLE_WECHAT,
            primary_structure_types=[
                StructureType.ARGUMENTATIVE,
                StructureType.NARRATIVE,
            ],
            secondary_structure_types=[
                StructureType.DATA_DRIVEN,
                StructureType.INSTRUCTIONAL,
            ],
            production_params={
                "word_count": "1500-2500字",
                "reading_time": "8-10分钟",
                "image_count": 3,
                "image_specs": "800x600px, 高质量配图",
                "formatting_notes": "段落清晰，配图穿插，引用标注",
                "section_count": "4-6段",
            },
            next_adapter="wechat-topic-outline-planner",
            description="公众号文章 - 深度内容，适合长篇幅论证和故事讲述",
        ),
        "video_script": MediaTypeConfig(
            media_type=MediaType.VIDEO_SCRIPT,
            primary_structure_types=[
                StructureType.NARRATIVE,
                StructureType.INTERVIEW,
            ],
            secondary_structure_types=[
                StructureType.DATA_DRIVEN,
                StructureType.INSTRUCTIONAL,
            ],
            production_params={
                "duration": "8-10分钟",
                "scene_count": 5,
                "speaker_count": 1,
                "background_music": "需要",
                "subtitle_required": True,
                "animation_required": False,
                "shot_types": ["开场", "主体论证", "案例展示", "结尾号召"],
            },
            next_adapter="video-script-generator",
            description="视频脚本 - 动态展现，适合故事讲述和采访形式",
        ),
        "image_post": MediaTypeConfig(
            media_type=MediaType.IMAGE_POST,
            primary_structure_types=[
                StructureType.COMPARATIVE,
                StructureType.DATA_DRIVEN,
            ],
            secondary_structure_types=[
                StructureType.NARRATIVE,
                StructureType.INSTRUCTIONAL,
            ],
            production_params={
                "image_count": 5,
                "text_length": "200-400字",
                "hashtag_count": 5,
                "platform_specific": {
                    "xiaohongshu": {
                        "image_ratio": "3:4",
                        "text_position": "first_image",
                        "emoji_usage": "moderate",
                    },
                    "weibo": {
                        "image_ratio": "1:1 or 16:9",
                        "text_position": "caption",
                        "emoji_usage": "high",
                    },
                },
            },
            next_adapter="image-post-planner",
            description="图文内容 - 视觉优先，适合对比和数据展示",
        ),
        "newsletter": MediaTypeConfig(
            media_type=MediaType.NEWSLETTER,
            primary_structure_types=[
                StructureType.MIXED,
                StructureType.NARRATIVE,
            ],
            secondary_structure_types=[
                StructureType.DATA_DRIVEN,
                StructureType.INSTRUCTIONAL,
            ],
            production_params={
                "word_count": "800-1200字",
                "section_count": 3,
                "reading_time": "5-7分钟",
                "cta_count": 2,
                "image_count": 2,
                "format": "标题 + 摘要 + 正文 + 推荐 + CTA",
            },
            next_adapter="newsletter-generator",
            description="邮件通讯 - 精选内容，适合混合形式和多个CTA",
        ),
        "short_video": MediaTypeConfig(
            media_type=MediaType.SHORT_VIDEO,
            primary_structure_types=[
                StructureType.NARRATIVE,
                StructureType.INSTRUCTIONAL,
            ],
            secondary_structure_types=[
                StructureType.DATA_DRIVEN,
                StructureType.COMPARATIVE,
            ],
            production_params={
                "duration": "30-60秒",
                "scene_count": 3,
                "hook_duration": "3秒",
                "music_required": True,
                "text_overlay": True,
                "transition_style": "fast_paced",
            },
            next_adapter="short-video-generator",
            description="短视频 - 快节奏，适合故事讲述和教学",
        ),
        "slide_deck": MediaTypeConfig(
            media_type=MediaType.SLIDE_DECK,
            primary_structure_types=[
                StructureType.INSTRUCTIONAL,
                StructureType.DATA_DRIVEN,
            ],
            secondary_structure_types=[
                StructureType.COMPARATIVE,
                StructureType.ARGUMENTATIVE,
            ],
            production_params={
                "slide_count": "15-20张",
                "text_per_slide": "30-50字",
                "image_count": 10,
                "chart_count": 3,
                "animation_level": "moderate",
            },
            next_adapter="slide-deck-generator",
            description="幻灯片演讲 - 结构化展现，适合教学和数据展示",
        ),
        "podcast_script": MediaTypeConfig(
            media_type=MediaType.PODCAST_SCRIPT,
            primary_structure_types=[
                StructureType.NARRATIVE,
                StructureType.INTERVIEW,
            ],
            secondary_structure_types=[
                StructureType.ARGUMENTATIVE,
                StructureType.INSTRUCTIONAL,
            ],
            production_params={
                "duration": "20-30分钟",
                "speaker_count": 1,
                "segment_count": 4,
                "intro_duration": "1分钟",
                "outro_duration": "1分钟",
                "music_required": True,
            },
            next_adapter="podcast-script-generator",
            description="播客脚本 - 音频优先，适合深度对话和故事讲述",
        ),
    }

    @classmethod
    def get_config(cls, media_type: str) -> Optional[MediaTypeConfig]:
        """获取媒介类型配置"""
        return cls.MEDIA_CONFIGS.get(media_type)

    @classmethod
    def get_primary_structure_type(cls, media_type: str) -> Optional[str]:
        """获取媒介的主要结构类型（用于默认选择）"""
        config = cls.get_config(media_type)
        if config and config.primary_structure_types:
            return config.primary_structure_types[0].value
        return None

    @classmethod
    def get_production_params(cls, media_type: str) -> Optional[Dict[str, Any]]:
        """获取媒介的生产参数"""
        config = cls.get_config(media_type)
        if config:
            return config.production_params
        return None

    @classmethod
    def get_next_adapter(cls, media_type: str) -> Optional[str]:
        """获取下一个适配器"""
        config = cls.get_config(media_type)
        if config:
            return config.next_adapter
        return None

    @classmethod
    def get_all_supported_media_types(cls) -> List[str]:
        """获取所有支持的媒介类型"""
        return list(cls.MEDIA_CONFIGS.keys())

    @classmethod
    def adapt_structure_type(
        cls, media_type: str, content_goals: List[str], core_claim: str
    ) -> str:
        """
        根据媒介类型、内容目标和核心观点，选择合适的结构类型

        Args:
            media_type: 媒介类型
            content_goals: 内容目标列表（如 ["增长", "认知"]）
            core_claim: 核心观点

        Returns:
            选择的结构类型
        """
        config = cls.get_config(media_type)
        if not config:
            return StructureType.MIXED.value

        # 根据内容目标选择结构类型
        if "数据" in str(content_goals) or "转化" in str(content_goals):
            if StructureType.DATA_DRIVEN in config.primary_structure_types:
                return StructureType.DATA_DRIVEN.value
            if StructureType.DATA_DRIVEN in config.secondary_structure_types:
                return StructureType.DATA_DRIVEN.value

        if "教育" in str(content_goals) or "认知" in str(content_goals):
            if StructureType.INSTRUCTIONAL in config.primary_structure_types:
                return StructureType.INSTRUCTIONAL.value
            if StructureType.INSTRUCTIONAL in config.secondary_structure_types:
                return StructureType.INSTRUCTIONAL.value

        # 默认使用主要结构类型
        return config.primary_structure_types[0].value

    @classmethod
    def generate_media_plan_outline(
        cls, media_type: str, core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """
        根据媒介类型生成对应的大纲框架

        Args:
            media_type: 媒介类型
            core_claim: 核心观点
            content_goals: 内容目标

        Returns:
            大纲框架列表
        """
        config = cls.get_config(media_type)
        if not config:
            return []

        # 根据媒介类型生成不同的大纲框架
        if media_type == "article_wechat":
            return cls._generate_article_outline(core_claim, content_goals)
        elif media_type == "video_script":
            return cls._generate_video_outline(core_claim, content_goals)
        elif media_type == "image_post":
            return cls._generate_image_outline(core_claim, content_goals)
        elif media_type == "newsletter":
            return cls._generate_newsletter_outline(core_claim, content_goals)
        elif media_type == "short_video":
            return cls._generate_short_video_outline(core_claim, content_goals)
        elif media_type == "slide_deck":
            return cls._generate_slide_outline(core_claim, content_goals)
        elif media_type == "podcast_script":
            return cls._generate_podcast_outline(core_claim, content_goals)

        return []

    @staticmethod
    def _generate_article_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成公众号文章大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "开篇：建立共鸣",
                "purpose": "吸引读者，引出问题",
                "key_points": ["问题背景", "为什么现在讨论", "读者关心的点"],
                "content_length": "300-400字",
            },
            {
                "section_number": 2,
                "section_title": "核心论证",
                "purpose": "阐述核心观点",
                "key_points": ["主要论点", "支撑证据", "逻辑推导"],
                "content_length": "800-1000字",
            },
            {
                "section_number": 3,
                "section_title": "深度分析",
                "purpose": "提供洞察和启发",
                "key_points": ["案例分析", "数据支撑", "趋势预测"],
                "content_length": "600-800字",
            },
            {
                "section_number": 4,
                "section_title": "行动指南",
                "purpose": "提供可操作的建议",
                "key_points": ["实践建议", "资源推荐", "下一步行动"],
                "content_length": "400-500字",
            },
            {
                "section_number": 5,
                "section_title": "结尾：强化观点",
                "purpose": "总结要点，行动号召",
                "key_points": ["核心总结", "鼓励行动", "互动邀请"],
                "content_length": "200-300字",
            },
        ]

    @staticmethod
    def _generate_video_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成视频脚本大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "开场（Hook）",
                "purpose": "吸引观众，建立期待",
                "key_points": ["问题提出", "视觉冲击", "承诺价值"],
                "content_length": "30-60秒",
            },
            {
                "section_number": 2,
                "section_title": "背景介绍",
                "purpose": "提供上下文",
                "key_points": ["问题背景", "现状分析", "为什么重要"],
                "content_length": "1-2分钟",
            },
            {
                "section_number": 3,
                "section_title": "核心内容",
                "purpose": "传递主要信息",
                "key_points": ["核心观点", "案例展示", "数据支撑"],
                "content_length": "4-5分钟",
            },
            {
                "section_number": 4,
                "section_title": "互动环节",
                "purpose": "增加参与感",
                "key_points": ["提问", "讨论", "评论邀请"],
                "content_length": "1-2分钟",
            },
            {
                "section_number": 5,
                "section_title": "结尾（CTA）",
                "purpose": "行动号召",
                "key_points": ["总结要点", "下一步行动", "订阅邀请"],
                "content_length": "30-60秒",
            },
        ]

    @staticmethod
    def _generate_image_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成图文大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "封面图 + 标题",
                "purpose": "吸引点击",
                "key_points": ["视觉冲击", "标题吸引力", "核心观点预告"],
                "content_length": "标题 20-30字",
            },
            {
                "section_number": 2,
                "section_title": "问题陈述",
                "purpose": "建立共鸣",
                "key_points": ["问题描述", "现状分析", "为什么重要"],
                "content_length": "50-80字",
            },
            {
                "section_number": 3,
                "section_title": "对比/数据展示",
                "purpose": "提供证据",
                "key_points": ["对比图表", "数据可视化", "趋势分析"],
                "content_length": "配图为主",
            },
            {
                "section_number": 4,
                "section_title": "核心观点",
                "purpose": "传递主要信息",
                "key_points": ["核心论点", "关键数据", "洞察"],
                "content_length": "50-80字",
            },
            {
                "section_number": 5,
                "section_title": "行动号召",
                "purpose": "驱动互动",
                "key_points": ["下一步建议", "互动邀请", "链接/标签"],
                "content_length": "30-50字",
            },
        ]

    @staticmethod
    def _generate_newsletter_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成邮件通讯大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "主题行 + 摘要",
                "purpose": "吸引打开",
                "key_points": ["主题行", "摘要", "价值承诺"],
                "content_length": "主题行 50字，摘要 100字",
            },
            {
                "section_number": 2,
                "section_title": "核心内容",
                "purpose": "传递主要信息",
                "key_points": ["核心观点", "案例", "数据"],
                "content_length": "400-600字",
            },
            {
                "section_number": 3,
                "section_title": "推荐阅读",
                "purpose": "提供延伸内容",
                "key_points": ["相关文章", "资源推荐", "链接"],
                "content_length": "3-5个推荐",
            },
            {
                "section_number": 4,
                "section_title": "行动号召",
                "purpose": "驱动转化",
                "key_points": ["主CTA", "次CTA", "反馈邀请"],
                "content_length": "2个CTA按钮",
            },
        ]

    @staticmethod
    def _generate_short_video_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成短视频大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "Hook（3秒）",
                "purpose": "停留用户",
                "key_points": ["视觉冲击", "问题提出", "承诺价值"],
                "content_length": "3秒",
            },
            {
                "section_number": 2,
                "section_title": "核心内容（20-40秒）",
                "purpose": "传递信息",
                "key_points": ["核心观点", "案例展示", "数据"],
                "content_length": "20-40秒",
            },
            {
                "section_number": 3,
                "section_title": "结尾（10-20秒）",
                "purpose": "行动号召",
                "key_points": ["总结", "CTA", "互动邀请"],
                "content_length": "10-20秒",
            },
        ]

    @staticmethod
    def _generate_slide_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成幻灯片大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "标题页",
                "purpose": "介绍主题",
                "key_points": ["标题", "副标题", "演讲者信息"],
                "content_length": "1张",
            },
            {
                "section_number": 2,
                "section_title": "问题陈述",
                "purpose": "建立背景",
                "key_points": ["问题描述", "现状分析", "重要性"],
                "content_length": "2-3张",
            },
            {
                "section_number": 3,
                "section_title": "核心内容",
                "purpose": "传递主要信息",
                "key_points": ["核心观点", "数据支撑", "案例分析"],
                "content_length": "8-10张",
            },
            {
                "section_number": 4,
                "section_title": "行动方案",
                "purpose": "提供建议",
                "key_points": ["实践建议", "资源推荐", "下一步"],
                "content_length": "3-4张",
            },
            {
                "section_number": 5,
                "section_title": "结尾页",
                "purpose": "总结和互动",
                "key_points": ["核心总结", "联系方式", "Q&A"],
                "content_length": "1张",
            },
        ]

    @staticmethod
    def _generate_podcast_outline(
        core_claim: str, content_goals: List[str]
    ) -> List[Dict[str, Any]]:
        """生成播客脚本大纲"""
        return [
            {
                "section_number": 1,
                "section_title": "开场（1分钟）",
                "purpose": "欢迎听众",
                "key_points": ["节目名称", "主题介绍", "嘉宾介绍"],
                "content_length": "1分钟",
            },
            {
                "section_number": 2,
                "section_title": "背景介绍（3-5分钟）",
                "purpose": "提供上下文",
                "key_points": ["问题背景", "为什么重要", "嘉宾经历"],
                "content_length": "3-5分钟",
            },
            {
                "section_number": 3,
                "section_title": "核心讨论（12-18分钟）",
                "purpose": "深度对话",
                "key_points": ["核心观点", "案例分享", "互动讨论"],
                "content_length": "12-18分钟",
            },
            {
                "section_number": 4,
                "section_title": "听众互动（2-3分钟）",
                "purpose": "回答问题",
                "key_points": ["常见问题", "听众提问", "建议"],
                "content_length": "2-3分钟",
            },
            {
                "section_number": 5,
                "section_title": "结尾（1分钟）",
                "purpose": "总结和告别",
                "key_points": ["核心总结", "资源推荐", "下期预告"],
                "content_length": "1分钟",
            },
        ]
