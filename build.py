#!/usr/bin/env python3
"""
Cloudflare Pages 构建脚本
确保所有依赖都正确安装
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装 Python 依赖"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def verify_app():
    """验证 Flask 应用是否可以导入"""
    print("Verifying Flask app...")
    try:
        from app import app
        print("Flask app imported successfully!")
        return True
    except ImportError as e:
        print(f"Failed to import Flask app: {e}")
        return False

def main():
    """主构建流程"""
    print("Starting Cloudflare Pages build...")
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 验证应用
    if not verify_app():
        sys.exit(1)
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main() 