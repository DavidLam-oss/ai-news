#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的模拟iPad协议微信助手服务
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Mock iPad WeChat Service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/webhook")
async def webhook(data: dict):
    print(f"📨 收到webhook请求: {data}")
    
    action = data.get("action", "")
    
    if action == "ping":
        return {
            "success": True,
            "message": "连接成功",
            "session_id": "session_123456"
        }
    else:
        return {
            "success": True,
            "message": f"处理 {action} 成功"
        }

if __name__ == "__main__":
    print("🚀 启动简化模拟服务...")
    uvicorn.run(app, host="0.0.0.0", port=8081)
