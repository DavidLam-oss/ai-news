#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试更新后的飞书配置
"""

import asyncio
import json
import os
from datetime import datetime

# 设置环境变量（必须在导入之前）
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def test_updated_feishu():
    """测试更新后的飞书配置"""
    print("🔧 测试更新后的飞书配置")
    print("=" * 50)
    
    try:
        # 创建飞书客户端
        client = FeishuClient()
        
        # 显示配置信息
        print(f"📋 配置信息:")
        print(f"   APP ID: {client.app_id}")
        print(f"   APP SECRET: {client.app_secret[:10]}...")
        print(f"   BASE URL: {client.base_url}")
        print(f"   TABLE TOKEN: {client.table_token}")
        print()
        
        # 测试获取访问令牌
        print("📡 正在获取飞书访问令牌...")
        access_token = await client.get_access_token()
        
        if access_token:
            print("✅ 飞书访问令牌获取成功！")
            print(f"🔑 访问令牌: {access_token[:20]}...")
            
            # 测试获取表格信息
            print("\n📊 正在测试表格连接...")
            table_info = await client.get_table_info()
            
            if table_info:
                print("✅ 表格连接成功！")
                print(f"📋 表格信息: {json.dumps(table_info, ensure_ascii=False, indent=2)}")
                
                # 测试创建记录
                print("\n💾 正在测试创建记录...")
                test_data = {
                    '日期': datetime.now().strftime('%Y-%m-%d'),
                    '早报原始内容': json.dumps({
                        'title': 'AI科技早报测试',
                        'test': True,
                        'timestamp': datetime.now().isoformat()
                    }, ensure_ascii=False, indent=2),
                    'AI处理后内容': '这是一个测试记录，用于验证飞书写入功能是否正常工作。',
                    '图片提示词1': '测试图片提示词1：现代科技感的设计元素',
                    '图片提示词2': '测试图片提示词2：简洁的未来主义风格',
                    '图片提示词3': '测试图片提示词3：AI与人类协作的视觉表现'
                }
                
                success = await client.create_record(test_data)
                
                if success:
                    print("✅ 记录创建成功！")
                    print("🎉 飞书配置完全正常，可以正常写入数据！")
                else:
                    print("❌ 记录创建失败")
                    print("💡 可能的原因：")
                    print("   1. 表格字段名称不匹配")
                    print("   2. 应用权限不足")
                    print("   3. 数据格式不正确")
            else:
                print("❌ 表格连接失败")
                print("💡 可能的原因：")
                print("   1. 表格token不正确")
                print("   2. 表格不存在")
                print("   3. 应用权限不足")
        else:
            print("❌ 飞书访问令牌获取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭客户端
        if 'client' in locals():
            await client.close()
    
    print("\n🏁 飞书配置测试完成")

if __name__ == "__main__":
    asyncio.run(test_updated_feishu())
