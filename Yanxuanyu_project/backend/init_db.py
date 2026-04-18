import pymysql

# 数据库配置（修改密码为你自己的）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # ⚠️ 改成你的MySQL密码
    'charset': 'utf8mb4'
}

print("=" * 50)
print("开始初始化MySQL数据库")
print("=" * 50)

try:
    # 连接MySQL
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("✓ 连接MySQL成功")
    
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS course_system")
    print("✓ 数据库 course_system 已创建")
    
    # 使用数据库
    cursor.execute("USE course_system")
    
    # 创建学生表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_no VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            gender VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ 学生表已创建")
    
    # 创建课程表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT PRIMARY KEY AUTO_INCREMENT,
            course_no VARCHAR(20) UNIQUE NOT NULL,
            course_name VARCHAR(100) NOT NULL,
            teacher VARCHAR(50),
            credits INT NOT NULL,
            max_students INT DEFAULT 50,
            current_students INT DEFAULT 0,
            description TEXT
        )
    """)
    print("✓ 课程表已创建")
    
    # 创建选课表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS selections (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            course_id INT NOT NULL,
            select_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            score DECIMAL(5,2) DEFAULT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            UNIQUE KEY unique_selection (student_id, course_id)
        )
    """)
    print("✓ 选课表已创建")
    
    # 检查并插入测试数据
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        # 插入学生
        students = [
            ('2024001', '张三', '男'),
            ('2024002', '李四', '女'),
            ('2024003', '王五', '男')
        ]
        cursor.executemany("INSERT INTO students (student_no, name, gender) VALUES (%s, %s, %s)", students)
        
        # 插入课程
        courses = [
            ('CS101', 'Python程序设计', '张教授', 3, 30, 'Python编程基础课程'),
            ('CS102', '数据库原理', '李教授', 4, 25, '数据库设计与SQL语言'),
            ('CS103', 'Web开发', '王教授', 3, 20, '前后端开发技术'),
            ('CS104', '数据结构', '赵教授', 4, 30, '算法与数据结构基础')
        ]
        cursor.executemany("""
            INSERT INTO courses (course_no, course_name, teacher, credits, max_students, description) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, courses)
        
        conn.commit()
        print("✓ 测试数据已添加")
    else:
        print("✓ 数据已存在")
    
    # 显示统计
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM courses")
    course_count = cursor.fetchone()[0]
    
    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print(f"学生数量: {student_count}")
    print(f"课程数量: {course_count}")
    print("=" * 50)
    
    conn.close()
    
except Exception as e:
    print(f"✗ 错误: {e}")
    print("\n请检查：")
    print("1. MySQL服务是否启动")
    print("2. 密码是否正确")