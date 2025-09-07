#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的飞书配置测试
"""

import asyncio
import os

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def simple_test():
    """简单测试"""
    print("🔧 简单飞书配置测试")
    print("=" * 50)
    
    client = FeishuClient()
    
    try:
        # 测试访问令牌
        print("🔑 测试访问令牌...")
        access_token = await client.get_access_token()
        if access_token:
            print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
        else:
            print("❌ 访问令牌获取失败")
            return
        
        # 测试获取记录
        print("\n📝 测试获取记录...")
        records = await client.get_records(page_size=5)
        if records:
            print(f"✅ 记录获取成功，共 {len(records)} 条记录")
            for i, record in enumerate(records[:3]):
                print(f"   记录 {i+1}: {record.get('record_id', 'N/A')}")
        else:
            print("❌ 记录获取失败")
        
        print("\n🎉 飞书配置测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(simple_test())
