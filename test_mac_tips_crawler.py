#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mac技巧爬虫测试脚本
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

async def test_mac_tips_sources():
    """测试Mac技巧源配置"""
    print("🔍 测试Mac技巧源配置...")
    
    sources_manager = MacTipsSources()
    
    # 测试获取源
    sources = sources_manager.get_sources()
    print(f"✅ 找到 {len(sources)} 个Mac技巧源")
    
    # 显示源信息
    for source in sources:
        print(f"  📡 {source['name']} - {source['description']} (权重: {source['weight']})")
    
    # 测试分类
    categories = sources_manager.get_categories()
    print(f"\n✅ 找到 {len(categories)} 个Mac技巧分类")
    
    for category, info in categories.items():
        print(f"  📂 {category}: {info['description']}")
    
    return True

async def test_mac_tips_processor():
    """测试Mac技巧处理器"""
    print("\n🔧 测试Mac技巧处理器...")
    
    processor = MacTipsProcessor()
    
    # 模拟Mac技巧数据
    mock_articles = [
        {
            "title": "Mac快捷键大全",
            "content": "Mac系统中有很多实用的快捷键，比如Command+C复制，Command+V粘贴等。掌握这些快捷键可以大大提高工作效率。",
            "url": "https://example.com/mac-shortcuts",
            "summary": "Mac快捷键使用技巧",
            "source": "测试源"
        },
        {
            "title": "Mac文件管理技巧",
            "content": "在Mac上管理文件有很多技巧，比如使用标签分类、快速预览文件内容等。这些技巧让文件管理更加高效。",
            "url": "https://example.com/mac-file-management",
            "summary": "Mac文件管理实用技巧",
            "source": "测试源"
        },
        {
            "title": "Mac软件推荐",
            "content": "Mac平台有很多优秀的软件，比如Alfred、CleanMyMac、Parallels等。这些软件可以大大提升Mac的使用体验。",
            "url": "https://example.com/mac-software",
            "summary": "Mac必装软件推荐",
            "source": "测试源"
        }
    ]
    
    try:
        # 处理内容
        result = await processor.process_mac_tips(mock_articles)
        
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
            print(f"  标签: {', '.join(sample['tags'][:3])}...")
            print(f"  引流: {sample['cta']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理器测试失败: {e}")
        return False

async def test_mac_tips_crawler():
    """测试Mac技巧爬虫（模拟模式）"""
    print("\n🕷️ 测试Mac技巧爬虫...")
    
    try:
        crawler = MacTipsCrawler()
        
        # 测试初始化
        print("  🔧 初始化爬虫...")
        # 注意：这里不实际初始化爬虫，避免网络请求
        
        # 测试内容处理
        print("  🔧 测试内容处理...")
        mock_articles = [
            {
                "title": "Mac隐藏技巧",
                "content": "Mac系统有很多隐藏的功能，比如三指拖拽、空格键预览等。",
                "url": "https://example.com/hidden-tips",
                "summary": "Mac隐藏功能技巧",
                "source": "测试源"
            }
        ]
        
        result = await crawler.processor.process_mac_tips(mock_articles)
        print(f"  ✅ 内容处理成功，生成 {len(result['xiaohongshu_content'])} 篇内容")
        
        return True
        
    except Exception as e:
        print(f"❌ 爬虫测试失败: {e}")
        return False

async def test_xiaohongshu_content_generation():
    """测试小红书内容生成"""
    print("\n📱 测试小红书内容生成...")
    
    sources_manager = MacTipsSources()
    
    # 测试标题生成
    test_content = "Mac快捷键使用技巧，提高工作效率"
    title = sources_manager.generate_xiaohongshu_title(test_content, "效率提升")
    print(f"✅ 生成标题: {title}")
    
    # 测试技巧卡片生成
    tip_data = {
        "title": "Command+Space快速搜索",
        "scenario": "快速启动应用",
        "steps": "按下Command+Space，输入应用名称，按回车启动",
        "notes": "确保Spotlight搜索已启用",
        "image_suggestion": "键盘快捷键示意图"
    }
    
    card = sources_manager.generate_tip_card(tip_data)
    print(f"✅ 生成技巧卡片:")
    for key, value in card.items():
        print(f"  {key}: {value}")
    
    return True

async def main():
    """主测试函数"""
    print("🚀 开始Mac技巧爬虫系统测试")
    print("=" * 50)
    
    tests = [
        ("Mac技巧源配置", test_mac_tips_sources),
        ("Mac技巧处理器", test_mac_tips_processor),
        ("Mac技巧爬虫", test_mac_tips_crawler),
        ("小红书内容生成", test_xiaohongshu_content_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 测试完成: {passed}/{len(results)} 项通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！Mac技巧爬虫系统准备就绪")
    else:
        print("⚠️ 部分测试失败，请检查配置")

if __name__ == "__main__":
    asyncio.run(main())
