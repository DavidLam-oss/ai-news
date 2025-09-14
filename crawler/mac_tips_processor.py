#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac技巧内容处理器
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .mac_tips_sources import MacTipsSources, MAC_TIPS_TEMPLATES
from .content_processor import ContentProcessor
from config.settings import settings

logger = logging.getLogger(__name__)

class MacTipsProcessor:
    """Mac技巧内容处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self.sources_manager = MacTipsSources()
        self.content_processor = ContentProcessor()
        self.templates = MAC_TIPS_TEMPLATES
    
    async def process_mac_tips(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """处理Mac技巧内容"""
        try:
            logger.info(f"开始处理 {len(articles)} 条Mac技巧内容")
            
            # 1. 内容分类和筛选
            categorized_tips = self._categorize_tips(articles)
            
            # 2. 生成小红书笔记内容
            xiaohongshu_content = await self._generate_xiaohongshu_content(categorized_tips)
            
            # 3. 生成技巧卡片
            tip_cards = self._generate_tip_cards(categorized_tips)
            
            # 4. 生成内容日历
            content_calendar = self._generate_content_calendar(categorized_tips)
            
            result = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "total_tips": len(articles),
                "categorized_tips": categorized_tips,
                "xiaohongshu_content": xiaohongshu_content,
                "tip_cards": tip_cards,
                "content_calendar": content_calendar,
                "created_at": datetime.now().isoformat()
            }
            
            logger.info("Mac技巧内容处理完成")
            return result
            
        except Exception as e:
            logger.error(f"处理Mac技巧内容失败: {e}")
            raise
    
    def _categorize_tips(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """对Mac技巧进行分类"""
        categorized = {}
        
        for article in articles:
            # 使用AI分类
            category = self.sources_manager.classify_tip(article.get('content', ''))
            
            if category not in categorized:
                categorized[category] = []
            
            # 添加分类信息
            article['category'] = category
            article['difficulty'] = self._assess_difficulty(article.get('content', ''))
            article['target_users'] = self._identify_target_users(article.get('content', ''))
            
            categorized[category].append(article)
        
        return categorized
    
    def _assess_difficulty(self, content: str) -> str:
        """评估技巧难度"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['基础', '入门', '新手', '简单']):
            return '初级'
        elif any(word in content_lower for word in ['高级', '专业', '复杂', '进阶']):
            return '高级'
        else:
            return '中级'
    
    def _identify_target_users(self, content: str) -> List[str]:
        """识别目标用户群体"""
        content_lower = content.lower()
        users = []
        
        if any(word in content_lower for word in ['职场', '办公', '工作']):
            users.append('职场人士')
        
        if any(word in content_lower for word in ['学生', '学习', '教育']):
            users.append('学生群体')
        
        if any(word in content_lower for word in ['设计', '开发', '编程']):
            users.append('专业人士')
        
        if not users:
            users = ['Mac用户']
        
        return users
    
    async def _generate_xiaohongshu_content(self, categorized_tips: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """生成小红书内容"""
        xiaohongshu_posts = []
        
        for category, tips in categorized_tips.items():
            if not tips:
                continue
            
            # 选择最优质的3-5个技巧
            selected_tips = tips[:5]
            
            # 生成标题
            title = self.sources_manager.generate_xiaohongshu_title(
                selected_tips[0].get('content', ''), category
            )
            
            # 生成正文内容
            content = await self._generate_xiaohongshu_body(selected_tips, category)
            
            # 生成标签
            tags = self._generate_xiaohongshu_tags(category, selected_tips)
            
            # 生成引流话术
            cta = self._generate_cta(category)
            
            post = {
                "title": title,
                "content": content,
                "tags": tags,
                "cta": cta,
                "category": category,
                "tips_count": len(selected_tips),
                "target_users": list(set([user for tip in selected_tips for user in tip.get('target_users', [])])),
                "difficulty": selected_tips[0].get('difficulty', '中级'),
                "image_suggestions": self._generate_image_suggestions(selected_tips)
            }
            
            xiaohongshu_posts.append(post)
        
        return xiaohongshu_posts
    
    async def _generate_xiaohongshu_body(self, tips: List[Dict[str, Any]], category: str) -> str:
        """生成小红书正文内容"""
        # 使用AI生成内容
        prompt = f"""
        基于以下Mac技巧内容，生成一篇小红书笔记正文，要求：
        
        1. 开头：描述痛点，引起共鸣
        2. 主体：介绍3-5个实用技巧，每个技巧包含：
           - 技巧名称
           - 适用场景
           - 操作步骤（简洁明了）
           - 效果说明
        3. 结尾：总结价值，引导互动
        
        分类：{category}
        技巧内容：
        {json.dumps([tip.get('content', '') for tip in tips], ensure_ascii=False, indent=2)}
        
        要求：
        - 语言生动有趣，符合小红书风格
        - 每个技巧用emoji标识
        - 总字数控制在800字以内
        - 包含实用的操作建议
        """
        
        try:
            # 使用现有的AI处理器
            result = await self.content_processor.process_with_ai(
                prompt, 
                enhancement_type="xiaohongshu_content"
            )
            return result.get('content', '')
        except Exception as e:
            logger.error(f"生成小红书内容失败: {e}")
            return self._generate_fallback_content(tips, category)
    
    def _generate_fallback_content(self, tips: List[Dict[str, Any]], category: str) -> str:
        """生成备用内容"""
        content = f"💻 Mac{category}技巧分享\n\n"
        
        for i, tip in enumerate(tips[:5], 1):
            content += f"🔸 技巧{i}：{tip.get('title', '实用技巧')}\n"
            content += f"   {tip.get('summary', '')}\n\n"
        
        content += "💡 更多技巧请评论获取完整资料包！"
        return content
    
    def _generate_xiaohongshu_tags(self, category: str, tips: List[Dict[str, Any]]) -> List[str]:
        """生成小红书标签"""
        base_tags = ["#Mac技巧", "#效率提升", "#苹果"]
        
        category_tags = {
            "基础操作": ["#Mac入门", "#新手必学"],
            "效率提升": ["#工作效率", "#快捷键"],
            "软件推荐": ["#Mac软件", "#应用推荐"],
            "系统优化": ["#系统设置", "#Mac优化"],
            "故障排除": ["#Mac问题", "#故障解决"],
            "专业应用": ["#Mac专业", "#设计工具"]
        }
        
        tags = base_tags + category_tags.get(category, [])
        
        # 根据技巧内容添加特定标签
        for tip in tips:
            content = tip.get('content', '').lower()
            if '快捷键' in content:
                tags.append("#快捷键")
            if '软件' in content:
                tags.append("#软件推荐")
            if '设置' in content:
                tags.append("#系统设置")
        
        return list(set(tags))[:10]  # 限制标签数量
    
    def _generate_cta(self, category: str) -> str:
        """生成引流话术"""
        ctas = {
            "基础操作": "评论\"Mac基础\"获取完整入门指南",
            "效率提升": "评论\"效率\"领取Mac效率提升资料包",
            "软件推荐": "评论\"软件\"获取Mac必装软件清单",
            "系统优化": "评论\"优化\"领取Mac系统优化指南",
            "故障排除": "评论\"问题\"获取Mac常见问题解决方案",
            "专业应用": "评论\"专业\"领取Mac专业应用技巧包"
        }
        
        return ctas.get(category, "评论\"Mac\"获取完整技巧资料包")
    
    def _generate_image_suggestions(self, tips: List[Dict[str, Any]]) -> List[str]:
        """生成配图建议"""
        suggestions = []
        
        for tip in tips:
            content = tip.get('content', '').lower()
            
            if '快捷键' in content:
                suggestions.append("Mac键盘快捷键示意图")
            elif '软件' in content:
                suggestions.append("Mac软件界面截图")
            elif '设置' in content:
                suggestions.append("系统设置界面截图")
            else:
                suggestions.append("Mac操作步骤截图")
        
        return suggestions[:3]  # 限制配图建议数量
    
    def _generate_tip_cards(self, categorized_tips: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """生成技巧卡片"""
        tip_cards = []
        
        for category, tips in categorized_tips.items():
            for tip in tips:
                card = self.sources_manager.generate_tip_card({
                    "title": tip.get('title', 'Mac技巧'),
                    "scenario": f"{category}场景",
                    "steps": tip.get('content', '')[:200] + "...",
                    "notes": "请根据实际情况调整操作步骤",
                    "image_suggestion": f"{category}操作截图"
                })
                
                card.update({
                    "category": category,
                    "difficulty": tip.get('difficulty', '中级'),
                    "target_users": tip.get('target_users', ['Mac用户']),
                    "source": tip.get('source', '未知'),
                    "url": tip.get('url', '')
                })
                
                tip_cards.append(card)
        
        return tip_cards
    
    def _generate_content_calendar(self, categorized_tips: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """生成内容日历"""
        calendar = []
        current_date = datetime.now()
        
        for i, (category, tips) in enumerate(categorized_tips.items()):
            if not tips:
                continue
            
            # 计算发布时间（每天一篇）
            publish_date = current_date.replace(day=current_date.day + i)
            
            # 选择最佳技巧
            best_tip = max(tips, key=lambda x: len(x.get('content', '')))
            
            calendar_item = {
                "date": publish_date.strftime('%Y-%m-%d'),
                "category": category,
                "title": self.sources_manager.generate_xiaohongshu_title(
                    best_tip.get('content', ''), category
                ),
                "content_type": "小红书笔记",
                "target_users": best_tip.get('target_users', ['Mac用户']),
                "difficulty": best_tip.get('difficulty', '中级'),
                "tags": self._generate_xiaohongshu_tags(category, [best_tip]),
                "cta": self._generate_cta(category),
                "status": "待发布"
            }
            
            calendar.append(calendar_item)
        
        return calendar
