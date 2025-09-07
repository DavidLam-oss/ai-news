#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找正确的飞书应用token
"""

import asyncio
import httpx
import json

async def find_correct_token():
    """查找正确的飞书应用token"""
    print("🔍 查找正确的飞书应用token")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 获取tenant_access_token
        print(f"🔑 获取tenant_access_token...")
        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            data = {"app_id": app_id, "app_secret": app_secret}
            
            response = await client.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    tenant_access_token = result.get("tenant_access_token")
                    print(f"✅ tenant_access_token获取成功: {tenant_access_token[:20]}...")
                else:
                    print(f"❌ 获取tenant_access_token失败: {result.get('msg')}")
                    return
            else:
                print(f"❌ 获取tenant_access_token失败: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 获取tenant_access_token异常: {e}")
            return
        
        # 2. 尝试获取应用列表
        print(f"\n📋 尝试获取应用列表...")
        await try_get_apps(client, tenant_access_token)
        
        # 3. 提供手动获取token的方法
        print(f"\n💡 手动获取token的方法:")
        print(f"   1. 在飞书中打开多维表格")
        print(f"   2. 点击右上角的'...'菜单")
        print(f"   3. 选择'复制链接'")
        print(f"   4. 检查链接格式:")
        print(f"      - 多维表格: https://xxx.feishu.cn/base/应用token?table=表格token")
        print(f"      - 知识库: https://xxx.feishu.cn/wiki/应用token?table=表格token")
        print(f"   5. 应用token是/base/或/wiki/后面的部分")

async def try_get_apps(client, tenant_access_token):
    """尝试获取应用列表"""
    # 尝试不同的API端点
    endpoints = [
        "https://open.feishu.cn/open-apis/bitable/v1/apps",
        "https://open.feishu.cn/open-apis/drive/v1/files/root_children",
        "https://open.feishu.cn/open-apis/drive/v1/files"
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 尝试端点: {endpoint}")
        try:
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            response = await client.get(endpoint, headers=headers)
            
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    data = result.get("data", {})
                    items = data.get("items", []) if isinstance(data, dict) else []
                    print(f"   ✅ 成功获取 {len(items)} 个项目")
                    for item in items[:5]:  # 只显示前5个
                        name = item.get('name', 'N/A')
                        token = item.get('token', item.get('app_token', 'N/A'))
                        item_type = item.get('type', 'N/A')
                        print(f"      - {name} (token: {token}, type: {item_type})")
                        if item_type == 'bitable':
                            print(f"        🎯 这是多维表格!")
                else:
                    print(f"   ❌ 失败: {result.get('msg')}")
            else:
                print(f"   ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")

if __name__ == "__main__":
    asyncio.run(find_correct_token())
