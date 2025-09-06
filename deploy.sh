#!/bin/bash

# AI早报系统部署脚本

set -e

echo "🚀 AI早报系统部署脚本"
echo "========================"

# 检查系统环境
check_environment() {
    echo "🔍 检查系统环境..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装，请先安装Python 3.8+"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 未安装，请先安装pip"
        exit 1
    fi
    
    # 检查Docker（可选）
    if command -v docker &> /dev/null; then
        echo "✅ Docker 已安装"
        DOCKER_AVAILABLE=true
    else
        echo "⚠️  Docker 未安装，将使用本地部署"
        DOCKER_AVAILABLE=false
    fi
    
    # 检查Redis
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            echo "✅ Redis 服务运行正常"
        else
            echo "⚠️  Redis 未运行，请启动Redis服务"
        fi
    else
        echo "⚠️  Redis 未安装，请安装Redis"
    fi
    
    echo "✅ 环境检查完成"
}

# 安装依赖
install_dependencies() {
    echo "📦 安装系统依赖..."
    
    # 检测操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "🍺 使用Homebrew安装依赖..."
            brew install redis node
        else
            echo "⚠️  请安装Homebrew或手动安装Redis和Node.js"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "🐧 使用apt安装依赖..."
            sudo apt-get update
            sudo apt-get install -y redis-server nodejs npm
        elif command -v yum &> /dev/null; then
            echo "🐧 使用yum安装依赖..."
            sudo yum install -y redis nodejs npm
        else
            echo "⚠️  请手动安装Redis和Node.js"
        fi
    fi
}

# 设置Python环境
setup_python_env() {
    echo "🐍 设置Python环境..."
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装Python依赖
    echo "📥 安装Python依赖..."
    pip install -r requirements.txt
    
    # 安装Playwright浏览器
    echo "🌐 安装Playwright浏览器..."
    playwright install chromium
    playwright install-deps chromium
    
    echo "✅ Python环境设置完成"
}

# 配置环境变量
setup_environment() {
    echo "⚙️  配置环境变量..."
    
    if [ ! -f ".env" ]; then
        if [ -f "config.env.example" ]; then
            cp config.env.example .env
            echo "📝 已创建 .env 文件"
            echo "⚠️  请编辑 .env 文件，填入必要的配置信息："
            echo "   - OPENAI_API_KEY"
            echo "   - FEISHU_APP_ID 和 FEISHU_APP_SECRET"
            echo "   - WECHAT_APP_ID 和 WECHAT_APP_SECRET"
        else
            echo "❌ 未找到环境变量示例文件"
            exit 1
        fi
    else
        echo "✅ .env 文件已存在"
    fi
}

# 创建必要目录
create_directories() {
    echo "📁 创建必要目录..."
    
    mkdir -p logs data
    
    echo "✅ 目录创建完成"
}

# Docker部署
deploy_with_docker() {
    echo "🐳 使用Docker部署..."
    
    if [ "$DOCKER_AVAILABLE" = true ]; then
        # 构建镜像
        echo "🔨 构建Docker镜像..."
        docker build -t ai-news .
        
        # 启动服务
        echo "🚀 启动Docker服务..."
        docker-compose up -d
        
        echo "✅ Docker部署完成"
        echo "📊 服务状态："
        docker-compose ps
    else
        echo "❌ Docker不可用，跳过Docker部署"
    fi
}

# 本地部署
deploy_locally() {
    echo "💻 本地部署..."
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 测试系统
    echo "🧪 运行系统测试..."
    python test_system.py
    
    echo "✅ 本地部署完成"
    echo "🚀 使用以下命令启动服务："
    echo "   ./start.sh"
}

# 启动服务
start_services() {
    echo "🎯 选择启动方式："
    echo "1) 立即启动服务"
    echo "2) 稍后手动启动"
    
    read -p "请选择 (1-2): " choice
    
    case $choice in
        1)
            echo "🚀 启动服务..."
            ./start.sh
            ;;
        2)
            echo "⏰ 稍后请运行 ./start.sh 启动服务"
            ;;
        *)
            echo "⏰ 稍后请运行 ./start.sh 启动服务"
            ;;
    esac
}

# 显示部署信息
show_deployment_info() {
    echo ""
    echo "🎉 部署完成！"
    echo "========================"
    echo "📋 部署信息："
    echo "   - 项目目录: $(pwd)"
    echo "   - Python环境: venv/"
    echo "   - 配置文件: .env"
    echo "   - 日志目录: logs/"
    echo "   - 数据目录: data/"
    echo ""
    echo "🚀 启动命令："
    echo "   ./start.sh"
    echo ""
    echo "📊 服务地址："
    echo "   - API服务: http://localhost:8000"
    echo "   - 健康检查: http://localhost:8000/health"
    echo "   - API文档: http://localhost:8000/docs"
    echo ""
    echo "📚 文档："
    echo "   - 使用说明: docs/usage.md"
    echo "   - 飞书配置: feishu/table_config.md"
    echo ""
    echo "🔧 管理命令："
    echo "   - 测试系统: python test_system.py"
    echo "   - 查看日志: tail -f logs/*.log"
    echo "   - 停止服务: Ctrl+C"
}

# 主函数
main() {
    echo "开始部署AI早报系统..."
    
    # 检查环境
    check_environment
    
    # 询问是否安装系统依赖
    read -p "是否安装系统依赖？(y/n): " install_deps
    if [ "$install_deps" = "y" ] || [ "$install_deps" = "Y" ]; then
        install_dependencies
    fi
    
    # 设置Python环境
    setup_python_env
    
    # 配置环境变量
    setup_environment
    
    # 创建目录
    create_directories
    
    # 选择部署方式
    echo "🎯 选择部署方式："
    echo "1) Docker部署（推荐）"
    echo "2) 本地部署"
    
    read -p "请选择 (1-2): " deploy_choice
    
    case $deploy_choice in
        1)
            deploy_with_docker
            ;;
        2)
            deploy_locally
            ;;
        *)
            deploy_locally
            ;;
    esac
    
    # 显示部署信息
    show_deployment_info
    
    # 询问是否启动服务
    start_services
}

# 运行主函数
main "$@"
