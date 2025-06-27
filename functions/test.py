def on_request(context):
    """简单的测试函数"""
    return Response("Hello from Cloudflare Functions! This means Functions are working.", 
                   status=200,
                   headers={"Content-Type": "text/html"}) 