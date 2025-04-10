from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response(f"Hello from Vercel! Path: /{path}", mimetype="text/html")

# 導出 Flask 應用供 Vercel 使用
app.debug = True 