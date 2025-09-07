#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的爬虫测试 - 更好的文章提取
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from crawler.main import AINewsCrawler
from crawler.content_processor import ContentProcessor

async def improved_crawler_test():
    """改进的爬虫测试"""
    
    print("🕷️ 改进的爬虫测试 - 更好的文章提取")
    print("=" * 60)
    
    # 创建爬虫实例
    crawler = AINewsCrawler()
    
    try:
        # 初始化爬虫
        await crawler.init_crawler()
        print("✅ 爬虫引擎初始化成功")
        
        # 测试更多网站
        test_sources = [
            {"name": "36氪", "url": "https://36kr.com", "type": "tech"},
            {"name": "量子位", "url": "https://www.qbitai.com", "type": "ai"},
            {"name": "CSDN", "url": "https://www.csdn.net", "type": "ai"},
            {"name": "掘金", "url": "https://juejin.cn", "type": "tech"},
            {"name": "少数派", "url": "https://sspai.com", "type": "tech"}
        ]
        
        print(f"\n🔍 开始爬取 {len(test_sources)} 个网站...")
        
        all_articles = []
        
        for source in test_sources:
            print(f"\n📰 正在爬取: {source['name']} ({source['url']})")
            
            try:
                # 执行爬取，使用更长的等待时间和重试机制
                max_retries = 2
                result = None
                
                for attempt in range(max_retries):
                    try:
                        print(f"  🔄 尝试 {attempt + 1}/{max_retries}...")
                        result = await crawler.crawler.arun(
                            url=source['url'],
                            wait_for="networkidle",
                            delay_before_return_html=3,
                            timeout=30000,  # 30秒超时
                            js_code="""
                            // 等待页面加载完成
                            await new Promise(resolve => setTimeout(resolve, 2000));
                            
                            // 尝试滚动页面以触发懒加载
                            window.scrollTo(0, document.body.scrollHeight);
                            await new Promise(resolve => setTimeout(resolve, 1500));
                            window.scrollTo(0, 0);
                            
                            // 尝试点击"加载更多"按钮
                            const loadMoreBtn = document.querySelector('[class*="load"], [class*="more"], [class*="展开"]');
                            if (loadMoreBtn) {
                                loadMoreBtn.click();
                                await new Promise(resolve => setTimeout(resolve, 1500));
                            }
                            """
                        )
                        if result.success:
                            break
                    except Exception as e:
                        print(f"  ⚠️ 尝试 {attempt + 1} 失败: {e}")
                        if attempt < max_retries - 1:
                            print(f"  ⏳ 等待2秒后重试...")
                            await asyncio.sleep(2)
                        else:
                            print(f"  ❌ 所有重试都失败了")
                
                if result.success:
                    print(f"✅ {source['name']} 爬取成功")
                    print(f"📄 页面标题: {result.metadata.get('title', 'N/A')}")
                    print(f"📊 内容长度: {len(result.html)} 字符")
                    
                    # 提取文章信息
                    articles = extract_articles_improved(result.html, source['name'], source['url'])
                    
                    print(f"📰 提取到 {len(articles)} 篇文章")
                    
                    # 显示前3篇文章
                    for i, article in enumerate(articles[:3], 1):
                        print(f"  {i}. {article['title'][:60]}...")
                        print(f"     来源: {article['source']}")
                        print(f"     摘要: {article['summary'][:100]}...")
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
            processor = ContentProcessor()
            result = await processor.process_articles(all_articles[:15])  # 处理前15篇
            
            print("✅ 内容处理完成！")
            print("\n📋 早报摘要:")
            print("-" * 50)
            print(result['summary'])
            
            print("\n📈 发展趋势:")
            print("-" * 50)
            for i, trend in enumerate(result['trends'][:5], 1):
                print(f"{i}. {trend}")
            
            print("\n🎨 图片提示词:")
            print("-" * 50)
            for i, prompt in enumerate(result['image_prompts'], 1):
                print(f"{i}. {prompt}")
            
            print(f"\n📊 处理统计:")
            print(f"处理时间: {result['processed_at']}")
            print(f"文章总数: {result['total_articles']}")
            print(f"保留文章: {len(result['articles'])}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理资源
        await crawler.cleanup()
        print("\n🧹 资源清理完成")

def extract_articles_improved(html, source_name, base_url):
    """改进的文章提取函数"""
    articles = []
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        if source_name == "36氪":
            # 36氪的文章选择器 - 更精确
            selectors = [
                'div[class*="article-item"]',
                'div[class*="news-item"]',
                'div[class*="item"]',
                'article',
                'div[class*="card"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:  # 只取前10篇
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or element.find('a')
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:  # 过滤太短的标题
                        continue
                    
                    # 获取链接
                    link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://36kr.com' + url
                    
                    # 获取摘要
                    summary_elem = element.find(['p', 'div'], class_=lambda x: x and 'summary' in x.lower()) or element.find('p')
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "虎嗅网":
            # 虎嗅网的文章选择器
            selectors = [
                'div[class*="article-item"]',
                'div[class*="news-item"]',
                'article',
                'div[class*="item"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.huxiu.com' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_=lambda x: x and 'summary' in x.lower())
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
            selectors = [
                'div[class*="article-item"]',
                'div[class*="news-item"]',
                'article',
                'div[class*="item"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.qbitai.com' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_=lambda x: x and 'summary' in x.lower())
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "CSDN":
            # CSDN的文章选择器 - 更精确的选择器
            selectors = [
                'div[class*="blog-list-box"] div[class*="blog-list-item"]',
                'div[class*="article-item"]',
                'div[class*="news-item"]',
                'article',
                'div[class*="item"]',
                'div[class*="blog"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                # 尝试多种标题选择器
                title_elem = (element.find(['h1', 'h2', 'h3', 'h4']) or 
                             element.find('a', class_=lambda x: x and 'title' in x.lower()) or
                             element.find('a', class_=lambda x: x and 'blog' in x.lower()))
                
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    # 获取链接
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.csdn.net' + url
                    
                    # 获取摘要
                    summary_elem = (element.find('p') or 
                                   element.find('div', class_=lambda x: x and 'summary' in x.lower()) or
                                   element.find('div', class_=lambda x: x and 'desc' in x.lower()))
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "InfoQ":
            # InfoQ的文章选择器
            selectors = [
                'div[class*="article-item"]',
                'div[class*="news-item"]',
                'article',
                'div[class*="item"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    link_elem = title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://www.infoq.cn' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_=lambda x: x and 'summary' in x.lower())
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "掘金":
            # 掘金的文章选择器
            selectors = [
                'div[class*="entry-list"] div[class*="item"]',
                'div[class*="article-item"]',
                'article',
                'div[class*="item"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4']) or element.find('a', class_=lambda x: x and 'title' in x.lower())
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://juejin.cn' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_=lambda x: x and 'summary' in x.lower())
                    summary = summary_elem.get_text().strip() if summary_elem else title
                    
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'source': source_name,
                        'url': url,
                        'publish_time': '2024-01-15T10:00:00Z'
                    })
        
        elif source_name == "少数派":
            # 少数派的文章选择器
            selectors = [
                'div[class*="article-item"]',
                'article',
                'div[class*="item"]',
                'div[class*="post"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f"  🔍 使用选择器: {selector} (找到 {len(elements)} 个元素)")
                    break
            
            for element in elements[:10]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4']) or element.find('a', class_=lambda x: x and 'title' in x.lower())
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a') or element.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    if url and not url.startswith('http'):
                        url = 'https://sspai.com' + url
                    
                    summary_elem = element.find('p') or element.find('div', class_=lambda x: x and 'summary' in x.lower())
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
            print(f"  🔍 使用通用选择器...")
            # 通用文章提取
            for element in soup.find_all(['article', 'div'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['article', 'news', 'item', 'card']))[:15]:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if title_elem:
                    title = title_elem.get_text().strip()
                    if len(title) < 10:
                        continue
                    
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
    asyncio.run(improved_crawler_test())

