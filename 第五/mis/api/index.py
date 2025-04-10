from flask import Flask
import sys
import os

# 確保可以導入主應用
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from index import app

# Vercel 需要這個入口點 