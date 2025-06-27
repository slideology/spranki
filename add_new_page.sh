#!/bin/bash
# add_new_page.sh - 自动化新增页面脚本
# 用法: ./add_new_page.sh <页面名称>

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色信息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查参数
if [ -z "$1" ]; then
    print_error "缺少页面名称参数"
    echo "用法: ./add_new_page.sh <页面名称>"
    echo "例如: ./add_new_page.sh new-sprunki-game"
    exit 1
fi

PAGE_NAME=$1

# 验证页面名称格式
if [[ ! "$PAGE_NAME" =~ ^[a-z0-9-]+$ ]]; then
    print_error "页面名称只能包含小写字母、数字和连字符"
    print_info "有效示例: new-game, sprunki-mod-2024, game-123"
    exit 1
fi

print_info "开始添加新页面: $PAGE_NAME"

# 检查必要文件是否存在
if [ ! -f "app.py" ]; then
    print_error "app.py 文件不存在，请在项目根目录运行此脚本"
    exit 1
fi

if [ ! -f "generate_static.py" ]; then
    print_error "generate_static.py 文件不存在"
    exit 1
fi

if [ ! -d "templates" ]; then
    print_error "templates 目录不存在"
    exit 1
fi

# 第一次运行：创建模板文件
if [ ! -f "templates/$PAGE_NAME.html" ]; then
    print_info "创建模板文件..."
    
    # 检查是否有基础模板
    if [ -f "templates/game-template.html" ]; then
        cp templates/game-template.html templates/$PAGE_NAME.html
        print_success "已复制游戏模板到 templates/$PAGE_NAME.html"
    elif [ -f "templates/base.html" ]; then
        cp templates/base.html templates/$PAGE_NAME.html
        print_success "已复制基础模板到 templates/$PAGE_NAME.html"
    else
        print_error "找不到基础模板文件 (game-template.html 或 base.html)"
        exit 1
    fi
    
    print_warning "请完成以下步骤后再次运行此脚本:"
    print_info "1. 编辑 templates/$PAGE_NAME.html 文件"
    print_info "2. 在 app.py 中添加以下路由:"
    echo ""
    echo "@app.route('/$PAGE_NAME')"
    echo "def ${PAGE_NAME//-/_}():"
    echo "    return render_template('$PAGE_NAME.html',"
    echo "        title='页面标题',"
    echo "        description='页面描述'"
    echo "    )"
    echo ""
    print_info "完成后运行: ./add_new_page.sh $PAGE_NAME"
    exit 0
fi

# 检查路由是否存在
print_info "检查路由配置..."
if ! grep -q "/$PAGE_NAME" app.py; then
    print_error "在 app.py 中找不到 /$PAGE_NAME 路由"
    print_info "请添加以下路由到 app.py:"
    echo ""
    echo "@app.route('/$PAGE_NAME')"
    echo "def ${PAGE_NAME//-/_}():"
    echo "    return render_template('$PAGE_NAME.html',"
    echo "        title='页面标题',"
    echo "        description='页面描述'"
    echo "    )"
    exit 1
fi

print_success "找到路由配置"

# 测试路由是否正常工作
print_info "测试路由功能..."
python3 -c "
import sys
sys.path.append('.')
from app import app

with app.test_client() as client:
    response = client.get('/$PAGE_NAME')
    if response.status_code == 200:
        print('✅ 路由测试通过')
    else:
        print(f'❌ 路由测试失败: HTTP {response.status_code}')
        sys.exit(1)
" || {
    print_error "路由测试失败，请检查 app.py 中的路由配置"
    exit 1
}

# 生成静态文件
print_info "生成静态文件..."
python3 generate_static.py

# 检查生成结果
if [ -f "dist/$PAGE_NAME/index.html" ]; then
    print_success "页面生成成功: dist/$PAGE_NAME/index.html"
    
    # 显示文件大小
    file_size=$(ls -lh "dist/$PAGE_NAME/index.html" | awk '{print $5}')
    print_info "生成的文件大小: $file_size"
else
    print_error "页面生成失败"
    print_info "可能的原因:"
    print_info "1. 模板文件语法错误"
    print_info "2. 路由返回的变量缺失"
    print_info "3. 静态生成器配置问题"
    exit 1
fi

# 本地验证
print_info "启动本地预览服务器..."
print_info "可以在浏览器中访问: http://localhost:8000/$PAGE_NAME/"
print_info "按 Ctrl+C 停止服务器并继续部署"

# 后台启动服务器
cd dist && python3 -m http.server 8000 > /dev/null 2>&1 &
SERVER_PID=$!
cd ..

# 等待用户确认
echo ""
read -p "预览页面后，按回车键继续部署，或输入 'skip' 跳过预览: " user_input

# 停止服务器
kill $SERVER_PID 2>/dev/null || true

if [ "$user_input" = "skip" ]; then
    print_info "跳过预览，直接部署"
fi

# Git操作
print_info "提交到Git..."

# 检查是否有未提交的更改
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add .
    git commit -m "Add new page: $PAGE_NAME

- Created templates/$PAGE_NAME.html
- Added route /$PAGE_NAME in app.py  
- Generated static files in dist/$PAGE_NAME/"
    
    print_success "已提交更改到本地仓库"
else
    print_warning "没有检测到更改，跳过提交"
fi

# 推送到远程
read -p "是否推送到远程仓库并触发部署? (y/N): " push_confirm

if [[ $push_confirm =~ ^[Yy]$ ]]; then
    print_info "推送到远程仓库..."
    git push origin main
    print_success "推送完成!"
    
    print_info "Cloudflare Pages 正在自动部署..."
    print_info "通常需要 1-3 分钟完成"
    print_info "部署完成后可访问: https://spranki.art/$PAGE_NAME/"
else
    print_info "已跳过推送，你可以稍后手动执行:"
    print_info "git push origin main"
fi

echo ""
print_success "新页面添加完成!"
echo ""
print_info "📁 本地文件:"
print_info "   • 模板: templates/$PAGE_NAME.html"
print_info "   • 静态: dist/$PAGE_NAME/index.html"
echo ""
print_info "🌐 访问地址:"
print_info "   • 本地: http://localhost:8000/$PAGE_NAME/"
print_info "   • 线上: https://spranki.art/$PAGE_NAME/ (部署后)"
echo ""
print_info "🔧 后续操作:"
print_info "   • 如需修改页面，编辑 templates/$PAGE_NAME.html"
print_info "   • 修改后运行: python3 generate_static.py"
print_info "   • 然后提交并推送更改" 