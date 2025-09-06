#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格客户端
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
import httpx
from loguru import logger

from config.settings import settings

class FeishuClient:
    """飞书多维表格客户端"""
    
    def __init__(self):
        """初始化飞书客户端"""
        self.app_id = settings.FEISHU_APP_ID
        self.app_secret = settings.FEISHU_APP_SECRET
        self.base_url = settings.FEISHU_BASE_URL
        self.table_token = settings.FEISHU_TABLE_TOKEN
        self.access_token = None
        
        # HTTP客户端
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AI-News-System/1.0"
            }
        )
    
    async def get_access_token(self) -> str:
        """获取访问令牌"""
        try:
            url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
            data = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                logger.info("飞书访问令牌获取成功")
                return self.access_token
            else:
                raise Exception(f"获取访问令牌失败: {result.get('msg', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"获取飞书访问令牌失败: {e}")
            raise
    
    async def ensure_access_token(self):
        """确保有有效的访问令牌"""
        if not self.access_token:
            await self.get_access_token()
    
    async def create_record(self, record_data: Dict[str, Any]) -> bool:
        """在多维表格中创建记录"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/tables/tblDefault/records"
            
            # 准备请求数据
            fields = {}
            for key, value in record_data.items():
                fields[key] = value
            
            data = {
                "fields": fields
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                logger.info("飞书记录创建成功")
                return True
            else:
                logger.error(f"创建飞书记录失败: {result.get('msg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"创建飞书记录时发生错误: {e}")
            return False
    
    async def update_record(self, record_id: str, record_data: Dict[str, Any]) -> bool:
        """更新多维表格记录"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/tables/tblDefault/records/{record_id}"
            
            # 准备请求数据
            fields = {}
            for key, value in record_data.items():
                fields[key] = value
            
            data = {
                "fields": fields
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.put(url, json=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                logger.info(f"飞书记录 {record_id} 更新成功")
                return True
            else:
                logger.error(f"更新飞书记录失败: {result.get('msg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"更新飞书记录时发生错误: {e}")
            return False
    
    async def get_records(self, page_size: int = 100, page_token: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取多维表格记录"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/tables/tblDefault/records"
            params = {
                "page_size": page_size
            }
            
            if page_token:
                params["page_token"] = page_token
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                records = result.get("data", {}).get("items", [])
                logger.info(f"获取到 {len(records)} 条飞书记录")
                return records
            else:
                logger.error(f"获取飞书记录失败: {result.get('msg', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"获取飞书记录时发生错误: {e}")
            return []
    
    async def delete_record(self, record_id: str) -> bool:
        """删除多维表格记录"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/tables/tblDefault/records/{record_id}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = await self.client.delete(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                logger.info(f"飞书记录 {record_id} 删除成功")
                return True
            else:
                logger.error(f"删除飞书记录失败: {result.get('msg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"删除飞书记录时发生错误: {e}")
            return False
    
    async def get_table_info(self) -> Dict[str, Any]:
        """获取表格信息"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/tables/tblDefault"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                table_info = result.get("data", {})
                logger.info("获取表格信息成功")
                return table_info
            else:
                logger.error(f"获取表格信息失败: {result.get('msg', 'Unknown error')}")
                return {}
                
        except Exception as e:
            logger.error(f"获取表格信息时发生错误: {e}")
            return {}
    
    async def create_automation(self, automation_config: Dict[str, Any]) -> bool:
        """创建自动化工作流"""
        try:
            await self.ensure_access_token()
            
            url = f"{self.base_url}/bitable/v1/apps/{self.table_token}/automations"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(url, json=automation_config, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                logger.info("自动化工作流创建成功")
                return True
            else:
                logger.error(f"创建自动化工作流失败: {result.get('msg', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"创建自动化工作流时发生错误: {e}")
            return False
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
        logger.info("飞书客户端已关闭")
