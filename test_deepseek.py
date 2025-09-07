#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试火山方舟DeepSeek API
"""

import asyncio
import openai
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

async def test_volcano_deepseek():
    """测试火山方舟DeepSeek API"""
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 未找到DEEPSEEK_API_KEY环境变量")
        return
    
    print(f"🔑 API Key: {api_key[:10]}...")
    
    try:
        # 创建客户端
        client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        
        print("🚀 正在测试火山方舟DeepSeek API...")
        
        # 发送测试请求
        response = await client.chat.completions.create(
            model="ep-20250823010411-p5fnv",
            messages=[
                {"role": "system", "content": "你是一个专业的AI科技早报编辑，擅长将复杂的科技新闻整理成简洁易懂的早报。"},
                {"role": "user", "content": "请将以下AI科技新闻整理成一份简洁的早报摘要：\n\n1. OpenAI发布GPT-4 Turbo模型，性能大幅提升\n2. Google推出Gemini AI模型，多模态能力突出\n3. Meta发布Llama 3模型，开源AI竞争加剧"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        print("✅ API调用成功！")
        print("📝 响应内容：")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_volcano_deepseek())

