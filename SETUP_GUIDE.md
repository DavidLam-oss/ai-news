# AI早报系统配置指南

## 🎯 系统当前状态
- ✅ 爬虫引擎正常运行
- ✅ API服务正常运行 (http://localhost:8000)
- ✅ DeepSeek AI处理正常
- ✅ 文章提取功能正常

## 📋 下一步配置步骤

### 1. 🚀 配置飞书多维表格（推荐优先完成）

#### 1.1 创建飞书应用
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`

#### 1.2 创建多维表格
1. 在飞书中创建多维表格
2. 设置以下字段：
   - 日期 (日期类型)
   - 早报原始内容 (多行文本)
   - AI处理后内容 (多行文本)
   - 图片提示词1 (单行文本)
   - 图片提示词2 (单行文本)
   - 图片提示词3 (单行文本)
   - 生成图片 (附件)

#### 1.3 配置权限
1. 给应用添加多维表格权限
2. 获取表格的 `Table Token`

#### 1.4 更新环境变量
```bash
# 运行配置脚本
python setup_api_keys.py

# 或手动编辑 .env 文件
FEISHU_APP_ID=你的飞书App_ID
FEISHU_APP_SECRET=你的飞书App_Secret
FEISHU_TABLE_TOKEN=你的表格Token
```

### 2. 💬 配置微信助手（可选）

#### 2.1 创建微信应用
1. 访问 [微信开放平台](https://open.weixin.qq.com/)
2. 创建应用
3. 获取 `App ID` 和 `App Secret`

#### 2.2 更新环境变量
```bash
WECHAT_APP_ID=你的微信App_ID
WECHAT_APP_SECRET=你的微信App_Secret
```

### 3. ⏰ 设置定时任务

#### 3.1 使用系统定时任务
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天上午8点执行）
0 8 * * * cd /Users/davidlin/Documents/GitHub/ai-news && source venv/bin/activate && python -c "import asyncio; from crawler.main import AINewsCrawler; asyncio.run(AINewsCrawler().run_daily_crawl())"
```

#### 3.2 使用PM2管理
```bash
# 安装PM2
npm install -g pm2

# 启动定时任务
pm2 start ecosystem.config.js
```

### 4. 🧪 测试完整工作流程

#### 4.1 测试爬虫
```bash
curl "http://localhost:8000/api/news?max_articles=5"
```

#### 4.2 测试AI处理
```bash
curl -X POST "http://localhost:8000/api/process" \
  -H "Content-Type: application/json" \
  -d '{"articles": [{"title": "测试文章", "summary": "测试摘要", "source": "测试源"}]}'
```

#### 4.3 测试飞书存储
```bash
curl -X POST "http://localhost:8000/api/feishu/record" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-15",
    "raw_content": "原始内容",
    "processed_content": "处理后内容",
    "image_prompts": ["提示词1", "提示词2", "提示词3"]
  }'
```

### 5. 📊 监控系统状态

#### 5.1 查看API文档
访问：http://localhost:8000/docs

#### 5.2 查看系统状态
```bash
curl http://localhost:8000/health
```

#### 5.3 查看日志
```bash
tail -f logs/crawler.log
```

## 🎯 推荐执行顺序

1. **立即行动**：配置飞书多维表格
2. **测试验证**：测试完整工作流程
3. **自动化**：设置定时任务
4. **扩展功能**：配置微信助手
5. **监控优化**：添加系统监控

## 📞 需要帮助？

如果遇到问题，可以：
1. 查看日志文件：`logs/crawler.log`
2. 检查API状态：`curl http://localhost:8000/health`
3. 运行测试脚本：`python simple_crawler_test.py`

## 🎉 完成后的效果

配置完成后，系统将：
- 每天自动爬取AI科技新闻
- 使用DeepSeek生成精美早报
- 自动存储到飞书多维表格
- 可选：自动发送到微信群聊


