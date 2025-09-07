#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细错误检查
"""

import asyncio
import httpx
import json

async def detailed_error_check():
    """详细错误检查"""
    print("🔍 详细错误检查")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    app_token = "DHzwwDvX6i3tCmk0rl8cpDsonSf"
    table_token = "tblsXDf7QkK9jLzI"
    
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
        
        # 2. 测试应用信息获取并显示详细错误
        print(f"\n📱 测试应用信息获取...")
        await test_with_detailed_error(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}", "应用信息")
        
        # 3. 测试表格列表获取并显示详细错误
        print(f"\n📊 测试表格列表获取...")
        await test_with_detailed_error(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables", "表格列表")
        
        # 4. 尝试不同的API端点
        print(f"\n🔄 尝试不同的API端点...")
        
        # 尝试获取所有应用
        print(f"\n📋 尝试获取所有应用...")
        await test_with_detailed_error(client, tenant_access_token, "https://open.feishu.cn/open-apis/bitable/v1/apps", "所有应用")
        
        # 尝试获取文件列表
        print(f"\n📁 尝试获取文件列表...")
        await test_with_detailed_error(client, tenant_access_token, "https://open.feishu.cn/open-apis/drive/v1/files/root_children", "文件列表")

async def test_with_detailed_error(client, tenant_access_token, url, test_name):
    """测试并显示详细错误信息"""
    try:
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        response = await client.get(url, headers=headers)
        
        print(f"   URL: {url}")
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        # 获取响应内容
        try:
            response_text = response.text
            print(f"   响应内容: {response_text}")
            
            # 尝试解析JSON
            if response_text:
                try:
                    result = json.loads(response_text)
                    print(f"   JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
                except:
                    print(f"   响应不是有效的JSON格式")
        except Exception as e:
            print(f"   读取响应内容失败: {e}")
        
        if response.status_code == 200:
            print(f"   ✅ {test_name} 获取成功")
            return True
        else:
            print(f"   ❌ {test_name} 失败")
            return False
                
    except Exception as e:
        print(f"   ❌ {test_name} 异常: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(detailed_error_check())
