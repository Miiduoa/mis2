from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify
import datetime
import os
import time

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

# 模擬電影爬蟲
def mock_fetch_movies():
    additional_movies = [
        {
            'id': 'movie3', 
            'title': '阿凡達：水之道',
            'release_date': '2023-05-01',
            'poster': 'https://via.placeholder.com/300x450?text=Avatar',
            'runtime': '192分鐘',
            'director': '詹姆斯·卡麥隆',
            'story': '《阿凡達：水之道》帶觀眾回到潘朵拉星球，故事設定在第一部的數年後。',
            'updated_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'link': '#'
        },
        {
            'id': 'movie4', 
            'title': '蜘蛛人：穿越新宇宙',
            'release_date': '2023-06-02',
            'poster': 'https://via.placeholder.com/300x450?text=SpiderMan',
            'runtime': '140分鐘',
            'director': '菲爾·羅德',
            'story': '邁爾斯·莫拉萊斯回歸，並與關妮薩·斯黛西一起穿越多元宇宙。',
            'updated_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'link': '#'
        }
    ]
    
    # 清空現有電影資料並加入新電影
    mock_movies.clear()
    mock_movies.extend(additional_movies)
    
    return mock_movies

# 首頁
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>顧晉瑋的綜合專案</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .feature-box {
                border: 1px solid #ddd;
                padding: a0px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">顧晉瑋的綜合專案</h1>
            <div class="alert alert-success">
                <strong>測試版本</strong> - 這個版本使用模擬數據，無需Firebase連接
            </div>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="feature-box">
                        <h3>個人網頁</h3>
                        <p>HTML、CSS與JavaScript設計的個人介紹頁面</p>
                        <a href="/about" class="btn btn-primary">查看</a>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-box">
                        <h3>使用者管理</h3>
                        <p>使用模擬Firebase資料庫的使用者管理功能</p>
                        <a href="/users" class="btn btn-primary">查看</a>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-box">
                        <h3>電影資訊</h3>
                        <p>從網路爬蟲獲取並顯示的電影資訊</p>
                        <a href="/movies" class="btn btn-primary">查看</a>
                    </div>
                </div>
            </div>
            
            <div class="mt-5">
                <h3>功能測試</h3>
                <ul>
                    <li><a href="/today">今日日期</a></li>
                    <li><a href="/welcome?nick=測試用戶">歡迎頁面</a></li>
                    <li><a href="/refresh-movies">更新電影資料</a></li>
                    <li><a href="/api/movies">電影API</a></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """)

# 課程簡介
@app.route('/mis')
def mis():
    return "<h1>資訊管理導論</h1><p>這是一門結合資訊科技與管理知識的課程</p>"

# 今日日期
@app.route('/today')
def today():
    now = datetime.datetime.now()
    return f"<h1>現在時間</h1><p>{now}</p><p><a href='/'>返回首頁</a></p>"

# 歡迎頁面
@app.route('/welcome')
def welcome():
    user = request.args.get('nick', '訪客')
    return f"<h1>歡迎, {user}!</h1><p><a href='/'>返回首頁</a></p>"

# 帳號登入
@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if user == 'admin' and pwd == '12345':
            return '<h1>登入成功</h1><p><a href="/">返回首頁</a></p>'
        else:
            return '<h1>登入失敗</h1><p><a href="/account">重新登入</a></p>'
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>帳號登入</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>帳號登入</h1>
            <form method="post">
                <div class="mb-3">
                    <label for="user" class="form-label">帳號</label>
                    <input type="text" class="form-control" id="user" name="user" required>
                </div>
                <div class="mb-3">
                    <label for="pwd" class="form-label">密碼</label>
                    <input type="password" class="form-control" id="pwd" name="pwd" required>
                </div>
                <button type="submit" class="btn btn-primary">登入</button>
            </form>
            <div class="mt-3">
                <p>測試帳號: admin</p>
                <p>測試密碼: 12345</p>
                <p><a href="/">返回首頁</a></p>
            </div>
        </div>
    </body>
    </html>
    """)

