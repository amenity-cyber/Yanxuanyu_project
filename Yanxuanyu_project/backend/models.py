from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    selections = db.relationship('Selection', backref='student', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_no': self.student_no,
            'name': self.name,
            'gender': self.gender
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_no = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(50))
    credits = db.Column(db.Integer, nullable=False)
    max_students = db.Column(db.Integer, default=50)
    current_students = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    
    selections = db.relationship('Selection', backref='course', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_no': self.course_no,
            'course_name': self.course_name,
            'teacher': self.teacher,
            'credits': self.credits,
            'max_students': self.max_students,
            'current_students': self.current_students,
            'description': self.description,
            'available_seats': self.max_students - self.current_students
        }

class Selection(db.Model):
    __tablename__ = 'selections'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    select_time = db.Column(db.DateTime, default=datetime.now)
    score = db.Column(db.Numeric(5, 2))