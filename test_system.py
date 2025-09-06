#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI早报系统测试脚本
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from crawler.news_sources import NewsSources
from crawler.content_processor import ContentProcessor

async def test_news_sources():
    """测试新闻源配置"""
    print("🔍 测试新闻源配置...")
    
    try:
        news_sources = NewsSources()
        sources = news_sources.get_sources()
        
        print(f"✅ 找到 {len(sources)} 个新闻源")
        
        # 验证配置
        errors = news_sources.validate_sources()
        if errors:
            print("❌ 新闻源配置错误:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ 新闻源配置验证通过")
        
        # 显示新闻源列表
        print("\n📰 新闻源列表:")
        for source in sources:
            print(f"   - {source['name']} ({source['category']}) - {source['url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 新闻源测试失败: {e}")
        return False

async def test_content_processor():
    """测试内容处理器"""
    print("\n🤖 测试内容处理器...")
    
    try:
        if not settings.OPENAI_API_KEY:
            print("⚠️  未配置OpenAI API密钥，跳过AI处理测试")
            return True
        
        processor = ContentProcessor()
        
        # 模拟文章数据
        test_articles = [
            {
                "title": "OpenAI发布GPT-4 Turbo模型",
                "summary": "OpenAI发布了新的GPT-4 Turbo模型，性能大幅提升",
                "source": "测试源",
                "url": "https://example.com/1",
                "publish_time": "2024-01-15T10:00:00Z"
            },
            {
                "title": "Google推出Gemini AI模型",
                "summary": "Google发布了新的Gemini AI模型，在多模态任务上表现优异",
                "source": "测试源",
                "url": "https://example.com/2",
                "publish_time": "2024-01-15T11:00:00Z"
            }
        ]
        
        print("📝 测试AI内容处理...")
        result = await processor.process_articles(test_articles)
        
        print("✅ AI内容处理测试通过")
        print(f"   - 摘要长度: {len(result['summary'])} 字符")
        print(f"   - 趋势数量: {len(result['trends'])}")
        print(f"   - 图片提示词数量: {len(result['image_prompts'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 内容处理器测试失败: {e}")
        return False

async def test_feishu_client():
    """测试飞书客户端"""
    print("\n📊 测试飞书客户端...")
    
    try:
        if not settings.FEISHU_APP_ID or not settings.FEISHU_APP_SECRET:
            print("⚠️  未配置飞书应用凭证，跳过飞书测试")
            return True
        
        from feishu.client import FeishuClient
        
        client = FeishuClient()
        
        # 测试获取访问令牌
        print("🔑 测试获取访问令牌...")
        token = await client.get_access_token()
        
        if token:
            print("✅ 飞书访问令牌获取成功")
        else:
            print("❌ 飞书访问令牌获取失败")
            return False
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 飞书客户端测试失败: {e}")
        return False

async def test_wechat_client():
    """测试微信客户端"""
    print("\n💬 测试微信客户端...")
    
    try:
        if not settings.WECHAT_APP_ID or not settings.WECHAT_APP_SECRET:
            print("⚠️  未配置微信应用凭证，跳过微信测试")
            return True
        
        from wechat.client import WechatClient
        
        client = WechatClient()
        
        # 测试获取访问令牌
        print("🔑 测试获取微信访问令牌...")
        token = await client.get_access_token()
        
        if token:
            print("✅ 微信访问令牌获取成功")
        else:
            print("❌ 微信访问令牌获取失败")
            return False
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 微信客户端测试失败: {e}")
        return False

async def test_api_server():
    """测试API服务器"""
    print("\n🌐 测试API服务器...")
    
    try:
        import httpx
        
        # 测试健康检查接口
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            
            if response.status_code == 200:
                print("✅ API服务器健康检查通过")
                return True
            else:
                print(f"❌ API服务器健康检查失败: {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print("⚠️  API服务器未运行，请先启动服务")
        return False
    except Exception as e:
        print(f"❌ API服务器测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 AI早报系统测试开始\n")
    
    tests = [
        ("新闻源配置", test_news_sources),
        ("内容处理器", test_content_processor),
        ("飞书客户端", test_feishu_client),
        ("微信客户端", test_wechat_client),
        ("API服务器", test_api_server)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n📋 测试结果汇总:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统配置正确。")
    else:
        print("⚠️  部分测试失败，请检查配置。")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())
