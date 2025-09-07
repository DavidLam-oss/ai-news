#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书配置设置脚本
"""

import os
import shutil
from pathlib import Path

def setup_feishu_config():
    """设置飞书配置"""
    print("🔧 开始设置飞书配置...")
    
    # 飞书配置信息
    feishu_config = {
        "FEISHU_APP_ID": "cli_a8366b7ef13a100c",
        "FEISHU_APP_SECRET": "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr",
        "FEISHU_BASE_URL": "https://open.feishu.cn/open-apis",
        "FEISHU_TABLE_TOKEN": "your_table_token"  # 需要用户后续配置
    }
    
    # 检查是否存在 .env 文件
    env_file = Path(".env")
    env_example_file = Path("config.env.example")
    
    if env_file.exists():
        print("📄 发现现有的 .env 文件")
        backup_file = Path(".env.backup")
        shutil.copy2(env_file, backup_file)
        print(f"💾 已备份到 {backup_file}")
    else:
        print("📄 未发现 .env 文件，将创建新文件")
    
    # 读取现有的 .env 文件内容（如果存在）
    existing_content = ""
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 准备新的配置内容
    new_content = []
    lines = existing_content.split('\n') if existing_content else []
    
    # 处理现有内容
    feishu_keys = set(feishu_config.keys())
    for line in lines:
        if line.strip() and not line.startswith('#'):
            key = line.split('=')[0].strip()
            if key in feishu_keys:
                # 更新飞书配置
                new_content.append(f"{key}={feishu_config[key]}")
                feishu_keys.remove(key)
            else:
                # 保留其他配置
                new_content.append(line)
        else:
            # 保留注释和空行
            new_content.append(line)
    
    # 添加新的飞书配置
    if feishu_keys:
        if new_content and new_content[-1].strip():
            new_content.append("")  # 添加空行分隔
        new_content.append("# 飞书配置")
        for key in sorted(feishu_keys):
            new_content.append(f"{key}={feishu_config[key]}")
    
    # 写入 .env 文件
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_content))
        print("✅ .env 文件配置完成")
    except Exception as e:
        print(f"❌ 写入 .env 文件失败: {e}")
        return False
    
    # 显示配置信息
    print("\n📋 飞书配置信息:")
    print(f"   APP ID: {feishu_config['FEISHU_APP_ID']}")
    print(f"   APP SECRET: {feishu_config['FEISHU_APP_SECRET'][:10]}...")
    print(f"   BASE URL: {feishu_config['FEISHU_BASE_URL']}")
    print(f"   TABLE TOKEN: {feishu_config['FEISHU_TABLE_TOKEN']}")
    
    print("\n💡 下一步操作:")
    print("   1. 在飞书多维表格中获取表格token")
    print("   2. 将表格token配置到 .env 文件中的 FEISHU_TABLE_TOKEN")
    print("   3. 运行测试脚本验证配置: python3 test_feishu_config.py")
    
    return True

def test_config():
    """测试配置"""
    print("\n🧪 测试飞书配置...")
    
    # 设置环境变量
    os.environ["FEISHU_APP_ID"] = "cli_a8366b7ef13a100c"
    os.environ["FEISHU_APP_SECRET"] = "5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
    os.environ["FEISHU_BASE_URL"] = "https://open.feishu.cn/open-apis"
    
    try:
        from feishu.client import FeishuClient
        import asyncio
        
        async def test():
            client = FeishuClient()
            try:
                access_token = await client.get_access_token()
                if access_token:
                    print("✅ 飞书配置测试成功！")
                    print(f"🔑 访问令牌: {access_token[:20]}...")
                    return True
                else:
                    print("❌ 飞书配置测试失败")
                    return False
            finally:
                await client.close()
        
        return asyncio.run(test())
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 飞书配置设置工具")
    print("=" * 50)
    
    # 设置配置
    if setup_feishu_config():
        # 测试配置
        if test_config():
            print("\n🎉 飞书配置完成并测试成功！")
        else:
            print("\n⚠️  配置完成但测试失败，请检查网络连接和权限设置")
    else:
        print("\n❌ 配置设置失败")
