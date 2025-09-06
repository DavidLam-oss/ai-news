#!/bin/bash

# AI早报系统启动脚本

set -e

echo "🚀 启动AI早报系统..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python版本过低，需要3.8+，当前版本：$python_version"
    exit 1
fi

echo "✅ Python版本检查通过：$python_version"

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 安装Playwright浏览器
echo "🌐 安装Playwright浏览器..."
playwright install chromium
playwright install-deps chromium

# 检查环境变量文件
if [ ! -f ".env" ]; then
    if [ -f "config.env.example" ]; then
        echo "📝 创建环境变量文件..."
        cp config.env.example .env
        echo "⚠️  请编辑 .env 文件，填入必要的配置信息"
    else
        echo "❌ 未找到环境变量示例文件"
        exit 1
    fi
fi

# 创建必要的目录
echo "📁 创建必要目录..."
mkdir -p logs data

# 检查Redis是否运行
echo "🔍 检查Redis服务..."
if ! pgrep -x "redis-server" > /dev/null; then
    echo "⚠️  Redis服务未运行，请先启动Redis"
    echo "    macOS: brew services start redis"
    echo "    Ubuntu: sudo systemctl start redis"
    echo "    Docker: docker run -d -p 6379:6379 redis:alpine"
fi

# 启动服务
echo "🎯 选择启动模式："
echo "1) API服务模式"
echo "2) 定时任务模式"
echo "3) 单次爬取模式"
echo "4) 开发模式（API + 定时任务）"

read -p "请选择模式 (1-4): " mode

case $mode in
    1)
        echo "🚀 启动API服务..."
        python api/server.py
        ;;
    2)
        echo "⏰ 启动定时任务..."
        python crawler/main.py --mode schedule
        ;;
    3)
        echo "🕷️  执行单次爬取..."
        python crawler/main.py --mode once
        ;;
    4)
        echo "🔧 启动开发模式..."
        echo "启动API服务..."
        python api/server.py &
        API_PID=$!
        
        echo "启动定时任务..."
        python crawler/main.py --mode schedule &
        SCHEDULER_PID=$!
        
        echo "✅ 服务已启动"
        echo "API服务PID: $API_PID"
        echo "定时任务PID: $SCHEDULER_PID"
        echo "按Ctrl+C停止所有服务"
        
        # 等待中断信号
        trap "kill $API_PID $SCHEDULER_PID; exit" INT
        wait
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
