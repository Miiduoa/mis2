import firebase_admin
from firebase_admin import credentials, firestore
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def init_firebase():
    """初始化Firebase連接"""
    try:
        # 嘗試從環境變數取得認證資訊 (用於Vercel部署)
        if os.environ.get('FIREBASE_KEY'):
            # 從環境變數獲取
            import json
            firebase_key = json.loads(os.environ.get('FIREBASE_KEY'))
            cred = credentials.Certificate(firebase_key)
        else:
            # 從本地檔案獲取
            cred = credentials.Certificate('credentials/serviceAccountKey.json')
        
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Firebase初始化失敗: {e}")
        return None

def fetch_movie_data():
    """從開眼電影網爬取近期上映電影資料"""
    try:
        url = "http://www.atmovies.com.tw/movie/next/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.select(".filmListAllX li")
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        movie_list = []
        
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
                
                movie_list.append(movie_data)
                
                print(f"已爬取電影: {title}")
            except Exception as e:
                print(f"處理電影資料時發生錯誤: {e}")
                continue
        
        return movie_list
    except Exception as e:
        print(f"爬取電影資料時發生錯誤: {e}")
        return []

def save_to_firebase(db, movies):
    """將電影資料存入Firebase"""
    if not db:
        print("Firebase未初始化，無法儲存資料")
        return 0
    
    count = 0
    for movie in movies:
        try:
            # 檢查是否已有此電影，如果有則更新，否則新增
            existing_movies = db.collection("電影").where("title", "==", movie["title"]).get()
            
            if len(list(existing_movies)) > 0:
                # 更新現有電影資料
                for doc in existing_movies:
                    db.collection("電影").document(doc.id).update(movie)
            else:
                # 新增電影資料
                db.collection("電影").add(movie)
            
            count += 1
        except Exception as e:
            print(f"儲存電影 {movie['title']} 時發生錯誤: {e}")
            continue
    
    return count

def main():
    """主函數"""
    print("開始爬取開眼電影網電影資料...")
    db = init_firebase()
    
    if not db:
        print("Firebase無法初始化，將只顯示爬取結果但不存入資料庫")
    
    movies = fetch_movie_data()
    
    if not movies:
        print("未爬取到任何電影資料")
        return
    
    print(f"共爬取到 {len(movies)} 部電影")
    
    if db:
        saved_count = save_to_firebase(db, movies)
        print(f"成功儲存 {saved_count} 部電影資料到Firebase")

if __name__ == "__main__":
    main() 