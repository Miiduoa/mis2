import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_student_by_id(student_id):
    """根據學生 ID 獲取學生資料"""
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"找到學生資料：{doc.id}")
        student_data = doc.to_dict()
        print_student_info(student_data)
        return student_data
    else:
        print(f"找不到 ID 為 {student_id} 的學生")
        return None

def get_all_students():
    """獲取所有學生資料"""
    students_ref = db.collection('students')
    docs = students_ref.stream()
    
    students = []
    print("所有學生資料：")
    print("-" * 50)
    
    for doc in docs:
        student_data = doc.to_dict()
        students.append(student_data)
        print_student_info(student_data)
        print("-" * 50)
    
    print(f"總共 {len(students)} 位學生")
    return students

def get_students_by_department(department):
    """根據系所獲取學生資料"""
    query = db.collection('students').where("department", "==", department)
    docs = query.stream()
    
    students = []
    print(f"系所：{department} 的學生資料：")
    print("-" * 50)
    
    for doc in docs:
        student_data = doc.to_dict()
        students.append(student_data)
        print_student_info(student_data)
        print("-" * 50)
    
    print(f"總共 {len(students)} 位 {department} 的學生")
    return students

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

def get_student_by_student_id(student_id_value):
    """根據學生編號獲取特定學生資料"""
    query = db.collection('students').where('student_id', '==', student_id_value)
    docs = query.stream()
    
    students = []
    for doc in docs:
        student_data = doc.to_dict()
        student_data['id'] = doc.id  # 添加文檔ID
        students.append(student_data)
    
    if students:
        return students[0]  # 假設學生編號是唯一的，返回第一個結果
    else:
        print(f"找不到學生編號為 {student_id_value} 的學生")
        return None

def get_all_courses():
    """獲取所有課程資料"""
    courses_ref = db.collection('courses')
    docs = courses_ref.stream()
    
    courses = []
    for doc in docs:
        course_data = doc.to_dict()
        course_data['id'] = doc.id  # 添加文檔ID
        courses.append(course_data)
    
    print(f"獲取了 {len(courses)} 門課程的資料")
    return courses

def get_enrollments_by_student(student_id):
    """獲取學生的所有選課記錄"""
    query = db.collection('enrollments').where('student_id', '==', student_id)
    docs = query.stream()
    
    enrollments = []
    for doc in docs:
        enrollment_data = doc.to_dict()
        enrollment_data['id'] = doc.id  # 添加文檔ID
        enrollments.append(enrollment_data)
    
    print(f"學生 {student_id} 有 {len(enrollments)} 筆選課記錄")
    return enrollments

if __name__ == "__main__":
    # 測試各種讀取操作
    print("\n1. 根據 ID 查詢學生資料:")
    get_student_by_id("A123456789")
    
    print("\n2. 獲取所有學生資料:")
    get_all_students()
    
    print("\n3. 根據系所查詢學生資料:")
    get_students_by_department("資訊管理學系")
    
    try:
        # 獲取所有課程
        print("\n=== 所有課程資料 ===")
        courses = get_all_courses()
        for course in courses:
            print(f"課程: {course.get('name')}, 教師: {course.get('teacher')}, 學分: {course.get('credits')}")
        
        # 如果有至少一位學生，顯示其選課記錄
        if students:
            first_student_id = students[0]['id']
            print(f"\n=== 學生 {students[0].get('name')} 的選課記錄 ===")
            enrollments = get_enrollments_by_student(first_student_id)
            for enrollment in enrollments:
                print(f"課程ID: {enrollment.get('course_id')}, 狀態: {enrollment.get('status')}")
        
    except Exception as e:
        print(f"發生錯誤: {e}") 