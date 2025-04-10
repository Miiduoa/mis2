from flask import Flask
import sys
import io
import os
import json

# 導入主應用
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

def handler(request):
    """
    處理 Vercel Serverless Functions 請求
    將 Flask 應用轉換為 Vercel Serverless 格式
    """
    # 獲取請求信息
    path = request.get('path', '/')
    method = request.get('method', 'GET')
    query = request.get('query', {})
    body = request.get('body', '')
    headers = request.get('headers', {})

    # 構建 WSGI 環境
    query_string = '&'.join(f"{k}={v}" for k, v in query.items()) if query else ''
    
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'wsgi.input': io.BytesIO(body.encode() if isinstance(body, str) else body),
        'wsgi.errors': io.StringIO(),
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': headers.get('host', 'vercel.app'),
        'SERVER_PORT': '443',
    }
    
    # 添加請求頭
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
        else:
            environ[key] = value
    
    # 準備響應
    response_data = {
        'statusCode': 200,
        'headers': {},
        'body': ''
    }
    
    # 捕獲響應信息
    response_headers = []
    
    def start_response(status, headers, exc_info=None):
        status_code = int(status.split()[0])
        response_data['statusCode'] = status_code
        response_headers.extend(headers)
        return lambda x: None
    
    # 執行 Flask 應用
    output = io.BytesIO()
    
    try:
        # 獲取應用響應
        response_body = b''
        for data in app(environ, start_response):
            if data:
                response_body += data if isinstance(data, bytes) else data.encode('utf-8')
        
        # 處理響應頭
        for header, value in response_headers:
            response_data['headers'][header] = value
        
        # 處理響應體
        response_data['body'] = response_body.decode('utf-8')
        
    except Exception as e:
        # 處理錯誤
        response_data['statusCode'] = 500
        response_data['body'] = json.dumps({
            'error': str(e),
            'message': 'Internal Server Error'
        })
    
    return response_data 