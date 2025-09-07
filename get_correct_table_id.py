#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取正确的飞书表格ID
"""

import asyncio
import os
import httpx

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

async def get_correct_table_id():
    """获取正确的表格ID"""
    print("🔍 获取正确的飞书表格ID")
    print("=" * 50)
    
    try:
        # 获取访问令牌
        print("📡 正在获取访问令牌...")
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        data = {
            "app_id": "cli_a8366b7ef13a100c",
            "app_secret": "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            result = response.json()
            
            if result.get("code") == 0:
                access_token = result.get("app_access_token") or result.get("tenant_access_token")
                print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
                
                # 尝试获取应用信息
                print("\n📋 正在获取应用信息...")
                app_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/F5I2bdNZxawzTqsRBVbcJWEMn9H"
                headers = {"Authorization": f"Bearer {access_token}"}
                
                app_response = await client.get(app_url, headers=headers)
                app_result = app_response.json()
                
                if app_result.get("code") == 0:
                    print("✅ 应用信息获取成功")
                    app_info = app_result.get("data", {})
                    print(f"📱 应用名称: {app_info.get('name', 'N/A')}")
                    print(f"📱 应用描述: {app_info.get('description', 'N/A')}")
                    
                    # 尝试获取表格列表
                    print("\n📊 正在获取表格列表...")
                    tables_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/F5I2bdNZxawzTqsRBVbcJWEMn9H/tables"
                    
                    tables_response = await client.get(tables_url, headers=headers)
                    tables_result = tables_response.json()
                    
                    if tables_result.get("code") == 0:
                        print("✅ 表格列表获取成功")
                        tables = tables_result.get("data", {}).get("items", [])
                        
                        if tables:
                            print(f"📋 找到 {len(tables)} 个表格:")
                            for i, table in enumerate(tables, 1):
                                print(f"  {i}. 表格名称: {table.get('name', 'N/A')}")
                                print(f"     表格ID: {table.get('table_id', 'N/A')}")
                                print(f"     表格类型: {table.get('revision', 'N/A')}")
                                print()
                            
                            # 使用第一个表格进行测试
                            first_table = tables[0]
                            table_id = first_table.get('table_id')
                            table_name = first_table.get('name')
                            
                            print(f"🎯 使用表格 '{table_name}' (ID: {table_id}) 进行测试...")
                            
                            # 测试获取表格信息
                            table_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/F5I2bdNZxawzTqsRBVbcJWEMn9H/tables/{table_id}"
                            table_response = await client.get(table_url, headers=headers)
                            table_result = table_response.json()
                            
                            if table_result.get("code") == 0:
                                print("✅ 表格信息获取成功")
                                table_info = table_result.get("data", {})
                                print(f"📊 表格名称: {table_info.get('name', 'N/A')}")
                                print(f"📊 表格ID: {table_info.get('table_id', 'N/A')}")
                                
                                # 测试创建记录
                                print(f"\n💾 正在测试创建记录...")
                                records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/F5I2bdNZxawzTqsRBVbcJWEMn9H/tables/{table_id}/records"
                                
                                test_data = {
                                    "fields": {
                                        "日期": "2025-09-07",
                                        "早报原始内容": "测试数据",
                                        "AI处理后内容": "这是一个测试记录",
                                        "图片提示词1": "测试提示词1",
                                        "图片提示词2": "测试提示词2",
                                        "图片提示词3": "测试提示词3"
                                    }
                                }
                                
                                create_response = await client.post(records_url, json=test_data, headers=headers)
                                create_result = create_response.json()
                                
                                if create_result.get("code") == 0:
                                    print("✅ 记录创建成功！")
                                    print("🎉 飞书写入功能完全正常！")
                                    print(f"📝 记录ID: {create_result.get('data', {}).get('record', {}).get('record_id', 'N/A')}")
                                else:
                                    print("❌ 记录创建失败")
                                    print(f"错误信息: {create_result.get('msg', 'Unknown error')}")
                                    print(f"错误代码: {create_result.get('code', 'N/A')}")
                                    
                                    # 显示字段信息
                                    print("\n🔍 尝试获取字段信息...")
                                    fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/F5I2bdNZxawzTqsRBVbcJWEMn9H/tables/{table_id}/fields"
                                    fields_response = await client.get(fields_url, headers=headers)
                                    fields_result = fields_response.json()
                                    
                                    if fields_result.get("code") == 0:
                                        fields = fields_result.get("data", {}).get("items", [])
                                        print(f"📋 表格字段 ({len(fields)} 个):")
                                        for field in fields:
                                            print(f"  - {field.get('field_name', 'N/A')} ({field.get('type', 'N/A')})")
                                    else:
                                        print(f"❌ 获取字段信息失败: {fields_result.get('msg', 'Unknown error')}")
                            else:
                                print("❌ 表格信息获取失败")
                                print(f"错误信息: {table_result.get('msg', 'Unknown error')}")
                        else:
                            print("❌ 未找到任何表格")
                    else:
                        print("❌ 表格列表获取失败")
                        print(f"错误信息: {tables_result.get('msg', 'Unknown error')}")
                        print(f"错误代码: {tables_result.get('code', 'N/A')}")
                else:
                    print("❌ 应用信息获取失败")
                    print(f"错误信息: {app_result.get('msg', 'Unknown error')}")
                    print(f"错误代码: {app_result.get('code', 'N/A')}")
            else:
                print("❌ 访问令牌获取失败")
                print(f"错误信息: {result.get('msg', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(get_correct_table_id())
