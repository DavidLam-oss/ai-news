
# AI早报系统使用说明

## 快速开始

### 1. 环境准备

#### 系统要求
- Python 3.8+
- Node.js 16+ (可选)
- Redis (用于缓存)
- 8GB+ 内存推荐

#### 安装依赖
```bash
# 克隆项目
git clone <your-repo-url>
cd ai-news

# 运行启动脚本
./start.sh
```

### 2. 配置环境变量

复制配置文件并填入必要信息：
```bash
cp config.env.example .env
```

编辑 `.env` 文件，填入以下配置：

#### AI服务配置
```bash
# OpenAI API密钥
OPENAI_API_KEY=sk-your-openai-api-key

# DeepSeek API密钥（可选）
DEEPSEEK_API_KEY=your-deepseek-api-key

# Anthropic API密钥（可选）
ANTHROPIC_API_KEY=your-anthropic-api-key
```

#### 飞书配置
```bash
# 飞书应用ID和密钥
FEISHU_APP_ID=your-feishu-app-id
FEISHU_APP_SECRET=your-feishu-app-secret

# 多维表格令牌
FEISHU_TABLE_TOKEN=your-table-token
```

 

### 3. 启动服务

#### 方式一：使用启动脚本
```bash
./start.sh
```

#### 方式二：手动启动
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动API服务
python api/server.py

# 或启动定时任务
python crawler/main.py --mode schedule
```

#### 方式三：Docker部署
```bash
# 构建镜像
docker build -t ai-news .

# 运行容器
docker run -d -p 8000:8000 ai-news

# 或使用docker-compose
docker-compose up -d
```

## 功能使用（更新）

### 1. API接口

#### 获取最新新闻
```bash
curl -X GET "http://localhost:8000/api/news?max_articles=20"
```

#### 处理早报内容
```bash
curl -X POST "http://localhost:8000/api/process" \
  -H "Content-Type: application/json" \
  -d '{"articles": [...], "enhancement_type": "summary"}'
```

#### 手动执行爬取
```bash
curl -X POST "http://localhost:8000/api/crawl/run"
```

### 2. 飞书多维表格集成

#### 创建表格
1. 登录飞书开放平台
2. 创建应用并获取凭证
3. 创建多维表格，配置字段结构
4. 设置自动化工作流

#### 自动化配置
参考 `feishu/table_config.md` 文件进行详细配置。

 

## 配置说明

### 1. 新闻源配置

在 `config/settings.py` 中配置新闻源：

```python
NEWS_SOURCES = [
    {
        "name": "36氪",
        "url": "https://36kr.com",
        "category": "tech",
        "weight": 1.0
    },
    # 更多新闻源...
]
```

### 2. AI处理配置

#### 提示词模板
在 `config/settings.py` 中自定义AI处理提示词：

```python
AI_PROMPTS = {
    "summary": "你的摘要生成提示词...",
    "trends": "你的趋势分析提示词...",
    "image_prompts": "你的图片提示词生成提示词..."
}
```

#### 模型配置
```python
# 在 content_processor.py 中修改模型
model="gpt-3.5-turbo"  # 或 "gpt-4", "claude-3" 等
```

### 3. 定时任务配置

#### 修改执行时间
在 `crawler/main.py` 中修改：
```python
# 每天上午8点执行
schedule.every().day.at("08:00").do(...)

# 每小时执行（测试用）
schedule.every().hour.do(...)
```

## 监控和维护

### 1. 日志查看

```bash
# 查看API服务日志
tail -f logs/api.log

# 查看爬虫日志
tail -f logs/crawler.log

# 查看所有日志
tail -f logs/*.log
```

### 2. 健康检查

```bash
# 检查API服务状态
curl http://localhost:8000/health

# 检查系统统计
curl http://localhost:8000/api/stats
```

### 3. 性能监控

#### 内存使用
```bash
# 查看进程内存使用
ps aux | grep python
```

#### Redis状态
```bash
# 连接Redis查看状态
redis-cli info
```

## 故障排除

### 1. 常见问题

#### 爬虫无法获取内容
- 检查网络连接
- 验证目标网站是否可访问
- 查看爬虫日志中的错误信息

#### AI处理失败
- 检查API密钥是否正确
- 确认API额度是否充足
- 查看OpenAI服务状态

#### 飞书集成失败
- 验证应用权限配置
- 检查访问令牌是否有效
- 确认表格分享权限

 

### 2. 调试技巧

#### 启用调试模式
```bash
# 设置环境变量
export DEBUG=True
export LOG_LEVEL=DEBUG

# 重新启动服务
python api/server.py
```

#### 单步测试
```bash
# 测试单个新闻源
python -c "
from crawler.news_sources import NewsSources
sources = NewsSources()
print(sources.get_sources())
"

# 测试AI处理
python -c "
from crawler.content_processor import ContentProcessor
processor = ContentProcessor()
# 测试代码...
"
```

### 3. 性能优化

#### 爬虫优化
- 调整并发数量
- 设置合理的延迟
- 使用代理池（如需要）

#### AI处理优化
- 批量处理文章
- 缓存处理结果
- 使用更快的模型

#### 系统优化
- 增加内存配置
- 使用SSD存储
- 配置负载均衡

## 扩展功能

### 1. 添加新的新闻源

```python
# 在 config/settings.py 中添加
{
    "name": "新新闻源",
    "url": "https://example.com",
    "category": "ai",
    "weight": 1.0,
    "selectors": {
        "title": ".article-title",
        "link": ".article-title a",
        "summary": ".article-summary"
    }
}
```

### 2. 自定义AI处理

```python
# 继承 ContentProcessor 类
class CustomContentProcessor(ContentProcessor):
    async def custom_process(self, articles):
        # 自定义处理逻辑
        pass
```

### 3. 集成其他平台（扩展）

```python
# 创建新的客户端类
class CustomPlatformClient:
    async def send_message(self, content):
        # 发送到自定义平台
        pass
```

## 安全注意事项

1. **保护API密钥**：不要将密钥提交到版本控制系统
2. **网络安全**：使用HTTPS和防火墙保护服务
3. **访问控制**：限制API访问权限
4. **数据备份**：定期备份重要数据
5. **监控告警**：设置异常监控和告警机制

## 更新和维护

### 1. 更新依赖
```bash
# 更新Python包
pip install --upgrade -r requirements.txt

# 更新Playwright
playwright install --force
```

### 2. 数据迁移
```bash
# 备份数据
cp data/ai_news.db data/ai_news.db.backup

# 执行迁移脚本
python scripts/migrate.py
```

### 3. 版本升级
```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖
pip install -r requirements.txt

# 重启服务
./start.sh
```
