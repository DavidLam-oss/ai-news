#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书连接诊断工具
"""

import asyncio
import httpx
import json
import os

async def diagnose_feishu_connection():
    """诊断飞书连接问题"""
    print("🔍 飞书连接诊断工具")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    app_token = "DHzwwDvX6i3tCmk0rl8cpDsonSf"
    table_token = "tblsXDf7QkK9jLzI"
    
    print(f"📋 配置信息:")
    print(f"   APP ID: {app_id}")
    print(f"   APP SECRET: {app_secret[:10]}...")
    print(f"   应用token: {app_token}")
    print(f"   表格token: {table_token}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 测试访问令牌获取
        print(f"\n🔑 步骤1: 测试访问令牌获取...")
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
        
        # 2. 测试应用信息获取
        print(f"\n📱 步骤2: 测试应用信息获取...")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await client.get(url, headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    app_info = result.get("data", {})
                    print(f"✅ 应用信息获取成功")
                    print(f"   应用名称: {app_info.get('name', 'N/A')}")
                    print(f"   应用描述: {app_info.get('description', 'N/A')}")
                else:
                    print(f"❌ 获取应用信息失败: {result.get('msg')}")
                    if "99991672" in str(result):
                        print("💡 这是权限不足的错误，需要申请以下权限:")
                        print("   - bitable:app:readonly")
                        print("   - bitable:app")
                        print("   - base:app:read")
            else:
                print(f"❌ 获取应用信息失败: {response.text}")
        except Exception as e:
            print(f"❌ 获取应用信息异常: {e}")
        
        # 3. 测试表格列表获取
        print(f"\n📊 步骤3: 测试表格列表获取...")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await client.get(url, headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    tables = result.get("data", {}).get("items", [])
                    print(f"✅ 表格列表获取成功，共 {len(tables)} 个表格")
                    for table in tables:
                        print(f"   表格ID: {table.get('table_id')}")
                        print(f"   表格名称: {table.get('name')}")
                        if table.get('table_id') == table_token:
                            print(f"   ✅ 找到目标表格!")
                else:
                    print(f"❌ 获取表格列表失败: {result.get('msg')}")
                    if "99991672" in str(result):
                        print("💡 这是权限不足的错误，需要申请以下权限:")
                        print("   - bitable:app:readonly")
                        print("   - bitable:app")
                        print("   - base:table:read")
            else:
                print(f"❌ 获取表格列表失败: {response.text}")
        except Exception as e:
            print(f"❌ 获取表格列表异常: {e}")
        
        # 4. 测试特定表格信息获取
        print(f"\n📋 步骤4: 测试特定表格信息获取...")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_token}"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await client.get(url, headers=headers)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    table_info = result.get("data", {})
                    print(f"✅ 表格信息获取成功")
                    print(f"   表格名称: {table_info.get('name', 'N/A')}")
                    print(f"   表格ID: {table_info.get('table_id', 'N/A')}")
                else:
                    print(f"❌ 获取表格信息失败: {result.get('msg')}")
            elif response.status_code == 404:
                print(f"❌ 表格不存在 (404)")
                print("💡 可能的原因:")
                print("   1. 表格token不正确")
                print("   2. 表格已被删除")
                print("   3. 应用没有访问该表格的权限")
            else:
                print(f"❌ 获取表格信息失败: {response.text}")
        except Exception as e:
            print(f"❌ 获取表格信息异常: {e}")
        
        # 5. 测试记录获取
        print(f"\n📝 步骤5: 测试记录获取...")
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_token}/records"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"page_size": 5}
            
            response = await client.get(url, headers=headers, params=params)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    records = result.get("data", {}).get("items", [])
                    print(f"✅ 记录获取成功，共 {len(records)} 条记录")
                else:
                    print(f"❌ 获取记录失败: {result.get('msg')}")
                    if "99991672" in str(result):
                        print("💡 这是权限不足的错误，需要申请以下权限:")
                        print("   - base:record:retrieve")
            else:
                print(f"❌ 获取记录失败: {response.text}")
        except Exception as e:
            print(f"❌ 获取记录异常: {e}")
    
    # 总结诊断结果
    print(f"\n📋 诊断总结:")
    print(f"   1. 检查权限申请状态")
    print(f"   2. 验证表格token是否正确")
    print(f"   3. 确认应用是否有访问权限")
    print(f"   4. 等待权限审核通过")

if __name__ == "__main__":
    asyncio.run(diagnose_feishu_connection())
