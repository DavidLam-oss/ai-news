# AI早报系统

基于飞书多维表格的智能AI早报系统，每天自动抓取全网AI科技信息，通过AI处理生成精美早报，并自动发送到微信群聊。

## 系统架构

```
AI爬虫服务 → 飞书多维表格 → AI内容处理 → 微信助手 → 群聊/朋友圈
```

## 功能特性

- 🤖 **智能爬虫**: 基于crawl4ai，自动抓取全网AI科技资讯
- 📊 **多维表格**: 飞书多维表格存储和管理早报数据
- 🎨 **AI处理**: 使用DeepSeek优化内容，生成图片提示词
- 📱 **自动推送**: 自动发送到微信群聊和朋友圈
- ⏰ **定时任务**: 每天自动执行，无需人工干预

## 项目结构

```
ai-news/
├── crawler/          # AI爬虫服务
├── feishu/          # 飞书多维表格配置
├── wechat/          # 微信助手集成
├── config/          # 配置文件
├── docs/            # 文档
└── README.md        # 项目说明
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- 飞书开发者账号
- 微信开发者账号

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖
npm install
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件，填入相关配置
```

### 4. 启动服务

```bash
# 启动爬虫服务
python crawler/main.py

# 启动API服务
python api/main.py
```

## 使用说明

### 配置飞书多维表格

1. 创建多维表格，包含以下字段：
   - 日期 (日期类型)
   - 早报原始内容 (多行文本)
   - AI处理后内容 (多行文本)
   - 图片提示词1 (单行文本)
   - 图片提示词2 (单行文本)
   - 图片提示词3 (单行文本)
   - 生成图片 (附件)

### 配置自动化工作流

1. 在多维表格中创建自动化流程
2. 设置定时触发（每天上午8点）
3. 添加HTTP请求动作，调用爬虫API
4. 添加AI处理动作，优化内容
5. 添加微信发送动作，推送到群聊

## API接口

### 爬虫服务

- `GET /api/news` - 获取最新AI资讯
- `POST /api/process` - 处理早报内容
- `GET /api/health` - 健康检查

### 微信助手

- `POST /api/wechat/send` - 发送消息到群聊
- `POST /api/wechat/moment` - 发布朋友圈

## 部署说明

### Docker部署

```bash
# 构建镜像
docker build -t ai-news .

# 运行容器
docker run -d -p 8000:8000 ai-news
```

### 服务器部署

```bash
# 使用PM2管理进程
pm2 start ecosystem.config.js
```

## 注意事项

1. 请遵守各平台的API使用规范
2. 注意爬虫频率，避免对目标网站造成压力
3. 定期更新爬虫规则，适应网站结构变化
4. 保护API密钥和访问令牌安全

## 项目完成情况

✅ **已完成功能**
- [x] AI爬虫服务 - 基于crawl4ai实现智能爬虫
- [x] 新闻源管理 - 支持8个主流AI科技媒体
- [x] AI内容处理 - 使用OpenAI/DeepSeek优化内容
- [x] 飞书多维表格集成 - 完整的数据存储和管理
- [x] 微信助手集成 - 支持群聊和朋友圈推送
- [x] RESTful API服务 - 完整的API接口
- [x] 自动化工作流 - 定时任务和流程自动化
- [x] Docker容器化 - 支持Docker部署
- [x] 完整的文档 - 使用说明和配置指南

## 快速体验

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd ai-news

# 2. 运行演示
python3 simple_demo.py

# 3. 部署系统
./deploy.sh

# 4. 启动服务
./start.sh
```

## 更新日志

- v1.0.0 - 初始版本，基础功能实现
- v1.1.0 - 增加图片生成功能
- v1.2.0 - 优化AI处理逻辑
- v1.3.0 - 完成完整系统架构，支持生产部署

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

MIT License