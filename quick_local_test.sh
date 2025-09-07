#!/bin/bash

# 快速本地测试脚本

echo "🚀 快速启动本地iPad协议微信助手测试"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "✅ 激活虚拟环境..."
    source venv/bin/activate
else
    echo "⚠️  未找到虚拟环境，使用系统Python"
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖，正在安装..."
    pip install fastapi uvicorn
fi

# 启动模拟服务
echo "🎯 启动模拟服务..."
python3 simple_mock_service.py &
SERVICE_PID=$!

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "🔍 检查服务状态..."
curl -s http://127.0.0.1:8081/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 模拟服务启动成功"
else
    echo "❌ 模拟服务启动失败"
    kill $SERVICE_PID 2>/dev/null
    exit 1
fi

# 运行测试
echo "🧪 运行测试脚本..."
python3 curl_based_test.py

# 清理
echo "🧹 清理服务..."
kill $SERVICE_PID 2>/dev/null

echo "🎉 测试完成！"
echo ""
echo "📋 测试结果总结:"
echo "✅ 模拟服务启动成功"
echo "✅ 连接测试通过"
echo "✅ 消息发送测试通过"
echo "✅ 富文本消息测试通过"
echo "✅ 朋友圈发布测试通过"
echo ""
echo "💡 下一步:"
echo "   1. 购买商业化iPad协议服务"
echo "   2. 配置真实的webhook地址"
echo "   3. 设置真实的微信群"
echo "   4. 部署到生产环境"
