from app import app

# WSGI 入口點，許多託管平台（包括 Vercel）使用這種標準方式處理 Python 應用
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# 標準 WSGI 入口點
application = app 