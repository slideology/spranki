# 🔄 **迁移备份记录**
> 创建时间: 2024年今天
> 迁移项目: spranki.art (Vercel → Cloudflare Pages)

## 📋 **当前 Vercel 配置备份**

### **vercel.json 配置**
```json
{
    "version": 2,
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python",
            "config": {
                "runtime": "python3.8"
            }
        }
    ],
    "routes": [
        {
            "src": "^/(.*)$",
            "has": [{"type": "host", "value": "www.spranki.art"}],
            "status": 301,
            "headers": {"Location": "https://spranki.art/$1"}
        },
        {
            "src": "^/(.*)$",
            "has": [{"type": "header", "key": "x-forwarded-proto", "value": "http"}],
            "status": 301,
            "headers": {"Location": "https://spranki.art/$1"}
        },
        {
            "src": "/internet-roadtrip",
            "dest": "app.py"
        },
        {
            "src": "/(.*)",
            "dest": "app.py"
        }
    ]
}
```

## 🌐 **当前 Cloudflare DNS 配置备份**

### **DNS 记录**
| 类型 | 名称 | 内容 | 代理状态 | TTL |
|------|------|------|----------|-----|
| A | spranki.art | 76.76.21.98 | 🟠 Proxied | Auto |
| A | spranki.art | 76.76.21.21 | 🟠 Proxied | Auto |
| CNAME | www | cname.vercel-dns.com | 🟠 Proxied | Auto |
| TXT | spranki.art | google-site-verification-... | DNS only | 1 hr |

### **SSL/TLS 配置**
- **加密模式**: Full (strict)
- **自动 HTTPS 重写**: 启用
- **HSTS**: 启用

### **安全设置**
- **防火墙**: 启用
- **DDoS 防护**: 启用
- **Bot Fight Mode**: 启用

## 📦 **项目依赖备份**

### **requirements.txt**
```
Flask==2.3.3
python-dotenv==1.0.0
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2
```

### **项目结构**
```
spranki.art/
├── app.py (主应用, 488行)
├── vercel.json (Vercel配置)
├── requirements.txt (Python依赖)
├── templates/ (HTML模板, 40+文件)
├── static/ (静态资源)
│   ├── data/faq.json
│   ├── robots.txt
│   ├── sitemap.xml
│   └── ads.txt
├── models.py (数据模型)
└── init_db.py (数据库初始化)
```

## 🔄 **回滚方案**

如果迁移失败，回滚步骤：

1. **DNS 回滚 (2分钟)**
   ```
   spranki.art A → 76.76.21.98
   spranki.art A → 76.76.21.21
   www CNAME → cname.vercel-dns.com
   ```

2. **Vercel 重新启用**
   - 重新部署 main 分支
   - 确认域名绑定

3. **代码回滚**
   ```bash
   git checkout main
   git branch -D cloudflare-migration
   ```

## 📊 **性能基准 (迁移前)**
> 将在迁移后对比

- **待测试**: 首屏加载时间
- **待测试**: 静态资源加载
- **待测试**: 函数响应时间
- **待测试**: 全球访问延迟

---
**备份完成时间**: 等待执行
**负责人**: AI助手
**确认人**: 用户 