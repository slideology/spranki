#!/bin/bash

# 🚀 Spranki.art 自动部署脚本
# 从Vercel迁移到Cloudflare Pages静态部署

echo "🎯 开始部署 Spranki.art 静态站点..."
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查Flask依赖
if ! python3 -c "import flask" &> /dev/null; then
    echo "❌ Flask 未安装，请运行: pip install flask"
    exit 1
fi

# 清理旧的构建文件
echo "🧹 清理旧文件..."
rm -rf dist/

# 生成静态站点
echo "🔄 生成静态站点..."
python3 generate_static.py

# 检查生成结果
if [ ! -d "dist" ]; then
    echo "❌ 静态站点生成失败"
    exit 1
fi

echo "📊 生成统计:"
echo "  - HTML文件: $(find dist -name "*.html" | wc -l) 个"
echo "  - 总大小: $(du -sh dist | cut -f1)"

# 检查关键文件
if [ ! -f "dist/index.html" ]; then
    echo "❌ 首页文件缺失"
    exit 1
fi

if [ ! -f "dist/robots.txt" ]; then
    echo "❌ robots.txt 文件缺失"
    exit 1
fi

echo "✅ 静态站点生成完成！"
echo ""
echo "🚀 部署步骤:"
echo "1. 提交代码到 GitHub"
echo "2. 在 Cloudflare Pages 中连接 GitHub 仓库"
echo "3. 设置构建命令: python3 generate_static.py"
echo "4. 设置输出目录: dist"
echo "5. 更新 DNS 记录指向 Cloudflare Pages"
echo ""
echo "📁 构建产物位置: ./dist/"
echo "👀 本地预览: 打开 dist/index.html" 