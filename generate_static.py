#!/usr/bin/env python3
"""
静态站点生成器
将Flask应用的所有页面预渲染为静态HTML文件
"""

import os
import sys
import shutil
from pathlib import Path
import time
from urllib.parse import urlparse

# 导入Flask应用
from app import app

class StaticSiteGenerator:
    def __init__(self, flask_app, output_dir='dist'):
        """
        初始化静态站点生成器
        
        Args:
            flask_app: Flask应用实例
            output_dir: 输出目录
        """
        self.app = flask_app
        self.output_dir = Path(output_dir)
        self.generated_count = 0
        self.failed_count = 0
        self.failed_routes = []
        
        # 需要生成的所有路由
        self.routes_to_generate = [
            '/', '/about', '/faq', '/contact', '/game', '/introduction',
            '/dadish', '/god-simulator', '/internet-roadtrip', '/ssspicy',
            '/incredibox-rainbow-animal', '/incredibox-irrelevant-reunion',
            '/sprunka', '/sprunki-1996', '/sprunki-agents', '/sprunki-angry',
            '/sprunki-banana', '/sprunki-banana-porridge', '/sprunki-brud-edition-finale',
            '/sprunki-chaotic-good', '/sprunki-dx', '/sprunki-fiddlebops',
            '/sprunki-garnold', '/sprunki-grown-up', '/sprunki-idle-clicker',
            '/sprunki-ketchup', '/sprunki-lily', '/sprunki-megalovania',
            '/sprunki-misfismix', '/sprunki-parodybox', '/sprunki-phase-1-7',
            '/sprunki-phase-19-update', '/sprunki-phase-6-definitive',
            '/sprunki-phase-6-definitive-all-alive', '/sprunki-phase-6-definitive-remaster',
            '/sprunki-phase-777-3-7', '/sprunki-pyramixed', '/sprunki-pyramixed-melophobia',
            '/sprunki-pyramixed-regretful', '/sprunki-pyramixed-ultimate-deluxe',
            '/sprunki-retake-but-human', '/sprunki-retake-new-human',
            '/sprunki-shatter', '/sprunki-spfundi', '/sprunki-sploinkers',
            '/sprunki-sprunkr', '/sprunki-sprunksters', '/sprunki-sprured',
            '/sprunki-spruted', '/sprunki-swap-retextured', '/sprunki-ultimate-deluxe',
            '/sprunki-upin-ipin', '/sprunki-wenda-edition', '/sprunklings',
            '/yet-another-boring-old-sprunki-mod'
        ]
        
        # 特殊文件路由（直接文件访问）
        self.special_files = [
            '/robots.txt', '/sitemap.xml', '/ads.txt'
        ]
    
    def setup_output_directory(self):
        """设置输出目录"""
        if self.output_dir.exists():
            print(f"🗑️  清理现有目录: {self.output_dir}")
            shutil.rmtree(self.output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建输出目录: {self.output_dir}")
        
        # 复制静态文件
        static_src = Path('static')
        static_dst = self.output_dir / 'static'
        
        if static_src.exists():
            shutil.copytree(static_src, static_dst)
            print(f"📂 复制静态文件: {static_src} -> {static_dst}")
    
    def get_file_path_for_route(self, route):
        """获取路由对应的文件路径"""
        if route == '/':
            return self.output_dir / 'index.html'
        elif route in self.special_files:
            # 特殊文件直接放在根目录
            filename = route.lstrip('/')
            return self.output_dir / filename
        else:
            # 其他路由创建目录结构
            clean_route = route.strip('/')
            route_dir = self.output_dir / clean_route
            route_dir.mkdir(parents=True, exist_ok=True)
            return route_dir / 'index.html'
    
    def generate_page(self, route):
        """
        生成单个页面
        
        Args:
            route: 路由路径，如 '/' 或 '/about'
            
        Returns:
            bool: 生成是否成功
        """
        try:
            with self.app.test_client() as client:
                print(f"🔄 生成页面: {route}")
                
                # 发送GET请求获取页面内容
                response = client.get(route)
                
                if response.status_code != 200:
                    print(f"❌ 页面请求失败: {route} (状态码: {response.status_code})")
                    return False
                
                # 获取响应内容
                content = response.get_data(as_text=True)
                
                # 确定输出文件路径
                file_path = self.get_file_path_for_route(route)
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                file_size = len(content.encode('utf-8'))
                print(f"✅ 生成成功: {route} -> {file_path} ({file_size:,} bytes)")
                
                self.generated_count += 1
                return True
                
        except Exception as e:
            print(f"❌ 生成失败: {route} - 错误: {str(e)}")
            self.failed_count += 1
            self.failed_routes.append(route)
            return False
    
    def generate_contact_page_static(self):
        """
        生成联系页面的静态版本（只包含GET内容）
        POST功能将由API Function处理
        """
        return self.generate_page('/contact')
    
    def generate_all(self):
        """生成所有页面"""
        print("🚀 开始生成静态站点...")
        print(f"📊 计划生成 {len(self.routes_to_generate + self.special_files)} 个页面")
        print("-" * 60)
        
        start_time = time.time()
        
        # 设置输出目录
        self.setup_output_directory()
        print()
        
        # 生成常规页面
        for route in self.routes_to_generate:
            self.generate_page(route)
            time.sleep(0.1)  # 短暂暂停，避免过快请求
        
        # 生成特殊文件
        print("\n📄 生成特殊文件...")
        for route in self.special_files:
            self.generate_page(route)
        
        # 生成报告
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 生成报告")
        print("=" * 60)
        print(f"✅ 成功生成: {self.generated_count} 个页面")
        print(f"❌ 生成失败: {self.failed_count} 个页面")
        print(f"⏱️  总耗时: {duration:.2f} 秒")
        print(f"📁 输出目录: {self.output_dir.absolute()}")
        
        if self.failed_routes:
            print(f"\n❌ 失败的页面:")
            for route in self.failed_routes:
                print(f"   - {route}")
        
        return self.failed_count == 0

def main():
    """主函数"""
    print("🎯 Spranki.art 静态站点生成器")
    print("=" * 60)
    
    # 创建生成器
    generator = StaticSiteGenerator(app)
    
    # 生成所有页面
    success = generator.generate_all()
    
    if success:
        print("\n🎉 静态站点生成完成！")
        print(f"👀 预览: 打开 {generator.output_dir}/index.html")
    else:
        print("\n⚠️  生成过程中有错误，请检查失败的页面")
        sys.exit(1)

if __name__ == "__main__":
    main() 