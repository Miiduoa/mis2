from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

# 設定 Flask 應用
app = Flask(__name__, 
            template_folder='../templates',  # 指向上一層的templates目錄
            static_folder='../static')       # 指向上一層的static目錄

# 測試環境變數 (避免部署時出錯)
def is_production():
    return 'VERCEL' in os.environ

# 首頁
@app.route('/')
def index():
    return render_template('index.html', title='首頁')

# 課程簡介
@app.route('/mis')
def mis():
    return render_template('mis.html', title='課程簡介')

# 今日日期
@app.route('/today')
def today():
    now = datetime.datetime.now()
    return render_template('today.html', datetime=str(now))

# 歡迎頁面
@app.route('/welcome')
def welcome():
    user = request.args.get('nick', '訪客')
    return render_template('welcome.html', name=user)

# 帳號登入
@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if user == 'admin' and pwd == '12345':
            return '<h1>登入成功</h1>'
        else:
            return '<h1>登入失敗</h1>'
    return render_template('account.html')

# 關於我
@app.route('/about')
def about():
    return render_template('about.html')

# 使用者管理 (模擬資料)
@app.route('/users')
def users():
    dummy_users = [
        {'id': 'user1', 'name': '測試用戶1', 'email': 'test1@example.com', 'role': '使用者', 'created_at': '2023-01-01'},
        {'id': 'user2', 'name': '測試用戶2', 'email': 'test2@example.com', 'role': '管理員', 'created_at': '2023-01-02'}
    ]
    return render_template('users.html', users=dummy_users)

# 電影資料 (模擬資料)
@app.route('/movies')
def movies():
    dummy_movies = [
        {
            'id': 'movie1', 
            'title': '測試電影1',
            'release_date': '2023-01-01',
            'poster': 'https://via.placeholder.com/300x450',
            'runtime': '120分鐘',
            'director': '導演名稱',
            'story': '這是一部測試電影的劇情簡介。',
            'link': '#'
        },
        {
            'id': 'movie2', 
            'title': '測試電影2',
            'release_date': '2023-02-01',
            'poster': 'https://via.placeholder.com/300x450',
            'runtime': '90分鐘',
            'director': '另一位導演',
            'story': '這是另一部測試電影的劇情簡介。',
            'link': '#'
        }
    ]
    return render_template('movies.html', movies=dummy_movies)

# 處理不存在的路徑
@app.route('/<path:path>')
def catch_all(path):
    return f'您訪問的頁面 {path} 不存在'

# Vercel 需要的 handler
def handler(event, context):
    return app.wsgi_app(event, context)

# 本地開發用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 