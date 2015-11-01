from . import db
from app.exceptions import ValidationError


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Student %r>' % self.name

    @staticmethod
    def from_json(json_student):
        name = json_student.get('name')
        if name is None or name == '':
            raise ValidationError('student does not have a name')
        return Student(name=name)

    def to_json(self):
        json_student = {'id': self.id, 'name': self.name}
        print(json_student)
        return json_student


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Grade %r>' % self.grade