"""
Cloudflare Pages Functions 适配器 - 简化版本
处理所有 Flask 应用路由
"""

import sys
import os

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 导入 Flask 应用
try:
    from app import app as flask_app
except ImportError as e:
    print(f"Import error: {e}")
    flask_app = None

def on_request(context):
    """
    Cloudflare Pages Functions 入口点
    """
    request = context.request
    
    # 检查 Flask 应用是否加载成功
    if not flask_app:
        return Response("Flask app import failed", status=500)
    
    try:
        # 获取请求信息
        method = request.method
        url = request.url
        path = url.pathname
        query = url.search.lstrip('?') if url.search else ''
        
        # 构建完整URL
        full_url = path
        if query:
            full_url += '?' + query
        
        # 获取请求头
        headers = {}
        for key, value in request.headers.items():
            headers[key] = value
        
        # 使用 Flask 测试客户端处理请求
        with flask_app.test_client() as client:
            if method == 'GET':
                response = client.get(full_url, headers=headers)
            elif method == 'POST':
                # 简化POST处理
                response = client.post(full_url, headers=headers)
            else:
                response = client.open(full_url, method=method, headers=headers)
        
        # 构建响应头
        response_headers = {}
        for key, value in response.headers:
            response_headers[key] = value
        
        # 返回响应
        return Response(
            response.get_data(),
            status=response.status_code,
            headers=response_headers
        )
        
    except Exception as e:
        print(f"Error: {e}")
        
        # 简单的错误页面
        error_html = f"""<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
    <h1>Internal Server Error</h1>
    <p>Error: {str(e)}</p>
</body>
</html>"""
        
        return Response(error_html, status=500, headers={'Content-Type': 'text/html'})

# 注：Response 类由 Cloudflare Pages Functions 运行时提供 