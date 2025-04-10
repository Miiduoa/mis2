from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html', title="首頁")

@app.route('/mis')
def mis():
    return "<h1>MIS 資訊管理課程網站</h1><p>這是資訊管理課程的網站，歡迎學習 Flask 動態網頁！</p>"

@app.route('/today')
def today():
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    return render_template('today.html', datetime=now)

@app.route('/welcome')
def welcome():
    nickname = request.args.get('nick', '訪客')
    return render_template('welcome.html', nickname=nickname)

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user = request.form.get('user', '')
        pwd = request.form.get('pwd', '')
        if user == 'admin' and pwd == '12345':
            return f'<h1>登入成功</h1><p>歡迎 {user} 回來！</p>'
        else:
            return render_template('account.html', message='帳號或密碼錯誤')
    return render_template('account.html')

@app.route('/about')
def about():
    return render_template('welcome.html', title="關於我們", content="這是一個使用 Flask 開發的資訊管理課程網站。")

if __name__ == '__main__':
    app.run(debug=True) 