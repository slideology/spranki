"""
Cloudflare Pages Functions 适配器 - 调试版本
"""

def on_request(context):
    """
    Cloudflare Pages Functions 入口点
    """
    request = context.request
    
    try:
        # 首先测试基本功能
        if request.url.pathname == "/test-function":
            return Response("Functions are working!", status=200)
        
        # 尝试导入 Flask 应用
        import sys
        import os
        
        # 添加项目根目录到 Python 路径
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        # 调试信息
        debug_info = f"""
        <h1>Debug Information</h1>
        <p><strong>Path:</strong> {request.url.pathname}</p>
        <p><strong>Method:</strong> {request.method}</p>
        <p><strong>Current dir:</strong> {current_dir}</p>
        <p><strong>Parent dir:</strong> {parent_dir}</p>
        <p><strong>Python path:</strong> {sys.path}</p>
        <p><strong>Files in parent dir:</strong> {os.listdir(parent_dir) if os.path.exists(parent_dir) else 'Directory not found'}</p>
        """
        
        # 尝试导入 Flask 应用
        try:
            from app import app as flask_app
            debug_info += "<p><strong>Flask import:</strong> ✅ Success</p>"
            
            # 处理 Flask 请求
            path = request.url.pathname
            query = request.url.search.lstrip('?') if request.url.search else ''
            full_url = path + ('?' + query if query else '')
            
            with flask_app.test_client() as client:
                if request.method == 'GET':
                    response = client.get(full_url)
                else:
                    response = client.open(full_url, method=request.method)
            
            # 构建响应头
            response_headers = {}
            for key, value in response.headers:
                response_headers[key] = value
            
            return Response(
                response.get_data(),
                status=response.status_code,
                headers=response_headers
            )
            
        except ImportError as import_error:
            debug_info += f"<p><strong>Flask import:</strong> ❌ Failed - {import_error}</p>"
            debug_info += "</body></html>"
            
            return Response(
                f"<html><body>{debug_info}</body></html>",
                status=500,
                headers={"Content-Type": "text/html"}
            )
            
    except Exception as e:
        # 详细的错误信息
        error_html = f"""
        <html>
        <body>
            <h1>Function Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p><strong>Type:</strong> {type(e).__name__}</p>
            <p><strong>Path:</strong> {request.url.pathname}</p>
        </body>
        </html>
        """
        
        return Response(error_html, status=500, headers={"Content-Type": "text/html"})

# 注：Response 类由 Cloudflare Pages Functions 运行时提供 