# index.py
# 這是 Vercel 的入口點檔案 - 必須簡單明確

from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import os
import firebase_service
import spider

# 設定 Flask 應用
app = Flask(__name__)

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
    return render_template('mis.html', title='資訊管理導論')

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

# 使用者管理
@app.route('/users')
def users():
    try:
        all_users = firebase_service.get_all_users()
        return render_template('users.html', users=all_users)
    except Exception as e:
        # 如果Firebase存取失敗，使用模擬資料
        dummy_users = [
            {'id': 'user1', 'name': '測試用戶1', 'email': 'test1@example.com', 'role': '使用者', 'created_at': '2023-01-01'},
            {'id': 'user2', 'name': '測試用戶2', 'email': 'test2@example.com', 'role': '管理員', 'created_at': '2023-01-02'}
        ]
        return render_template('users.html', users=dummy_users, error=str(e))

# 新增使用者
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            user_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'role': request.form.get('role', 'user'),
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            user_id = request.form.get('user_id', '')
            if not user_id:
                user_id = user_data['email'].split('@')[0]  # 使用郵件前綴作為ID
            
            firebase_service.create_user(user_id, user_data)
            return redirect('/users')
        except Exception as e:
            return f"新增使用者時發生錯誤: {str(e)}"
    return render_template('add_user.html')

# 刪除使用者
@app.route('/user/delete/<user_id>')
def delete_user(user_id):
    try:
        firebase_service.delete_user(user_id)
        return redirect('/users')
    except Exception as e:
        return f"刪除使用者時發生錯誤: {str(e)}"

# 電影資料
@app.route('/movies')
def movies():
    try:
        all_movies = firebase_service.get_all_movies()
        return render_template('movies.html', movies=all_movies)
    except Exception as e:
        # 如果Firebase存取失敗，使用模擬資料
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
        return render_template('movies.html', movies=dummy_movies, error=str(e))

# 重新爬取電影資料
@app.route('/refresh-movies')
def refresh_movies():
    try:
        # 清除所有現有電影資料
        firebase_service.delete_all_movies()
        # 重新爬取電影資料
        movies = spider.fetch_movie_data()
        return f"成功爬取並更新了 {len(movies)} 部電影資料。<a href='/movies'>查看電影列表</a>"
    except Exception as e:
        return f"爬取電影資料時發生錯誤: {str(e)}"

# API端點 - 獲取所有電影資料
@app.route('/api/movies')
def api_movies():
    try:
        all_movies = firebase_service.get_all_movies()
        return jsonify(all_movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 處理不存在的路徑
@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html', path=path), 404

# Vercel 需要的 handler
def handler(event, context):
    return app.wsgi_app(event, context)

# 本地開發用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 