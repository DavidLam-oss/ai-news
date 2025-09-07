#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日自动爬虫脚本
每天定时执行，生成AI早报
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import schedule
import time

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor

async def daily_crawl_task():
    """每日爬虫任务"""
    
    print(f"🕷️ 开始执行每日爬虫任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 1. 初始化爬虫
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 2. 爬取新闻
        print("\n📰 开始爬取新闻...")
        articles = await crawler.crawl_news_sources()
        print(f"✅ 爬取完成，获取到 {len(articles)} 篇文章")
        
        if not articles:
            print("❌ 没有获取到文章，任务结束")
            return
        
        # 3. AI内容处理
        print("\n🤖 开始AI内容处理...")
        processor = ContentProcessor()
        processed_result = await processor.process_articles(articles[:10])  # 处理前10篇
        
        print("✅ AI处理完成！")
        print(f"📋 早报摘要: {processed_result['summary'][:100]}...")
        
        # 4. 保存到飞书（如果配置了）
        print("\n📊 保存到飞书多维表格...")
        try:
            record_data = {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '早报原始内容': f"爬取到{len(articles)}篇文章",
                'AI处理后内容': processed_result['summary'],
                '图片提示词1': processed_result['image_prompts'][0] if processed_result['image_prompts'] else '',
                '图片提示词2': processed_result['image_prompts'][1] if len(processed_result['image_prompts']) > 1 else '',
                '图片提示词3': processed_result['image_prompts'][2] if len(processed_result['image_prompts']) > 2 else ''
            }
            
            success = await crawler.save_to_feishu(record_data)
            if success:
                print("✅ 飞书存储成功！")
            else:
                print("⚠️ 飞书存储失败（可能未配置）")
                
        except Exception as e:
            print(f"⚠️ 飞书存储失败: {e}")
        
        # 5. 微信发送功能已下线（风险规避）
        
        print(f"\n🎉 每日爬虫任务完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ 任务执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("🧹 资源清理完成")

def run_daily_crawl():
    """运行每日爬虫任务"""
    asyncio.run(daily_crawl_task())

def setup_schedule():
    """设置定时任务"""
    print("⏰ 设置定时任务...")
    
    # 每天上午8点执行
    schedule.every().day.at("08:00").do(run_daily_crawl)
    
    # 每天下午6点执行（可选）
    # schedule.every().day.at("18:00").do(run_daily_crawl)
    
    print("✅ 定时任务设置完成")
    print("📅 执行时间: 每天上午8:00")
    print("🔄 开始监控定时任务...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI早报系统定时任务')
    parser.add_argument('--mode', choices=['once', 'schedule'], default='once',
                       help='运行模式: once=执行一次, schedule=定时执行')
    
    args = parser.parse_args()
    
    if args.mode == 'once':
        print("🚀 执行单次爬虫任务...")
        run_daily_crawl()
    else:
        print("🚀 启动定时任务服务...")
        setup_schedule()


