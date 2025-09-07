#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取飞书应用列表
"""

import asyncio
import httpx
import json

async def get_app_list():
    """获取飞书应用列表"""
    print("🔍 获取飞书应用列表")
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
        
        # 2. 尝试不同的API端点获取应用列表
        print(f"\n📋 尝试获取应用列表...")
        
        # 方法1: 使用drive API获取文件列表
        await try_drive_api(client, tenant_access_token)
        
        # 方法2: 使用bitable API获取应用列表
        await try_bitable_api(client, tenant_access_token)
        
        # 方法3: 使用其他可能的API端点
        await try_other_apis(client, tenant_access_token)

async def try_drive_api(client, tenant_access_token):
    """尝试使用drive API获取文件列表"""
    print(f"\n🔍 方法1: 使用drive API...")
    
    endpoints = [
        "https://open.feishu.cn/open-apis/drive/v1/files/root_children",
        "https://open.feishu.cn/open-apis/drive/v1/files",
        "https://open.feishu.cn/open-apis/drive/v1/files/search"
    ]
    
    for endpoint in endpoints:
        print(f"   尝试端点: {endpoint}")
        try:
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            response = await client.get(endpoint, headers=headers)
            
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    data = result.get("data", {})
                    files = data.get("files", []) if isinstance(data, dict) else []
                    print(f"   ✅ 成功获取 {len(files)} 个文件")
                    for file in files:
                        print(f"      - {file.get('name', 'N/A')} (token: {file.get('token', 'N/A')})")
                        if file.get('type') == 'bitable':
                            print(f"        🎯 这是多维表格!")
                else:
                    print(f"   ❌ 失败: {result.get('msg')}")
            else:
                print(f"   ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")

async def try_bitable_api(client, tenant_access_token):
    """尝试使用bitable API获取应用列表"""
    print(f"\n🔍 方法2: 使用bitable API...")
    
    endpoints = [
        "https://open.feishu.cn/open-apis/bitable/v1/apps",
        "https://open.feishu.cn/open-apis/bitable/v1/apps?page_size=100"
    ]
    
    for endpoint in endpoints:
        print(f"   尝试端点: {endpoint}")
        try:
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            response = await client.get(endpoint, headers=headers)
            
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    data = result.get("data", {})
                    apps = data.get("items", []) if isinstance(data, dict) else []
                    print(f"   ✅ 成功获取 {len(apps)} 个应用")
                    for app in apps:
                        print(f"      - {app.get('name', 'N/A')} (token: {app.get('app_token', 'N/A')})")
                else:
                    print(f"   ❌ 失败: {result.get('msg')}")
            else:
                print(f"   ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")

async def try_other_apis(client, tenant_access_token):
    """尝试其他可能的API端点"""
    print(f"\n🔍 方法3: 尝试其他API端点...")
    
    endpoints = [
        "https://open.feishu.cn/open-apis/application/v6/applications/self",
        "https://open.feishu.cn/open-apis/tenant/v2/tenant",
        "https://open.feishu.cn/open-apis/authen/v1/user_info"
    ]
    
    for endpoint in endpoints:
        print(f"   尝试端点: {endpoint}")
        try:
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            response = await client.get(endpoint, headers=headers)
            
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    print(f"   ✅ 成功获取信息")
                    data = result.get("data", {})
                    print(f"   数据: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                else:
                    print(f"   ❌ 失败: {result.get('msg')}")
            else:
                print(f"   ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")

if __name__ == "__main__":
    asyncio.run(get_app_list())
