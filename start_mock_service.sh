#!/bin/bash

# 启动模拟iPad协议微信助手服务

echo "🚀 启动模拟iPad协议微信助手服务..."
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 检测到虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  建议在虚拟环境中运行"
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖，正在安装..."
    pip install fastapi uvicorn
fi

# 启动服务
echo "🎯 启动服务..."
echo "📡 服务地址: http://localhost:8080"
echo "🔗 Webhook地址: http://localhost:8080/webhook"
echo "📋 健康检查: http://localhost:8080/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=================================="

python3 mock_ipad_service.py
