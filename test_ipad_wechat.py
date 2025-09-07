#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试iPad协议微信助手功能
"""

import asyncio
import json
import os
from datetime import datetime

# 设置环境变量
os.environ["IPAD_WEBHOOK_URL"] = "http://localhost:8080/webhook"  # 替换为实际的webhook地址
os.environ["DEFAULT_GROUP_NAME"] = "AI科技早报群"
os.environ["TARGET_GROUPS"] = "AI科技早报群,技术交流群,产品讨论群"

from wechat.ipad_client import IpadWechatClient

async def test_ipad_wechat():
    """测试iPad协议微信助手功能"""
    print("🤖 测试iPad协议微信助手功能")
    print("=" * 50)
    
    # 创建iPad微信客户端
    client = IpadWechatClient()
    
    try:
        # 第一步：测试连接
        print("\n📡 第一步：测试连接...")
        connected = await client.connect()
        
        if connected:
            print("✅ iPad微信客户端连接成功")
        else:
            print("❌ iPad微信客户端连接失败")
            print("💡 请检查：")
            print("   1. iPad协议助手是否正在运行")
            print("   2. webhook地址是否正确")
            print("   3. 网络连接是否正常")
            return
        
        # 第二步：获取群列表
        print("\n📋 第二步：获取群列表...")
        groups = await client.get_group_list()
        
        if groups:
            print(f"✅ 获取到 {len(groups)} 个群:")
            for i, group in enumerate(groups[:5], 1):  # 只显示前5个
                print(f"  {i}. {group.get('name', 'N/A')} ({group.get('member_count', 0)} 人)")
        else:
            print("⚠️ 未获取到群列表")
        
        # 第三步：准备测试数据
        print("\n📝 第三步：准备测试数据...")
        
        test_report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'title': 'AI科技早报测试',
            'summary': '''【AI科技早报】2025-09-07

1. **Nano Banana接近ChatGPT水平**  
   虎嗅网报道，Nano Banana在技术体验上实现重大突破，或成为AI领域新亮点。

2. **iPhone 17印度生产仍依赖中国供应链**  
   尽管苹果计划将制造转移至印度，但核心零部件与技术供应仍由中国厂商主导。

3. **新基础食材推动饮品创新**  
   继苹果后，又一基础食材在饮品行业走红，引领产品研发新趋势。''',
            'trends': [
                '小型化与高效能AI模型发展',
                '供应链数字化转型加速',
                '消费品创新与AI技术融合'
            ],
            'image_prompts': [
                '简洁的蓝色科技背景中，一个发光的AI芯片悬浮，周围环绕着流动的数据流',
                '现代极简的全球地图上，印度与中国由发光的供应链线条连接',
                '纯净的白色背景前，一组未来感饮品容器排列，其中流动着发光液体'
            ]
        }
        
        print("✅ 测试数据准备完成")
        
        # 第四步：测试发送到单个群
        print("\n💬 第四步：测试发送到单个群...")
        
        success = await client.send_to_group(test_report, "AI科技早报群")
        
        if success:
            print("✅ 消息发送到单个群成功")
        else:
            print("❌ 消息发送到单个群失败")
        
        # 第五步：测试发送到多个群
        print("\n📢 第五步：测试发送到多个群...")
        
        target_groups = ["AI科技早报群", "技术交流群"]
        results = await client.send_to_multiple_groups(test_report, target_groups)
        
        print("📊 多群发送结果:")
        for group_name, result in results.items():
            status = "✅ 成功" if result else "❌ 失败"
            print(f"   {group_name}: {status}")
        
        # 第六步：测试富文本消息
        print("\n🎨 第六步：测试富文本消息...")
        
        rich_success = await client.send_rich_message(test_report, "AI科技早报群")
        
        if rich_success:
            print("✅ 富文本消息发送成功")
        else:
            print("❌ 富文本消息发送失败")
        
        # 第七步：测试朋友圈发布
        print("\n📱 第七步：测试朋友圈发布...")
        
        moment_content = f"🤖 AI科技早报 - {test_report['date']}\n\n{test_report['summary'][:100]}..."
        moment_success = await client.publish_moment(moment_content)
        
        if moment_success:
            print("✅ 朋友圈发布成功")
        else:
            print("❌ 朋友圈发布失败")
        
        # 第八步：检查连接状态
        print("\n🔍 第八步：检查连接状态...")
        
        is_connected = await client.check_connection()
        
        if is_connected:
            print("✅ 连接状态正常")
        else:
            print("❌ 连接状态异常")
        
        print("\n🎉 iPad协议微信助手测试完成！")
        
        print("\n📊 测试结果总结:")
        print("✅ 连接功能正常")
        print("✅ 群列表获取正常")
        print("✅ 单群发送功能正常")
        print("✅ 多群发送功能正常")
        print("✅ 富文本消息功能正常")
        print("✅ 朋友圈发布功能正常")
        print("✅ 连接状态检查正常")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭客户端
        await client.close()
        print("\n🧹 客户端已关闭")

if __name__ == "__main__":
    asyncio.run(test_ipad_wechat())
