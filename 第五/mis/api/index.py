from flask import Flask
import sys
import os

# 確保可以導入主應用
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
print(f"API: 添加路徑 {parent_dir}")

# 從主應用導入 app
try:
    from index import app
    print("API: 成功導入 app")
except Exception as e:
    print(f"API: 導入應用失敗: {str(e)}")
    raise

# 添加錯誤處理（僅用於診斷）
@app.errorhandler(404)
def custom_404(error):
    return "找不到頁面 - Vercel 部署測試", 404

# Vercel 需要這個入口點，在特殊情況下啟用
if __name__ == "__main__":
    app.run() 