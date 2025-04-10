import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# 初始化 Firebase
# 請將 serviceAccountKey.json 放在與此檔案相同的資料夾中
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# 獲取 Firestore 客戶端
db = firestore.client()

def add_data():
    """新增資料到 Firestore 資料庫"""
    # 準備要新增的資料
    data = {
        "name": "王小明",
        "student_id": "A123456789",
        "department": "資訊管理學系",
        "courses": ["網頁設計", "資料庫管理", "Python 程式設計"],
        "grades": {
            "網頁設計": 95,
            "資料庫管理": 88,
            "Python 程式設計": 92
        },
        "email": "student@example.com",
        "created_at": firestore.SERVER_TIMESTAMP
    }
    
    # 新增資料到 'students' 集合中
    doc_ref = db.collection('students').document(data["student_id"])
    doc_ref.set(data)
    print(f"已成功新增學生資料：{data['name']} ({data['student_id']})")
    
    # 返回資料 ID
    return data["student_id"]

def add_course():
    """新增課程資料到 Firestore"""
    # 課程集合參考
    courses_ref = db.collection('courses')
    
    # 新增課程資料
    course_data = {
        'course_id': 'C101',
        'name': '資訊管理導論',
        'teacher': '張教授',
        'credits': 3,
        'semester': '112-1',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    # 使用自訂 ID 新增文檔
    doc_ref = courses_ref.document('C101')
    doc_ref.set(course_data)
    
    print(f"課程資料已新增，文檔ID: {doc_ref.id}")
    return doc_ref.id

def add_enrollment(student_id, course_id):
    """新增選課記錄到 Firestore"""
    # 選課集合參考
    enrollments_ref = db.collection('enrollments')
    
    # 新增選課資料
    enrollment_data = {
        'student_id': student_id,
        'course_id': course_id,
        'enrollment_date': datetime.datetime.now(),
        'status': 'active',
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    # 新增文檔，讓 Firestore 自動生成 ID
    doc_ref = enrollments_ref.add(enrollment_data)
    
    print(f"選課記錄已新增，文檔ID: {doc_ref[1].id}")
    return doc_ref[1].id

if __name__ == "__main__":
    try:
        # 執行新增資料函數
        student_id = add_data()
        
        # 新增課程資料
        course_id = add_course()
        
        # 新增選課記錄
        add_enrollment(student_id, course_id)
        
        print("所有資料已成功新增到 Firestore！")
    except Exception as e:
        print(f"發生錯誤: {e}") 