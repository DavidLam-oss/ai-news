#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的爬虫测试 - 直接使用我们之前成功的逻辑
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor

async def simple_crawler_test():
    """简化的爬虫测试"""
    
    print("🕷️ 简化爬虫测试 - 使用成功的逻辑")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 初始化爬虫
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 测试单个网站
        test_url = "https://36kr.com"
        print(f"\n📰 正在爬取: {test_url}")
        
        # 直接使用crawler.arun方法
        result = await crawler.crawler.arun(
            url=test_url,
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
            print(f"✅ 爬取成功")
            print(f"📄 页面标题: {result.metadata.get('title', 'N/A')}")
            print(f"📊 内容长度: {len(result.html)} 字符")
            
            # 使用我们之前成功的文章提取逻辑
            from improved_crawler_test import extract_articles_improved
            articles = extract_articles_improved(result.html, "36氪", test_url)
            
            print(f"📰 提取到 {len(articles)} 篇文章")
            
            # 显示文章
            for i, article in enumerate(articles[:3], 1):
                print(f"  {i}. {article['title'][:60]}...")
                print(f"     来源: {article['source']}")
                print(f"     摘要: {article['summary'][:100]}...")
                print()
            
            if articles:
                print(f"\n🤖 使用DeepSeek处理 {len(articles)} 篇文章...")
                
                # 使用内容处理器处理文章
                processor = ContentProcessor()
                result = await processor.process_articles(articles[:5])  # 处理前5篇
                
                print("✅ 内容处理完成！")
                print("\n📋 早报摘要:")
                print("-" * 50)
                print(result['summary'])
                
                print("\n📈 发展趋势:")
                print("-" * 50)
                for i, trend in enumerate(result['trends'][:3], 1):
                    print(f"{i}. {trend}")
                
                print("\n🎨 图片提示词:")
                print("-" * 50)
                for i, prompt in enumerate(result['image_prompts'], 1):
                    print(f"{i}. {prompt}")
        
        else:
            print(f"❌ 爬取失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

if __name__ == "__main__":
    asyncio.run(simple_crawler_test())
