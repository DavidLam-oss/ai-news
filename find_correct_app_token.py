#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找正确的应用token
"""

import asyncio
import httpx
import json

async def find_correct_app_token():
    """查找正确的应用token"""
    print("🔍 查找正确的应用token")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    
    # 从URL中提取的所有可能的token
    url = "https://o7y2a6yi3x.feishu.cn/wiki/DHzwwDvX6i3tCmk0rl8cpDsonSf?table=tblsXDf7QkK9jLzI&view=vewbnRFlyq"
    
    print(f"📋 原始URL: {url}")
    print(f"📋 从URL提取的token:")
    print(f"   域名前缀: o7y2a6yi3x")
    print(f"   wiki路径: DHzwwDvX6i3tCmk0rl8cpDsonSf")
    print(f"   table参数: tblsXDf7QkK9jLzI")
    print(f"   view参数: vewbnRFlyq")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 获取tenant_access_token
        print(f"\n🔑 获取tenant_access_token...")
        try:
            url_auth = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            data = {"app_id": app_id, "app_secret": app_secret}
            
            response = await client.post(url_auth, json=data)
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
        
        # 2. 尝试不同的方法获取应用列表
        print(f"\n📋 尝试获取应用列表...")
        
        # 方法1: 使用drive API获取文件列表
        print(f"\n🔍 方法1: 使用drive API获取文件列表...")
        await try_get_files_via_drive(client, tenant_access_token)
        
        # 方法2: 尝试直接访问多维表格
        print(f"\n🔍 方法2: 尝试直接访问多维表格...")
        await try_direct_bitable_access(client, tenant_access_token)
        
        # 方法3: 尝试使用不同的API版本
        print(f"\n🔍 方法3: 尝试使用不同的API版本...")
        await try_different_api_versions(client, tenant_access_token)

async def try_get_files_via_drive(client, tenant_access_token):
    """通过drive API获取文件列表"""
    try:
        # 尝试获取根目录文件
        url = "https://open.feishu.cn/open-apis/drive/v1/files/root_children"
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        
        response = await client.get(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                files = result.get("data", {}).get("files", [])
                print(f"   ✅ 获取到 {len(files)} 个文件")
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

async def try_direct_bitable_access(client, tenant_access_token):
    """尝试直接访问多维表格"""
    # 尝试不同的应用token
    possible_tokens = [
        "DHzwwDvX6i3tCmk0rl8cpDsonSf",  # 原始wiki token
        "tblsXDf7QkK9jLzI",             # 表格token
        "o7y2a6yi3x",                   # 域名前缀
    ]
    
    for token in possible_tokens:
        print(f"\n   🔍 测试token: {token}")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{token}"
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            
            response = await client.get(url, headers=headers)
            print(f"      状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    app_info = result.get("data", {})
                    print(f"      ✅ 成功! 应用名称: {app_info.get('name', 'N/A')}")
                    return token
                else:
                    print(f"      ❌ 失败: {result.get('msg')}")
            else:
                print(f"      ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ 异常: {e}")
    
    return None

async def try_different_api_versions(client, tenant_access_token):
    """尝试不同的API版本"""
    api_versions = [
        "v1",
        "v2", 
        "v3",
        "v4"
    ]
    
    for version in api_versions:
        print(f"\n   🔍 测试API版本: {version}")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/{version}/apps"
            headers = {"Authorization": f"Bearer {tenant_access_token}"}
            
            response = await client.get(url, headers=headers)
            print(f"      状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    print(f"      ✅ 成功! 找到可用的API版本: {version}")
                    return version
                else:
                    print(f"      ❌ 失败: {result.get('msg')}")
            else:
                print(f"      ❌ 失败: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ 异常: {e}")
    
    return None

if __name__ == "__main__":
    asyncio.run(find_correct_app_token())
