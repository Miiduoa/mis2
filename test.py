from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

# 模擬使用者資料
mock_users = [
    {'id': 'user1', 'name': '測試用戶1', 'email': 'test1@example.com', 'role': '使用者', 'created_at': '2023-01-01'},
    {'id': 'user2', 'name': '測試用戶2', 'email': 'test2@example.com', 'role': '管理員', 'created_at': '2023-01-02'}
]

# 模擬電影資料
mock_movies = [
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

# 首頁
@app.route('/')
def index():
    return "<h1>Flask應用程式測試成功!</h1><p>這個專案使用了Flask、Firebase和爬蟲技術</p><ul><li><a href='/about'>關於我</a></li><li><a href='/users'>使用者列表</a></li><li><a href='/movies'>電影列表</a></li></ul>"

# 今日日期
@app.route('/today')
def today():
    now = datetime.datetime.now()
    return f"<h1>現在時間</h1><p>{now}</p>"

# 歡迎頁面
@app.route('/welcome')
def welcome():
    user = request.args.get('nick', '訪客')
    return f"<h1>歡迎, {user}!</h1>"

# 關於我
@app.route('/about')
def about():
    return "<h1>關於我</h1><p>這是顧晉瑋的個人網頁</p>"

# 使用者管理
@app.route('/users')
def users():
    return render_template_string("""
        <h1>使用者列表</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>姓名</th>
                <th>郵箱</th>
                <th>角色</th>
                <th>創建時間</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>{{ user.created_at }}</td>
            </tr>
            {% endfor %}
        </table>
    """, users=mock_users)

# 電影資料
@app.route('/movies')
def movies():
    return render_template_string("""
        <h1>電影列表</h1>
        <div style="display: flex; flex-wrap: wrap;">
            {% for movie in movies %}
            <div style="margin: 10px; width: 300px; border: 1px solid #ddd; padding: 10px;">
                <h2>{{ movie.title }}</h2>
                <img src="{{ movie.poster }}" style="max-width: 100%;" alt="{{ movie.title }}">
                <p><strong>上映日期:</strong> {{ movie.release_date }}</p>
                <p><strong>片長:</strong> {{ movie.runtime }}</p>
                <p><strong>導演:</strong> {{ movie.director }}</p>
                <p><strong>劇情:</strong> {{ movie.story }}</p>
            </div>
            {% endfor %}
        </div>
    """, movies=mock_movies)

# API端點 - 獲取所有電影資料
@app.route('/api/movies')
def api_movies():
    return jsonify(mock_movies)

# 處理不存在的路徑
@app.route('/<path:path>')
def catch_all(path):
    return f"<h1>404 找不到頁面</h1><p>您訪問的頁面 '{path}' 不存在</p>", 404

# 本地開發用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 