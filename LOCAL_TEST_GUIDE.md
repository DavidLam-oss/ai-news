# 本地iPad协议微信助手测试指南

## 🎯 概述

本指南将帮助你在本地环境测试iPad协议微信助手功能，无需购买外部服务即可验证所有功能。

## 🚀 快速开始

### 第一步：启动模拟服务

```bash
# 方法一：使用启动脚本（推荐）
./start_mock_service.sh

# 方法二：直接运行Python脚本
python3 simple_mock_service.py

# 方法三：使用简化版本（推荐用于测试）
python3 simple_mock_service.py
```

### 第二步：验证服务运行

打开浏览器访问：
- **服务状态**: http://127.0.0.1:8081
- **健康检查**: http://127.0.0.1:8081/health
- **Webhook地址**: http://127.0.0.1:8081/webhook

### 第三步：运行测试脚本

```bash
# 测试iPad微信功能（基于curl，推荐）
python3 curl_based_test.py

# 测试原始iPad微信功能
python3 test_ipad_wechat.py

# 测试完整系统
python3 test_complete_system_with_wechat.py
```

## 📋 测试功能清单

### ✅ 基础功能测试

1. **连接测试**
   - 测试与模拟服务的连接
   - 验证session_id生成

2. **群列表获取**
   - 获取模拟群列表
   - 验证群信息格式

3. **消息发送**
   - 发送文本消息到单个群
   - 发送消息到多个群
   - 发送富文本消息

4. **高级功能**
   - 发送图片和文字
   - 发布朋友圈
   - 发送私聊消息

### 📊 模拟数据

模拟服务提供以下测试数据：

#### 群列表
- AI科技早报群 (25人)
- 技术交流群 (18人)
- 产品讨论群 (12人)
- 开发者社区 (35人)
- AI学习群 (28人)

#### 群成员
- 张三 (管理员)
- 李四 (成员)
- 王五 (成员)
- 赵六 (成员)

## 🔧 配置说明

### 环境变量配置

在 `.env` 文件中设置：

```bash
# iPad协议微信助手配置
IPAD_WEBHOOK_URL=http://127.0.0.1:8081/webhook
DEFAULT_GROUP_NAME=AI科技早报群
TARGET_GROUPS=AI科技早报群,技术交流群,产品讨论群

# 本地测试配置
LOCAL_TEST_MODE=true
MOCK_SERVICE_PORT=8081
```

### 测试数据配置

模拟服务会自动生成测试数据，包括：
- 模拟群列表
- 模拟群成员
- 模拟消息ID
- 模拟发送结果

## 🧪 测试用例

### 1. 基础连接测试

```python
from wechat.ipad_client import IpadWechatClient

client = IpadWechatClient()
connected = await client.connect()
print(f"连接状态: {'成功' if connected else '失败'}")
```

### 2. 群消息发送测试

```python
# 发送到单个群
success = await client.send_to_group(report, "AI科技早报群")

# 发送到多个群
target_groups = ["AI科技早报群", "技术交流群"]
results = await client.send_to_multiple_groups(report, target_groups)
```

### 3. 富文本消息测试

```python
# 发送富文本消息
success = await client.send_rich_message(report, "AI科技早报群")
```

### 4. 朋友圈发布测试

```python
# 发布朋友圈
content = "🤖 AI科技早报测试内容"
success = await client.publish_moment(content)
```

## 📈 测试结果示例

运行测试后，你会看到类似以下的输出：

```
🤖 测试iPad协议微信助手功能
==================================================

📡 第一步：测试连接...
✅ iPad微信客户端连接成功

📋 第二步：获取群列表...
✅ 获取到 5 个群:
  1. AI科技早报群 (25 人)
  2. 技术交流群 (18 人)
  3. 产品讨论群 (12 人)

💬 第四步：测试发送到单个群...
✅ 消息发送到单个群成功

📢 第五步：测试发送到多个群...
📊 多群发送结果:
   AI科技早报群: ✅ 成功
   技术交流群: ✅ 成功

🎨 第六步：测试富文本消息...
✅ 富文本消息发送成功

📱 第七步：测试朋友圈发布...
✅ 朋友圈发布成功

🎉 iPad协议微信助手测试完成！
```

## 🔍 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查端口是否被占用
   lsof -i :8080
   
   # 安装缺少的依赖
   pip install fastapi uvicorn
   ```

2. **连接失败**
   ```bash
   # 检查服务是否运行
   curl http://localhost:8080/health
   
   # 检查防火墙设置
   ```

3. **测试脚本错误**
   ```bash
   # 检查环境变量
   echo $IPAD_WEBHOOK_URL
   
   # 重新设置环境变量
   export IPAD_WEBHOOK_URL=http://localhost:8080/webhook
   ```

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 下一步

本地测试成功后，你可以：

1. **购买商业化服务**
   - 联系iPad协议服务商
   - 获取真实的webhook地址
   - 替换本地配置

2. **部署到服务器**
   - 将模拟服务部署到云服务器
   - 配置域名和SSL证书
   - 设置生产环境

3. **集成到生产系统**
   - 配置真实的微信群
   - 设置定时任务
   - 监控系统运行状态

## ⚠️ 注意事项

1. **仅用于测试**：模拟服务仅用于功能测试，不能发送真实消息
2. **数据安全**：测试数据不会保存，重启服务后重置
3. **性能限制**：模拟服务有延迟，模拟真实网络环境
4. **功能完整**：支持所有API接口，但返回模拟结果

---

**测试完成时间**: 2025-01-27  
**服务状态**: ✅ 本地测试环境就绪  
**下一步**: 运行测试脚本验证功能
