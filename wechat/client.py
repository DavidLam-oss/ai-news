#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信助手客户端
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
import httpx
from loguru import logger

from config.settings import settings, WECHAT_TEMPLATES

class WechatClient:
    """微信助手客户端"""
    
    def __init__(self):
        """初始化微信客户端"""
        self.app_id = settings.WECHAT_APP_ID
        self.app_secret = settings.WECHAT_APP_SECRET
        self.access_token = settings.WECHAT_ACCESS_TOKEN
        
        # HTTP客户端
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AI-News-System/1.0"
            }
        )
    
    async def get_access_token(self) -> str:
        """获取微信访问令牌"""
        try:
            url = "https://api.weixin.qq.com/cgi-bin/token"
            params = {
                "grant_type": "client_credential",
                "appid": self.app_id,
                "secret": self.app_secret
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            if "access_token" in result:
                self.access_token = result["access_token"]
                logger.info("微信访问令牌获取成功")
                return self.access_token
            else:
                raise Exception(f"获取微信访问令牌失败: {result.get('errmsg', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"获取微信访问令牌失败: {e}")
            raise
    
    async def ensure_access_token(self):
        """确保有有效的访问令牌"""
        if not self.access_token:
            await self.get_access_token()
    
    async def send_to_group(self, report: Dict[str, Any]) -> bool:
        """发送早报到微信群"""
        try:
            await self.ensure_access_token()
            
            # 准备消息内容
            message_content = WECHAT_TEMPLATES['group_message'].format(
                date=report.get('date', ''),
                summary=report.get('summary', ''),
                trends='\n'.join([f"• {trend}" for trend in report.get('trends', [])])
            )
            
            # 这里需要根据具体的微信机器人API来调整
            # 示例使用企业微信机器人
            webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
            
            data = {
                "msgtype": "text",
                "text": {
                    "content": message_content
                }
            }
            
            response = await self.client.post(webhook_url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                logger.info("早报已发送到微信群")
                return True
            else:
                logger.error(f"发送到微信群失败: {result.get('errmsg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送到微信群时发生错误: {e}")
            return False
    
    async def publish_moment(self, report: Dict[str, Any]) -> bool:
        """发布朋友圈"""
        try:
            await self.ensure_access_token()
            
            # 准备朋友圈内容
            moment_content = WECHAT_TEMPLATES['moment_content'].format(
                summary=report.get('summary', '')
            )
            
            # 这里需要根据具体的微信API来调整
            # 示例使用微信开放平台API
            url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.access_token}"
            
            data = {
                "touser": "OPENID",  # 需要替换为实际的用户OPENID
                "msgtype": "text",
                "text": {
                    "content": moment_content
                }
            }
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                logger.info("朋友圈发布成功")
                return True
            else:
                logger.error(f"发布朋友圈失败: {result.get('errmsg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发布朋友圈时发生错误: {e}")
            return False
    
    async def send_text_message(self, content: str, target_id: str) -> bool:
        """发送文本消息"""
        try:
            await self.ensure_access_token()
            
            url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.access_token}"
            
            data = {
                "touser": target_id,
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                logger.info(f"文本消息已发送给 {target_id}")
                return True
            else:
                logger.error(f"发送文本消息失败: {result.get('errmsg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送文本消息时发生错误: {e}")
            return False
    
    async def send_news_message(self, articles: List[Dict[str, Any]], target_id: str) -> bool:
        """发送图文消息"""
        try:
            await self.ensure_access_token()
            
            url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.access_token}"
            
            # 准备图文消息
            news_items = []
            for article in articles[:8]:  # 最多8条图文
                news_item = {
                    "title": article.get('title', ''),
                    "description": article.get('summary', ''),
                    "url": article.get('url', ''),
                    "picurl": article.get('image_url', '')
                }
                news_items.append(news_item)
            
            data = {
                "touser": target_id,
                "msgtype": "news",
                "news": {
                    "articles": news_items
                }
            }
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                logger.info(f"图文消息已发送给 {target_id}")
                return True
            else:
                logger.error(f"发送图文消息失败: {result.get('errmsg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送图文消息时发生错误: {e}")
            return False
    
    async def upload_media(self, media_type: str, media_data: bytes) -> str:
        """上传媒体文件"""
        try:
            await self.ensure_access_token()
            
            url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={media_type}"
            
            files = {
                "media": ("media", media_data, "image/jpeg")
            }
            
            response = await self.client.post(url, files=files)
            response.raise_for_status()
            
            result = response.json()
            if "media_id" in result:
                media_id = result["media_id"]
                logger.info(f"媒体文件上传成功，media_id: {media_id}")
                return media_id
            else:
                raise Exception(f"上传媒体文件失败: {result.get('errmsg', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"上传媒体文件时发生错误: {e}")
            raise
    
    async def send_image_message(self, media_id: str, target_id: str) -> bool:
        """发送图片消息"""
        try:
            await self.ensure_access_token()
            
            url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.access_token}"
            
            data = {
                "touser": target_id,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                }
            }
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                logger.info(f"图片消息已发送给 {target_id}")
                return True
            else:
                logger.error(f"发送图片消息失败: {result.get('errmsg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"发送图片消息时发生错误: {e}")
            return False
    
    async def get_user_info(self, openid: str) -> Dict[str, Any]:
        """获取用户信息"""
        try:
            await self.ensure_access_token()
            
            url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={self.access_token}&openid={openid}&lang=zh_CN"
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            result = response.json()
            if "openid" in result:
                logger.info(f"获取用户信息成功: {openid}")
                return result
            else:
                logger.error(f"获取用户信息失败: {result.get('errmsg', 'Unknown error')}")
                return {}
                
        except Exception as e:
            logger.error(f"获取用户信息时发生错误: {e}")
            return {}
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
        logger.info("微信客户端已关闭")
