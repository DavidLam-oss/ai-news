# AI早报系统使用指南

## 🚀 快速开始

### 1. 环境准备
```bash
# 激活虚拟环境
source venv/bin/activate

# 检查依赖是否安装
pip list | grep -E "(crawl4ai|httpx|loguru)"
```

### 2. 运行系统测试
```bash
# 运行完整工作流程演示
python3 demo_full_workflow.py

# 运行简化爬虫测试
python3 simple_crawler_test.py

# 测试飞书连接
python3 test_feishu_config.py
```

## 📋 功能说明

### 爬虫功能
- **支持的网站**: 36氪、虎嗅网、机器之心、CSDN、掘金等
- **爬取内容**: 文章标题、摘要、链接、发布时间
- **去重处理**: 自动去除重复文章
- **智能提取**: 使用多种选择器策略

### AI处理功能
- **内容摘要**: 生成简洁的早报摘要
- **趋势分析**: 分析AI领域发展趋势
- **图片提示词**: 生成3个图片制作提示词
- **智能优化**: 使用DeepSeek API进行内容优化

### 飞书集成
- **数据存储**: 将早报数据存储到多维表格
- **字段映射**: 自动映射到预定义字段
- **格式转换**: JSON格式数据转换

## 🔧 配置说明

### 环境变量配置
```bash
# 飞书配置
export FEISHU_APP_ID="cli_a8366b7ef13a100c"
export FEISHU_APP_SECRET="5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr"
export FEISHU_BASE_URL="https://open.feishu.cn/open-apis"
export FEISHU_TABLE_TOKEN="F5I2bdNZxawzTqsRBVbcJWEMn9H"

# AI服务配置
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```

### 飞书多维表格字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | 日期 | 早报日期 |
| 早报原始内容 | 多行文本 | 完整的早报JSON数据 |
| AI处理后内容 | 多行文本 | 处理后的摘要内容 |
| 图片提示词1 | 单行文本 | 第一个图片提示词 |
| 图片提示词2 | 单行文本 | 第二个图片提示词 |
| 图片提示词3 | 单行文本 | 第三个图片提示词 |

## 📊 数据流程

```
1. 爬虫抓取新闻 → 2. AI处理内容 → 3. 格式转换 → 4. 写入飞书
```

### 详细流程
1. **新闻抓取**: 从多个AI科技网站抓取最新文章
2. **内容处理**: 使用AI生成摘要、分析趋势、创建图片提示词
3. **数据整理**: 将处理结果整理成结构化数据
4. **存储写入**: 将数据写入飞书多维表格

## 🛠️ 故障排除

### 常见问题

#### 1. 爬虫无法获取文章
```bash
# 检查网络连接
ping 36kr.com

# 检查选择器是否有效
python3 debug_content_processor.py
```

#### 2. 飞书连接失败
```bash
# 检查访问令牌
python3 test_feishu_config.py

# 检查表格token
python3 find_correct_token.py
```

#### 3. AI处理失败
```bash
# 检查API密钥
echo $DEEPSEEK_API_KEY

# 测试API连接
python3 test_deepseek.py
```

### 日志查看
```bash
# 查看爬虫日志
tail -f logs/crawler.log

# 查看错误日志
grep ERROR logs/crawler.log
```

## 📈 性能优化

### 爬虫优化
- 调整爬取间隔避免被封
- 使用代理IP（如需要）
- 优化选择器提高提取效率

### AI处理优化
- 批量处理文章提高效率
- 缓存处理结果避免重复
- 调整提示词优化输出质量

## 🔄 定时任务

### 设置定时爬取
```bash
# 使用crontab设置每天8点执行
0 8 * * * cd /path/to/ai-news && source venv/bin/activate && python3 crawler/main.py

# 或使用系统定时任务
python3 crawler/main.py --mode schedule
```

### 监控任务状态
```bash
# 检查任务是否正常运行
ps aux | grep python

# 查看最近执行日志
ls -la logs/
```

## 📞 技术支持

### 获取帮助
1. 查看日志文件了解错误详情
2. 运行测试脚本诊断问题
3. 检查配置文件是否正确
4. 参考项目文档和示例

### 常用命令
```bash
# 完整系统测试
python3 demo_full_workflow.py

# 快速功能测试
python3 quick_test.py

# 飞书配置测试
python3 test_feishu_config.py

# 爬虫功能测试
python3 simple_crawler_test.py
```

## 🎯 最佳实践

1. **定期更新**: 保持依赖包和选择器更新
2. **监控运行**: 设置日志监控和告警
3. **备份数据**: 定期备份重要配置和数据
4. **测试验证**: 部署前充分测试所有功能
5. **文档维护**: 及时更新配置和操作文档

