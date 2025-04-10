from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup
import os

# 在Firebase初始化失敗時提供退路
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # 嘗試從環境變數取得認證資訊 (用於Vercel部署)
    # 如果本地開發，需將serviceAccountKey.json放在credentials資料夾
    if os.environ.get('FIREBASE_KEY'):
        # 從環境變數獲取
        import json
        firebase_key = json.loads(os.environ.get('FIREBASE_KEY'))
        cred = credentials.Certificate(firebase_key)
    else:
        # 從本地檔案獲取
        try:
            cred = credentials.Certificate('credentials/serviceAccountKey.json')
        except:
            print("Firebase認證失敗: 請確保credentials/serviceAccountKey.json存在或設置FIREBASE_KEY環境變數")
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    firebase_available = True
except Exception as e:
    print(f"Firebase初始化失敗: {e}")
    firebase_available = False

app = Flask(__name__)

@app.route("/")
def index():
    # 首頁包含顧晉瑋的標題與超連結
    homepage = "<h1>顧晉瑋Python網頁</h1>"
    homepage += "<a href='/today'>顯示日期時間</a><br>"
    homepage += "<a href='/about'>顧晉瑋簡介網頁</a><br>"
    homepage += "<a href='/account'>網頁表單傳值</a><br>"
    if firebase_available:
        homepage += "<a href='/movies'>電影列表</a><br>"
        homepage += "<a href='/movie/update'>更新電影資料</a><br>"
    return homepage

@app.route("/today")
def today():
    # 設定時區為 UTC+8（臺灣）
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html", datetime=str(now))

@app.route("/about")
def about():
    # 使用模板顯示個人簡介網頁
    return render_template("about.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        # 取得使用者在表單中輸入的帳號與密碼
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd
        
        # 若Firebase可用，將帳號資訊存入Firebase
        if firebase_available:
            try:
                doc = {
                    "user": user,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db.collection("users").add(doc)
            except Exception as e:
                print(f"儲存使用者資料失敗: {e}")
                
        return result
    else:
        # GET 請求時，呈現表單頁面
        return render_template("account.html")

@app.route("/welcome")
def welcome():
    # 取得URL參數中的nick值
    name = request.args.get("nick", "訪客")
    return render_template("welcome.html", name=name)

@app.route("/movies")
def movies():
    # 如果Firebase不可用則返回錯誤訊息
    if not firebase_available:
        return "Firebase未設置或初始化失敗，無法顯示電影資料"
    
    try:
        # 從Firebase讀取電影資料
        movies_ref = db.collection("電影")
        movies_data = movies_ref.get()
        
        # 準備電影資料
        movies_list = []
        for doc in movies_data:
            movie = doc.to_dict()
            movie['id'] = doc.id
            movies_list.append(movie)
        
        # 如果沒有電影資料，建議更新
        if not movies_list:
            return "目前無電影資料，請先<a href='/movie/update'>更新電影資料</a>"
        
        # 將資料傳送到範本
        return render_template("movies.html", movies=movies_list)
    except Exception as e:
        return f"讀取電影資料時發生錯誤: {e}"

@app.route("/movie/update")
def update_movies():
    # 如果Firebase不可用則返回錯誤訊息
    if not firebase_available:
        return "Firebase未設置或初始化失敗，無法更新電影資料"
    
    try:
        # 爬取電影網站資料
        url = "http://www.atmovies.com.tw/movie/next/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.select(".filmListAllX li")
        
        # 儲存更新時間
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 計算新增或更新的電影數量
        count = 0
        
        # 遍歷每一部電影
        for movie in movies:
            try:
                title_element = movie.find("div", class_="filmtitle")
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                
                # 取得電影連結
                link_element = title_element.find("a")
                if link_element:
                    movie_id = link_element.get("href").replace("/movie/", "").replace("/", "")
                    hyperlink = "http://www.atmovies.com.tw" + link_element.get("href")
                else:
                    continue
                
                # 取得海報圖片
                img_element = movie.find("img")
                picture = img_element.get("src").strip() if img_element else ""
                
                # 取得上映日期與片長
                runtime_element = movie.find("div", class_="runtime")
                if runtime_element:
                    runtime_text = runtime_element.text.strip()
                    # 分析上映日期與片長
                    show_date = ""
                    show_length = ""
                    
                    if "上映日期" in runtime_text:
                        date_parts = runtime_text.split("上映日期：")
                        if len(date_parts) > 1:
                            date_info = date_parts[1].split("片長：")[0].strip()
                            show_date = date_info
                    
                    if "片長：" in runtime_text:
                        length_parts = runtime_text.split("片長：")
                        if len(length_parts) > 1:
                            length_info = length_parts[1].strip()
                            show_length = length_info
                
                # 準備電影資料
                movie_data = {
                    "title": title,
                    "picture": picture,
                    "hyperlink": hyperlink,
                    "showDate": show_date,
                    "showLength": show_length,
                    "lastUpdate": last_update
                }
                
                # 儲存到Firebase
                # 檢查是否已有此電影，如果有則更新，否則新增
                existing_movies = db.collection("電影").where("title", "==", title).get()
                
                if len(list(existing_movies)) > 0:
                    # 更新現有電影資料
                    for doc in existing_movies:
                        db.collection("電影").document(doc.id).update(movie_data)
                else:
                    # 新增電影資料
                    db.collection("電影").add(movie_data)
                
                count += 1
            except Exception as e:
                print(f"處理電影資料時發生錯誤: {e}")
                continue
        
        return f"成功更新了 {count} 部電影資料！<br><a href='/movies'>查看電影列表</a>"
    except Exception as e:
        return f"更新電影資料時發生錯誤: {e}"

if __name__ == "__main__":
    app.run(debug=True)