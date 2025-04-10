from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz
import os

# 如果存在 Firebase 配置文件，則導入相關模塊
has_firebase = os.path.exists("serviceAccountKey.json")
if has_firebase:
    import firebase_admin
    from firebase_admin import credentials, firestore
    # 初始化 Firebase
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

app = Flask(__name__)

# 錯誤處理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="找不到頁面"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message="伺服器錯誤"), 500

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

# 以下是 Firebase 相關的路由
@app.route('/read')
def read_data():
    if not has_firebase:
        return jsonify({"error": "Firebase 未配置"}), 500
    
    try:
        # 獲取所有學生資料
        students_ref = db.collection('students')
        students = []
        for doc in students_ref.stream():
            student_data = doc.to_dict()
            students.append(student_data)
        
        return render_template('firebase_data.html', students=students, title="學生資料")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if not has_firebase:
        return jsonify({"error": "Firebase 未配置"}), 500
    
    if request.method == 'POST':
        try:
            # 獲取表單資料
            name = request.form.get('name')
            student_id = request.form.get('student_id')
            department = request.form.get('department')
            email = request.form.get('email')
            
            # 準備要新增的資料
            data = {
                "name": name,
                "student_id": student_id,
                "department": department,
                "email": email,
                "created_at": firestore.SERVER_TIMESTAMP
            }
            
            # 新增資料到 'students' 集合中
            doc_ref = db.collection('students').document(student_id)
            doc_ref.set(data)
            
            return render_template('add_student.html', success=True, student=data)
        except Exception as e:
            return render_template('add_student.html', error=str(e))
    
    return render_template('add_student.html')

# Vercel 需要訪問 Flask 的 app 對象
if __name__ == '__main__':
    app.run(debug=True) 