from . import db
from sqlalchemy.ext.associationproxy import association_proxy

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))
    sections = association_proxy('schedules', 'sections')

    def __repr__(self):
        return '<Student %r>' % self.name

    def has_grade(self):
        return self.grade is not None


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(128), unique=True)
    students = db.relationship('Student', backref='grade')
    sections = db.relationship('Section', backref='grade')

    def __repr__(self):
        return '<Grade %r>' % self.grade

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    sections = db.relationship('Section', backref='subject')

    def __repr__(self):
        return '<Subject %r>' % self.name

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    sections = db.relationship('Section', backref='teacher')

    def __repr__(self):
        return '<Teacher %r>' % self.name

class ScheduleDay(db.Model):
    __tablename__ = 'schedule_days'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Schedule Day %r>' % self.name

class Period(db.Model):
    __tablename__ = 'periods'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    sections = db.relationship('Section', backref='period')

    def __repr__(self):
        return '<Period %r>' % self.number

    def start_time_as_str(self):
        return self.start_time.strftime('%I:%M %p')

    def end_time_as_str(self):
        return self.end_time.strftime('%I:%M %p')

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    note = db.Column(db.String(128))
    students = association_proxy('schedules', 'students')

    def __repr__(self):
        return '<Section %r>' % self.name

class Schedule(db.Model):
    __tablename__ = 'schedules'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), primary_key=True)
    schedule_day_id = db.Column(db.Integer, db.ForeignKey('schedule_days.id'), primary_key=True, index=True)
    student = db.relationship("Student", backref="schedule")
    section = db.relationship("Section", backref="schedule")
    schedule_day = db.relationship("ScheduleDay", backref="schedule")
    period = db.relationship("Period", secondary='sections')
