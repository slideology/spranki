#!/bin/bash

# Cloudflare Pages 构建脚本
echo "🎯 开始构建 Spranki.art 静态站点..."

# 检查Python版本
if command -v python3 &> /dev/null; then
    echo "✅ 使用 Python3"
    python3 generate_static.py
elif command -v python &> /dev/null; then
    echo "✅ 使用 Python"
    python generate_static.py
else
    echo "❌ 未找到Python环境"
    exit 1
fi

echo "🎉 构建完成！" 