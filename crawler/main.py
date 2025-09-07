#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI早报爬虫服务主程序
基于crawl4ai实现智能爬虫，抓取AI科技资讯
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy, LLMConfig
from loguru import logger
import schedule
import time
from dotenv import load_dotenv

from config.settings import Settings
from crawler.news_sources import NewsSources
from crawler.content_processor import ContentProcessor
import uvicorn

# 加载环境变量
load_dotenv()

class AINewsCrawler:
    """AI早报爬虫主类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.settings = Settings()
        self.news_sources = NewsSources()
        self.content_processor = ContentProcessor()
        self.crawler = None
        
        # 配置日志
        logger.add(
            "logs/crawler.log",
            rotation="1 day",
            retention="30 days",
            level=self.settings.LOG_LEVEL
        )
        
    async def init_crawler(self):
        """初始化爬虫引擎"""
        try:
            self.crawler = AsyncWebCrawler(
                headless=True,
                browser_type="chromium",
                user_agent=self.settings.USER_AGENT
            )
            await self.crawler.start()
            logger.info("爬虫引擎初始化成功")
        except Exception as e:
            logger.error(f"爬虫引擎初始化失败: {e}")
            raise
    
    async def crawl_news_sources(self) -> List[Dict[str, Any]]:
        """爬取所有新闻源"""
        all_articles = []
        
        # 使用简化的爬取策略，避免LLM提取的复杂性
        for source in self.news_sources.get_sources()[:3]:  # 先测试前3个源
            try:
                logger.info(f"开始爬取: {source['name']}")
                
                # 执行简单爬取
                result = await self.crawler.arun(
                    url=source['url'],
                    wait_for="networkidle",
                    delay_before_return_html=3,
                    js_code="""
                    // 等待页面加载完成
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                    // 尝试滚动页面以触发懒加载
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(resolve => setTimeout(resolve, 1500));
                    window.scrollTo(0, 0);
                    """
                )
                
                if result.success:
                    # 使用我们成功的文章提取逻辑
                    from improved_crawler_test import extract_articles_improved
                    articles = extract_articles_improved(result.html, source['name'], source['url'])
                    
                    # 添加来源信息
                    for article in articles:
                        article['source_url'] = source['url']
                        article['crawl_time'] = datetime.now().isoformat()
                    
                    all_articles.extend(articles)
                    logger.info(f"从 {source['name']} 获取到 {len(articles)} 篇文章")
                else:
                    logger.warning(f"爬取 {source['name']} 失败")
                    
            except Exception as e:
                logger.error(f"爬取 {source['name']} 时发生错误: {e}")
                continue
        
        # 去重和排序
        unique_articles = self._deduplicate_articles(all_articles)
        sorted_articles = sorted(
            unique_articles, 
            key=lambda x: x.get('publish_time', ''), 
            reverse=True
        )
        
        logger.info(f"总共获取到 {len(sorted_articles)} 篇去重后的文章")
        return sorted_articles[:self.settings.MAX_ARTICLES]
    
    def _deduplicate_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """文章去重"""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
    
    async def generate_daily_report(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成每日早报"""
        try:
            # 使用AI处理内容
            processed_content = await self.content_processor.process_articles(articles)
            
            # 生成早报
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'title': f"AI科技早报 - {datetime.now().strftime('%Y年%m月%d日')}",
                'summary': processed_content['summary'],
                'articles': processed_content['articles'],
                'trends': processed_content['trends'],
                'image_prompts': processed_content['image_prompts'],
                'created_at': datetime.now().isoformat()
            }
            
            logger.info("每日早报生成成功")
            return report
            
        except Exception as e:
            logger.error(f"生成每日早报失败: {e}")
            raise
    
    async def save_to_feishu(self, report: Dict[str, Any]) -> bool:
        """保存到飞书多维表格"""
        try:
            from feishu.client import FeishuClient
            
            client = FeishuClient()
            
            # 准备数据 - 使用正确的字段名称和日期格式
            from datetime import datetime
            current_date = datetime.now()
            
            record_data = {
                '日期': int(current_date.timestamp() * 1000),  # 使用时间戳格式
                '早报原始内容': json.dumps(report, ensure_ascii=False, indent=2),
                '图片提示词1': report['image_prompts'][0] if len(report['image_prompts']) > 0 else '',
                '图片提示词2': report['image_prompts'][1] if len(report['image_prompts']) > 1 else '',
                '图片提示词3': report['image_prompts'][2] if len(report['image_prompts']) > 2 else ''
            }
            
            # 创建记录
            success = await client.create_record(record_data)
            
            if success:
                logger.info("早报已保存到飞书多维表格")
            else:
                logger.error("保存到飞书多维表格失败")
                
            return success
            
        except Exception as e:
            logger.error(f"保存到飞书多维表格时发生错误: {e}")
            return False
    
    async def run_daily_crawl(self):
        """执行每日爬取任务"""
        try:
            logger.info("开始执行每日爬取任务")
            
            # 爬取新闻
            articles = await self.crawl_news_sources()
            
            if not articles:
                logger.warning("未获取到任何文章，跳过早报生成")
                return
            
            # 生成早报
            report = await self.generate_daily_report(articles)
            
            # 保存到飞书
            await self.save_to_feishu(report)
            
            # 微信发送功能已移除（风险规避）
            
            logger.info("每日爬取任务完成")
            
        except Exception as e:
            logger.error(f"执行每日爬取任务失败: {e}")
    
    # 微信发送功能已移除（风险规避）
    
    async def cleanup(self):
        """清理资源"""
        if self.crawler:
            await self.crawler.close()
            logger.info("爬虫引擎已关闭")

def run_scheduler():
    """运行定时任务"""
    crawler = AINewsCrawler()
    
    # 设置定时任务 - 每天上午8点执行
    schedule.every().day.at("08:00").do(
        lambda: asyncio.run(crawler.run_daily_crawl())
    )
    
    # 也可以设置每小时执行一次（用于测试）
    if os.getenv('DEBUG', 'False').lower() == 'true':
        schedule.every().hour.do(
            lambda: asyncio.run(crawler.run_daily_crawl())
        )
    
    logger.info("定时任务已启动，每天上午8点执行爬取")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

async def main():
    """主函数"""
    crawler = AINewsCrawler()
    
    try:
        # 初始化爬虫
        await crawler.init_crawler()
        
        # 执行一次爬取（用于测试）
        await crawler.run_daily_crawl()
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭...")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        await crawler.cleanup()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI早报爬虫服务")
    parser.add_argument("--mode", choices=["once", "schedule", "api"], 
                       default="once", help="运行模式")
    parser.add_argument("--host", default="0.0.0.0", help="API服务主机")
    parser.add_argument("--port", type=int, default=8000, help="API服务端口")
    
    args = parser.parse_args()
    
    if args.mode == "once":
        # 执行一次爬取
        asyncio.run(main())
    elif args.mode == "schedule":
        # 运行定时任务
        run_scheduler()
    elif args.mode == "api":
        # 启动API服务
        uvicorn.run(app, host=args.host, port=args.port)
