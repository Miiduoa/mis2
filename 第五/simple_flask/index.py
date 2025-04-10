from flask import Flask, render_template

# 初始化 Flask 應用
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "Hello, World! 這是一個簡單的測試頁面!"

# 添加一個API路由來測試JSON響應
@app.route('/api/test')
def api_test():
    return {"message": "API測試成功!", "status": "ok"}

# Vercel 部署需要這個
if __name__ == '__main__':
    app.run(debug=True) 