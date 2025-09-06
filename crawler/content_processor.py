#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容处理模块
使用AI处理爬取的内容，生成早报
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from loguru import logger

from config.settings import settings, AI_PROMPTS

class ContentProcessor:
    """内容处理器"""
    
    def __init__(self):
        """初始化内容处理器"""
        self.openai_client = openai.AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
    
    async def process_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """处理文章列表，生成早报内容"""
        try:
            # 准备文章内容
            articles_text = self._format_articles_for_ai(articles)
            
            # 并行处理多个AI任务
            tasks = [
                self._generate_summary(articles_text),
                self._analyze_trends(articles_text),
                self._generate_image_prompts(articles_text)
            ]
            
            summary, trends, image_prompts = await asyncio.gather(*tasks)
            
            return {
                'summary': summary,
                'trends': trends,
                'image_prompts': image_prompts,
                'articles': articles[:10],  # 只保留前10篇重要文章
                'total_articles': len(articles),
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"处理文章内容失败: {e}")
            raise
    
    def _format_articles_for_ai(self, articles: List[Dict[str, Any]]) -> str:
        """格式化文章内容供AI处理"""
        formatted_articles = []
        
        for i, article in enumerate(articles[:20], 1):  # 只处理前20篇
            formatted_article = f"""
文章 {i}:
标题: {article.get('title', 'N/A')}
来源: {article.get('source', 'N/A')}
发布时间: {article.get('publish_time', 'N/A')}
摘要: {article.get('summary', 'N/A')}
链接: {article.get('url', 'N/A')}
"""
            formatted_articles.append(formatted_article)
        
        return "\n".join(formatted_articles)
    
    async def _generate_summary(self, articles_text: str) -> str:
        """生成早报摘要"""
        try:
            prompt = AI_PROMPTS['summary'].format(articles=articles_text)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的AI科技早报编辑，擅长将复杂的科技新闻整理成简洁易懂的早报。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info("早报摘要生成成功")
            return summary
            
        except Exception as e:
            logger.error(f"生成早报摘要失败: {e}")
            return "今日AI科技新闻摘要生成失败，请查看详细内容。"
    
    async def _analyze_trends(self, articles_text: str) -> List[str]:
        """分析AI发展趋势"""
        try:
            prompt = AI_PROMPTS['trends'].format(articles=articles_text)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个AI行业分析师，擅长识别和分析AI技术的发展趋势。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            trends_text = response.choices[0].message.content.strip()
            
            # 将趋势文本转换为列表
            trends = [trend.strip() for trend in trends_text.split('\n') if trend.strip()]
            logger.info(f"分析出 {len(trends)} 个发展趋势")
            return trends
            
        except Exception as e:
            logger.error(f"分析发展趋势失败: {e}")
            return ["AI技术持续快速发展", "各行业AI应用不断深化"]
    
    async def _generate_image_prompts(self, articles_text: str) -> List[str]:
        """生成图片提示词"""
        try:
            prompt = AI_PROMPTS['image_prompts'].format(articles=articles_text)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的视觉设计师，擅长为AI科技内容创作视觉提示词。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            prompts_text = response.choices[0].message.content.strip()
            
            # 将提示词文本转换为列表
            prompts = [prompt.strip() for prompt in prompts_text.split('\n') if prompt.strip()]
            
            # 确保有3个提示词
            while len(prompts) < 3:
                prompts.append("AI科技未来场景，简洁现代设计风格")
            
            logger.info(f"生成了 {len(prompts)} 个图片提示词")
            return prompts[:3]
            
        except Exception as e:
            logger.error(f"生成图片提示词失败: {e}")
            return [
                "AI科技未来场景，简洁现代设计风格",
                "人工智能与人类协作，科技感十足",
                "数字化世界，AI驱动的未来生活"
            ]
    
    async def enhance_content(self, content: str, enhancement_type: str = "summary") -> str:
        """增强内容质量"""
        try:
            enhancement_prompts = {
                "summary": "请将以下内容优化为更简洁、更吸引人的摘要：",
                "title": "请为以下内容生成一个吸引人的标题：",
                "trend": "请将以下内容优化为更专业的发展趋势分析："
            }
            
            prompt = enhancement_prompts.get(enhancement_type, "请优化以下内容：")
            full_prompt = f"{prompt}\n\n{content}"
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的内容编辑，擅长优化各种类型的文本内容。"},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            enhanced_content = response.choices[0].message.content.strip()
            logger.info(f"内容增强成功: {enhancement_type}")
            return enhanced_content
            
        except Exception as e:
            logger.error(f"内容增强失败: {e}")
            return content
    
    def filter_articles_by_keywords(self, articles: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """根据关键词过滤文章"""
        filtered_articles = []
        
        for article in articles:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            content = article.get('content', '').lower()
            
            # 检查是否包含任何关键词
            for keyword in keywords:
                if keyword.lower() in title or keyword.lower() in summary or keyword.lower() in content:
                    filtered_articles.append(article)
                    break
        
        return filtered_articles
    
    def rank_articles_by_importance(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """根据重要性对文章进行排序"""
        # 定义重要性关键词
        importance_keywords = {
            'high': ['突破', '重大', '首次', '革命性', '里程碑', '创新', '领先'],
            'medium': ['发布', '推出', '合作', '投资', '融资', '上市'],
            'low': ['更新', '优化', '改进', '修复', '调整']
        }
        
        def calculate_importance_score(article):
            score = 0
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            
            # 检查高重要性关键词
            for keyword in importance_keywords['high']:
                if keyword in title or keyword in summary:
                    score += 3
            
            # 检查中等重要性关键词
            for keyword in importance_keywords['medium']:
                if keyword in title or keyword in summary:
                    score += 2
            
            # 检查低重要性关键词
            for keyword in importance_keywords['low']:
                if keyword in title or keyword in summary:
                    score += 1
            
            # 根据来源权重调整分数
            source_weight = article.get('source_weight', 1.0)
            score *= source_weight
            
            return score
        
        # 计算分数并排序
        scored_articles = []
        for article in articles:
            article['importance_score'] = calculate_importance_score(article)
            scored_articles.append(article)
        
        # 按分数降序排序
        ranked_articles = sorted(scored_articles, key=lambda x: x['importance_score'], reverse=True)
        
        return ranked_articles
