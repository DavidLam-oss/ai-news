#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻源管理模块
"""

from typing import List, Dict, Any
from config.settings import NEWS_SOURCES

class NewsSources:
    """新闻源管理类"""
    
    def __init__(self):
        """初始化新闻源"""
        self.sources = NEWS_SOURCES
    
    def get_sources(self) -> List[Dict[str, Any]]:
        """获取所有新闻源"""
        return self.sources
    
    def get_sources_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取新闻源"""
        return [source for source in self.sources if source.get('category') == category]
    
    def get_ai_sources(self) -> List[Dict[str, Any]]:
        """获取AI相关的新闻源"""
        return self.get_sources_by_category('ai')
    
    def get_tech_sources(self) -> List[Dict[str, Any]]:
        """获取科技相关的新闻源"""
        return self.get_sources_by_category('tech')
    
    def get_weighted_sources(self) -> List[Dict[str, Any]]:
        """获取按权重排序的新闻源"""
        return sorted(self.sources, key=lambda x: x.get('weight', 1.0), reverse=True)
    
    def add_source(self, source: Dict[str, Any]) -> bool:
        """添加新的新闻源"""
        try:
            # 验证必要字段
            required_fields = ['name', 'url', 'category']
            if not all(field in source for field in required_fields):
                return False
            
            # 设置默认值
            source.setdefault('weight', 1.0)
            source.setdefault('selectors', {})
            
            self.sources.append(source)
            return True
        except Exception:
            return False
    
    def remove_source(self, name: str) -> bool:
        """移除新闻源"""
        try:
            self.sources = [source for source in self.sources if source['name'] != name]
            return True
        except Exception:
            return False
    
    def update_source(self, name: str, updates: Dict[str, Any]) -> bool:
        """更新新闻源"""
        try:
            for i, source in enumerate(self.sources):
                if source['name'] == name:
                    self.sources[i].update(updates)
                    return True
            return False
        except Exception:
            return False
    
    def get_source_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取新闻源"""
        for source in self.sources:
            if source['name'] == name:
                return source
        return {}
    
    def validate_sources(self) -> List[str]:
        """验证新闻源配置"""
        errors = []
        
        for source in self.sources:
            # 检查必要字段
            if not source.get('name'):
                errors.append(f"新闻源缺少名称: {source}")
            
            if not source.get('url'):
                errors.append(f"新闻源 {source.get('name', 'Unknown')} 缺少URL")
            
            if not source.get('category'):
                errors.append(f"新闻源 {source.get('name', 'Unknown')} 缺少分类")
            
            # 检查URL格式
            url = source.get('url', '')
            if not url.startswith(('http://', 'https://')):
                errors.append(f"新闻源 {source.get('name', 'Unknown')} URL格式错误: {url}")
        
        return errors
