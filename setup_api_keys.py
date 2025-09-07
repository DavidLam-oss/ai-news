#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥配置脚本
"""

import os
from pathlib import Path

def setup_api_keys():
    """设置API密钥"""
    print("🔑 AI早报系统 - API密钥配置")
    print("=" * 50)
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env文件不存在，请先运行部署脚本")
        return
    
    print("📝 请配置以下API密钥：")
    print()
    
    # 读取当前配置
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # DeepSeek API密钥
    current_deepseek = "your_deepseek_api_key"
    if current_deepseek in content:
        print("🤖 DeepSeek API密钥配置：")
        deepseek_key = input("请输入你的DeepSeek API密钥 (或按回车跳过): ").strip()
        if deepseek_key:
            content = content.replace(current_deepseek, deepseek_key)
            print("✅ DeepSeek API密钥已配置")
        else:
            print("⚠️ 跳过DeepSeek API密钥配置")
    
    # 飞书配置
    current_feishu_app_id = "your_feishu_app_id"
    if current_feishu_app_id in content:
        print("\n📊 飞书配置 (可选)：")
        feishu_app_id = input("请输入飞书App ID (或按回车跳过): ").strip()
        if feishu_app_id:
            content = content.replace(current_feishu_app_id, feishu_app_id)
            print("✅ 飞书App ID已配置")
        
        feishu_app_secret = input("请输入飞书App Secret (或按回车跳过): ").strip()
        if feishu_app_secret:
            content = content.replace("your_feishu_app_secret", feishu_app_secret)
            print("✅ 飞书App Secret已配置")
    
    # 微信相关功能已下线（风险规避）
    
    # 保存配置
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 配置完成！")
    print("📋 下一步：")
    print("1. 重启API服务: Ctrl+C 然后重新运行 uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload")
    print("2. 测试爬虫: curl 'http://localhost:8000/api/news?max_articles=3'")
    print("3. 查看API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    setup_api_keys()
