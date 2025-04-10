from http.server import BaseHTTPRequestHandler
import sys, os

# 將父目錄添加到路徑中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 導入主應用
from index import app

# 處理請求的函數
def handler(request, context):
    # 返回簡單的響應
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '<h1>Vercel Serverless Function is working!</h1><p>訪問 <a href="/">/</a> 以查看完整應用</p>'
    } 