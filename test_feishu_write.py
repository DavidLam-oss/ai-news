#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书写入功能
"""

import asyncio
import json
import os
from datetime import datetime

# 设置环境变量（必须在导入之前）
os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
os.environ["FEISHU_TABLE_TOKEN"] = "F5I2bdNZxawzTqsRBVbcJWEMn9H"

from feishu.client import FeishuClient

async def test_feishu_write():
    """测试飞书写入功能"""
    print("🔧 开始测试飞书写入功能...")
    
    try:
        # 创建飞书客户端
        client = FeishuClient()
        
        # 测试获取访问令牌
        print("📡 正在获取飞书访问令牌...")
        access_token = await client.get_access_token()
        
        if access_token:
            print("✅ 飞书访问令牌获取成功！")
            print(f"🔑 访问令牌: {access_token[:20]}...")
            
            # 准备测试数据
            test_data = {
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '早报原始内容': json.dumps({
                    'title': 'AI科技早报测试',
                    'articles': [
                        {
                            'title': 'Nano Banana或迎来ChatGPT式突破',
                            'summary': '新型AI技术Nano Banana展现出类似ChatGPT的颠覆潜力',
                            'source': '36氪'
                        },
                        {
                            'title': 'iPhone 17印度生产仍依赖中国供应链',
                            'summary': '尽管苹果计划将iPhone 17制造转移至印度，但其核心零部件和技术供应仍由中国厂商主导',
                            'source': '36氪'
                        }
                    ]
                }, ensure_ascii=False, indent=2),
                'AI处理后内容': '【AI科技早报】2024-01-15\n\n1. **Nano Banana或迎来ChatGPT式突破**\n   新型AI技术Nano Banana展现出类似ChatGPT的颠覆潜力，可能成为下一代智能交互的核心突破。\n\n2. **iPhone 17印度生产仍依赖中国供应链**\n   尽管苹果计划将iPhone 17制造转移至印度，但其核心零部件和技术供应仍由中国厂商主导。',
                '图片提示词1': '发光的AI芯片悬浮于简洁背景前，蓝色数据流环绕，展现科技未来感与现代极简美学。',
                '图片提示词2': '全球供应链地图以发光线条连接中印两地，AI图标在关键节点闪烁，呈现科技互联的简洁视觉。',
                '图片提示词3': '透明饮品杯中浮现数字化食材粒子，AI能量波从中迸发，用现代设计语言诠释科技与饮品的创新融合。'
            }
            
            print("\n📝 准备写入测试数据...")
            print(f"📅 日期: {test_data['日期']}")
            print(f"📰 标题: AI科技早报测试")
            print(f"🎨 图片提示词数量: 3")
            
            # 尝试写入数据
            print("\n💾 正在尝试写入飞书多维表格...")
            success = await client.create_record(test_data)
            
            if success:
                print("✅ 数据写入成功！")
                print("🎉 飞书写入功能测试通过！")
            else:
                print("❌ 数据写入失败")
                print("💡 可能的原因：")
                print("   1. 表格token不正确")
                print("   2. 表格字段名称不匹配")
                print("   3. 应用权限不足")
                print("   4. 表格不存在或已被删除")
                
                # 尝试获取表格信息来诊断问题
                print("\n🔍 尝试获取表格信息进行诊断...")
                table_info = await client.get_table_info()
                if table_info:
                    print("✅ 表格信息获取成功")
                    print(f"📋 表格信息: {json.dumps(table_info, ensure_ascii=False, indent=2)}")
                else:
                    print("❌ 无法获取表格信息")
            
        else:
            print("❌ 飞书访问令牌获取失败")
            
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
    asyncio.run(test_feishu_write())
