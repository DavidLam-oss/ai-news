#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac技巧源管理模块
"""

from typing import List, Dict, Any

# Mac技巧相关源配置
MAC_TIPS_SOURCES = [
    {
        "name": "MacRumors",
        "url": "https://www.macrumors.com",
        "category": "mac_tips",
        "weight": 1.5,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary",
            "content": ".article-content"
        },
        "description": "Mac最新资讯和技巧"
    },
    {
        "name": "Apple Support",
        "url": "https://support.apple.com",
        "category": "mac_tips",
        "weight": 1.8,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        },
        "description": "苹果官方支持文档"
    },
    {
        "name": "少数派",
        "url": "https://sspai.com",
        "category": "mac_tips",
        "weight": 1.3,
        "selectors": {
            "title": ".title",
            "link": ".title a",
            "summary": ".summary"
        },
        "description": "Mac使用技巧和软件推荐"
    },
    {
        "name": "Mac玩儿法",
        "url": "https://www.waerfa.com",
        "category": "mac_tips",
        "weight": 1.2,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        },
        "description": "Mac使用技巧分享"
    },
    {
        "name": "Mac毒",
        "url": "https://www.macdo.cn",
        "category": "mac_tips",
        "weight": 1.1,
        "selectors": {
            "title": ".title",
            "link": ".title a",
            "summary": ".summary"
        },
        "description": "Mac软件和技巧"
    },
    {
        "name": "MacWk",
        "url": "https://www.macwk.com",
        "category": "mac_tips",
        "weight": 1.0,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        },
        "description": "Mac软件下载和技巧"
    }
]

# Mac技巧分类
MAC_TIPS_CATEGORIES = {
    "基础操作": {
        "keywords": ["快捷键", "基础", "入门", "新手", "操作"],
        "description": "Mac基础操作技巧"
    },
    "效率提升": {
        "keywords": ["效率", "快捷", "自动化", "工作流", "提升"],
        "description": "提升Mac使用效率的技巧"
    },
    "软件推荐": {
        "keywords": ["软件", "应用", "推荐", "工具", "神器"],
        "description": "Mac软件推荐和使用技巧"
    },
    "系统优化": {
        "keywords": ["系统", "优化", "设置", "配置", "性能"],
        "description": "Mac系统优化和配置技巧"
    },
    "故障排除": {
        "keywords": ["故障", "问题", "解决", "修复", "错误"],
        "description": "Mac常见问题解决方案"
    },
    "专业应用": {
        "keywords": ["设计", "开发", "编程", "视频", "音频"],
        "description": "Mac专业应用技巧"
    }
}

# Mac技巧内容模板
MAC_TIPS_TEMPLATES = {
    "小红书笔记": {
        "标题模板": [
            "Mac用了{time}才知道的{feature}，{benefit}！",
            "{feature}不用{problem}，这{number}个技巧让你{result}",
            "Mac新手必学！{feature}的{number}个{type}技巧",
            "{feature}效率提升{number}倍，这{number}个{type}太实用了",
            "Mac{feature}隐藏技巧，{benefit}不是梦"
        ],
        "正文结构": {
            "开头": "痛点描述 + 解决方案预告",
            "主体": "3-5个实用技巧 + 配图建议",
            "结尾": "总结 + 引流话术"
        },
        "引流话术": [
            "评论\"{keyword}\"获取完整{type}清单",
            "私信\"{keyword}\"免费获取{type}资料包",
            "评论\"{keyword}\"领取{type}模板"
        ]
    },
    "技巧卡片": {
        "格式": {
            "标题": "技巧名称",
            "适用场景": "使用场景描述",
            "操作步骤": "详细操作步骤",
            "注意事项": "使用注意事项",
            "配图建议": "配图描述"
        }
    }
}

class MacTipsSources:
    """Mac技巧源管理类"""
    
    def __init__(self):
        """初始化Mac技巧源"""
        self.sources = MAC_TIPS_SOURCES
        self.categories = MAC_TIPS_CATEGORIES
        self.templates = MAC_TIPS_TEMPLATES
    
    def get_sources(self) -> List[Dict[str, Any]]:
        """获取所有Mac技巧源"""
        return self.sources
    
    def get_sources_by_weight(self) -> List[Dict[str, Any]]:
        """获取按权重排序的Mac技巧源"""
        return sorted(self.sources, key=lambda x: x.get('weight', 1.0), reverse=True)
    
    def get_categories(self) -> Dict[str, Dict[str, Any]]:
        """获取Mac技巧分类"""
        return self.categories
    
    def get_templates(self) -> Dict[str, Any]:
        """获取内容模板"""
        return self.templates
    
    def classify_tip(self, content: str) -> str:
        """根据内容自动分类Mac技巧"""
        content_lower = content.lower()
        
        for category, info in self.categories.items():
            for keyword in info['keywords']:
                if keyword in content_lower:
                    return category
        
        return "基础操作"  # 默认分类
    
    def generate_xiaohongshu_title(self, tip_content: str, category: str) -> str:
        """生成小红书标题"""
        import random
        
        templates = self.templates["小红书笔记"]["标题模板"]
        template = random.choice(templates)
        
        # 根据分类和内容填充模板变量
        variables = {
            "time": random.choice(["3年", "5年", "这么久"]),
            "feature": self._extract_feature(tip_content),
            "benefit": random.choice(["效率翻倍", "告别加班", "轻松搞定"]),
            "problem": random.choice(["熬夜", "加班", "麻烦"]),
            "number": random.choice(["3", "5", "10"]),
            "type": random.choice(["实用", "隐藏", "高效"]),
            "result": random.choice(["轻松搞定", "效率翻倍", "事半功倍"])
        }
        
        return template.format(**variables)
    
    def _extract_feature(self, content: str) -> str:
        """从内容中提取主要功能特征"""
        features = ["快捷键", "文件管理", "系统设置", "软件使用", "效率工具"]
        
        for feature in features:
            if feature in content:
                return feature
        
        return "隐藏功能"
    
    def generate_tip_card(self, tip_data: Dict[str, Any]) -> Dict[str, str]:
        """生成技巧卡片"""
        card_format = self.templates["技巧卡片"]["格式"]
        
        return {
            "标题": tip_data.get("title", "Mac技巧"),
            "适用场景": tip_data.get("scenario", "日常使用"),
            "操作步骤": tip_data.get("steps", "详细步骤"),
            "注意事项": tip_data.get("notes", "使用注意"),
            "配图建议": tip_data.get("image_suggestion", "操作截图")
        }
