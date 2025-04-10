import os
import json
import uuid
import datetime

# 是否強制使用模擬模式
FORCE_MOCK_MODE = True

print("使用模擬資料庫...")

# 模擬資料庫類定義
class MockDB:
    def __init__(self):
        self.collections = {
            'users': {},
            'movies': {}
        }
    
    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = {}
        return MockCollection(self.collections[name])

class MockCollection:
    def __init__(self, data):
        self.data = data
    
    def document(self, doc_id):
        return MockDocument(self.data, doc_id)
    
    def stream(self):
        return [MockDocumentSnapshot(doc_id, data) for doc_id, data in self.data.items()]
    
    def add(self, data):
        doc_id = str(uuid.uuid4())
        self.data[doc_id] = data
        return doc_id

class MockDocument:
    def __init__(self, collection_data, doc_id):
        self.collection_data = collection_data
        self.doc_id = doc_id
    
    def set(self, data):
        self.collection_data[self.doc_id] = data
        return self.doc_id
    
    def update(self, data):
        if self.doc_id in self.collection_data:
            self.collection_data[self.doc_id].update(data)
        return self.doc_id
    
    def get(self):
        return MockDocumentSnapshot(self.doc_id, self.collection_data.get(self.doc_id, {}))
    
    def delete(self):
        if self.doc_id in self.collection_data:
            del self.collection_data[self.doc_id]

class MockDocumentSnapshot:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self._data = data
        self.exists = bool(data)
    
    def to_dict(self):
        return self._data
    
    @property
    def reference(self):
        return self
    
    def delete(self):
        pass

# 創建模擬數據庫實例
db = MockDB()

# 增加一些初始模擬數據
users_collection = db.collection('users')
users_collection.document('user1').set({
    'name': '測試用戶1',
    'email': 'test1@example.com',
    'role': '使用者',
    'created_at': '2023-01-01'
})
users_collection.document('user2').set({
    'name': '測試用戶2',
    'email': 'test2@example.com',
    'role': '管理員',
    'created_at': '2023-01-02'
})

movies_collection = db.collection('movies')
movies_collection.document('movie1').set({
    'title': '測試電影1',
    'release_date': '2023-01-01',
    'poster': 'https://via.placeholder.com/300x450',
    'runtime': '120分鐘',
    'director': '導演名稱',
    'story': '這是一部測試電影的劇情簡介。',
    'link': '#'
})
movies_collection.document('movie2').set({
    'title': '測試電影2',
    'release_date': '2023-02-01',
    'poster': 'https://via.placeholder.com/300x450',
    'runtime': '90分鐘',
    'director': '另一位導演',
    'story': '這是另一部測試電影的劇情簡介。',
    'link': '#'
})

# 使用者管理功能
def create_user(user_id, user_data):
    """新增使用者資料"""
    try:
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # 加入時間戳記
        if 'created_at' not in user_data:
            user_data['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        user_ref = db.collection('users').document(user_id)
        user_ref.set(user_data)
        return user_id
    except Exception as e:
        print(f"創建使用者時發生錯誤: {e}")
        raise e

def get_user(user_id):
    """取得使用者資料"""
    try:
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get()
        if user.exists:
            return user.to_dict()
        return None
    except Exception as e:
        print(f"獲取使用者時發生錯誤: {e}")
        return None

def get_all_users():
    """取得所有使用者資料"""
    try:
        users = []
        docs = db.collection('users').stream()
        for doc in docs:
            user = doc.to_dict()
            user['id'] = doc.id
            users.append(user)
        return users
    except Exception as e:
        print(f"獲取所有使用者時發生錯誤: {e}")
        raise e

def update_user(user_id, user_data):
    """更新使用者資料"""
    try:
        user_ref = db.collection('users').document(user_id)
        
        # 加入更新時間
        user_data['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        user_ref.update(user_data)
        return user_id
    except Exception as e:
        print(f"更新使用者時發生錯誤: {e}")
        raise e

def delete_user(user_id):
    """刪除使用者資料"""
    try:
        db.collection('users').document(user_id).delete()
        return user_id
    except Exception as e:
        print(f"刪除使用者時發生錯誤: {e}")
        raise e

# 電影資料功能
def create_movie(movie_data):
    """新增電影資料"""
    try:
        # 使用電影標題作為文件ID (或指定一個唯一ID)
        movie_id = movie_data.get('title', str(uuid.uuid4()))
        
        # 處理特殊字符，避免ID無效
        movie_id = movie_id.replace('/', '_').replace(' ', '_')
        
        # 加入時間戳記
        if 'created_at' not in movie_data:
            movie_data['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        movie_ref = db.collection('movies').document(movie_id)
        movie_ref.set(movie_data)
        return movie_id
    except Exception as e:
        print(f"創建電影資料時發生錯誤: {e}")
        raise e

def get_movie(movie_id):
    """取得電影資料"""
    try:
        movie_ref = db.collection('movies').document(movie_id)
        movie = movie_ref.get()
        if movie.exists:
            return movie.to_dict()
        return None
    except Exception as e:
        print(f"獲取電影資料時發生錯誤: {e}")
        return None

def get_all_movies():
    """取得所有電影資料"""
    try:
        movies = []
        docs = db.collection('movies').stream()
        for doc in docs:
            movie = doc.to_dict()
            movie['id'] = doc.id
            movies.append(movie)
        return movies
    except Exception as e:
        print(f"獲取所有電影資料時發生錯誤: {e}")
        raise e

def update_movie(movie_id, movie_data):
    """更新電影資料"""
    try:
        movie_ref = db.collection('movies').document(movie_id)
        
        # 加入更新時間
        movie_data['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        movie_ref.update(movie_data)
        return movie_id
    except Exception as e:
        print(f"更新電影資料時發生錯誤: {e}")
        raise e

def delete_movie(movie_id):
    """刪除電影資料"""
    try:
        db.collection('movies').document(movie_id).delete()
        return movie_id
    except Exception as e:
        print(f"刪除電影資料時發生錯誤: {e}")
        raise e

def delete_all_movies():
    """刪除所有電影資料"""
    try:
        docs = db.collection('movies').stream()
        for doc in docs:
            doc.reference.delete()
        print("已成功刪除所有電影資料")
    except Exception as e:
        print(f"刪除所有電影資料時發生錯誤: {e}")
        raise e 