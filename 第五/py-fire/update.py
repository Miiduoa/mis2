import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def update_student_info(student_id, update_data):
    """更新學生資料"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # 更新文檔
        doc_ref.update(update_data)
        print(f"已成功更新學生 ID {student_id} 的資料")
        
        # 顯示更新後的資料
        updated_doc = doc_ref.get()
        print("更新後的資料：")
        print_student_info(updated_doc.to_dict())
        return True
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return False

def update_student_grade(student_id, course, new_grade):
    """更新學生的特定課程成績"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # 使用 . 符號指定巢狀欄位
        doc_ref.update({
            f"grades.{course}": new_grade
        })
        print(f"已成功更新學生 {student_id} 的 {course} 成績為 {new_grade}")
        return True
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return False

def add_student_course(student_id, new_course):
    """新增學生課程"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        student_data = doc.to_dict()
        
        # 檢查課程是否已存在
        courses = student_data.get('courses', [])
        if new_course in courses:
            print(f"學生已經有 {new_course} 課程")
            return False
        
        # 使用 arrayUnion 添加新課程
        doc_ref.update({
            "courses": firestore.ArrayUnion([new_course])
        })
        print(f"已成功為學生 {student_id} 新增 {new_course} 課程")
        return True
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return False

def print_student_info(student):
    """格式化打印學生資訊"""
    print(f"姓名：{student.get('name')}")
    print(f"學號：{student.get('student_id')}")
    print(f"系所：{student.get('department')}")
    print(f"Email：{student.get('email')}")
    
    # 打印課程和成績
    if 'courses' in student:
        print("課程：")
        for course in student.get('courses', []):
            print(f"  - {course}")
    
    if 'grades' in student:
        print("成績：")
        grades = student.get('grades', {})
        for course, grade in grades.items():
            print(f"  - {course}: {grade}")

if __name__ == "__main__":
    student_id = "A123456789"
    
    # 1. 更新基本資料
    update_data = {
        "name": "王小明（已更新）",
        "email": "updated_email@example.com"
    }
    print("\n1. 更新學生基本資料:")
    update_student_info(student_id, update_data)
    
    # 2. 更新特定課程成績
    print("\n2. 更新學生課程成績:")
    update_student_grade(student_id, "網頁設計", 98)
    
    # 3. 新增課程
    print("\n3. 為學生新增課程:")
    add_student_course(student_id, "雲端運算") 