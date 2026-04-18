from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import traceback
from contextlib import contextmanager

app = Flask(__name__)
CORS(app)

# 数据库配置 - 修改为你的密码
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 改成你的MySQL密码
    'database': 'course_system',
    'charset': 'utf8mb4'
}


@contextmanager
def get_db_connection():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, student_no, name, gender, created_at FROM students")
            students = cursor.fetchall()
            for s in students:
                if s.get('created_at'):
                    s['created_at'] = str(s['created_at'])
            return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT id, course_no, course_name, teacher, credits, 
                       max_students, current_students, description,
                       (max_students - current_students) as available_seats
                FROM courses
            """)
            courses = cursor.fetchall()
            return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/selections', methods=['POST'])
def select_course():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
            if not cursor.fetchone():
                return jsonify({'error': '学生不存在'}), 404

            cursor.execute("SELECT id, current_students, max_students FROM courses WHERE id = %s", (course_id,))
            course = cursor.fetchone()
            if not course:
                return jsonify({'error': '课程不存在'}), 404

            if course['current_students'] >= course['max_students']:
                return jsonify({'error': '课程已满'}), 400

            cursor.execute("SELECT id FROM selections WHERE student_id = %s AND course_id = %s",
                           (student_id, course_id))
            if cursor.fetchone():
                return jsonify({'error': '已经选过该课程'}), 400

            cursor.execute("INSERT INTO selections (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
            cursor.execute("UPDATE courses SET current_students = current_students + 1 WHERE id = %s", (course_id,))

            return jsonify({'message': '选课成功'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/selections/<int:student_id>', methods=['GET'])
def get_student_selections(student_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT s.id as selection_id, c.id as course_id, c.course_no, c.course_name, 
                       c.teacher, c.credits, s.select_time, s.score
                FROM selections s
                JOIN courses c ON s.course_id = c.id
                WHERE s.student_id = %s
                ORDER BY s.select_time DESC
            """, (student_id,))
            selections = cursor.fetchall()
            for sel in selections:
                if sel.get('select_time'):
                    sel['select_time'] = str(sel['select_time'])
            return jsonify(selections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/selections/<int:selection_id>', methods=['DELETE'])
def drop_course(selection_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT course_id FROM selections WHERE id = %s", (selection_id,))
            selection = cursor.fetchone()
            if not selection:
                return jsonify({'error': '选课记录不存在'}), 404

            cursor.execute("DELETE FROM selections WHERE id = %s", (selection_id,))
            cursor.execute("UPDATE courses SET current_students = current_students - 1 WHERE id = %s",
                           (selection['course_id'],))

            return jsonify({'message': '退课成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT COUNT(*) as count FROM students")
            total_students = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM courses")
            total_courses = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM selections")
            total_selections = cursor.fetchone()['count']

            cursor.execute("""
                SELECT course_name, current_students, max_students
                FROM courses
                ORDER BY current_students DESC
                LIMIT 5
            """)
            popular_courses = cursor.fetchall()

            return jsonify({
                'total_students': total_students,
                'total_courses': total_courses,
                'total_selections': total_selections,
                'popular_courses': popular_courses
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': '后端服务正常运行！', 'status': 'ok', 'database': 'MySQL'})


if __name__ == '__main__':
    print("=" * 50)
    print("学生选课系统后端服务 (MySQL版本)")
    print("=" * 50)
    print(f"数据库: {DB_CONFIG['database']} @ {DB_CONFIG['host']}")
    print("服务器: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)