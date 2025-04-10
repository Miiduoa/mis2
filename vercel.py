from app import app
from flask import request

def handler(req, res):
    # 使用絕對最簡化的處理函數，完全符合 Vercel Python 規範
    with app.request_context(req):
        return app.full_dispatch_request() 