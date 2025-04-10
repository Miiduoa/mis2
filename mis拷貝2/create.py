import firebase_admin
from firebase_admin import credentials, firestore

# 初始化Firebase
try:
    # 初始化憑證
    cred = credentials.Certificate("credentials/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    print("Firebase初始化成功")
    
    # 建立資料庫連線
    db = firestore.client()
    
    # 準備要存入的資料
    doc = {
        "name": "顧晉瑋",
        "mail": "tcyang@pu.edu.tw",
        "lab": 579
    }
    
    # 方法一：使用指定的文件ID
    doc_ref = db.collection("靜宜資管").document("tcyang")
    doc_ref.set(doc)
    print("使用指定文件ID儲存資料成功")
    
    # 方法二：使用自動產生的文件ID
    doc_ref = db.collection("靜宜資管").add(doc)
    print(f"使用自動產生文件ID儲存資料成功，文件ID: {doc_ref[1].id}")
    
except Exception as e:
    print(f"發生錯誤: {e}")
    print("請確認credentials/serviceAccountKey.json存在且格式正確") 