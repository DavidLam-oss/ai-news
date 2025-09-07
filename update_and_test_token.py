#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新并测试新的飞书token
"""

import asyncio
import httpx
import json
import os

async def update_and_test_token():
    """更新并测试新的飞书token"""
    print("🔧 更新并测试新的飞书token")
    print("=" * 50)
    
    # 新的配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    app_token = "F5I2bdNZxawzTqsRBVbcJWEMn9H"  # 新的正确token
    
    print(f"📋 新的配置信息:")
    print(f"   APP ID: {app_id}")
    print(f"   APP SECRET: {app_secret[:10]}...")
    print(f"   应用token: {app_token}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 获取tenant_access_token
        print(f"\n🔑 获取tenant_access_token...")
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
        
        # 2. 测试应用信息获取
        print(f"\n📱 测试应用信息获取...")
        await test_app_info(client, tenant_access_token, app_token)
        
        # 3. 测试表格列表获取
        print(f"\n📊 测试表格列表获取...")
        await test_table_list(client, tenant_access_token, app_token)
        
        # 4. 测试记录获取
        print(f"\n📝 测试记录获取...")
        await test_records(client, tenant_access_token, app_token)

async def test_app_info(client, tenant_access_token, app_token):
    """测试应用信息获取"""
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}"
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        
        response = await client.get(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                app_info = result.get("data", {})
                print(f"   ✅ 应用信息获取成功!")
                print(f"   应用名称: {app_info.get('name', 'N/A')}")
                print(f"   应用描述: {app_info.get('description', 'N/A')}")
                return True
            else:
                print(f"   ❌ 失败: {result.get('msg')}")
        else:
            print(f"   ❌ 失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    return False

async def test_table_list(client, tenant_access_token, app_token):
    """测试表格列表获取"""
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        
        response = await client.get(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                tables = result.get("data", {}).get("items", [])
                print(f"   ✅ 表格列表获取成功，共 {len(tables)} 个表格")
                for table in tables:
                    print(f"      - {table.get('name', 'N/A')} (ID: {table.get('table_id', 'N/A')})")
                return True
            else:
                print(f"   ❌ 失败: {result.get('msg')}")
        else:
            print(f"   ❌ 失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    return False

async def test_records(client, tenant_access_token, app_token):
    """测试记录获取"""
    try:
        # 先获取表格列表
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                tables = result.get("data", {}).get("items", [])
                if tables:
                    # 使用第一个表格测试记录获取
                    table_id = tables[0].get('table_id')
                    print(f"   使用表格: {tables[0].get('name', 'N/A')} (ID: {table_id})")
                    
                    # 获取记录
                    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
                    params = {"page_size": 5}
                    
                    response = await client.get(url, headers=headers, params=params)
                    print(f"   状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("code") == 0:
                            records = result.get("data", {}).get("items", [])
                            print(f"   ✅ 记录获取成功，共 {len(records)} 条记录")
                            return True
                        else:
                            print(f"   ❌ 失败: {result.get('msg')}")
                    else:
                        print(f"   ❌ 失败: {response.status_code}")
                        print(f"   响应: {response.text}")
                else:
                    print(f"   ⚠️  没有找到表格")
            else:
                print(f"   ❌ 获取表格列表失败: {result.get('msg')}")
        else:
            print(f"   ❌ 获取表格列表失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    return False

if __name__ == "__main__":
    asyncio.run(update_and_test_token())
