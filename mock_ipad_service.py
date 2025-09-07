#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地模拟iPad协议微信助手服务
用于测试和开发环境
"""

import json
import asyncio
import time
import random
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock iPad WeChat Service", version="1.0.0")

# 模拟数据
MOCK_GROUPS = [
    {"name": "AI科技早报群", "member_count": 25, "id": "group_001"},
    {"name": "技术交流群", "member_count": 18, "id": "group_002"},
    {"name": "产品讨论群", "member_count": 12, "id": "group_003"},
    {"name": "开发者社区", "member_count": 35, "id": "group_004"},
    {"name": "AI学习群", "member_count": 28, "id": "group_005"}
]

MOCK_MEMBERS = [
    {"name": "张三", "id": "user_001", "role": "admin"},
    {"name": "李四", "id": "user_002", "role": "member"},
    {"name": "王五", "id": "user_003", "role": "member"},
    {"name": "赵六", "id": "user_004", "role": "member"}
]

# 请求模型
class WebhookRequest(BaseModel):
    action: str
    session_id: str = None
    group_name: str = None
    user_name: str = None
    message: Dict[str, Any] = None
    content: str = None
    image_paths: List[str] = None
    timestamp: int = None

# 响应模型
class WebhookResponse(BaseModel):
    success: bool
    message: str = ""
    data: Dict[str, Any] = {}
    session_id: str = None

@app.post("/webhook", response_model=WebhookResponse)
async def webhook_handler(request: WebhookRequest):
    """处理webhook请求"""
    try:
        print(f"📨 收到请求: {request.action}")
        print(f"📊 请求数据: {request.dict()}")
        
        # 根据action类型处理请求
        if request.action == "ping":
            return await handle_ping(request)
        elif request.action == "send_group_message":
            return await handle_send_group_message(request)
        elif request.action == "send_rich_message":
            return await handle_send_rich_message(request)
        elif request.action == "send_image_with_text":
            return await handle_send_image_with_text(request)
        elif request.action == "get_group_list":
            return await handle_get_group_list(request)
        elif request.action == "get_group_members":
            return await handle_get_group_members(request)
        elif request.action == "send_private_message":
            return await handle_send_private_message(request)
        elif request.action == "publish_moment":
            return await handle_publish_moment(request)
        elif request.action == "check_status":
            return await handle_check_status(request)
        elif request.action == "disconnect":
            return await handle_disconnect(request)
        else:
            return WebhookResponse(
                success=False,
                message=f"未知的action: {request.action}"
            )
            
    except Exception as e:
        print(f"❌ 处理请求时发生错误: {e}")
        return WebhookResponse(
            success=False,
            message=f"服务器内部错误: {str(e)}"
        )

async def handle_ping(request: WebhookRequest) -> WebhookResponse:
    """处理ping请求"""
    session_id = f"session_{int(time.time())}"
    print(f"✅ Ping成功，生成session_id: {session_id}")
    
    return WebhookResponse(
        success=True,
        message="连接成功",
        session_id=session_id
    )

async def handle_send_group_message(request: WebhookRequest) -> WebhookResponse:
    """处理发送群消息请求"""
    group_name = request.group_name or "默认群"
    message_content = request.message.get("content", "") if request.message else ""
    
    print(f"📤 发送群消息到: {group_name}")
    print(f"📝 消息内容: {message_content[:100]}...")
    
    # 模拟发送延迟
    await asyncio.sleep(0.5)
    
    # 模拟90%成功率
    success = random.random() > 0.1
    
    if success:
        print(f"✅ 消息发送成功到群: {group_name}")
        return WebhookResponse(
            success=True,
            message=f"消息已发送到群: {group_name}",
            data={"group_name": group_name, "message_id": f"msg_{int(time.time())}"}
        )
    else:
        print(f"❌ 消息发送失败到群: {group_name}")
        return WebhookResponse(
            success=False,
            message=f"发送到群 {group_name} 失败"
        )

async def handle_send_rich_message(request: WebhookRequest) -> WebhookResponse:
    """处理发送富文本消息请求"""
    group_name = request.group_name or "默认群"
    rich_content = request.message.get("content", {}) if request.message else {}
    
    print(f"🎨 发送富文本消息到: {group_name}")
    print(f"📊 富文本内容: {rich_content}")
    
    # 模拟发送延迟
    await asyncio.sleep(1.0)
    
    print(f"✅ 富文本消息发送成功到群: {group_name}")
    return WebhookResponse(
        success=True,
        message=f"富文本消息已发送到群: {group_name}",
        data={"group_name": group_name, "message_id": f"rich_msg_{int(time.time())}"}
    )

async def handle_send_image_with_text(request: WebhookRequest) -> WebhookResponse:
    """处理发送图片和文字消息请求"""
    group_name = request.group_name or "默认群"
    image_path = request.message.get("image_path", "") if request.message else ""
    text = request.message.get("text", "") if request.message else ""
    
    print(f"🖼️ 发送图片和文字到: {group_name}")
    print(f"📷 图片路径: {image_path}")
    print(f"📝 文字内容: {text[:50]}...")
    
    # 模拟发送延迟
    await asyncio.sleep(1.5)
    
    print(f"✅ 图片和文字消息发送成功到群: {group_name}")
    return WebhookResponse(
        success=True,
        message=f"图片和文字消息已发送到群: {group_name}",
        data={"group_name": group_name, "message_id": f"img_msg_{int(time.time())}"}
    )

async def handle_get_group_list(request: WebhookRequest) -> WebhookResponse:
    """处理获取群列表请求"""
    print("📋 获取群列表")
    
    # 模拟网络延迟
    await asyncio.sleep(0.3)
    
    print(f"✅ 返回 {len(MOCK_GROUPS)} 个群")
    return WebhookResponse(
        success=True,
        message=f"获取到 {len(MOCK_GROUPS)} 个群",
        data={"groups": MOCK_GROUPS}
    )

async def handle_get_group_members(request: WebhookRequest) -> WebhookResponse:
    """处理获取群成员请求"""
    group_name = request.group_name or "默认群"
    
    print(f"👥 获取群成员: {group_name}")
    
    # 模拟网络延迟
    await asyncio.sleep(0.3)
    
    print(f"✅ 返回 {len(MOCK_MEMBERS)} 个成员")
    return WebhookResponse(
        success=True,
        message=f"群 {group_name} 有 {len(MOCK_MEMBERS)} 个成员",
        data={"members": MOCK_MEMBERS}
    )

async def handle_send_private_message(request: WebhookRequest) -> WebhookResponse:
    """处理发送私聊消息请求"""
    user_name = request.user_name or "未知用户"
    message_content = request.message.get("content", "") if request.message else ""
    
    print(f"💬 发送私聊消息给: {user_name}")
    print(f"📝 消息内容: {message_content[:50]}...")
    
    # 模拟发送延迟
    await asyncio.sleep(0.5)
    
    print(f"✅ 私聊消息发送成功给: {user_name}")
    return WebhookResponse(
        success=True,
        message=f"私聊消息已发送给: {user_name}",
        data={"user_name": user_name, "message_id": f"private_msg_{int(time.time())}"}
    )

async def handle_publish_moment(request: WebhookRequest) -> WebhookResponse:
    """处理发布朋友圈请求"""
    content = request.content or ""
    image_paths = request.image_paths or []
    
    print(f"📱 发布朋友圈")
    print(f"📝 内容: {content[:50]}...")
    print(f"🖼️ 图片数量: {len(image_paths)}")
    
    # 模拟发布延迟
    await asyncio.sleep(2.0)
    
    print("✅ 朋友圈发布成功")
    return WebhookResponse(
        success=True,
        message="朋友圈发布成功",
        data={"moment_id": f"moment_{int(time.time())}"}
    )

async def handle_check_status(request: WebhookRequest) -> WebhookResponse:
    """处理检查状态请求"""
    print("🔍 检查连接状态")
    
    # 模拟状态检查
    await asyncio.sleep(0.1)
    
    print("✅ 连接状态正常")
    return WebhookResponse(
        success=True,
        message="连接状态正常",
        data={"status": "connected", "timestamp": int(time.time())}
    )

async def handle_disconnect(request: WebhookRequest) -> WebhookResponse:
    """处理断开连接请求"""
    print("🔌 断开连接")
    
    print("✅ 连接已断开")
    return WebhookResponse(
        success=True,
        message="连接已断开"
    )

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "Mock iPad WeChat Service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mock_groups": len(MOCK_GROUPS),
        "mock_members": len(MOCK_MEMBERS)
    }

if __name__ == "__main__":
    print("🚀 启动模拟iPad协议微信助手服务...")
    print("📡 服务地址: http://localhost:8080")
    print("🔗 Webhook地址: http://localhost:8080/webhook")
    print("📋 健康检查: http://localhost:8080/health")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
