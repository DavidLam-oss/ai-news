#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复飞书token问题
"""

import asyncio
import httpx
import json
import os

async def test_different_tokens():
    """测试不同的token组合"""
    print("🔧 飞书token修复工具")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    
    # 从URL中提取的不同token
    url_tokens = {
        "wiki_token": "DHzwwDvX6i3tCmk0rl8cpDsonSf",  # 从/wiki/后面提取
        "table_token": "tblsXDf7QkK9jLzI",             # 从table=后面提取
        "view_token": "vewbnRFlyq",                    # 从view=后面提取
        "base_token": "o7y2a6yi3x"                     # 从域名前面提取
    }
    
    print(f"📋 从URL提取的token:")
    for name, token in url_tokens.items():
        print(f"   {name}: {token}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 获取访问令牌
        print(f"\n🔑 获取访问令牌...")
        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
            data = {"app_id": app_id, "app_secret": app_secret}
            
            response = await client.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    access_token = result.get("app_access_token")
                    print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
                else:
                    print(f"❌ 获取访问令牌失败: {result.get('msg')}")
                    return
            else:
                print(f"❌ 获取访问令牌失败: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 获取访问令牌异常: {e}")
            return
        
        # 2. 测试不同的token组合
        print(f"\n🧪 测试不同的token组合...")
        
        # 测试wiki_token作为应用token
        print(f"\n📱 测试1: 使用wiki_token作为应用token")
        await test_app_token(client, access_token, url_tokens["wiki_token"], "wiki_token")
        
        # 测试table_token作为应用token
        print(f"\n📱 测试2: 使用table_token作为应用token")
        await test_app_token(client, access_token, url_tokens["table_token"], "table_token")
        
        # 测试base_token作为应用token
        print(f"\n📱 测试3: 使用base_token作为应用token")
        await test_app_token(client, access_token, url_tokens["base_token"], "base_token")
        
        # 3. 尝试获取用户的应用列表
        print(f"\n📋 尝试获取应用列表...")
        await get_user_apps(client, access_token)

async def test_app_token(client, access_token, app_token, token_name):
    """测试应用token"""
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = await client.get(url, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                app_info = result.get("data", {})
                print(f"   ✅ {token_name} 作为应用token成功!")
                print(f"   应用名称: {app_info.get('name', 'N/A')}")
                print(f"   应用描述: {app_info.get('description', 'N/A')}")
                return True
            else:
                print(f"   ❌ {token_name} 失败: {result.get('msg')}")
        else:
            print(f"   ❌ {token_name} 失败: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ {token_name} 异常: {e}")
    
    return False

async def get_user_apps(client, access_token):
    """尝试获取用户的应用列表"""
    try:
        # 尝试不同的API端点
        endpoints = [
            "https://open.feishu.cn/open-apis/bitable/v1/apps",
            "https://open.feishu.cn/open-apis/drive/v1/files",
            "https://open.feishu.cn/open-apis/drive/v1/files/root_children"
        ]
        
        for endpoint in endpoints:
            print(f"\n🔍 尝试端点: {endpoint}")
            try:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.get(endpoint, headers=headers)
                print(f"   状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 0:
                        data = result.get("data", {})
                        items = data.get("items", []) if isinstance(data, dict) else []
                        print(f"   ✅ 成功获取 {len(items)} 个项目")
                        for item in items[:3]:  # 只显示前3个
                            print(f"      - {item.get('name', 'N/A')} (ID: {item.get('token', item.get('file_token', 'N/A'))})")
                    else:
                        print(f"   ❌ 失败: {result.get('msg')}")
                else:
                    print(f"   ❌ 失败: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 异常: {e}")
                
    except Exception as e:
        print(f"❌ 获取应用列表异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_different_tokens())
