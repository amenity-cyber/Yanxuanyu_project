-- 创建数据库
CREATE DATABASE IF NOT EXISTS course_system;
USE course_system;

-- 学生表
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 课程表
CREATE TABLE IF NOT EXISTS courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_no VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    teacher VARCHAR(50),
    credits INT NOT NULL,
    max_students INT DEFAULT 50,
    current_students INT DEFAULT 0,
    description TEXT
);

-- 选课表
CREATE TABLE IF NOT EXISTS selections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    select_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score DECIMAL(5,2) DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_selection (student_id, course_id)
);

-- 插入测试数据
INSERT INTO students (student_no, name, gender) VALUES
('2024001', '张三', '男'),
('2024002', '李四', '女'),
('2024003', '王五', '男');

INSERT INTO courses (course_no, course_name, teacher, credits, max_students, description) VALUES
('CS101', 'Python程序设计', '张教授', 3, 30, 'Python编程基础课程'),
('CS102', '数据库原理', '李教授', 4, 25, '数据库设计与SQL语言'),
('CS103', 'Web开发', '王教授', 3, 20, '前后端开发技术'),
('CS104', '数据结构', '赵教授', 4, 30, '算法与数据结构基础');