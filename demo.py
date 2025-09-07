#!/usr/bin/env pytho# -*- coding: utf-8 -*-
"""
AI早报系统演示脚本
展示系统的主要功能
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from crawler.news_sources import NewsSources
from crawler.content_processor import ContentProcessor

async def demo_news_sources():
    """演示新闻源功能"""
    print("📰 新闻源演示")
    print("=" * 50)
    
    news_sources = NewsSources()
    
    # 显示所有新闻源
    sources = news_sources.get_sources()
    print(f"配置了 {len(sources)} 个新闻源：")
    
    for i, source in enumerate(sources, 1):
        print(f"{i:2d}. {source['name']:<15} ({source['category']:<3}) - {source['url']}")
    
    # 按分类显示
    print(f"\n📊 按分类统计：")
    ai_sources = news_sources.get_ai_sources()
    tech_sources = news_sources.get_tech_sources()
    
    print(f"   AI相关: {len(ai_sources)} 个")
    print(f"   科技相关: {len(tech_sources)} 个")
    
    print()

async def demo_content_processing():
    """演示内容处理功能"""
    print("🤖 AI内容处理演示")
    print("=" * 50)
    
    # 模拟文章数据
    sample_articles = [
        {
            "title": "OpenAI发布GPT-4 Turbo模型，性能大幅提升",
            "summary": "OpenAI发布了新的GPT-4 Turbo模型，在保持高质量输出的同时，处理速度提升了3倍，成本降低了50%。",
            "source": "36氪",
            "url": "https://example.com/1",
            "publish_time": "2024-01-15T10:00:00Z",
            "content": "OpenAI今日发布了GPT-4 Turbo模型，这是该公司最新的语言模型..."
        },
        {
            "title": "Google推出Gemini AI模型，多模态能力突出",
            "summary": "Google发布了新的Gemini AI模型，在图像、文本、音频等多模态任务上表现优异，超越了GPT-4。",
            "source": "机器之心",
            "url": "https://example.com/2",
            "publish_time": "2024-01-15T11:00:00Z",
            "content": "Google今日发布了Gemini AI模型，这是该公司最先进的多模态AI系统..."
        },
        {
            "title": "Meta发布Llama 3模型，开源AI竞争加剧",
            "summary": "Meta发布了Llama 3开源大语言模型，在多个基准测试中表现优异，进一步推动了开源AI的发展。",
            "source": "量子位",
            "url": "https://example.com/3",
            "publish_time": "2024-01-15T12:00:00Z",
            "content": "Meta今日发布了Llama 3开源大语言模型，这是该公司最新的开源AI模型..."
        },
        {
            "title": "Anthropic发布Claude 3，AI安全成为焦点",
            "summary": "Anthropic发布了Claude 3 AI模型，特别强调AI安全性和对齐性，在安全评估中表现优异。",
            "source": "AI前线",
            "url": "https://example.com/4",
            "publish_time": "2024-01-15T13:00:00Z",
            "content": "Anthropic今日发布了Claude 3 AI模型，该公司特别注重AI的安全性和对齐性..."
        },
        {
            "title": "微软Copilot全面升级，AI助手进入新时代",
            "summary": "微软宣布Copilot AI助手全面升级，集成到更多产品中，提供更智能的办公体验。",
            "source": "虎嗅网",
            "url": "https://example.com/5",
            "publish_time": "2024-01-15T14:00:00Z",
            "content": "微软今日宣布Copilot AI助手全面升级，将AI能力集成到更多产品中..."
        }
    ]
    
    print(f"📝 模拟文章数据 ({len(sample_articles)} 篇)：")
    for i, article in enumerate(sample_articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   来源: {article['source']} | 时间: {article['publish_time']}")
        print(f"   摘要: {article['summary'][:80]}...")
        print()
    
    # 检查是否有API密钥
    if not settings.OPENAI_API_KEY:
        print("⚠️  未配置OpenAI API密钥，跳过AI处理演示")
        print("   请设置 OPENAI_API_KEY 环境变量来体验AI处理功能")
        return
    
    try:
        processor = ContentProcessor()
        
        print("🔄 正在使用AI处理文章内容...")
        result = await processor.process_articles(sample_articles)
        
        print("✅ AI处理完成！")
        print()
        
        # 显示处理结果
        print("📋 早报摘要：")
        print("-" * 30)
        print(result['summary'])
        print()
        
        print("📈 发展趋势：")
        print("-" * 30)
        for i, trend in enumerate(result['trends'], 1):
            print(f"{i}. {trend}")
        print()
        
        print("🎨 图片提示词：")
        print("-" * 30)
        for i, prompt in enumerate(result['image_prompts'], 1):
            print(f"{i}. {prompt}")
        print()
        
    except Exception as e:
        print(f"❌ AI处理失败: {e}")
        print("   请检查API密钥配置和网络连接")

async def demo_system_architecture():
    """演示系统架构"""
    print("🏗️  系统架构演示")
    print("=" * 50)
    
    architecture = """
    ┌─────────────────┐    ┌─────────────────┐
    │   AI爬虫服务     │───▶│  飞书多维表格    │
    │  (crawl4ai)     │    │   (数据存储)     │
    └─────────────────┘    └─────────────────┘
           │                        │
           ▼                        ▼
    ┌─────────────────┐    ┌─────────────────┐
    │   新闻源管理     │    │   AI内容处理     │
    │  (多源抓取)     │    │  (DeepSeek)     │
    └─────────────────┘    └─────────────────┘
    """
    
    print(architecture)
    
    print("🔄 数据流程：")
    print("1. 爬虫服务定时抓取AI科技新闻")
    print("2. AI处理服务优化和整理内容")
    print("3. 飞书多维表格存储和管理数据")
    print("4. 自动化工作流触发处理流程")
    
    print()

async def demo_api_endpoints():
    """演示API接口"""
    print("🌐 API接口演示")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/", "系统首页"),
        ("GET", "/health", "健康检查"),
        ("GET", "/api/news", "获取最新新闻"),
        ("POST", "/api/process", "处理早报内容"),
        ("POST", "/api/feishu/record", "创建飞书记录"),
        
        ("GET", "/api/sources", "获取新闻源列表"),
        ("POST", "/api/crawl/run", "手动执行爬取"),
        ("GET", "/api/stats", "获取系统统计")
    ]
    
    print("📡 可用的API接口：")
    for method, endpoint, description in endpoints:
        print(f"   {method:<6} {endpoint:<25} - {description}")
    
    print()
    print("🔗 API文档地址：http://localhost:8000/docs")
    print("💡 使用curl测试API：")
    print("   curl http://localhost:8000/health")
    print("   curl http://localhost:8000/api/news")
    print()

async def demo_deployment_options():
    """演示部署选项"""
    print("🚀 部署选项演示")
    print("=" * 50)
    
    print("📦 部署方式：")
    print("1. 本地部署")
    print("   ./start.sh")
    print()
    print("2. Docker部署")
    print("   docker-compose up -d")
    print()
    print("3. PM2部署")
    print("   pm2 start ecosystem.config.js")
    print()
    
    print("⚙️  配置要求：")
    print("   - Python 3.8+")
    print("   - Redis服务")
    print("   - OpenAI API密钥")
    print("   - 飞书应用凭证")
    
    print()
    
    print("🔧 管理命令：")
    print("   - 测试系统: python test_system.py")
    print("   - 部署系统: ./deploy.sh")
    print("   - 查看日志: tail -f logs/*.log")
    print()

async def main():
    """主演示函数"""
    print("🎬 AI早报系统功能演示")
    print("=" * 60)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 运行各个演示
    await demo_news_sources()
    await demo_content_processing()
    await demo_system_architecture()
    await demo_api_endpoints()
    await demo_deployment_options()
    
    print("🎉 演示完成！")
    print("=" * 60)
    print("📚 更多信息请查看：")
    print("   - README.md - 项目说明")
    print("   - docs/usage.md - 使用指南")
    print("   - feishu/table_config.md - 飞书配置")
    print()
    print("🚀 快速开始：")
    print("   1. 配置环境变量 (.env)")
    print("   2. 运行部署脚本 (./deploy.sh)")
    print("   3. 启动服务 (./start.sh)")
    print("   4. 访问API文档 (http://localhost:8000/docs)")

if __name__ == "__main__":
    asyncio.run(main())
