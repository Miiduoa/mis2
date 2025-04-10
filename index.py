# index.py - Vercel 入口點

from app import app

# Vercel 函數處理器
from flask.cli import ScriptInfo

def handler(event, context):
    """處理 Vercel 的 serverless 請求"""
    from urllib.parse import urlencode
    
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {})
    
    # 處理查詢參數
    query_params = event.get('queryStringParameters', {}) or {}
    query_string = urlencode(query_params)
    
    # 處理請求體
    body = event.get('body', '')
    
    # 創建 WSGI 環境
    environ = {
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': body.encode() if isinstance(body, str) else body,
        'wsgi.errors': '',
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'SERVER_NAME': 'vercel.app',
        'SERVER_PORT': '443',
        'REQUEST_METHOD': http_method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'HTTP_HOST': headers.get('host', 'vercel.app'),
    }
    
    # 添加 HTTP 頭
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # 運行 WSGI 應用
    response_data = {'statusCode': 200, 'body': '', 'headers': {}}
    
    def start_response(status, response_headers, exc_info=None):
        response_data['statusCode'] = int(status.split()[0])
        response_data['headers'] = dict(response_headers)
    
    chunks = app(environ, start_response)
    response_data['body'] = ''.join(chunk.decode('utf-8') for chunk in chunks)
    
    return response_data 