#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终飞书测试 - 使用tenant_access_token
"""

import asyncio
import httpx
import json

async def final_feishu_test():
    """最终飞书测试"""
    print("🔧 最终飞书测试")
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
        
        # 2. 测试应用信息获取
        print(f"\n📱 测试应用信息获取...")
        await test_with_tenant_token(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}", "应用信息")
        
        # 3. 测试表格列表获取
        print(f"\n📊 测试表格列表获取...")
        await test_with_tenant_token(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables", "表格列表")
        
        # 4. 测试特定表格信息获取
        print(f"\n📋 测试特定表格信息获取...")
        await test_with_tenant_token(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_token}", "表格信息")
        
        # 5. 测试记录获取
        print(f"\n📝 测试记录获取...")
        await test_with_tenant_token(client, tenant_access_token, f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_token}/records?page_size=5", "记录列表")

async def test_with_tenant_token(client, tenant_access_token, url, test_name):
    """使用tenant_access_token测试"""
    try:
        headers = {"Authorization": f"Bearer {tenant_access_token}"}
        response = await client.get(url, headers=headers)
        
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print(f"   ✅ {test_name} 获取成功")
                data = result.get("data", {})
                if isinstance(data, dict):
                    if "items" in data:
                        items = data["items"]
                        print(f"   📊 共 {len(items)} 个项目")
                        for item in items[:3]:  # 只显示前3个
                            print(f"      - {item.get('name', 'N/A')} (ID: {item.get('table_id', item.get('token', 'N/A'))})")
                    else:
                        print(f"   📋 数据: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                return True
            else:
                print(f"   ❌ {test_name} 失败: {result.get('msg')}")
                if "99991672" in str(result):
                    print(f"   💡 权限不足，需要申请相应权限")
                elif "91402" in str(result):
                    print(f"   💡 资源不存在，请检查token是否正确")
        else:
            print(f"   ❌ {test_name} 失败: {response.status_code}")
            if response.status_code == 403:
                print(f"   💡 权限被拒绝，需要申请相应权限")
            elif response.status_code == 404:
                print(f"   💡 资源不存在或权限不足")
                
    except Exception as e:
        print(f"   ❌ {test_name} 异常: {e}")
    
    return False

if __name__ == "__main__":
    asyncio.run(final_feishu_test())
