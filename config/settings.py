#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置管理
"""

import os
from typing import List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    """系统配置类"""
    
    # AI服务配置
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    DEEPSEEK_API_KEY: str = Field(default="", env="DEEPSEEK_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    # 飞书配置
    FEISHU_APP_ID: str = Field(default="", env="FEISHU_APP_ID")
    FEISHU_APP_SECRET: str = Field(default="", env="FEISHU_APP_SECRET")
    FEISHU_BASE_URL: str = Field(default="https://open.feishu.cn/open-apis", env="FEISHU_BASE_URL")
    FEISHU_TABLE_TOKEN: str = Field(default="", env="FEISHU_TABLE_TOKEN")
    
    # 微信配置
    WECHAT_APP_ID: str = Field(default="", env="WECHAT_APP_ID")
    WECHAT_APP_SECRET: str = Field(default="", env="WECHAT_APP_SECRET")
    WECHAT_ACCESS_TOKEN: str = Field(default="", env="WECHAT_ACCESS_TOKEN")
    
    # iPad协议微信助手配置
    IPAD_WEBHOOK_URL: str = Field(default="", env="IPAD_WEBHOOK_URL")
    DEFAULT_GROUP_NAME: str = Field(default="AI科技早报群", env="DEFAULT_GROUP_NAME")
    TARGET_GROUPS: str = Field(default="", env="TARGET_GROUPS")  # 逗号分隔的群名称
    
    # 爬虫配置
    CRAWL_INTERVAL: int = Field(default=3600, env="CRAWL_INTERVAL")
    MAX_ARTICLES: int = Field(default=50, env="MAX_ARTICLES")
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        env="USER_AGENT"
    )
    
    # 服务器配置
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Redis配置
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # 数据库配置
    DATABASE_URL: str = Field(default="sqlite:///./ai_news.db", env="DATABASE_URL")
    
    # 功能开关
    ENABLE_WECHAT: bool = Field(default=True, env="ENABLE_WECHAT")
    ENABLE_IMAGE_GENERATION: bool = Field(default=True, env="ENABLE_IMAGE_GENERATION")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 全局配置实例
settings = Settings()

# 新闻源配置
NEWS_SOURCES = [
    {
        "name": "36氪",
        "url": "https://36kr.com",
        "category": "tech",
        "weight": 1.0,
        "selectors": {
            "title": ".article-item-title",
            "link": ".article-item-title a",
            "summary": ".article-item-summary"
        }
    },
    {
        "name": "虎嗅网",
        "url": "https://www.huxiu.com",
        "category": "tech",
        "weight": 1.0,
        "selectors": {
            "title": ".article-item-title",
            "link": ".article-item-title a",
            "summary": ".article-item-summary"
        }
    },
    {
        "name": "机器之心",
        "url": "https://www.jiqizhixin.com",
        "category": "ai",
        "weight": 1.2,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        }
    },
    {
        "name": "AI科技大本营",
        "url": "https://www.csdn.net",
        "category": "ai",
        "weight": 1.1,
        "selectors": {
            "title": ".title",
            "link": ".title a",
            "summary": ".summary"
        }
    },
    {
        "name": "量子位",
        "url": "https://www.qbitai.com",
        "category": "ai",
        "weight": 1.3,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        }
    },
    {
        "name": "新智元",
        "url": "https://www.aiera.cn",
        "category": "ai",
        "weight": 1.2,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        }
    },
    {
        "name": "AI前线",
        "url": "https://www.infoq.cn",
        "category": "ai",
        "weight": 1.1,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        }
    },
    {
        "name": "雷锋网",
        "url": "https://www.leiphone.com",
        "category": "tech",
        "weight": 1.0,
        "selectors": {
            "title": ".article-title",
            "link": ".article-title a",
            "summary": ".article-summary"
        }
    }
]

# AI处理提示词模板
AI_PROMPTS = {
    "summary": """
请将以下AI科技新闻整理成一份简洁的早报摘要，要求：
1. 突出最重要的3-5条新闻
2. 每条新闻用1-2句话概括
3. 语言简洁明了，适合快速阅读
4. 按重要性排序
5. 总字数控制在300字以内

新闻内容：
{articles}
""",
    
    "trends": """
基于以下AI科技新闻，分析当前AI领域的发展趋势，要求：
1. 识别3-5个主要趋势
2. 每个趋势用1句话描述
3. 分析趋势的影响和意义
4. 语言专业但易懂

新闻内容：
{articles}
""",
    
    "image_prompts": """
基于以下AI科技新闻内容，生成3个适合制作早报图片的提示词，要求：
1. 每个提示词描述一个视觉场景
2. 包含AI、科技、未来等元素
3. 适合制作简洁现代的图片
4. 每个提示词不超过50字
5. 风格统一，适合早报使用

新闻内容：
{articles}
"""
}

# 微信消息模板
WECHAT_TEMPLATES = {
    "group_message": """
🤖 AI科技早报 - {date}

{summary}

📈 今日趋势：
{trends}

🔗 详细内容请查看群文件或访问早报链接
""",
    
    "moment_content": """
AI科技早报 📰

{summary}

#AI #科技 #早报
"""
}
