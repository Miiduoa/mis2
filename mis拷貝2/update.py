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
    
    # 方法一：更新特定文件的特定欄位
    doc_ref = db.collection("靜宜資管").document("tcyang")
    
    # 確認文件是否存在
    doc = doc_ref.get()
    if doc.exists:
        print("更新前文件內容:", doc.to_dict())
        
        # 更新特定欄位
        doc_ref.update({
            "lab": 580,
            "last_updated": firestore.SERVER_TIMESTAMP
        })
        print("文件更新成功")
        
        # 確認更新後的內容
        updated_doc = doc_ref.get()
        print("更新後文件內容:", updated_doc.to_dict())
    else:
        print("文件不存在，無法更新")
    
    # 方法二：使用條件篩選更新多個文件
    print("\n使用條件篩選更新多個文件:")
    query_ref = db.collection("靜宜資管").where("name", "==", "顧晉瑋")
    results = query_ref.get()
    
    update_count = 0
    for doc in results:
        db.collection("靜宜資管").document(doc.id).update({
            "title": "教授",
            "last_updated": firestore.SERVER_TIMESTAMP
        })
        update_count += 1
    
    print(f"已更新 {update_count} 筆文件")
    
except Exception as e:
    print(f"發生錯誤: {e}")
    print("請確認credentials/serviceAccountKey.json存在且格式正確") 