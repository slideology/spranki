"""
Cloudflare Pages Functions 适配器
处理所有 Flask 应用路由
"""

import sys
import os
import json
from urllib.parse import unquote, parse_qs

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入 Flask 应用
try:
    from app import app as flask_app
    print("Successfully imported Flask app")
except ImportError as e:
    print(f"Failed to import Flask app: {e}")
    flask_app = None

def create_wsgi_environ(request):
    """
    将 Cloudflare Request 转换为 WSGI environ
    """
    url = request.url
    
    environ = {
        'REQUEST_METHOD': request.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': unquote(url.pathname),
        'QUERY_STRING': url.search.lstrip('?') if url.search else '',
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(request.body)) if hasattr(request, 'body') and request.body else '0',
        'SERVER_NAME': url.hostname,
        'SERVER_PORT': str(url.port or (443 if url.protocol == 'https:' else 80)),
        'HTTPS': 'on' if url.protocol == 'https:' else 'off',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': url.protocol.rstrip(':'),
        'wsgi.input': None,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # 添加 HTTP 头部
    for key, value in request.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    return environ

def create_response_from_wsgi(status, headers, body):
    """
    将 WSGI 响应转换为 Cloudflare Response
    """
    # 解析状态码
    status_code = int(status.split()[0])
    
    # 转换头部
    response_headers = {}
    for header in headers:
        if isinstance(header, (list, tuple)) and len(header) == 2:
            response_headers[header[0]] = header[1]
    
    # 合并响应体
    if isinstance(body, (list, tuple)):
        body_content = b''.join(body)
    else:
        body_content = body
    
    return Response(body_content, {
        'status': status_code,
        'headers': response_headers
    })

async def on_request(context):
    """
    Cloudflare Pages Functions 入口点
    """
    request = context.request
    
    # 检查 Flask 应用是否加载成功
    if not flask_app:
        return Response("Flask application failed to load", {'status': 500})
    
    try:
        # 处理请求体（如果有）
        request_body = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request_body = await request.text()
            except:
                request_body = ""
        
        # 创建 WSGI environ
        environ = create_wsgi_environ(request)
        
        # 如果有请求体，添加到 environ
        if request_body:
            environ['wsgi.input'] = request_body
            environ['CONTENT_LENGTH'] = str(len(request_body.encode('utf-8')))
        
        # 使用 Flask 测试客户端模拟请求
        with flask_app.test_client() as client:
            # 构建 URL
            url = environ['PATH_INFO']
            if environ['QUERY_STRING']:
                url += '?' + environ['QUERY_STRING']
            
            # 构建头部
            headers = {}
            for key, value in environ.items():
                if key.startswith('HTTP_'):
                    header_name = key[5:].replace('_', '-').lower()
                    headers[header_name] = value
                elif key in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                    headers[key.lower().replace('_', '-')] = value
            
            # 发送请求到 Flask
            if request.method == 'GET':
                response = client.get(url, headers=headers)
            elif request.method == 'POST':
                response = client.post(url, data=request_body, headers=headers)
            elif request.method == 'PUT':
                response = client.put(url, data=request_body, headers=headers)
            elif request.method == 'PATCH':
                response = client.patch(url, data=request_body, headers=headers)
            elif request.method == 'DELETE':
                response = client.delete(url, headers=headers)
            else:
                response = client.open(url, method=request.method, data=request_body, headers=headers)
        
        # 构建响应头部
        response_headers = {}
        for key, value in response.headers:
            response_headers[key] = value
        
        # 返回 Cloudflare Response
        return Response(response.get_data(), {
            'status': response.status_code,
            'headers': response_headers
        })
        
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回错误响应
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>An error occurred while processing your request.</p>
            <p>Error: {str(e)}</p>
        </body>
        </html>
        """
        
        return Response(error_html, {
            'status': 500,
            'headers': {'Content-Type': 'text/html'}
        })

# 导出函数（Cloudflare Pages Functions 要求）
__all__ = ['on_request'] 