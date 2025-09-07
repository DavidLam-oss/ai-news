#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI早报API服务
提供RESTful API接口供飞书多维表格和微信助手调用
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from loguru import logger

from config.settings import settings
from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor
from crawler.news_sources import NewsSources

# 创建FastAPI应用
app = FastAPI(
    title="AI早报API服务",
    description="基于飞书多维表格的AI早报系统API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
crawler_instance = None
content_processor = None
news_sources = None

# Pydantic模型
class NewsRequest(BaseModel):
    """新闻请求模型"""
    sources: Optional[List[str]] = None
    max_articles: Optional[int] = 50
    categories: Optional[List[str]] = None

class ProcessRequest(BaseModel):
    """内容处理请求模型"""
    articles: List[Dict[str, Any]]
    enhancement_type: Optional[str] = "summary"

class WechatSendRequest(BaseModel):
    """微信发送请求模型"""
    content: str
    target_type: str  # "group" or "moment"
    target_id: Optional[str] = None

class FeishuRecordRequest(BaseModel):
    """飞书记录请求模型"""
    date: str
    raw_content: str
    processed_content: str
    image_prompts: List[str]

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    global crawler_instance, content_processor, news_sources
    
    try:
        # 初始化组件
        crawler_instance = AINewsCrawler()
        await crawler_instance.init_crawler()
        
        # 使用爬虫实例中的内容处理器
        content_processor = crawler_instance.content_processor
        news_sources = NewsSources()
        
        logger.info("API服务启动成功")
    except Exception as e:
        logger.error(f"API服务启动失败: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    global crawler_instance
    
    if crawler_instance:
        await crawler_instance.cleanup()
        logger.info("API服务已关闭")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI早报API服务",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "crawler": crawler_instance is not None,
            "content_processor": content_processor is not None,
            "news_sources": news_sources is not None
        }
    }

@app.get("/api/news")
async def get_news(request: NewsRequest = Depends()):
    """获取最新AI资讯"""
    try:
        if not crawler_instance:
            raise HTTPException(status_code=500, detail="爬虫服务未初始化")
        
        # 爬取新闻
        articles = await crawler_instance.crawl_news_sources()
        
        # 根据请求参数过滤
        if request.sources:
            articles = [a for a in articles if a.get('source') in request.sources]
        
        if request.categories:
            articles = [a for a in articles if a.get('category') in request.categories]
        
        # 限制数量
        articles = articles[:request.max_articles]
        
        return {
            "success": True,
            "data": {
                "articles": articles,
                "total": len(articles),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"获取新闻失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
async def process_content(request: ProcessRequest):
    """处理早报内容"""
    try:
        logger.info(f"content_processor: {content_processor}")
        logger.info(f"content_processor type: {type(content_processor)}")
        
        if not content_processor:
            raise HTTPException(status_code=500, detail="内容处理器未初始化")
        
        # 处理文章
        processed_content = await content_processor.process_articles(request.articles)
        
        return {
            "success": True,
            "data": processed_content
        }
        
    except Exception as e:
        logger.error(f"处理内容失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feishu/record")
async def create_feishu_record(request: FeishuRecordRequest):
    """创建飞书记录"""
    try:
        if not crawler_instance:
            raise HTTPException(status_code=500, detail="爬虫服务未初始化")
        
        # 准备记录数据
        record_data = {
            '日期': request.date,
            '早报原始内容': request.raw_content,
            'AI处理后内容': request.processed_content,
            '图片提示词1': request.image_prompts[0] if len(request.image_prompts) > 0 else '',
            '图片提示词2': request.image_prompts[1] if len(request.image_prompts) > 1 else '',
            '图片提示词3': request.image_prompts[2] if len(request.image_prompts) > 2 else ''
        }
        
        # 保存到飞书
        success = await crawler_instance.save_to_feishu(record_data)
        
        if success:
            return {
                "success": True,
                "message": "记录已保存到飞书多维表格"
            }
        else:
            raise HTTPException(status_code=500, detail="保存到飞书失败")
        
    except Exception as e:
        logger.error(f"创建飞书记录失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wechat/send")
async def send_to_wechat(request: WechatSendRequest):
    """发送到微信"""
    try:
        if not crawler_instance:
            raise HTTPException(status_code=500, detail="爬虫服务未初始化")
        
        # 准备报告数据
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'summary': request.content,
            'created_at': datetime.now().isoformat()
        }
        
        # 发送到微信
        await crawler_instance.send_to_wechat(report)
        
        return {
            "success": True,
            "message": "消息已发送到微信"
        }
        
    except Exception as e:
        logger.error(f"发送到微信失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sources")
async def get_news_sources():
    """获取新闻源列表"""
    try:
        if not news_sources:
            raise HTTPException(status_code=500, detail="新闻源服务未初始化")
        
        sources = news_sources.get_sources()
        
        return {
            "success": True,
            "data": {
                "sources": sources,
                "total": len(sources)
            }
        }
        
    except Exception as e:
        logger.error(f"获取新闻源失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sources")
async def add_news_source(source: Dict[str, Any]):
    """添加新闻源"""
    try:
        if not news_sources:
            raise HTTPException(status_code=500, detail="新闻源服务未初始化")
        
        success = news_sources.add_source(source)
        
        if success:
            return {
                "success": True,
                "message": "新闻源添加成功"
            }
        else:
            raise HTTPException(status_code=400, detail="新闻源添加失败")
        
    except Exception as e:
        logger.error(f"添加新闻源失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sources/{source_name}")
async def remove_news_source(source_name: str):
    """删除新闻源"""
    try:
        if not news_sources:
            raise HTTPException(status_code=500, detail="新闻源服务未初始化")
        
        success = news_sources.remove_source(source_name)
        
        if success:
            return {
                "success": True,
                "message": f"新闻源 {source_name} 删除成功"
            }
        else:
            raise HTTPException(status_code=404, detail="新闻源不存在")
        
    except Exception as e:
        logger.error(f"删除新闻源失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crawl/run")
async def run_crawl_task(background_tasks: BackgroundTasks):
    """手动执行爬取任务"""
    try:
        if not crawler_instance:
            raise HTTPException(status_code=500, detail="爬虫服务未初始化")
        
        # 在后台执行爬取任务
        background_tasks.add_task(crawler_instance.run_daily_crawl)
        
        return {
            "success": True,
            "message": "爬取任务已启动"
        }
        
    except Exception as e:
        logger.error(f"执行爬取任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """获取系统统计信息"""
    try:
        # 这里可以添加更多的统计信息
        stats = {
            "total_sources": len(news_sources.get_sources()) if news_sources else 0,
            "ai_sources": len(news_sources.get_ai_sources()) if news_sources else 0,
            "tech_sources": len(news_sources.get_tech_sources()) if news_sources else 0,
            "last_crawl": datetime.now().isoformat(),
            "system_status": "running"
        }
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "内部服务器错误",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
