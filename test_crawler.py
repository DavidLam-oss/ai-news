#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试爬虫功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor

async def test_crawler():
    """测试爬虫功能"""
    
    print("🕷️ 开始测试爬虫功能...")
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 初始化爬虫
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 测试爬取一个简单的网站
        print("🔍 正在爬取测试网站...")
        
        # 使用crawl4ai爬取一个简单的AI新闻网站
        from crawl4ai import AsyncWebCrawler
        
        # 创建一个简单的测试
        test_url = "https://www.36kr.com"
        
        print(f"📰 正在爬取: {test_url}")
        
        # 执行爬取
        result = await crawler.crawler.arun(
            url=test_url,
            wait_for="networkidle",
            delay_before_return_html=2
        )
        
        if result.success:
            print("✅ 爬取成功！")
            print(f"📄 页面标题: {result.metadata.get('title', 'N/A')}")
            print(f"📊 内容长度: {len(result.html)} 字符")
            
            # 提取一些文本内容
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(result.html, 'html.parser')
            
            # 查找可能的新闻标题
            titles = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if tag.get_text().strip():
                    titles.append(tag.get_text().strip())
            
            print(f"📰 找到 {len(titles)} 个标题:")
            for i, title in enumerate(titles[:5], 1):  # 只显示前5个
                print(f"  {i}. {title}")
            
            # 模拟一些文章数据
            mock_articles = [
                {
                    "title": "AI技术突破：大语言模型性能再创新高",
                    "summary": "最新研究显示，大语言模型在多个基准测试中表现优异，为AI应用带来新的可能性。",
                    "source": "36氪",
                    "url": "https://example.com/ai-breakthrough",
                    "publish_time": "2024-01-15T10:00:00Z"
                },
                {
                    "title": "OpenAI发布GPT-4 Turbo，成本降低50%",
                    "summary": "OpenAI宣布推出GPT-4 Turbo模型，在保持高质量输出的同时，大幅降低了使用成本。",
                    "source": "机器之心",
                    "url": "https://example.com/gpt4-turbo",
                    "publish_time": "2024-01-15T11:00:00Z"
                },
                {
                    "title": "Google Gemini多模态AI能力突出",
                    "summary": "Google发布的Gemini模型在图像、文本、音频等多模态任务上表现优异，超越了之前的模型。",
                    "source": "量子位",
                    "url": "https://example.com/gemini",
                    "publish_time": "2024-01-15T12:00:00Z"
                }
            ]
            
            print("\n🤖 使用火山方舟DeepSeek处理内容...")
            
            # 使用内容处理器处理文章
            processor = ContentProcessor()
            result = await processor.process_articles(mock_articles)
            
            print("✅ 内容处理完成！")
            print("\n📋 早报摘要:")
            print("-" * 50)
            print(result['summary'])
            
            print("\n📈 发展趋势:")
            print("-" * 50)
            for i, trend in enumerate(result['trends'], 1):
                print(f"{i}. {trend}")
            
            print("\n🎨 图片提示词:")
            print("-" * 50)
            for i, prompt in enumerate(result['image_prompts'], 1):
                print(f"{i}. {prompt}")
                
        else:
            print("❌ 爬取失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("🧹 资源清理完成")

if __name__ == "__main__":
    asyncio.run(test_crawler())

