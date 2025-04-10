import requests
from bs4 import BeautifulSoup
import time
import os
import firebase_service
import json

# 是否強制使用模擬數據
USE_MOCK_DATA = True

# 檢測是否可以進行網絡請求
def is_network_available():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except:
        return False

def fetch_movie_data(use_mock=USE_MOCK_DATA):
    """從電影網站爬取電影資料"""
    
    # 如果使用模擬數據或網絡不可用，則返回模擬電影數據
    if use_mock or not is_network_available():
        print("使用模擬電影數據")
        mock_movies = get_mock_movies()
        
        # 存入 Firebase
        for movie in mock_movies:
            try:
                firebase_service.create_movie(movie)
            except Exception as e:
                print(f"存入模擬電影數據失敗: {e}")
        
        return mock_movies
    
    url = "https://www.atmovies.com.tw/movie/now/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("開始爬取電影資料...")
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # 確保中文編碼正確
        
        # 檢查請求是否成功
        if response.status_code != 200:
            print(f"請求失敗: {response.status_code}")
            return get_mock_movies()
            
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找出所有電影區塊
        movie_list = soup.select("ul.filmListAll li")
        print(f"找到 {len(movie_list)} 部電影")
        
        if not movie_list:
            print("沒有找到電影，可能是選擇器有誤或網站結構已變更")
            return get_mock_movies()
        
        movies = []
        for movie in movie_list:
            try:
                # 電影標題
                title_element = movie.select_one("div.filmtitle a")
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                movie_link = "https://www.atmovies.com.tw" + title_element["href"]
                
                # 電影海報
                poster_element = movie.select_one("a.filmListPoster img")
                poster = poster_element["src"] if poster_element else ""
                
                # 上映日期
                date_element = movie.select_one("div.filmdate")
                release_date = date_element.text.strip() if date_element else "未知"
                
                print(f"正在爬取電影: {title}")
                
                # 獲取電影詳細資訊
                movie_details = get_movie_details(movie_link)
                
                # 合併基本資訊和詳細資訊
                movie_data = {
                    "title": title,
                    "poster": poster,
                    "release_date": release_date,
                    "link": movie_link,
                    "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    **movie_details
                }
                
                movies.append(movie_data)
                
                # 存入 Firebase
                try:
                    firebase_service.create_movie(movie_data)
                    print(f"電影 '{title}' 已成功存入 Firebase")
                except Exception as e:
                    print(f"存入 Firebase 失敗: {e}")
                
                # 簡單的防止過度爬取
                time.sleep(1)
                
            except Exception as e:
                print(f"處理電影時發生錯誤: {e}")
                continue
        
        print(f"總共爬取了 {len(movies)} 部電影")
        return movies
        
    except Exception as e:
        print(f"爬取電影資料時發生錯誤: {e}")
        return get_mock_movies()

def get_movie_details(movie_url):
    """獲取電影詳細資訊"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(movie_url, headers=headers)
        response.encoding = "utf-8"
        
        if response.status_code != 200:
            return {}
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 片長
        runtime_element = soup.select_one("div.runtime_txt")
        runtime = runtime_element.text.strip() if runtime_element else "未知"
        
        # 導演
        director_element = soup.select_one("div.movie_intro_list h3:contains('導演') + div")
        director = director_element.text.strip() if director_element else "未知"
        
        # 演員
        cast_element = soup.select_one("div.movie_intro_list h3:contains('演員') + div")
        cast = cast_element.text.strip() if cast_element else "未知"
        
        # 劇情簡介
        story_element = soup.select_one("div.gray_infobox_inner span[id^='story']")
        story = story_element.text.strip() if story_element else "未提供劇情簡介"
        
        return {
            "runtime": runtime,
            "director": director,
            "cast": cast,
            "story": story
        }
        
    except Exception as e:
        print(f"獲取電影詳細資訊時發生錯誤: {e}")
        return {}

def get_mock_movies():
    """返回模擬電影數據"""
    mock_movies = [
        {
            "title": "阿凡達：水之道",
            "poster": "https://via.placeholder.com/300x450?text=Avatar",
            "release_date": "2023-05-01",
            "link": "#",
            "runtime": "192分鐘",
            "director": "詹姆斯·卡麥隆",
            "cast": "山姆·沃辛頓, 柔伊·莎達娜, 凱特·溫絲蕾",
            "story": "《阿凡達：水之道》帶觀眾回到潘朵拉星球，故事設定在第一部的數年後，講述蘇麗和傑克組建家庭後的冒險故事，以及他們為保護家園而戰的歷程。",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "title": "蜘蛛人：穿越新宇宙",
            "poster": "https://via.placeholder.com/300x450?text=SpiderMan",
            "release_date": "2023-06-02",
            "link": "#",
            "runtime": "140分鐘",
            "director": "菲爾·羅德, 克里斯托弗·米勒",
            "cast": "沙梅克·摩爾, 海莉·斯坦菲爾德, 奧斯卡·伊薩克",
            "story": "邁爾斯·莫拉萊斯回歸，並與關妮薩·斯黛西一起穿越多元宇宙，遇見一群保護各自世界的蜘蛛人。當強大的新威脅出現，他們必須共同合作。",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "title": "奧本海默",
            "poster": "https://via.placeholder.com/300x450?text=Oppenheimer",
            "release_date": "2023-07-21",
            "link": "#",
            "runtime": "180分鐘",
            "director": "克里斯多福·諾蘭",
            "cast": "基里安·墨菲, 艾蜜莉·布朗, 羅伯特·唐尼Jr.",
            "story": "這部電影講述了J·羅伯特·奧本海默的故事，他是「曼哈頓計劃」的關鍵人物，這個計劃開發了第一枚原子彈。影片深入探討了他的生活和對科學的貢獻，以及他所作選擇帶來的道德困境。",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "title": "芭比",
            "poster": "https://via.placeholder.com/300x450?text=Barbie",
            "release_date": "2023-07-21",
            "link": "#",
            "runtime": "114分鐘",
            "director": "格蕾塔·葛韋格",
            "cast": "瑪格羅比, 萊恩·葛斯林, 美國·法拉",
            "story": "住在完美世界的芭比娃娃突然開始思考死亡等難題，繼而被逐出烏托邦，踏上人類世界之旅，發現真實生活的喜悅和複雜。",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "title": "玩命關頭10",
            "poster": "https://via.placeholder.com/300x450?text=FastX",
            "release_date": "2023-05-19",
            "link": "#",
            "runtime": "141分鐘",
            "director": "路易·萊特里爾",
            "cast": "馮·迪索, 米歇爾·羅德里奎茲, 傑森·摩莫亞",
            "story": "唐老大與他的家人在前作擊敗了反派後，本集出現了更強大的敵人。他將面對自己過往的陰影，必須再次團結所有人來對抗這個新威脅。",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    return mock_movies

if __name__ == "__main__":
    # 清除所有電影資料，重新爬取
    try:
        firebase_service.delete_all_movies()
        print("已清除所有舊電影資料")
    except Exception as e:
        print(f"清除電影資料失敗: {e}")
    
    # 參數 True 表示使用模擬數據，False 表示嘗試實際爬取
    movies = fetch_movie_data(use_mock=True)
    print(f"成功爬取 {len(movies)} 部電影資料") 