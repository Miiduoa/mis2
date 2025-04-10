import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def delete_student(student_id):
    """刪除學生資料"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # 保存資料以顯示刪除內容
        student_data = doc.to_dict()
        
        # 刪除文檔
        doc_ref.delete()
        print(f"已成功刪除學生，ID: {student_id}")
        print("被刪除的資料：")
        print_student_info(student_data)
        return True
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return False

def remove_student_course(student_id, course_to_remove):
    """從學生的課程列表中移除特定課程"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        student_data = doc.to_dict()
        
        # 檢查課程是否存在
        courses = student_data.get('courses', [])
        if course_to_remove not in courses:
            print(f"學生沒有選修 {course_to_remove} 課程")
            return False
        
        # 使用 arrayRemove 移除課程
        doc_ref.update({
            "courses": firestore.ArrayRemove([course_to_remove])
        })
        
        # 如果有該課程的成績，也一併移除
        if 'grades' in student_data and course_to_remove in student_data['grades']:
            # 建立一個新的成績字典，不包含要刪除的課程
            grades = student_data['grades']
            if course_to_remove in grades:
                # 在 Firestore 中刪除特定字段
                doc_ref.update({
                    f"grades.{course_to_remove}": firestore.DELETE_FIELD
                })
        
        print(f"已從學生 {student_id} 的課程列表中移除 {course_to_remove}")
        return True
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return False

def delete_field(student_id, field_to_delete):
    """刪除學生資料中的特定欄位"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # 確認欄位存在
        student_data = doc.to_dict()
        if field_to_delete not in student_data:
            print(f"學生資料中沒有 {field_to_delete} 欄位")
            return False
        
        # 刪除欄位
        doc_ref.update({
            field_to_delete: firestore.DELETE_FIELD
        })
        
        print(f"已從學生 {student_id} 的資料中刪除 {field_to_delete} 欄位")
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
    
    # 1. 移除學生的特定課程
    print("\n1. 移除學生的課程:")
    remove_student_course(student_id, "網頁設計")
    
    # 2. 刪除學生資料中的特定欄位
    print("\n2. 刪除學生資料中的特定欄位:")
    delete_field(student_id, "email")
    
    # 3. 刪除學生資料
    # 注意：通常在實際應用中，不會輕易刪除整筆資料，
    # 而是添加一個 'active' 欄位來標記資料是否有效
    print("\n3. 刪除整筆學生資料:")
    user_confirm = input("確定要刪除學生資料嗎？(y/n): ")
    if user_confirm.lower() == 'y':
        delete_student(student_id)
    else:
        print("取消刪除操作") 