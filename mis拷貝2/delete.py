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
    
    # 方法一：刪除特定文件
    doc_ref = db.collection("靜宜資管").document("tcyang")
    
    # 確認文件是否存在
    doc = doc_ref.get()
    if doc.exists:
        print("刪除前文件內容:", doc.to_dict())
        
        # 刪除文件
        doc_ref.delete()
        print("文件刪除成功")
        
        # 確認文件已刪除
        deleted_doc = doc_ref.get()
        if not deleted_doc.exists:
            print("文件已確認刪除")
    else:
        print("文件不存在，無法刪除")
    
    # 方法二：使用條件篩選刪除多個文件
    print("\n使用條件篩選刪除多個文件:")
    query_ref = db.collection("靜宜資管").where("title", "==", "教授")
    results = query_ref.get()
    
    delete_count = 0
    for doc in results:
        db.collection("靜宜資管").document(doc.id).delete()
        delete_count += 1
    
    print(f"已刪除 {delete_count} 筆文件")
    
    # 方法三：批次刪除（效能較佳的方法）
    print("\n批次刪除:")
    batch = db.batch()
    
    # 找出要刪除的文件
    to_delete = db.collection("靜宜資管").limit(5).get()
    
    for doc in to_delete:
        batch.delete(db.collection("靜宜資管").document(doc.id))
    
    # 執行批次操作
    batch.commit()
    print(f"已批次刪除 {len(to_delete)} 筆文件")
    
except Exception as e:
    print(f"發生錯誤: {e}")
    print("請確認credentials/serviceAccountKey.json存在且格式正確") 