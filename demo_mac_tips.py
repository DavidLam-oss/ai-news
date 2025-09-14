#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac技巧系统演示脚本
"""

import asyncio
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from crawler.mac_tips_crawler import MacTipsCrawler
from crawler.mac_tips_sources import MacTipsSources
from crawler.mac_tips_processor import MacTipsProcessor

async def demo_mac_tips_system():
    """演示Mac技巧系统"""
    print("🚀 Mac技巧系统演示")
    print("=" * 50)
    
    # 1. 演示Mac技巧源配置
    print("\n📡 1. Mac技巧源配置")
    sources_manager = MacTipsSources()
    sources = sources_manager.get_sources()
    
    print(f"✅ 配置了 {len(sources)} 个Mac技巧源:")
    for source in sources:
        print(f"  📡 {source['name']} - {source['description']} (权重: {source['weight']})")
    
    # 2. 演示分类系统
    print("\n📂 2. Mac技巧分类系统")
    categories = sources_manager.get_categories()
    
    print(f"✅ 定义了 {len(categories)} 个分类:")
    for category, info in categories.items():
        print(f"  📂 {category}: {info['description']}")
        print(f"     关键词: {', '.join(info['keywords'][:3])}...")
    
    # 3. 演示内容模板
    print("\n📝 3. 内容模板系统")
    templates = sources_manager.get_templates()
    
    print("✅ 小红书笔记模板:")
    xiaohongshu_templates = templates["小红书笔记"]["标题模板"]
    for i, template in enumerate(xiaohongshu_templates[:3], 1):
        print(f"  {i}. {template}")
    
    # 4. 演示内容处理
    print("\n🔧 4. 内容处理演示")
    processor = MacTipsProcessor()
    
    # 模拟Mac技巧数据
    mock_tips = [
        {
            "title": "Mac快捷键大全",
            "content": "Mac系统中有很多实用的快捷键，比如Command+C复制，Command+V粘贴，Command+Space快速搜索等。掌握这些快捷键可以大大提高工作效率。",
            "url": "https://example.com/mac-shortcuts",
            "summary": "Mac快捷键使用技巧",
            "source": "MacRumors"
        },
        {
            "title": "Mac文件管理技巧",
            "content": "在Mac上管理文件有很多技巧，比如使用标签分类、快速预览文件内容、使用Spotlight搜索等。这些技巧让文件管理更加高效。",
            "url": "https://example.com/mac-file-management",
            "summary": "Mac文件管理实用技巧",
            "source": "少数派"
        },
        {
            "title": "Mac必装软件推荐",
            "content": "Mac平台有很多优秀的软件，比如Alfred、CleanMyMac、Parallels、Sketch等。这些软件可以大大提升Mac的使用体验和工作效率。",
            "url": "https://example.com/mac-software",
            "summary": "Mac必装软件推荐",
            "source": "Mac毒"
        }
    ]
    
    try:
        # 处理内容
        result = await processor.process_mac_tips(mock_tips)
        
        print(f"✅ 处理完成，共 {result['total_tips']} 条技巧")
        print(f"✅ 生成 {len(result['xiaohongshu_content'])} 篇小红书内容")
        print(f"✅ 生成 {len(result['tip_cards'])} 张技巧卡片")
        print(f"✅ 生成 {len(result['content_calendar'])} 个内容日历项")
        
        # 显示分类结果
        print("\n📊 分类统计:")
        for category, tips in result['categorized_tips'].items():
            print(f"  📂 {category}: {len(tips)} 条")
        
        # 显示小红书内容示例
        if result['xiaohongshu_content']:
            print("\n📱 小红书内容示例:")
            sample = result['xiaohongshu_content'][0]
            print(f"  标题: {sample['title']}")
            print(f"  分类: {sample['category']}")
            print(f"  标签: {', '.join(sample['tags'][:5])}")
            print(f"  引流: {sample['cta']}")
            print(f"  配图建议: {', '.join(sample['image_suggestions'][:2])}")
        
        # 显示技巧卡片示例
        if result['tip_cards']:
            print("\n🎴 技巧卡片示例:")
            sample_card = result['tip_cards'][0]
            print(f"  标题: {sample_card['标题']}")
            print(f"  适用场景: {sample_card['适用场景']}")
            print(f"  操作步骤: {sample_card['操作步骤'][:100]}...")
            print(f"  配图建议: {sample_card['配图建议']}")
        
        # 显示内容日历示例
        if result['content_calendar']:
            print("\n📅 内容日历示例:")
            sample_calendar = result['content_calendar'][0]
            print(f"  发布日期: {sample_calendar['date']}")
            print(f"  标题: {sample_calendar['title']}")
            print(f"  分类: {sample_calendar['category']}")
            print(f"  状态: {sample_calendar['status']}")
        
    except Exception as e:
        print(f"❌ 内容处理失败: {e}")
    
    # 5. 演示标题生成
    print("\n🎯 5. 标题生成演示")
    test_content = "Mac快捷键使用技巧，提高工作效率"
    generated_title = sources_manager.generate_xiaohongshu_title(test_content, "效率提升")
    print(f"✅ 生成标题: {generated_title}")
    
    # 6. 演示技巧卡片生成
    print("\n🎴 6. 技巧卡片生成演示")
    tip_data = {
        "title": "Command+Space快速搜索",
        "scenario": "快速启动应用",
        "steps": "按下Command+Space，输入应用名称，按回车启动",
        "notes": "确保Spotlight搜索已启用",
        "image_suggestion": "键盘快捷键示意图"
    }
    
    card = sources_manager.generate_tip_card(tip_data)
    print("✅ 生成技巧卡片:")
    for key, value in card.items():
        print(f"  {key}: {value}")
    
    # 7. 演示API接口
    print("\n🌐 7. API接口演示")
    print("✅ 可用的Mac技巧API接口:")
    api_endpoints = [
        ("GET", "/api/mac-tips/sources", "获取Mac技巧源列表"),
        ("GET", "/api/mac-tips/categories", "获取Mac技巧分类"),
        ("POST", "/api/mac-tips/crawl", "爬取Mac技巧内容"),
        ("POST", "/api/mac-tips/process", "处理Mac技巧内容"),
        ("GET", "/api/mac-tips/templates", "获取Mac技巧内容模板"),
        ("GET", "/api/stats", "获取系统统计信息（包含Mac技巧统计）")
    ]
    
    for method, endpoint, description in api_endpoints:
        print(f"  {method} {endpoint} - {description}")
    
    print("\n" + "=" * 50)
    print("🎉 Mac技巧系统演示完成！")
    print("\n💡 使用建议:")
    print("1. 配置飞书多维表格来存储Mac技巧内容")
    print("2. 设置定时任务自动爬取Mac技巧")
    print("3. 使用生成的内容在小红书发布笔记")
    print("4. 根据数据反馈优化内容策略")
    
    print("\n🚀 下一步:")
    print("1. 运行 'python3 test_mac_tips_crawler.py' 进行完整测试")
    print("2. 启动API服务: 'python3 api/server.py'")
    print("3. 访问 http://localhost:8000/docs 查看API文档")

async def demo_xiaohongshu_content_generation():
    """演示小红书内容生成"""
    print("\n📱 小红书内容生成演示")
    print("-" * 30)
    
    sources_manager = MacTipsSources()
    
    # 演示不同分类的标题生成
    categories = ["基础操作", "效率提升", "软件推荐", "系统优化"]
    
    for category in categories:
        test_content = f"Mac{category}相关技巧"
        title = sources_manager.generate_xiaohongshu_title(test_content, category)
        print(f"📂 {category}: {title}")
    
    # 演示引流话术生成
    print("\n💬 引流话术示例:")
    processor = MacTipsProcessor()
    for category in categories:
        cta = processor._generate_cta(category)
        print(f"  {category}: {cta}")

if __name__ == "__main__":
    asyncio.run(demo_mac_tips_system())
    asyncio.run(demo_xiaohongshu_content_generation())