# 關於我
@app.route('/about')
def about():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>關於我</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .profile-image {
                max-width: 200px;
                border-radius: 50%;
                margin-bottom: 20px;
            }
            .skill-badge {
                margin-right: 8px;
                margin-bottom: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row">
                <div class="col-md-4 text-center">
                    <img src="https://via.placeholder.com/400" alt="顧晉瑋照片" class="profile-image">
                </div>
                <div class="col-md-8">
                    <h1>顧晉瑋</h1>
                    <h3 class="text-muted">資訊科技愛好者</h3>
                    <p>一位對網頁開發、Python程式設計與資料分析充滿熱情的學生，擁有豐富的專案經驗。</p>
                    <hr>
                    <h4>專業技能</h4>
                    <div>
                        <span class="badge bg-primary skill-badge">HTML/CSS</span>
                        <span class="badge bg-primary skill-badge">JavaScript</span>
                        <span class="badge bg-primary skill-badge">Python</span>
                        <span class="badge bg-primary skill-badge">Flask</span>
                        <span class="badge bg-primary skill-badge">Firebase</span>
                        <span class="badge bg-secondary skill-badge">網路爬蟲</span>
                    </div>
                    <hr>
                    <a href="/" class="btn btn-primary">返回首頁</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

# 使用者管理
@app.route('/users')
def users():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>使用者管理</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>使用者列表</h1>
            <div class="alert alert-info">這是使用模擬數據顯示的用戶列表</div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>姓名</th>
                        <th>郵箱</th>
                        <th>角色</th>
                        <th>創建時間</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.role }}</td>
                        <td>{{ user.created_at }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="/" class="btn btn-primary">返回首頁</a>
        </div>
    </body>
    </html>
    """, users=mock_users)

# 電影資料
@app.route('/movies')
def movies():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>電影列表</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>電影列表</h1>
            <div class="alert alert-info">這是使用模擬數據顯示的電影列表</div>
            <div class="row">
                {% for movie in movies %}
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <img src="{{ movie.poster }}" class="card-img-top" alt="{{ movie.title }}">
                        <div class="card-body">
                            <h5 class="card-title">{{ movie.title }}</h5>
                            <p class="card-text"><strong>上映日期:</strong> {{ movie.release_date }}</p>
                            <p class="card-text"><strong>片長:</strong> {{ movie.runtime }}</p>
                            <p class="card-text"><strong>導演:</strong> {{ movie.director }}</p>
                            <p class="card-text"><small>{{ movie.story[:100] }}...</small></p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="mt-3">
                <a href="/refresh-movies" class="btn btn-warning">重新爬取電影資料</a>
                <a href="/" class="btn btn-primary">返回首頁</a>
            </div>
        </div>
    </body>
    </html>
    """, movies=mock_movies)

# 重新爬取電影資料
@app.route('/refresh-movies')
def refresh_movies():
    try:
        # 模擬爬取電影數據
        movies = mock_fetch_movies()
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>爬取成功</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success">
                    <h4>成功爬取電影資料</h4>
                    <p>成功爬取並更新了 {{ count }} 部電影資料。</p>
                </div>
                <a href="/movies" class="btn btn-primary">查看電影列表</a>
                <a href="/" class="btn btn-secondary">返回首頁</a>
            </div>
        </body>
        </html>
        """, count=len(movies))
    except Exception as e:
        return f"爬取電影資料時發生錯誤: {str(e)}"

# API端點 - 獲取所有電影資料
@app.route('/api/movies')
def api_movies():
    return jsonify(mock_movies)

# 處理不存在的路徑
@app.route('/<path:path>')
def catch_all(path):
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 找不到頁面</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5 text-center">
            <h1>404 找不到頁面</h1>
            <p>您訪問的頁面 '{{ path }}' 不存在</p>
            <a href="/" class="btn btn-primary">返回首頁</a>
        </div>
    </body>
    </html>
    """, path=path), 404

# 本地開發用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 