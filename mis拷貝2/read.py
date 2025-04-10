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
    
    # 方法一：讀取特定文件
    doc_ref = db.collection("靜宜資管").document("tcyang")
    doc = doc_ref.get()
    if doc.exists:
        print("文件內容:", doc.to_dict())
    else:
        print("文件不存在")
    
    # 方法二：讀取整個集合
    print("\n讀取集合內所有文件:")
    docs = db.collection("靜宜資管").get()
    for doc in docs:
        print(f"文件ID: {doc.id}, 內容: {doc.to_dict()}")
    
    # 方法三：使用條件篩選
    print("\n使用條件篩選:")
    query_ref = db.collection("靜宜資管").where("lab", "==", 579)
    results = query_ref.get()
    for doc in results:
        print(f"文件ID: {doc.id}, 內容: {doc.to_dict()}")
    
    # 方法四：排序結果
    print("\n排序結果:")
    ordered_ref = db.collection("靜宜資管").order_by("name")
    ordered_results = ordered_ref.get()
    for doc in ordered_results:
        print(f"文件ID: {doc.id}, 內容: {doc.to_dict()}")
    
    # 方法五：限制結果數量
    print("\n限制結果數量:")
    limited_ref = db.collection("靜宜資管").limit(2)
    limited_results = limited_ref.get()
    for doc in limited_results:
        print(f"文件ID: {doc.id}, 內容: {doc.to_dict()}")
    
except Exception as e:
    print(f"發生錯誤: {e}")
    print("請確認credentials/serviceAccountKey.json存在且格式正確") 