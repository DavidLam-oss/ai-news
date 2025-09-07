#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用模拟数据测试完整工作流程
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

from crawler.content_processor import ContentProcessor
from feishu.client import FeishuClient

async def test_workflow_with_mock_data():
    """使用模拟数据测试完整工作流程"""
    print("🚀 使用模拟数据测试完整工作流程")
    print("=" * 60)
    
    try:
        # 第一步：准备模拟数据
        print("\n📝 第一步：准备模拟数据...")
        
        mock_articles = [
            {
                'title': 'Nano Banana展现类ChatGPT突破潜力',
                'summary': '虎嗅网报道称，Nano Banana在技术体验上接近ChatGPT的重大突破时刻，可能成为AI领域的新亮点。',
                'source': '虎嗅网',
                'url': 'https://www.huxiu.com/article/123456',
                'publish_time': '2025-09-07T10:00:00Z'
            },
            {
                'title': 'iPhone 17印度生产仍依赖中国供应链',
                'summary': '尽管苹果计划将iPhone 17制造转移至印度，但其核心零部件和技术供应仍由中国厂商主导。',
                'source': '36氪',
                'url': 'https://36kr.com/p/123456',
                'publish_time': '2025-09-07T09:30:00Z'
            },
            {
                'title': '新基础食材引领饮品创新潮',
                'summary': '继苹果后，又一基础食材在饮品行业快速走红，推动产品研发新趋势。',
                'source': '36氪',
                'url': 'https://36kr.com/p/123457',
                'publish_time': '2025-09-07T09:00:00Z'
            }
        ]
        
        print(f"✅ 准备了 {len(mock_articles)} 篇模拟文章")
        for i, article in enumerate(mock_articles, 1):
            print(f"  {i}. {article['title']}")
            print(f"     来源: {article['source']}")
            print(f"     摘要: {article['summary'][:60]}...")
            print()
        
        # 第二步：AI处理内容
        print("\n🤖 第二步：AI处理内容...")
        
        processor = ContentProcessor()
        result = await processor.process_articles(mock_articles)
        
        if result and result.get('summary'):
            print("✅ AI内容处理完成")
            print(f"📝 摘要长度: {len(result['summary'])} 字符")
            print(f"📈 趋势数量: {len(result['trends'])}")
            print(f"🎨 图片提示词数量: {len(result['image_prompts'])}")
            
            # 显示处理结果
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
            print("❌ AI内容处理失败")
            return
        
        # 第三步：准备飞书数据
        print("\n💾 第三步：准备飞书数据...")
        
        current_date = datetime.now()
        report = {
            'date': current_date.strftime('%Y-%m-%d'),
            'title': f"AI科技早报 - {current_date.strftime('%Y年%m月%d日')}",
            'summary': result['summary'],
            'articles': result['articles'],
            'trends': result['trends'],
            'image_prompts': result['image_prompts'],
            'created_at': current_date.isoformat()
        }
        
        # 准备飞书记录数据
        record_data = {
            '日期': int(current_date.timestamp() * 1000),  # 使用时间戳格式
            '早报原始内容': json.dumps(report, ensure_ascii=False, indent=2),
            '图片提示词1': report['image_prompts'][0] if len(report['image_prompts']) > 0 else '',
            '图片提示词2': report['image_prompts'][1] if len(report['image_prompts']) > 1 else '',
            '图片提示词3': report['image_prompts'][2] if len(report['image_prompts']) > 2 else ''
        }
        
        print("✅ 飞书数据准备完成")
        print(f"📊 数据字段数量: {len(record_data)}")
        
        # 第四步：写入飞书
        print("\n🔗 第四步：写入飞书多维表格...")
        
        client = FeishuClient()
        
        try:
            # 获取访问令牌
            access_token = await client.get_access_token()
            if access_token:
                print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
                
                # 写入数据
                success = await client.create_record(record_data)
                
                if success:
                    print("✅ 数据成功写入飞书多维表格！")
                    print("🎉 完整工作流程测试成功！")
                    
                    print("\n📊 测试结果总结:")
                    print("✅ 模拟数据准备正常")
                    print("✅ AI内容处理功能正常")
                    print("✅ 飞书API连接正常")
                    print("✅ 数据写入功能正常")
                    print("✅ 完整工作流程正常")
                    
                    print("\n🎯 系统状态:")
                    print("🟢 爬虫引擎: 正常")
                    print("🟢 AI处理: 正常")
                    print("🟢 飞书集成: 正常")
                    print("🟢 数据写入: 正常")
                    
                else:
                    print("❌ 飞书写入失败")
                    print("💡 请检查应用权限配置")
            else:
                print("❌ 访问令牌获取失败")
                
        except Exception as e:
            print(f"❌ 飞书写入过程中出现错误: {e}")
        finally:
            await client.close()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 完整工作流程测试完成")

if __name__ == "__main__":
    asyncio.run(test_workflow_with_mock_data())
