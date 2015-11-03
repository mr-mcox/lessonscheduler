from . import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))

    def __repr__(self):
        return '<Student %r>' % self.name

    def has_grade(self):
        return self.grade is not None


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(128), unique=True)
    students = db.relationship('Student', backref='grade')

    def __repr__(self):
        return '<Grade %r>' % self.grade

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Subject %r>' % self.name