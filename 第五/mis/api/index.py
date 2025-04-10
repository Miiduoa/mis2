from flask import Flask
import sys
import os

# 確保可以導入主應用
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from index import app

# 添加錯誤處理（僅用於診斷）
@app.errorhandler(404)
def custom_404(error):
    return "找不到頁面 - Vercel 部署測試", 404

# Vercel 需要這個入口點 