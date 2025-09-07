#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试飞书写入功能
"""

import asyncio
import json
import os
from datetime import datetime

# 设置环境变量
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def test_feishu_write_final():
    """最终测试飞书写入功能"""
    print("🚀 最终测试飞书写入功能")
    print("=" * 50)
    
    try:
        # 创建飞书客户端
        client = FeishuClient()
        
        print(f"📋 配置信息:")
        print(f"   APP ID: {client.app_id}")
        print(f"   TABLE TOKEN: {client.table_token}")
        print(f"   TABLE ID: tblsXDf7QkK9jLzI")
        print()
        
        # 获取访问令牌
        print("📡 正在获取访问令牌...")
        access_token = await client.get_access_token()
        
        if access_token:
            print(f"✅ 访问令牌获取成功: {access_token[:20]}...")
            
            # 准备测试数据
            test_data = {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '早报原始内容': json.dumps({
                    'title': 'AI科技早报测试',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'articles': [
                        {
                            'title': 'Nano Banana展现类ChatGPT突破潜力',
                            'summary': '虎嗅网报道称，Nano Banana在技术体验上接近ChatGPT的重大突破时刻',
                            'source': '虎嗅网'
                        }
                    ],
                    'test': True
                }, ensure_ascii=False, indent=2),
                'AI处理后内容': '【AI科技早报】2025-09-07\n\n1. **Nano Banana展现类ChatGPT突破潜力**\n   虎嗅网报道称，Nano Banana在技术体验上接近ChatGPT的重大突破时刻，可能成为AI领域的新亮点。\n\n---\n*本期早报由AI整理，仅供参考。*',
                '图片提示词1': '未来感线条构成的香蕉轮廓，内部流动着蓝色数据流，象征AI与科技创新的融合，背景简洁现代。',
                '图片提示词2': '发光的数字香蕉悬浮于科技蓝背景中，周围环绕微小的二进制代码粒子，展现智能科技的未来感。',
                '图片提示词3': '极简风格的AI芯片嵌入香蕉剖面，散发柔和光晕，背景干净明亮，传递科技与自然的和谐创新。'
            }
            
            print(f"\n📝 准备写入测试数据:")
            print(f"   📅 日期: {test_data['日期']}")
            print(f"   📰 标题: AI科技早报测试")
            print(f"   🎨 图片提示词数量: 3")
            print()
            
            # 尝试写入数据
            print("💾 正在尝试写入飞书多维表格...")
            success = await client.create_record(test_data)
            
            if success:
                print("✅ 数据写入成功！")
                print("🎉 飞书写入功能完全正常！")
                print("\n📊 写入的数据:")
                for key, value in test_data.items():
                    if key == '早报原始内容':
                        print(f"   {key}: {value[:100]}...")
                    else:
                        print(f"   {key}: {value}")
            else:
                print("❌ 数据写入失败")
                print("💡 可能的原因：")
                print("   1. 表格字段名称不匹配")
                print("   2. 应用权限不足")
                print("   3. 数据格式不正确")
                
                # 尝试获取表格字段信息
                print("\n🔍 尝试获取表格字段信息...")
                try:
                    import httpx
                    async with httpx.AsyncClient() as http_client:
                        fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{client.table_token}/tables/tblsXDf7QkK9jLzI/fields"
                        headers = {"Authorization": f"Bearer {access_token}"}
                        
                        fields_response = await http_client.get(fields_url, headers=headers)
                        fields_result = fields_response.json()
                        
                        if fields_result.get("code") == 0:
                            fields = fields_result.get("data", {}).get("items", [])
                            print(f"📋 表格字段 ({len(fields)} 个):")
                            for field in fields:
                                field_name = field.get('field_name', 'N/A')
                                field_type = field.get('type', 'N/A')
                                print(f"   - {field_name} ({field_type})")
                        else:
                            print(f"❌ 获取字段信息失败: {fields_result.get('msg', 'Unknown error')}")
                except Exception as e:
                    print(f"❌ 获取字段信息时出错: {e}")
        else:
            print("❌ 访问令牌获取失败")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭客户端
        if 'client' in locals():
            await client.close()
    
    print("\n🏁 飞书写入功能测试完成")

if __name__ == "__main__":
    asyncio.run(test_feishu_write_final())
