#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书权限申请工具
"""

import webbrowser
import os
from pathlib import Path

def generate_permission_links():
    """生成权限申请链接"""
    
    # 应用信息
    app_id = "cli_a8366b7ef13a100c"
    
    # 必需权限列表
    required_permissions = [
        "bitable:app:readonly",  # 多维表格应用只读权限
        "bitable:app",           # 多维表格应用权限
        "base:app:read",         # 基础应用读取权限
        "base:table:read",       # 基础表格读取权限
        "base:record:retrieve",  # 基础记录检索权限
        "base:record:create",    # 基础记录创建权限
        "base:record:update",    # 基础记录更新权限
    ]
    
    # 可选权限列表
    optional_permissions = [
        "base:record:delete",    # 基础记录删除权限
        "base:field:read",       # 基础字段读取权限
        "base:field:create",     # 基础字段创建权限
    ]
    
    print("🚀 飞书权限申请工具")
    print("=" * 50)
    print(f"📱 应用ID: {app_id}")
    print(f"📋 应用名称: AI早报系统")
    
    # 生成权限申请链接
    required_permissions_str = ",".join(required_permissions)
    optional_permissions_str = ",".join(optional_permissions)
    all_permissions_str = ",".join(required_permissions + optional_permissions)
    
    # 必需权限申请链接
    required_link = f"https://open.feishu.cn/app/{app_id}/auth?q={required_permissions_str}&op_from=openapi&token_type=tenant"
    
    # 所有权限申请链接
    all_link = f"https://open.feishu.cn/app/{app_id}/auth?q={all_permissions_str}&op_from=openapi&token_type=tenant"
    
    print(f"\n📝 权限申请链接:")
    print(f"   必需权限: {required_link}")
    print(f"   所有权限: {all_link}")
    
    return required_link, all_link

def open_permission_links():
    """打开权限申请链接"""
    required_link, all_link = generate_permission_links()
    
    print(f"\n🌐 正在打开权限申请页面...")
    
    try:
        # 打开必需权限申请页面
        webbrowser.open(required_link)
        print("✅ 已打开必需权限申请页面")
        
        # 询问是否打开所有权限页面
        choice = input("\n是否同时申请可选权限？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            webbrowser.open(all_link)
            print("✅ 已打开所有权限申请页面")
        
    except Exception as e:
        print(f"❌ 打开浏览器失败: {e}")
        print("💡 请手动复制以下链接到浏览器:")
        print(f"   必需权限: {required_link}")
        print(f"   所有权限: {all_link}")

def create_permission_checklist():
    """创建权限检查清单"""
    checklist_content = """
# 飞书权限配置检查清单

## 必需权限
- [ ] bitable:app:readonly - 多维表格应用只读权限
- [ ] bitable:app - 多维表格应用权限
- [ ] base:app:read - 基础应用读取权限
- [ ] base:table:read - 基础表格读取权限
- [ ] base:record:retrieve - 基础记录检索权限
- [ ] base:record:create - 基础记录创建权限
- [ ] base:record:update - 基础记录更新权限

## 可选权限
- [ ] base:record:delete - 基础记录删除权限
- [ ] base:field:read - 基础字段读取权限
- [ ] base:field:create - 基础字段创建权限

## 发布步骤
- [ ] 权限申请完成
- [ ] 创建新版本
- [ ] 填写版本信息
- [ ] 申请发布
- [ ] 管理员审核通过
- [ ] 权限测试通过

## 测试命令
```bash
# 测试权限配置
python3 test_feishu_tokens.py

# 测试完整功能
python3 test_feishu_config.py
```
"""
    
    checklist_file = Path("FEISHU_PERMISSION_CHECKLIST.md")
    with open(checklist_file, 'w', encoding='utf-8') as f:
        f.write(checklist_content)
    
    print(f"✅ 已创建权限检查清单: {checklist_file}")

def show_manual_steps():
    """显示手动配置步骤"""
    print(f"\n📋 手动配置步骤:")
    print(f"   1. 登录飞书开放平台: https://open.feishu.cn/")
    print(f"   2. 进入应用管理后台")
    print(f"   3. 选择应用: cli_a8366b7ef13a100c")
    print(f"   4. 点击'权限管理'")
    print(f"   5. 点击'申请权限'")
    print(f"   6. 搜索并添加以下权限:")
    
    permissions = [
        "bitable:app:readonly",
        "bitable:app", 
        "base:app:read",
        "base:table:read",
        "base:record:retrieve",
        "base:record:create",
        "base:record:update"
    ]
    
    for i, perm in enumerate(permissions, 1):
        print(f"      {i}. {perm}")
    
    print(f"   7. 创建新版本并发布")
    print(f"   8. 等待管理员审核")
    print(f"   9. 运行测试脚本验证")

def main():
    """主函数"""
    print("🔧 飞书权限配置助手")
    print("=" * 50)
    
    # 生成权限链接
    required_link, all_link = generate_permission_links()
    
    # 创建检查清单
    create_permission_checklist()
    
    # 显示选项
    print(f"\n🎯 请选择操作:")
    print(f"   1. 自动打开权限申请页面")
    print(f"   2. 显示手动配置步骤")
    print(f"   3. 显示权限申请链接")
    print(f"   4. 退出")
    
    while True:
        choice = input(f"\n请输入选项 (1-4): ").strip()
        
        if choice == "1":
            open_permission_links()
            break
        elif choice == "2":
            show_manual_steps()
            break
        elif choice == "3":
            print(f"\n📋 权限申请链接:")
            print(f"   必需权限: {required_link}")
            print(f"   所有权限: {all_link}")
            break
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重新输入")
    
    print(f"\n💡 提示:")
    print(f"   - 权限申请完成后，请运行测试脚本验证")
    print(f"   - 如有问题，请查看 FEISHU_PERMISSION_GUIDE.md")
    print(f"   - 检查清单已保存到 FEISHU_PERMISSION_CHECKLIST.md")

if __name__ == "__main__":
    main()
