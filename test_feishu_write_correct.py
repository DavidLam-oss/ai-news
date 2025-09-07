#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用正确字段名称测试飞书写入功能
"""

import asyncio
import json
import os
from datetime import datetime

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def test_feishu_write_correct():
    """使用正确字段名称测试飞书写入功能"""
    print("🎯 使用正确字段名称测试飞书写入功能")
    print("=" * 60)
    
    try:
        # 创建飞书客户端
        client = FeishuClient()
        
        print(f"📋 配置信息:")
        print(f"   APP ID: {client.app_id}")
        print(f"   TABLE TOKEN: {client.table_token}")
        print(f"   TABLE ID: tblsXDf7QkK9jLzI")
        print()
        
        # 获取访问令牌
        print("📡 正在获取访问令牌...")
        access_token = await client.get_access_token()
        
        if access_token:
            print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
            
            # 准备测试数据 - 使用正确的字段名称
            test_data = {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '早报原始内容': json.dumps({
                    'title': 'AI科技早报测试',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'articles': [
                        {
                            'title': 'Nano Banana展现类ChatGPT突破潜力',
                            'summary': '虎嗅网报道称，Nano Banana在技术体验上接近ChatGPT的重大突破时刻',
                            'source': '虎嗅网'
                        }
                    ],
                    'test': True
                }, ensure_ascii=False, indent=2),
                '图片提示词1': '未来感线条构成的香蕉轮廓，内部流动着蓝色数据流，象征AI与科技创新的融合，背景简洁现代。',
                '图片提示词2': '发光的数字香蕉悬浮于科技蓝背景中，周围环绕微小的二进制代码粒子，展现智能科技的未来感。',
                '图片提示词3': '极简风格的AI芯片嵌入香蕉剖面，散发柔和光晕，背景干净明亮，传递科技与自然的和谐创新。'
            }
            
            print(f"\n📝 准备写入测试数据 (使用正确字段名称):")
            print(f"   📅 日期: {test_data['日期']}")
            print(f"   📰 早报原始内容: {len(test_data['早报原始内容'])} 字符")
            print(f"   🎨 图片提示词1: {test_data['图片提示词1'][:30]}...")
            print(f"   🎨 图片提示词2: {test_data['图片提示词2'][:30]}...")
            print(f"   🎨 图片提示词3: {test_data['图片提示词3'][:30]}...")
            print()
            
            # 尝试写入数据
            print("💾 正在尝试写入飞书多维表格...")
            success = await client.create_record(test_data)
            
            if success:
                print("✅ 数据写入成功！")
                print("🎉 飞书写入功能完全正常！")
                print("\n📊 成功写入的数据:")
                for key, value in test_data.items():
                    if key == '早报原始内容':
                        print(f"   {key}: {value[:100]}...")
                    else:
                        print(f"   {key}: {value}")
                        
                print("\n🎯 测试结果:")
                print("✅ 飞书API连接正常")
                print("✅ 访问令牌获取成功")
                print("✅ 表格连接正常")
                print("✅ 数据写入成功")
                print("✅ 字段名称匹配正确")
                
            else:
                print("❌ 数据写入失败")
                print("💡 请检查应用权限配置")
        else:
            print("❌ 访问令牌获取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭客户端
        if 'client' in locals():
            await client.close()
    
    print("\n🏁 飞书写入功能测试完成")

if __name__ == "__main__":
    asyncio.run(test_feishu_write_correct())
