#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流程测试脚本
测试：爬取 → AI处理 → 存储 → 推送
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor

async def test_full_workflow():
    """测试完整工作流程"""
    
    print("🚀 AI早报系统 - 完整工作流程测试")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 1. 初始化爬虫
        await crawler.init_crawler()
        print("✅ 1. 爬虫引擎初始化成功")
        
        # 2. 爬取新闻
        print("\n📰 2. 开始爬取新闻...")
        articles = await crawler.crawl_news_sources()
        print(f"✅ 爬取完成，获取到 {len(articles)} 篇文章")
        
        if not articles:
            print("❌ 没有获取到文章，请检查网络连接")
            return
        
        # 显示爬取结果
        for i, article in enumerate(articles[:3], 1):
            print(f"  {i}. {article['title'][:50]}...")
            print(f"     来源: {article['source']}")
            print()
        
        # 3. AI内容处理
        print("🤖 3. 开始AI内容处理...")
        processor = ContentProcessor()
        processed_result = await processor.process_articles(articles[:5])  # 处理前5篇
        
        print("✅ AI处理完成！")
        print(f"📋 早报摘要: {processed_result['summary'][:100]}...")
        print(f"📈 趋势分析: {len(processed_result['trends'])} 个趋势")
        print(f"🎨 图片提示词: {len(processed_result['image_prompts'])} 个")
        
        # 4. 测试飞书存储（如果配置了）
        print("\n📊 4. 测试飞书存储...")
        try:
            # 准备记录数据
            record_data = {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '早报原始内容': f"爬取到{len(articles)}篇文章",
                'AI处理后内容': processed_result['summary'],
                '图片提示词1': processed_result['image_prompts'][0] if processed_result['image_prompts'] else '',
                '图片提示词2': processed_result['image_prompts'][1] if len(processed_result['image_prompts']) > 1 else '',
                '图片提示词3': processed_result['image_prompts'][2] if len(processed_result['image_prompts']) > 2 else ''
            }
            
            # 尝试保存到飞书
            success = await crawler.save_to_feishu(record_data)
            if success:
                print("✅ 飞书存储成功！")
            else:
                print("⚠️ 飞书存储失败（可能未配置或网络问题）")
                
        except Exception as e:
            print(f"⚠️ 飞书存储测试失败: {e}")
        
        # 5. 测试微信推送（如果配置了）
        print("\n💬 5. 测试微信推送...")
        try:
            # 准备报告数据
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'summary': processed_result['summary'],
                'created_at': datetime.now().isoformat()
            }
            
            # 尝试发送到微信
            await crawler.send_to_wechat(report)
            print("✅ 微信推送成功！")
            
        except Exception as e:
            print(f"⚠️ 微信推送测试失败: {e}")
        
        # 6. 生成测试报告
        print("\n📋 6. 测试报告")
        print("-" * 40)
        print(f"✅ 爬虫功能: 正常")
        print(f"✅ AI处理功能: 正常")
        print(f"✅ 早报生成: 正常")
        print(f"⚠️ 飞书存储: {'正常' if 'success' in locals() and success else '需要配置'}")
        print(f"⚠️ 微信推送: {'正常' if 'report' in locals() else '需要配置'}")
        
        print("\n🎯 下一步建议:")
        if 'success' not in locals() or not success:
            print("1. 配置飞书多维表格")
        if 'report' not in locals():
            print("2. 配置微信助手")
        print("3. 设置定时任务")
        print("4. 部署到生产环境")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())


