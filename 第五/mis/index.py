from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pytz
import os
import traceback
import json

# 調整路徑以確保在 Vercel 上正確查找檔案
base_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(base_dir, "serviceAccountKey.json")

# 檢查環境變數
has_firebase = False
firebase_env_key = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

if firebase_env_key:
    try:
        # 從環境變數讀取
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # 將環境變數字串轉換為 JSON
        service_account_info = json.loads(firebase_env_key)
        
        # 初始化 Firebase
        if not firebase_admin._apps:  # 避免重複初始化
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        has_firebase = True
        print("Firebase 從環境變數成功初始化")
    except Exception as e:
        print(f"從環境變數初始化 Firebase 失敗: {str(e)}")
        traceback.print_exc()
# 如果環境變數不存在，則嘗試從檔案讀取
elif os.path.exists(service_account_path):
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        # 初始化 Firebase
        if not firebase_admin._apps:  # 避免重複初始化
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        has_firebase = True
        print("Firebase 從檔案成功初始化")
    except Exception as e:
        print(f"從檔案初始化 Firebase 失敗: {str(e)}")
        traceback.print_exc()
else:
    print(f"無法初始化 Firebase: 環境變數和檔案都不存在")

# 延遲導入以避免循環依賴
try:
    from spider import scrape_movies
except ImportError as e:
    print(f"無法導入爬蟲模組: {str(e)}")
    def scrape_movies():
        return {"success": False, "message": "爬蟲模組未正確加載"}

app = Flask(__name__)

# 錯誤處理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', error_code=500, error_message="伺服器錯誤"), 500

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
        error_msg = "Firebase 未配置或初始化失敗，請確保 serviceAccountKey.json 檔案存在於程式目錄中"
        return render_template('404.html', error_code=500, error_message=error_msg), 500
    
    try:
        # 獲取所有學生資料
        students_ref = db.collection('students')
        students = []
        for doc in students_ref.stream():
            student_data = doc.to_dict()
            student_data['id'] = doc.id  # 添加文檔ID
            students.append(student_data)
        
        return render_template('firebase_data.html', students=students, title="學生資料")
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"讀取學生資料時出錯: {str(e)}")
        print(error_details)
        return render_template('404.html', 
                               error_code=500, 
                               error_message=f"讀取學生資料時發生錯誤: {str(e)}")

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if not has_firebase:
        return render_template('404.html', error_code=500, error_message="Firebase 未配置"), 500
    
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

# 新增電影資訊爬取路由
@app.route('/movie')
def movie():
    try:
        # 爬取電影資訊
        result = scrape_movies()
        
        if result["success"]:
            return render_template('movies.html', 
                                  movies=result["data"], 
                                  count=result["count"], 
                                  lastUpdate=result["lastUpdate"])
        else:
            return render_template('404.html', 
                                  error_code="爬蟲錯誤", 
                                  error_message=result["message"])
    except Exception as e:
        return render_template('404.html', 
                              error_code=500, 
                              error_message=f"處理電影資訊時發生錯誤: {str(e)}")

# Vercel 需要訪問 Flask 的 app 對象
if __name__ == '__main__':
    app.run(debug=True) 