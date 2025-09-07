#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示AI内容处理效果
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.content_processor import ContentProcessor

async def demo_ai_processing():
    """演示AI内容处理效果"""
    
    print("🤖 AI早报系统内容处理演示")
    print("=" * 60)
    
    # 模拟真实的AI科技新闻
    articles = [
        {
            "title": "OpenAI发布GPT-4 Turbo模型，性能大幅提升",
            "summary": "OpenAI发布了新的GPT-4 Turbo模型，在保持高质量输出的同时，处理速度提升了3倍，成本降低了50%。该模型在代码生成、数学推理和创意写作等任务上表现优异。",
            "source": "36氪",
            "url": "https://example.com/1",
            "publish_time": "2024-01-15T10:00:00Z"
        },
        {
            "title": "Google推出Gemini AI模型，多模态能力突出",
            "summary": "Google发布了新的Gemini AI模型，在图像、文本、音频等多模态任务上表现优异，超越了GPT-4。该模型能够同时理解和处理多种类型的数据，为AI应用开辟了新的可能性。",
            "source": "机器之心",
            "url": "https://example.com/2",
            "publish_time": "2024-01-15T11:00:00Z"
        },
        {
            "title": "Meta发布Llama 3模型，开源AI竞争加剧",
            "summary": "Meta发布了Llama 3开源大语言模型，在多个基准测试中表现优异，进一步推动了开源AI的发展。该模型支持多种语言，在代码生成和数学推理方面表现突出。",
            "source": "量子位",
            "url": "https://example.com/3",
            "publish_time": "2024-01-15T12:00:00Z"
        },
        {
            "title": "Anthropic发布Claude 3，AI安全成为焦点",
            "summary": "Anthropic发布了Claude 3 AI模型，特别强调AI安全性和对齐性，在安全评估中表现优异。该模型在减少有害输出和提高有用性方面取得了显著进展。",
            "source": "AI前线",
            "url": "https://example.com/4",
            "publish_time": "2024-01-15T13:00:00Z"
        },
        {
            "title": "微软Copilot全面升级，AI助手进入新时代",
            "summary": "微软宣布Copilot AI助手全面升级，集成到更多产品中，提供更智能的办公体验。新版本在文档处理、数据分析和工作流程优化方面有了显著改进。",
            "source": "虎嗅网",
            "url": "https://example.com/5",
            "publish_time": "2024-01-15T14:00:00Z"
        }
    ]
    
    print(f"📰 输入文章数量: {len(articles)}")
    print("\n📋 原始文章列表:")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   来源: {article['source']} | 时间: {article['publish_time']}")
        print(f"   摘要: {article['summary'][:80]}...")
        print()
    
    print("🔄 正在使用火山方舟DeepSeek处理内容...")
    print("-" * 60)
    
    # 创建内容处理器
    processor = ContentProcessor()
    
    # 处理文章
    result = await processor.process_articles(articles)
    
    print("✅ 内容处理完成！")
    print("\n📋 早报摘要:")
    print("=" * 60)
    print(result['summary'])
    
    print("\n📈 发展趋势分析:")
    print("=" * 60)
    for i, trend in enumerate(result['trends'], 1):
        print(f"{i}. {trend}")
    
    print("\n🎨 图片提示词:")
    print("=" * 60)
    for i, prompt in enumerate(result['image_prompts'], 1):
        print(f"{i}. {prompt}")
    
    print("\n📊 处理统计:")
    print("=" * 60)
    print(f"处理时间: {result['processed_at']}")
    print(f"文章总数: {result['total_articles']}")
    print(f"保留文章: {len(result['articles'])}")
    
    print("\n🎉 演示完成！")
    print("=" * 60)
    print("💡 系统特点:")
    print("✅ 使用火山方舟DeepSeek API")
    print("✅ 智能内容摘要生成")
    print("✅ 趋势分析")
    print("✅ 图片提示词生成")
    print("✅ 支持中文内容处理")

if __name__ == "__main__":
    asyncio.run(demo_ai_processing())

