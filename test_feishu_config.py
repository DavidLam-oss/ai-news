#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书配置
"""

import asyncio
import os

# 设置环境变量（必须在导入之前）
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def test_feishu_config():
    """测试飞书配置"""
    print("🔧 开始测试飞书配置...")
    
    try:
        # 创建飞书客户端
        client = FeishuClient()
        
        # 测试获取访问令牌
        print("📡 正在获取飞书访问令牌...")
        access_token = await client.get_access_token()
        
        if access_token:
            print("✅ 飞书访问令牌获取成功！")
            print(f"🔑 访问令牌: {access_token[:20]}...")
            
            # 测试获取表格信息（如果有表格token的话）
            if hasattr(client, 'table_token') and client.table_token and client.table_token != "your_table_token":
                print("📊 正在测试表格连接...")
                table_info = await client.get_table_info()
                if table_info:
                    print("✅ 表格连接成功！")
                    print(f"📋 表格信息: {table_info}")
                else:
                    print("⚠️  表格连接失败，请检查表格token配置")
            else:
                print("⚠️  未配置表格token，跳过表格连接测试")
                print("💡 提示：请在飞书多维表格中获取表格token并配置到环境变量中")
            
        else:
            print("❌ 飞书访问令牌获取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        print("💡 请检查以下配置：")
        print("   1. APP ID 是否正确")
        print("   2. APP SECRET 是否正确")
        print("   3. 网络连接是否正常")
        print("   4. 飞书应用权限是否配置正确")
    
    finally:
        # 关闭客户端
        if 'client' in locals():
            await client.close()
    
    print("🏁 飞书配置测试完成")

if __name__ == "__main__":
    asyncio.run(test_feishu_config())
