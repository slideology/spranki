# Cloudflare Pages 快速迁移指南

> 基于 spranki.art 成功迁移经验，适用于其他网站的快速迁移

## 🔍 迁移前评估 (15分钟)

### 1. 网站类型判断
```bash
# 检查是否适合静态化
✅ 内容展示为主
✅ 少量动态功能
✅ SEO要求高

❌ 复杂用户交互  
❌ 实时数据处理
❌ 文件上传功能
```

### 2. 技术栈分析
```bash
# 路由扫描
python -c "
from your_app import app
for rule in app.url_map.iter_rules():
    print(f'{rule.rule} - {rule.methods}')
"

# 依赖检查
pip list | grep -E "(flask|django|fastapi)"
```

### 3. 功能清单
- [ ] 路由总数: ___个
- [ ] 静态页面: ___个  
- [ ] 动态API: ___个
- [ ] 表单功能: ___个
- [ ] 文件上传: ___个

## ⚡ 快速实施步骤

### 步骤1: 创建静态生成器 (30分钟)

```python
# generate_static.py
import os
import shutil
from flask import Flask
from your_app import app  # 替换为你的应用

class StaticGenerator:
    def __init__(self, app, output_dir='dist'):
        self.app = app
        self.output_dir = output_dir
    
    def generate_all(self):
        # 清理输出目录
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        
        # 获取所有路由
        routes = []
        for rule in self.app.url_map.iter_rules():
            if 'GET' in rule.methods and not rule.rule.startswith('/api'):
                routes.append(rule.rule)
        
        # 生成页面
        with self.app.test_client() as client:
            for route in routes:
                try:
                    response = client.get(route)
                    if response.status_code == 200:
                        self.save_page(route, response.data)
                        print(f"✅ {route}")
                    else:
                        print(f"❌ {route} - {response.status_code}")
                except Exception as e:
                    print(f"🔥 {route} - {e}")
        
        # 复制静态文件
        if os.path.exists('static'):
            shutil.copytree('static', f'{self.output_dir}/static')
    
    def save_page(self, route, content):
        # 创建目录结构
        if route == '/':
            file_path = f'{self.output_dir}/index.html'
        else:
            dir_path = f'{self.output_dir}{route}'
            os.makedirs(dir_path, exist_ok=True)
            file_path = f'{dir_path}/index.html'
        
        # 保存文件
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(content)

if __name__ == "__main__":
    generator = StaticGenerator(app)
    generator.generate_all()
    print("🎉 静态网站生成完成！")
```

### 步骤2: Cloudflare Pages 配置 (10分钟)

#### wrangler.toml
```toml
name = "your-site-name"
compatibility_date = "2024-12-27"

[env.production]
route = "*yourdomain.com/*"
```

#### _headers
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Cache-Control: public, max-age=31536000

/*.html
  Cache-Control: public, max-age=3600
```

#### _redirects
```
# HTTP to HTTPS
http://yourdomain.com/* https://yourdomain.com/:splat 301!

# WWW redirect (根据需要选择)
https://www.yourdomain.com/* https://yourdomain.com/:splat 301!
```

### 步骤3: 部署配置 (5分钟)

#### build.sh
```bash
#!/bin/bash
echo "🚀 构建静态网站..."
python3 generate_static.py
echo "✅ 构建完成!"
```

#### 简化 requirements.txt
```txt
Flask==2.3.3
# 移除不必要的依赖
# smtplib (内置)
# email (内置)
```

### 步骤4: GitHub 设置 (5分钟)

```bash
# 提交代码
git add .
git commit -m "Add static site generator"
git push origin main
```

### 步骤5: Cloudflare Pages 部署 (10分钟)

1. **创建项目**
   - 连接 GitHub 仓库
   - 选择分支: `main`

2. **构建设置**
   ```
   Framework preset: None
   Build command: chmod +x build.sh && ./build.sh
   Build output directory: dist
   Root directory: /
   ```

3. **环境变量** (如果需要)
   ```
   PYTHON_VERSION=3.9
   ```

### 步骤6: 域名配置 (10分钟)

1. **添加自定义域名**
   - 在 Cloudflare Pages 项目中添加域名
   - 验证 DNS 记录

2. **DNS 设置**
   ```
   Type: CNAME
   Name: @
   Target: your-project.pages.dev
   Proxy: Enabled
   ```

## 🚨 常见问题快速解决

### 问题1: 页面生成失败
```bash
# 检查模板文件
find templates/ -name "*.html" | wc -l

# 创建缺失模板
cp templates/base.html templates/missing-page.html
```

### 问题2: 404错误
```bash
# 删除冲突配置
rm -rf functions/
rm _routes.json

# 检查构建输出
ls -la dist/
```

### 问题3: 静态资源404
```bash
# 检查资源路径
grep -r "href=\|src=" dist/ | head -5

# 修复相对路径
sed -i 's|href="/static|href="./static|g' dist/**/*.html
```

## 📋 检查清单

### 迁移前
- [ ] 备份原网站
- [ ] 记录DNS设置  
- [ ] 测试核心功能
- [ ] 准备回滚方案

### 迁移中
- [ ] 生成器测试通过
- [ ] 所有页面生成成功
- [ ] 静态资源正确复制
- [ ] 构建配置正确

### 迁移后
- [ ] 网站正常访问
- [ ] 核心页面功能正常
- [ ] SEO标签完整
- [ ] 性能符合预期

## 🎯 成功指标

- **页面生成成功率**: >95%
- **首屏加载时间**: <500ms
- **构建时间**: <10分钟  
- **SEO分数**: 保持或提升

## 📞 紧急回滚方案

```bash
# DNS快速回滚
# 1. 修改DNS记录指向原服务器
# 2. 等待DNS传播 (5-30分钟)  
# 3. 验证网站恢复

# Git回滚
git revert HEAD
git push origin main
```

---

💡 **提示**: 这个指南基于 spranki.art 的成功迁移经验，根据你的具体情况调整实施细节。重点是**快速验证可行性**和**渐进式迁移**。 