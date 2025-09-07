#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流程测试 - 爬虫 + AI处理 + 飞书写入
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from crawler.main import AINewsCrawler
from improved_crawler_test import extract_articles_improved

async def test_complete_workflow():
    """测试完整工作流程"""
    print("🚀 完整工作流程测试 - 爬虫 + AI处理 + 飞书写入")
    print("=" * 70)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 第一步：初始化爬虫
        print("\n📡 第一步：初始化爬虫引擎...")
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 第二步：爬取新闻（使用简化的方法）
        print("\n🕷️ 第二步：爬取AI科技新闻...")
        
        # 使用已知有效的网站进行测试
        test_url = "https://36kr.com"
        print(f"   正在爬取: {test_url}")
        
        result = await crawler.crawler.arun(
            url=test_url,
            wait_for="networkidle",
            delay_before_return_html=2
        )
        
        if result.success:
            print("✅ 爬取成功")
            print(f"📄 页面标题: {result.metadata.get('title', 'N/A')}")
            print(f"📊 内容长度: {len(result.html)} 字符")
            
            # 提取文章
            articles = extract_articles_improved(result.html, "36氪", test_url)
            print(f"📰 提取到 {len(articles)} 篇文章")
            
            if articles:
                # 显示前3篇文章
                for i, article in enumerate(articles[:3], 1):
                    print(f"  {i}. {article['title'][:60]}...")
                    print(f"     来源: {article['source']}")
                    print(f"     摘要: {article['summary'][:80]}...")
                    print()
            else:
                print("❌ 未提取到文章")
                return
        else:
            print("❌ 爬取失败")
            return
        
        # 第三步：AI处理内容
        print("\n🤖 第三步：AI处理内容...")
        report = await crawler.generate_daily_report(articles)
        
        print("✅ AI内容处理完成")
        print(f"📅 早报日期: {report['date']}")
        print(f"📝 早报标题: {report['title']}")
        
        # 显示处理结果
        print("\n📋 早报摘要:")
        print("-" * 50)
        print(report['summary'])
        
        print("\n📈 发展趋势:")
        print("-" * 50)
        for i, trend in enumerate(report['trends'][:3], 1):
            print(f"{i}. {trend}")
        
        print("\n🎨 图片提示词:")
        print("-" * 50)
        for i, prompt in enumerate(report['image_prompts'], 1):
            print(f"{i}. {prompt}")
        
        # 第四步：写入飞书
        print("\n💾 第四步：写入飞书多维表格...")
        
        try:
            success = await crawler.save_to_feishu(report)
            
            if success:
                print("✅ 数据成功写入飞书多维表格！")
                print("🎉 完整工作流程测试成功！")
                
                print("\n📊 测试结果总结:")
                print("✅ 爬虫引擎正常工作")
                print("✅ 新闻抓取功能正常")
                print("✅ AI内容处理功能正常")
                print("✅ 飞书API连接正常")
                print("✅ 数据写入功能正常")
                print("✅ 完整工作流程正常")
                
            else:
                print("❌ 飞书写入失败")
                print("💡 请检查应用权限配置")
                
        except Exception as e:
            print(f"❌ 飞书写入过程中出现错误: {e}")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())
