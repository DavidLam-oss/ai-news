#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流程演示 - 爬虫 + AI处理 + 飞书写入模拟
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
from crawler.content_processor import ContentProcessor

async def demo_full_workflow():
    """演示完整工作流程"""
    print("🚀 AI早报系统完整工作流程演示")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 第一步：初始化爬虫
        print("\n📡 第一步：初始化爬虫引擎...")
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 第二步：爬取新闻
        print("\n🕷️ 第二步：爬取AI科技新闻...")
        articles = await crawler.crawl_news_sources()
        
        if articles:
            print(f"✅ 成功爬取到 {len(articles)} 篇文章")
            
            # 显示前3篇文章
            print("\n📰 爬取到的文章预览：")
            for i, article in enumerate(articles[:3], 1):
                print(f"  {i}. {article['title'][:60]}...")
                print(f"     来源: {article['source']}")
                print(f"     摘要: {article['summary'][:80]}...")
                print()
        else:
            print("❌ 未获取到任何文章")
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
        for i, trend in enumerate(report['trends'][:5], 1):
            print(f"{i}. {trend}")
        
        print("\n🎨 图片提示词:")
        print("-" * 50)
        for i, prompt in enumerate(report['image_prompts'], 1):
            print(f"{i}. {prompt}")
        
        # 第四步：模拟飞书写入
        print("\n💾 第四步：准备写入飞书多维表格...")
        
        # 准备飞书数据格式
        feishu_data = {
            '日期': report['date'],
            '早报原始内容': json.dumps(report, ensure_ascii=False, indent=2),
            'AI处理后内容': report['summary'],
            '图片提示词1': report['image_prompts'][0] if len(report['image_prompts']) > 0 else '',
            '图片提示词2': report['image_prompts'][1] if len(report['image_prompts']) > 1 else '',
            '图片提示词3': report['image_prompts'][2] if len(report['image_prompts']) > 2 else ''
        }
        
        print("✅ 数据格式准备完成")
        print(f"📊 数据字段数量: {len(feishu_data)}")
        
        # 尝试写入飞书（可能会失败，但展示流程）
        print("\n🔗 第五步：尝试写入飞书多维表格...")
        try:
            success = await crawler.save_to_feishu(report)
            if success:
                print("✅ 数据成功写入飞书多维表格！")
            else:
                print("⚠️ 飞书写入失败（可能是配置问题）")
                print("💡 这是正常的，因为需要正确的表格token和权限")
        except Exception as e:
            print(f"⚠️ 飞书写入过程中出现错误: {e}")
            print("💡 这是正常的，因为需要正确的表格token和权限")
        
        # 显示完整的数据结构
        print("\n📋 完整的数据结构预览：")
        print("-" * 50)
        print(json.dumps(feishu_data, ensure_ascii=False, indent=2)[:500] + "...")
        
        print("\n🎉 工作流程演示完成！")
        print("\n📝 总结：")
        print("✅ 爬虫引擎正常工作")
        print("✅ 新闻抓取功能正常")
        print("✅ AI内容处理功能正常")
        print("✅ 数据格式转换正常")
        print("⚠️ 飞书写入需要正确的配置")
        
        print("\n🔧 下一步需要做的：")
        print("1. 获取正确的飞书多维表格token")
        print("2. 配置应用权限")
        print("3. 确保表格字段名称匹配")
        print("4. 测试完整的写入功能")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

if __name__ == "__main__":
    asyncio.run(demo_full_workflow())
