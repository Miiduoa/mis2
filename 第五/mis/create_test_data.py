import firebase_admin
from firebase_admin import credentials, firestore
import os

# 檢查是否存在 Firebase 配置文件
if not os.path.exists("serviceAccountKey.json"):
    print("錯誤：找不到 serviceAccountKey.json 文件")
    exit(1)

# 初始化 Firebase
try:
    # 避免重複初始化
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    print("Firebase 成功初始化")
except Exception as e:
    print(f"Firebase 初始化失敗: {str(e)}")
    exit(1)

# 測試數據
test_students = [
    {
        "name": "張三",
        "student_id": "S001",
        "department": "資訊管理學系",
        "email": "test1@example.com",
        "courses": ["程式設計", "資料庫管理", "網頁設計"],
        "grades": {
            "程式設計": 85,
            "資料庫管理": 92,
            "網頁設計": 78
        },
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "李四",
        "student_id": "S002",
        "department": "企業管理學系",
        "email": "test2@example.com",
        "courses": ["管理學", "經濟學", "會計學"],
        "grades": {
            "管理學": 75,
            "經濟學": 88,
            "會計學": 82
        },
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "王五",
        "student_id": "S003",
        "department": "資訊工程學系",
        "email": "test3@example.com",
        "courses": ["演算法", "資料結構", "作業系統"],
        "grades": {
            "演算法": 90,
            "資料結構": 95,
            "作業系統": 87
        },
        "created_at": firestore.SERVER_TIMESTAMP
    }
]

# 新增資料到 Firestore
try:
    for student in test_students:
        doc_ref = db.collection('students').document(student["student_id"])
        doc_ref.set(student)
        print(f"已新增學生: {student['name']} (學號: {student['student_id']})")
    
    print("所有測試資料已成功新增到 Firebase")
except Exception as e:
    print(f"新增資料時發生錯誤: {str(e)}") 