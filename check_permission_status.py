#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查飞书权限状态
"""

import asyncio
import httpx
import json

async def check_permission_status():
    """检查飞书权限状态"""
    print("🔍 飞书权限状态检查")
    print("=" * 50)
    
    # 配置信息
    app_id = "cli_a8366b7ef13a100c"
    app_secret = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 获取访问令牌
        print(f"🔑 获取访问令牌...")
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
        
        # 2. 测试基础权限
        print(f"\n🧪 测试基础权限...")
        
        # 测试获取应用信息
        print(f"\n📱 测试获取应用信息...")
        await test_basic_permission(client, access_token, "https://open.feishu.cn/open-apis/application/v6/applications/self", "应用信息")
        
        # 测试获取用户信息
        print(f"\n👤 测试获取用户信息...")
        await test_basic_permission(client, access_token, "https://open.feishu.cn/open-apis/authen/v1/user_info", "用户信息")
        
        # 测试获取租户信息
        print(f"\n🏢 测试获取租户信息...")
        await test_basic_permission(client, access_token, "https://open.feishu.cn/open-apis/tenant/v2/tenant", "租户信息")
        
        # 3. 检查权限申请状态
        print(f"\n📋 权限申请状态检查...")
        print(f"   应用ID: {app_id}")
        print(f"   权限申请链接: https://open.feishu.cn/app/{app_id}/auth")
        print(f"   应用管理后台: https://open.feishu.cn/app/{app_id}")
        
        # 4. 提供解决方案
        print(f"\n💡 解决方案:")
        print(f"   1. 检查权限申请是否已提交")
        print(f"   2. 确认管理员是否已审核通过")
        print(f"   3. 检查应用版本是否已发布")
        print(f"   4. 等待权限生效（通常需要几分钟）")

async def test_basic_permission(client, access_token, url, permission_name):
    """测试基础权限"""
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(url, headers=headers)
        
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print(f"   ✅ {permission_name} 获取成功")
                return True
            else:
                print(f"   ❌ {permission_name} 失败: {result.get('msg')}")
                if "99991672" in str(result):
                    print(f"   💡 权限不足，需要申请相应权限")
        else:
            print(f"   ❌ {permission_name} 失败: {response.status_code}")
            if response.status_code == 403:
                print(f"   💡 权限被拒绝，需要申请相应权限")
            elif response.status_code == 404:
                print(f"   💡 资源不存在或权限不足")
                
    except Exception as e:
        print(f"   ❌ {permission_name} 异常: {e}")
    
    return False

if __name__ == "__main__":
    asyncio.run(check_permission_status())
