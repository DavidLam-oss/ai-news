#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac技巧专用爬虫
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from crawl4ai import AsyncWebCrawler
from .mac_tips_sources import MacTipsSources
from .mac_tips_processor import MacTipsProcessor
from .content_processor import ContentProcessor
from feishu.client import FeishuClient
from config.settings import settings

logger = logging.getLogger(__name__)

class MacTipsCrawler:
    """Mac技巧专用爬虫"""
    
    def __init__(self):
        """初始化爬虫"""
        self.sources_manager = MacTipsSources()
        self.processor = MacTipsProcessor()
        self.content_processor = ContentProcessor()
        self.feishu_client = FeishuClient()
        self.crawler = None
    
    async def initialize(self):
        """初始化爬虫"""
        try:
            self.crawler = AsyncWebCrawler(
                headless=True,
                user_agent=settings.USER_AGENT
            )
            await self.crawler.astart()
            logger.info("Mac技巧爬虫初始化完成")
        except Exception as e:
            logger.error(f"Mac技巧爬虫初始化失败: {e}")
            raise
    
    async def crawl_mac_tips(self) -> Dict[str, Any]:
        """爬取Mac技巧内容"""
        try:
            logger.info("开始爬取Mac技巧内容")
            
            # 获取Mac技巧源
            sources = self.sources_manager.get_sources_by_weight()
            
            all_articles = []
            
            # 爬取每个源的内容
            for source in sources:
                try:
                    articles = await self._crawl_source(source)
                    all_articles.extend(articles)
                    logger.info(f"从 {source['name']} 爬取到 {len(articles)} 条内容")
                except Exception as e:
                    logger.error(f"爬取 {source['name']} 失败: {e}")
                    continue
            
            logger.info(f"总共爬取到 {len(all_articles)} 条Mac技巧内容")
            
            # 处理内容
            processed_result = await self.processor.process_mac_tips(all_articles)
            
            # 保存到飞书
            await self._save_to_feishu(processed_result)
            
            return processed_result
            
        except Exception as e:
            logger.error(f"爬取Mac技巧内容失败: {e}")
            raise
    
    async def _crawl_source(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """爬取单个源的内容"""
        try:
            url = source['url']
            selectors = source.get('selectors', {})
            
            # 爬取页面内容
            result = await self.crawler.arun(
                url=url,
                word_count_threshold=50,
                extraction_strategy="LLMExtractionStrategy",
                extraction_schema={
                    "type": "object",
                    "properties": {
                        "articles": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "content": {"type": "string"},
                                    "url": {"type": "string"},
                                    "summary": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
            
            if not result.success:
                logger.warning(f"爬取 {source['name']} 失败: {result.error_message}")
                return []
            
            # 解析内容
            articles = []
            extracted_data = result.extracted_content
            
            if isinstance(extracted_data, dict) and 'articles' in extracted_data:
                for article_data in extracted_data['articles']:
                    article = {
                        'title': article_data.get('title', ''),
                        'content': article_data.get('content', ''),
                        'url': article_data.get('url', ''),
                        'summary': article_data.get('summary', ''),
                        'source': source['name'],
                        'category': source['category'],
                        'weight': source['weight'],
                        'crawled_at': datetime.now().isoformat()
                    }
                    
                    # 过滤Mac技巧相关内容
                    if self._is_mac_tips_related(article):
                        articles.append(article)
            
            return articles
            
        except Exception as e:
            logger.error(f"爬取源 {source['name']} 失败: {e}")
            return []
    
    def _is_mac_tips_related(self, article: Dict[str, Any]) -> bool:
        """判断是否为Mac技巧相关内容"""
        mac_keywords = [
            'mac', 'macbook', 'macos', '苹果', 'apple',
            '快捷键', '技巧', '教程', '使用', '操作',
            '效率', '软件', '应用', '工具', '设置'
        ]
        
        content = (article.get('title', '') + ' ' + 
                  article.get('content', '') + ' ' + 
                  article.get('summary', '')).lower()
        
        return any(keyword in content for keyword in mac_keywords)
    
    async def _save_to_feishu(self, processed_result: Dict[str, Any]):
        """保存到飞书多维表格"""
        try:
            if not settings.FEISHU_TABLE_TOKEN:
                logger.warning("未配置飞书表格Token，跳过保存")
                return
            
            # 保存技巧卡片
            tip_cards = processed_result.get('tip_cards', [])
            for card in tip_cards:
                await self.feishu_client.create_record({
                    "技巧名称": card.get('标题', ''),
                    "分类": card.get('category', ''),
                    "适用场景": card.get('适用场景', ''),
                    "操作步骤": card.get('操作步骤', ''),
                    "注意事项": card.get('注意事项', ''),
                    "配图建议": card.get('配图建议', ''),
                    "难度": card.get('difficulty', ''),
                    "目标用户": ', '.join(card.get('target_users', [])),
                    "来源": card.get('source', ''),
                    "创建时间": processed_result.get('created_at', '')
                })
            
            # 保存小红书内容
            xiaohongshu_content = processed_result.get('xiaohongshu_content', [])
            for content in xiaohongshu_content:
                await self.feishu_client.create_record({
                    "标题": content.get('title', ''),
                    "内容类型": "小红书笔记",
                    "分类": content.get('category', ''),
                    "正文": content.get('content', ''),
                    "标签": ', '.join(content.get('tags', [])),
                    "引流话术": content.get('cta', ''),
                    "目标用户": ', '.join(content.get('target_users', [])),
                    "难度": content.get('difficulty', ''),
                    "配图建议": ', '.join(content.get('image_suggestions', [])),
                    "创建时间": processed_result.get('created_at', '')
                })
            
            # 保存内容日历
            content_calendar = processed_result.get('content_calendar', [])
            for calendar_item in content_calendar:
                await self.feishu_client.create_record({
                    "发布日期": calendar_item.get('date', ''),
                    "内容类型": calendar_item.get('content_type', ''),
                    "分类": calendar_item.get('category', ''),
                    "标题": calendar_item.get('title', ''),
                    "目标用户": ', '.join(calendar_item.get('target_users', [])),
                    "难度": calendar_item.get('difficulty', ''),
                    "标签": ', '.join(calendar_item.get('tags', [])),
                    "引流话术": calendar_item.get('cta', ''),
                    "状态": calendar_item.get('status', ''),
                    "创建时间": processed_result.get('created_at', '')
                })
            
            logger.info("Mac技巧内容已保存到飞书多维表格")
            
        except Exception as e:
            logger.error(f"保存到飞书失败: {e}")
    
    async def run_daily_mac_tips_crawl(self):
        """运行每日Mac技巧爬取任务"""
        try:
            logger.info("开始执行每日Mac技巧爬取任务")
            
            # 初始化爬虫
            await self.initialize()
            
            # 爬取内容
            result = await self.crawl_mac_tips()
            
            logger.info(f"每日Mac技巧爬取任务完成，共处理 {result.get('total_tips', 0)} 条技巧")
            
            return result
            
        except Exception as e:
            logger.error(f"执行每日Mac技巧爬取任务失败: {e}")
            raise
        finally:
            if self.crawler:
                await self.crawler.aclose()
    
    async def cleanup(self):
        """清理资源"""
        if self.crawler:
            await self.crawler.aclose()
            logger.info("Mac技巧爬虫资源已清理")

# 便捷函数
async def run_mac_tips_crawl():
    """运行Mac技巧爬取"""
    crawler = MacTipsCrawler()
    try:
        return await crawler.run_daily_mac_tips_crawl()
    finally:
        await crawler.cleanup()

if __name__ == "__main__":
    # 测试运行
    asyncio.run(run_mac_tips_crawl())
