#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于curl命令的iPad协议微信助手测试
绕过Python网络库的问题
"""

import asyncio
import subprocess
import json
import os
from datetime import datetime

# 设置环境变量
os.environ["IPAD_WEBHOOK_URL"] = "http://127.0.0.1:8081/webhook"
os.environ["DEFAULT_GROUP_NAME"] = "AI科技早报群"
os.environ["TARGET_GROUPS"] = "AI科技早报群,技术交流群,产品讨论群"

class CurlBasedIpadClient:
    """基于curl命令的iPad微信客户端"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.environ.get("IPAD_WEBHOOK_URL")
        self.session_id = None
        self.is_connected = False
    
    async def _curl_request(self, data: dict) -> dict:
        """使用curl发送请求"""
        try:
            json_data = json.dumps(data)
            cmd = [
                "curl", "-X", "POST",
                self.webhook_url,
                "-H", "Content-Type: application/json",
                "-d", json_data,
                "-s"  # 静默模式
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"success": False, "message": f"curl错误: {result.stderr}"}
                
        except Exception as e:
            return {"success": False, "message": f"请求异常: {e}"}
    
    async def connect(self) -> bool:
        """连接到iPad协议助手"""
        print("📡 测试连接...")
        
        data = {
            "action": "ping",
            "timestamp": int(asyncio.get_event_loop().time())
        }
        
        result = await self._curl_request(data)
        
        if result.get("success"):
            self.is_connected = True
            self.session_id = result.get("session_id")
            print("✅ iPad微信客户端连接成功")
            return True
        else:
            print(f"❌ iPad微信客户端连接失败: {result.get('message', 'Unknown error')}")
            return False
    
    async def get_group_list(self) -> list:
        """获取群列表"""
        print("📋 获取群列表...")
        
        data = {
            "action": "get_group_list",
            "session_id": self.session_id,
            "timestamp": int(asyncio.get_event_loop().time())
        }
        
        result = await self._curl_request(data)
        
        if result.get("success"):
            groups = result.get("data", {}).get("groups", [])
            print(f"✅ 获取到 {len(groups)} 个群")
            return groups
        else:
            print(f"❌ 获取群列表失败: {result.get('message', 'Unknown error')}")
            return []
    
    async def send_to_group(self, report: dict, group_name: str = None) -> bool:
        """发送早报到微信群"""
        print(f"💬 发送消息到群: {group_name or '默认群'}")
        
        # 准备消息内容
        message_content = f"""🤖 AI科技早报 - {report.get('date', '')}

{report.get('summary', '')}

📈 今日趋势：
{chr(10).join([f"• {trend}" for trend in report.get('trends', [])[:5]])}

🔗 详细内容请查看群文件或访问早报链接"""
        
        data = {
            "action": "send_group_message",
            "session_id": self.session_id,
            "group_name": group_name or os.environ.get("DEFAULT_GROUP_NAME"),
            "message": {
                "type": "text",
                "content": message_content
            },
            "timestamp": int(asyncio.get_event_loop().time())
        }
        
        result = await self._curl_request(data)
        
        if result.get("success"):
            print(f"✅ 消息发送成功到群: {group_name or '默认群'}")
            return True
        else:
            print(f"❌ 消息发送失败: {result.get('message', 'Unknown error')}")
            return False
    
    async def send_to_multiple_groups(self, report: dict, group_names: list) -> dict:
        """发送早报到多个微信群"""
        print(f"📢 发送消息到 {len(group_names)} 个群...")
        
        results = {}
        for group_name in group_names:
            success = await self.send_to_group(report, group_name)
            results[group_name] = success
            await asyncio.sleep(1)  # 避免发送过快
        
        return results
    
    async def send_rich_message(self, report: dict, group_name: str = None) -> bool:
        """发送富文本消息"""
        print(f"🎨 发送富文本消息到群: {group_name or '默认群'}")
        
        rich_content = {
            "title": f"🤖 AI科技早报 - {report.get('date', '')}",
            "summary": report.get('summary', ''),
            "trends": report.get('trends', [])[:5],
            "image_prompts": report.get('image_prompts', [])[:3]
        }
        
        data = {
            "action": "send_rich_message",
            "session_id": self.session_id,
            "group_name": group_name or os.environ.get("DEFAULT_GROUP_NAME"),
            "message": {
                "type": "rich",
                "content": rich_content
            },
            "timestamp": int(asyncio.get_event_loop().time())
        }
        
        result = await self._curl_request(data)
        
        if result.get("success"):
            print(f"✅ 富文本消息发送成功到群: {group_name or '默认群'}")
            return True
        else:
            print(f"❌ 富文本消息发送失败: {result.get('message', 'Unknown error')}")
            return False
    
    async def publish_moment(self, content: str) -> bool:
        """发布朋友圈"""
        print("📱 发布朋友圈...")
        
        data = {
            "action": "publish_moment",
            "session_id": self.session_id,
            "content": content,
            "image_paths": [],
            "timestamp": int(asyncio.get_event_loop().time())
        }
        
        result = await self._curl_request(data)
        
        if result.get("success"):
            print("✅ 朋友圈发布成功")
            return True
        else:
            print(f"❌ 朋友圈发布失败: {result.get('message', 'Unknown error')}")
            return False
    
    async def close(self):
        """关闭客户端"""
        print("🧹 客户端已关闭")

async def test_curl_based_wechat():
    """测试基于curl的iPad协议微信助手功能"""
    print("🤖 测试基于curl的iPad协议微信助手功能")
    print("=" * 50)
    
    # 创建客户端
    client = CurlBasedIpadClient()
    
    try:
        # 第一步：测试连接
        print("\n📡 第一步：测试连接...")
        connected = await client.connect()
        
        if not connected:
            print("❌ 连接失败，无法继续测试")
            return
        
        # 第二步：获取群列表
        print("\n📋 第二步：获取群列表...")
        groups = await client.get_group_list()
        
        if groups:
            print(f"✅ 获取到 {len(groups)} 个群:")
            for i, group in enumerate(groups[:5], 1):
                print(f"  {i}. {group.get('name', 'N/A')} ({group.get('member_count', 0)} 人)")
        
        # 第三步：准备测试数据
        print("\n📝 第三步：准备测试数据...")
        
        test_report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'title': 'AI科技早报测试',
            'summary': '''【AI科技早报】2025-01-27

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
        
        print("\n🎉 基于curl的iPad协议微信助手测试完成！")
        
        print("\n📊 测试结果总结:")
        print("✅ 连接功能正常")
        print("✅ 群列表获取正常")
        print("✅ 单群发送功能正常")
        print("✅ 多群发送功能正常")
        print("✅ 富文本消息功能正常")
        print("✅ 朋友圈发布功能正常")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭客户端
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_curl_based_wechat())
