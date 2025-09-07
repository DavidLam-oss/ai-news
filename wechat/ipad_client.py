#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于iPad协议的微信助手客户端
稳定可靠，避免被封号风险
"""

import json
import asyncio
import time
from typing import Dict, Any, List, Optional
import httpx
from loguru import logger
from datetime import datetime

from config.settings import settings, WECHAT_TEMPLATES

class IpadWechatClient:
    """基于iPad协议的微信助手客户端"""
    
    def __init__(self, webhook_url: str = None):
        """
        初始化iPad微信客户端
        
        Args:
            webhook_url: iPad协议助手的webhook地址
        """
        self.webhook_url = webhook_url or settings.IPAD_WEBHOOK_URL
        self.session_id = None
        self.is_connected = False
        
        # HTTP客户端
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AI-News-System/1.0"
            }
        )
        
        logger.info("iPad微信客户端初始化完成")
    
    async def connect(self) -> bool:
        """连接到iPad协议助手"""
        try:
            if not self.webhook_url:
                logger.error("未配置iPad协议助手的webhook地址")
                return False
            
            # 测试连接
            test_data = {
                "action": "ping",
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=test_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                self.is_connected = True
                self.session_id = result.get("session_id")
                logger.info("iPad微信客户端连接成功")
                return True
            else:
                logger.error(f"iPad微信客户端连接失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"连接iPad微信客户端时发生错误: {e}")
            return False
    
    async def send_to_group(self, report: Dict[str, Any], group_name: str = None) -> bool:
        """
        发送早报到微信群
        
        Args:
            report: 早报数据
            group_name: 群名称，如果为None则发送到默认群
        """
        try:
            if not self.is_connected:
                await self.connect()
            
            # 准备消息内容
            message_content = WECHAT_TEMPLATES['group_message'].format(
                date=report.get('date', ''),
                summary=report.get('summary', ''),
                trends='\n'.join([f"• {trend}" for trend in report.get('trends', [])[:5]])
            )
            
            # 构建发送数据
            send_data = {
                "action": "send_group_message",
                "session_id": self.session_id,
                "group_name": group_name or settings.DEFAULT_GROUP_NAME,
                "message": {
                    "type": "text",
                    "content": message_content
                },
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                logger.info(f"早报已发送到微信群: {group_name or '默认群'}")
                return True
            else:
                logger.error(f"发送到微信群失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送到微信群时发生错误: {e}")
            return False
    
    async def send_to_multiple_groups(self, report: Dict[str, Any], group_names: List[str]) -> Dict[str, bool]:
        """
        发送早报到多个微信群
        
        Args:
            report: 早报数据
            group_names: 群名称列表
            
        Returns:
            Dict[str, bool]: 每个群的发送结果
        """
        results = {}
        
        for group_name in group_names:
            try:
                success = await self.send_to_group(report, group_name)
                results[group_name] = success
                
                # 避免发送过快，添加延迟
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"发送到群 {group_name} 时发生错误: {e}")
                results[group_name] = False
        
        return results
    
    async def send_rich_message(self, report: Dict[str, Any], group_name: str = None) -> bool:
        """
        发送富文本消息（包含图片和文字）
        
        Args:
            report: 早报数据
            group_name: 群名称
        """
        try:
            if not self.is_connected:
                await self.connect()
            
            # 准备富文本消息
            rich_content = {
                "title": f"🤖 AI科技早报 - {report.get('date', '')}",
                "summary": report.get('summary', ''),
                "trends": report.get('trends', [])[:5],
                "image_prompts": report.get('image_prompts', [])[:3]
            }
            
            send_data = {
                "action": "send_rich_message",
                "session_id": self.session_id,
                "group_name": group_name or settings.DEFAULT_GROUP_NAME,
                "message": {
                    "type": "rich",
                    "content": rich_content
                },
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                logger.info(f"富文本早报已发送到微信群: {group_name or '默认群'}")
                return True
            else:
                logger.error(f"发送富文本消息失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送富文本消息时发生错误: {e}")
            return False
    
    async def send_image_with_text(self, image_path: str, text: str, group_name: str = None) -> bool:
        """
        发送图片和文字消息
        
        Args:
            image_path: 图片路径
            text: 文字内容
            group_name: 群名称
        """
        try:
            if not self.is_connected:
                await self.connect()
            
            send_data = {
                "action": "send_image_with_text",
                "session_id": self.session_id,
                "group_name": group_name or settings.DEFAULT_GROUP_NAME,
                "message": {
                    "type": "image_with_text",
                    "image_path": image_path,
                    "text": text
                },
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                logger.info(f"图片和文字消息已发送到微信群: {group_name or '默认群'}")
                return True
            else:
                logger.error(f"发送图片和文字消息失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送图片和文字消息时发生错误: {e}")
            return False
    
    async def get_group_list(self) -> List[Dict[str, Any]]:
        """获取群列表"""
        try:
            if not self.is_connected:
                await self.connect()
            
            send_data = {
                "action": "get_group_list",
                "session_id": self.session_id,
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                groups = result.get("data", {}).get("groups", [])
                logger.info(f"获取到 {len(groups)} 个群")
                return groups
            else:
                logger.error(f"获取群列表失败: {result.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"获取群列表时发生错误: {e}")
            return []
    
    async def get_group_members(self, group_name: str) -> List[Dict[str, Any]]:
        """获取群成员列表"""
        try:
            if not self.is_connected:
                await self.connect()
            
            send_data = {
                "action": "get_group_members",
                "session_id": self.session_id,
                "group_name": group_name,
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                members = result.get("data", {}).get("members", [])
                logger.info(f"群 {group_name} 有 {len(members)} 个成员")
                return members
            else:
                logger.error(f"获取群成员失败: {result.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"获取群成员时发生错误: {e}")
            return []
    
    async def send_private_message(self, user_name: str, message: str) -> bool:
        """发送私聊消息"""
        try:
            if not self.is_connected:
                await self.connect()
            
            send_data = {
                "action": "send_private_message",
                "session_id": self.session_id,
                "user_name": user_name,
                "message": {
                    "type": "text",
                    "content": message
                },
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                logger.info(f"私聊消息已发送给: {user_name}")
                return True
            else:
                logger.error(f"发送私聊消息失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送私聊消息时发生错误: {e}")
            return False
    
    async def publish_moment(self, content: str, image_paths: List[str] = None) -> bool:
        """发布朋友圈"""
        try:
            if not self.is_connected:
                await self.connect()
            
            send_data = {
                "action": "publish_moment",
                "session_id": self.session_id,
                "content": content,
                "image_paths": image_paths or [],
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                logger.info("朋友圈发布成功")
                return True
            else:
                logger.error(f"发布朋友圈失败: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发布朋友圈时发生错误: {e}")
            return False
    
    async def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            send_data = {
                "action": "check_status",
                "session_id": self.session_id,
                "timestamp": int(time.time())
            }
            
            response = await self.client.post(self.webhook_url, json=send_data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                self.is_connected = True
                return True
            else:
                self.is_connected = False
                return False
                
        except Exception as e:
            logger.error(f"检查连接状态时发生错误: {e}")
            self.is_connected = False
            return False
    
    async def close(self):
        """关闭客户端"""
        try:
            if self.is_connected:
                send_data = {
                    "action": "disconnect",
                    "session_id": self.session_id,
                    "timestamp": int(time.time())
                }
                
                await self.client.post(self.webhook_url, json=send_data)
            
            await self.client.aclose()
            self.is_connected = False
            logger.info("iPad微信客户端已关闭")
            
        except Exception as e:
            logger.error(f"关闭iPad微信客户端时发生错误: {e}")
