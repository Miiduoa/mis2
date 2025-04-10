import requests
from bs4 import BeautifulSoup
import os
import json
import traceback

# 避免重複初始化 Firebase
firebase_initialized = False
has_firebase = False
db = None

# 檢查 Firebase 初始化狀態
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # 如果已經初始化，直接使用
    if firebase_admin._apps:
        db = firestore.client()
        has_firebase = True
        firebase_initialized = True
    else:
        # 檢查環境變數
        firebase_env_key = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        
        if firebase_env_key:
            # 從環境變數讀取
            service_account_info = json.loads(firebase_env_key)
            
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            has_firebase = True
            firebase_initialized = True
            print("Spider: Firebase 從環境變數初始化")
        else:
            # 從檔案讀取
            base_dir = os.path.dirname(os.path.abspath(__file__))
            service_account_path = os.path.join(base_dir, "serviceAccountKey.json")
            
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                has_firebase = True
                firebase_initialized = True
                print("Spider: Firebase 從檔案初始化")
            else:
                print("Spider: Firebase 未初始化 - 找不到金鑰")
except Exception as e:
    print(f"Spider: Firebase 初始化錯誤: {str(e)}")
    traceback.print_exc()

def scrape_movies():
    """爬取電影資訊並返回結果"""
    url = "http://www.atmovies.com.tw/movie/next/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        
        if response.status_code != 200:
            return {"success": False, "message": f"爬取失敗: HTTP {response.status_code}"}
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找到電影列表
        movie_list = soup.select(".filmListAllX li")
        last_update = soup.find("div", class_="smaller09").text[5:] if soup.find("div", class_="smaller09") else "未知"
        
        movies = []
        for item in movie_list:
            try:
                # 取得海報圖片
                picture = item.find("img").get("src").strip() if item.find("img") else ""
                
                # 取得片名
                title = item.find("div", class_="filmtitle").text.strip() if item.find("div", class_="filmtitle") else "未知片名"
                
                # 取得電影連結
                link_element = item.find("div", class_="filmtitle").find("a") if item.find("div", class_="filmtitle") else None
                movie_id = link_element.get("href").replace("/", "").replace("movie", "") if link_element else ""
                hyperlink = "http://www.atmovies.com.tw" + link_element.get("href").strip() if link_element else ""
                
                # 取得上映日期與片長
                runtime_div = item.find("div", class_="runtime") 
                runtime_text = runtime_div.text.strip() if runtime_div else ""
                
                show_date = ""
                show_length = ""
                
                if runtime_text:
                    # 解析上映日期和片長
                    parts = runtime_text.split("片長：")
                    if len(parts) > 0:
                        date_part = parts[0].replace("上映日期：", "").strip()
                        show_date = date_part if date_part else "未知"
                    
                    if len(parts) > 1:
                        length_part = parts[1].replace("分", "").strip()
                        show_length = length_part if length_part else "未知"
                
                movie_data = {
                    "title": title,
                    "picture": picture,
                    "hyperlink": hyperlink,
                    "movie_id": movie_id,
                    "showDate": show_date,
                    "showLength": show_length
                }
                
                movies.append(movie_data)
                
                # 如果有 Firebase 配置，存入資料庫
                if has_firebase and db:
                    try:
                        movie_ref = db.collection("movies").document(movie_id if movie_id else None)
                        movie_ref.set(movie_data)
                    except Exception as firebase_error:
                        print(f"存入 Firebase 時出錯: {str(firebase_error)}")
            except Exception as e:
                print(f"處理電影時出錯: {str(e)}")
                continue
        
        return {
            "success": True, 
            "data": movies, 
            "count": len(movies),
            "lastUpdate": last_update
        }
        
    except Exception as e:
        return {"success": False, "message": f"發生錯誤: {str(e)}"}

# 用於測試
if __name__ == "__main__":
    result = scrape_movies()
    if result["success"]:
        print(f"成功爬取 {result['count']} 部電影")
        for movie in result["data"]:
            print(f"片名: {movie['title']}")
            print(f"海報: {movie['picture']}")
            print(f"連結: {movie['hyperlink']}")
            print(f"上映日期: {movie['showDate']}")
            print(f"片長: {movie['showLength']}分鐘")
            print("-" * 50)
    else:
        print(f"爬取失敗: {result['message']}") 