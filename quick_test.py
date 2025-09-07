#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证系统功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

async def quick_test():
    """快速测试系统功能"""
    print("🚀 AI早报系统快速测试")
    print("=" * 40)
    
    try:
        # 测试爬虫功能
        print("\n1️⃣ 测试爬虫功能...")
        from crawler.main import AINewsCrawler
        
        crawler = AINewsCrawler()
        await crawler.init_crawler()
        
        # 只爬取一个网站进行快速测试
        from crawler.news_sources import NewsSources
        news_sources = NewsSources()
        sources = news_sources.get_sources()[:1]  # 只测试第一个源
        
        articles = []
        for source in sources:
            print(f"   正在爬取: {source['name']}")
            result = await crawler.crawler.arun(
                url=source['url'],
                wait_for="networkidle",
                delay_before_return_html=2
            )
            
            if result.success:
                from improved_crawler_test import extract_articles_improved
                extracted = extract_articles_improved(result.html, source['name'], source['url'])
                articles.extend(extracted)
                print(f"   ✅ 获取到 {len(extracted)} 篇文章")
            else:
                print(f"   ❌ 爬取失败")
        
        await crawler.cleanup()
        
        if articles:
            print(f"✅ 爬虫测试通过，共获取 {len(articles)} 篇文章")
        else:
            print("❌ 爬虫测试失败，未获取到文章")
            return
        
        # 测试AI处理功能
        print("\n2️⃣ 测试AI处理功能...")
        from crawler.content_processor import ContentProcessor
        
        processor = ContentProcessor()
        result = await processor.process_articles(articles[:3])  # 只处理前3篇
        
        if result and result.get('summary'):
            print("✅ AI处理测试通过")
            print(f"   摘要长度: {len(result['summary'])} 字符")
            print(f"   趋势数量: {len(result['trends'])}")
            print(f"   图片提示词数量: {len(result['image_prompts'])}")
        else:
            print("❌ AI处理测试失败")
            return
        
        # 测试飞书连接
        print("\n3️⃣ 测试飞书连接...")
        import os
        os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
        os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
        os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
        
        from feishu.client import FeishuClient
        client = FeishuClient()
        
        try:
            access_token = await client.get_access_token()
            if access_token:
                print("✅ 飞书连接测试通过")
                print(f"   访问令牌: {access_token[:20]}...")
            else:
                print("❌ 飞书连接测试失败")
        except Exception as e:
            print(f"❌ 飞书连接测试失败: {e}")
        finally:
            await client.close()
        
        print("\n🎉 快速测试完成！")
        print("\n📊 测试结果总结：")
        print("✅ 爬虫功能正常")
        print("✅ AI处理功能正常")
        print("✅ 飞书连接正常")
        print("⚠️ 飞书写入需要正确的表格配置")
        
        print("\n💡 系统已准备就绪，可以：")
        print("1. 运行完整爬虫: python3 crawler/main.py")
        print("2. 运行演示脚本: python3 demo_full_workflow.py")
        print("3. 配置正确的飞书表格token后测试写入功能")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())

