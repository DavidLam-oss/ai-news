#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实网站爬取功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.news_sources import NewsSources

async def test_real_crawling():
    """测试真实网站爬取"""
    
    print("🕷️ 开始测试真实网站爬取功能...")
    print("=" * 60)
    
    # 获取新闻源
    news_sources = NewsSources()
    sources = news_sources.get_sources()
    
    print(f"📰 配置的新闻源数量: {len(sources)}")
    print("\n📋 新闻源列表:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source['name']} - {source['url']} ({source['category']})")
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 初始化爬虫
        await crawler.init_crawler()
        print("\n✅ 爬虫引擎初始化成功")
        
        # 选择几个网站进行测试
        test_sources = [
            {"name": "36氪", "url": "https://36kr.com"},
            {"name": "机器之心", "url": "https://www.jiqizhixin.com"},
            {"name": "量子位", "url": "https://www.qbitai.com"}
        ]
        
        print(f"\n🔍 开始爬取 {len(test_sources)} 个网站...")
        
        all_articles = []
        
        for source in test_sources:
            print(f"\n📰 正在爬取: {source['name']} ({source['url']})")
            
            try:
                # 执行爬取
                result = await crawler.crawler.arun(
                    url=source['url'],
                    wait_for="networkidle",
                    delay_before_return_html=3,
                    js_code="""
                    // 等待页面加载完成
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    
                    // 尝试滚动页面以触发懒加载
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    window.scrollTo(0, 0);
                    """
                )
                
                if result.success:
                    print(f"✅ {source['name']} 爬取成功")
                    print(f"📄 页面标题: {result.metadata.get('title', 'N/A')}")
                    print(f"📊 内容长度: {len(result.html)} 字符")
                    
                    # 提取文章信息
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(result.html, 'html.parser')
                    
                    # 根据网站类型提取文章
                    articles = extract_articles(soup, source['name'])
                    
                    print(f"📰 提取到 {len(articles)} 篇文章")
                    
                    # 显示前3篇文章
                    for i, article in enumerate(articles[:3], 1):
                        print(f"  {i}. {article['title'][:50]}...")
                        print(f"     来源: {article['source']}")
                        print(f"     摘要: {article['summary'][:80]}...")
                        print()
                    
                    all_articles.extend(articles)
                    
                else:
                    print(f"❌ {source['name']} 爬取失败")
                    
            except Exception as e:
                print(f"❌ {source['name']} 爬取出错: {e}")
        
        print(f"\n📊 爬取统计:")
        print(f"总文章数: {len(all_articles)}")
        print(f"成功网站: {len([s for s in test_sources if any(a['source'] == s['name'] for a in all_articles)])}")
        
        if all_articles:
            print(f"\n🤖 使用火山方舟DeepSeek处理 {len(all_articles)} 篇文章...")
            
            # 使用内容处理器处理文章
            from crawler.content_processor import ContentProcessor
            processor = ContentProcessor()
            result = await processor.process_articles(all_articles[:10])  # 只处理前10篇
            
            print("✅ 内容处理完成！")
            print("\n📋 早报摘要:")
            print("-" * 50)
            print(result['summary'])
            
            print("\n📈 发展趋势:")
            print("-" * 50)
            for i, trend in enumerate(result['trends'][:5], 1):  # 只显示前5个
                print(f"{i}. {trend}")
            
            print("\n🎨 图片提示词:")
            print("-" * 50)
            for i, prompt in enumerate(result['image_prompts'], 1):
                print(f"{i}. {prompt}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

def extract_articles(soup, source_name):
    """根据网站提取文章信息"""
    articles = []
    
    try:
        if source_name == "36氪":
            # 36氪的文章选择器
            article_elements = soup.find_all('div', class_='article-item')
            for element in article_elements[:5]:  # 只取前5篇
                title_elem = element.find('a', class_='article-item-title')
                if title_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    if not url.startswith('http'):
                        url = 'https://36kr.com' + url
                    
                    summary_elem = element.find('div', class_='article-item-summary')
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "机器之心":
            # 机器之心的文章选择器
            article_elements = soup.find_all('div', class_='article-item')
            for element in article_elements[:5]:
                title_elem = element.find('h3') or element.find('h2')
                if title_elem:
                    title = title_elem.get_text().strip()
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.jiqizhixin.com' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_='summary')
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "量子位":
            # 量子位的文章选择器
            article_elements = soup.find_all('div', class_='article-item') or soup.find_all('article')
            for element in article_elements[:5]:
                title_elem = element.find('h3') or element.find('h2') or element.find('h1')
                if title_elem:
                    title = title_elem.get_text().strip()
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.qbitai.com' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_='summary')
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        # 如果没有找到特定选择器，使用通用选择器
        if not articles:
            # 通用文章提取
            for element in soup.find_all(['article', 'div'], class_=lambda x: x and 'article' in x.lower())[:5]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text().strip()
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    summary_elem = element.find('p')
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
    
    except Exception as e:
        print(f"⚠️ 提取文章时出错: {e}")
    
    return articles

if __name__ == "__main__":
    asyncio.run(test_real_crawling())


