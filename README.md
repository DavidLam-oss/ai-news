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

#### 方法一：使用配置脚本（推荐）

```bash
# 运行飞书配置脚本
python3 setup_feishu_config.py
```

#### 方法二：手动配置

```bash
# 复制配置文件模板
cp config.env.example .env

# 编辑.env文件，填入相关配置
# 飞书配置示例：
# FEISHU_APP_ID=cli_a8366b7ef13a100c
# FEISHU_APP_SECRET=5nkWuj9xfU5bjg0qEJBcKhmX1H1ptjvr
# FEISHU_BASE_URL=https://open.feishu.cn/open-apis
# FEISHU_TABLE_TOKEN=F5I2bdNZxawzTqsRBVbcJWEMn9H
```

#### 飞书配置说明

1. **获取飞书应用凭证**：
   - 登录[飞书开放平台](https://open.feishu.cn/)
   - 创建企业自建应用
   - 在"凭证与基础信息"中获取 App ID 和 App Secret

2. **配置多维表格**：
   - 创建多维表格，包含以下字段：
     - 日期 (日期类型)
     - 早报原始内容 (多行文本)
     - AI处理后内容 (多行文本)
     - 图片提示词1 (单行文本)
     - 图片提示词2 (单行文本)
     - 图片提示词3 (单行文本)
     - 生成图片 (附件)
   - 获取表格token并配置到 `FEISHU_TABLE_TOKEN`

3. **配置应用权限**：
   ```bash
   # 运行权限申请工具
   python3 request_feishu_permissions.py
   ```
   
   或者手动申请权限：
   - 登录[飞书开放平台](https://open.feishu.cn/)
   - 进入应用管理后台
   - 添加以下必需权限：
     - `bitable:app:readonly` - 多维表格应用只读权限
     - `bitable:app` - 多维表格应用权限
     - `base:app:read` - 基础应用读取权限
     - `base:table:read` - 基础表格读取权限
     - `base:record:retrieve` - 基础记录检索权限
     - `base:record:create` - 基础记录创建权限
     - `base:record:update` - 基础记录更新权限
   - 创建新版本并发布
   - 等待管理员审核通过

4. **测试配置**：
   ```bash
   python3 test_feishu_config.py
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

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 快速本地测试（推荐）
./quick_local_test.sh

# 4. 运行完整工作流程演示
python3 demo_full_workflow.py

# 5. 运行简化爬虫测试
python3 simple_crawler_test.py

# 6. 测试飞书连接
python3 test_feishu_config.py

# 7. 部署系统
./deploy.sh

# 8. 启动服务
./start.sh
```

## 本地测试指南

### iPad协议微信助手本地测试

无需购买外部服务，即可在本地测试所有微信功能：

```bash
# 快速测试（一键完成）
./quick_local_test.sh

# 手动测试步骤
# 1. 启动模拟服务
python3 simple_mock_service.py

# 2. 运行测试脚本
python3 curl_based_test.py
```

详细说明请查看：[LOCAL_TEST_GUIDE.md](./LOCAL_TEST_GUIDE.md)

## 🎉 系统测试状态

### ✅ 已验证功能
- **爬虫引擎**: Crawl4AI 0.7.4 正常工作
- **AI内容处理**: DeepSeek API 集成正常
- **飞书API连接**: 访问令牌获取成功
- **数据格式转换**: 爬虫数据到飞书格式转换正常

### ⚠️ 需要配置
- **飞书多维表格**: 需要正确的表格token
- **应用权限**: 需要配置相关权限

### 📊 测试结果
详细测试结果请查看: [TEST_RESULTS.md](./TEST_RESULTS.md)

## 更新日志

- v1.0.0 - 初始版本，基础功能实现
- v1.1.0 - 增加图片生成功能
- v1.2.0 - 优化AI处理逻辑
- v1.3.0 - 完成完整系统架构，支持生产部署

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

MIT License