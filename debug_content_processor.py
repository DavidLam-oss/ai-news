#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试内容处理器
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from crawler.content_processor import ContentProcessor

async def debug_content_processor():
    """调试内容处理器"""
    
    print("🔍 调试内容处理器...")
    print(f"DeepSeek API Key: {settings.DEEPSEEK_API_KEY[:10] if settings.DEEPSEEK_API_KEY else 'None'}...")
    print(f"OpenAI API Key: {settings.OPENAI_API_KEY[:10] if settings.OPENAI_API_KEY else 'None'}...")
    
    # 创建内容处理器
    processor = ContentProcessor()
    
    print(f"AI Client: {processor.ai_client}")
    print(f"AI Model: {processor.ai_model}")
    
    # 测试文章
    test_articles = [
        {
            "title": "测试文章",
            "summary": "这是一个测试文章",
            "source": "测试源",
            "url": "https://example.com",
            "publish_time": "2024-01-15T10:00:00Z"
        }
    ]
    
    print("\n🚀 开始处理文章...")
    
    try:
        result = await processor.process_articles(test_articles)
        print("✅ 处理成功！")
        print(f"摘要: {result['summary'][:100]}...")
        print(f"趋势: {result['trends']}")
        print(f"图片提示词: {result['image_prompts']}")
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_content_processor())

