from flask import url_for
from app.models import Student, Grade, LessonDay
import pytest

@pytest.fixture
def grade(db):
    grade = Grade(grade='6th')
    db.session.add(grade)
    db.session.commit()
    return grade


@pytest.fixture
def lesson_day(db):
    lesson_day = LessonDay(name='6th')
    db.session.add(lesson_day)
    db.session.commit()
    return lesson_day


def test_create_new_student(client, app, grade, lesson_day):
    s_name = 'Elliot'
    resp = client.post(url_for('main.new_student'),
                       data={'name': s_name,
                             'grade': grade.id,
                             'lesson_day': lesson_day.id,
                             },
                       follow_redirects=False)

    with app.app_context():
        s_record = Student.query.filter_by(name=s_name).first()
        assert resp.location == url_for('.edit_schedule', student_id=s_record.id, _external=True)

    # Test Elliot in all students
    resp = client.get(url_for('main.students'))
    assert b'Elliot' in resp.data

    # Test that editing has value
    s_record = Student.query.filter_by(name=s_name).first()
    resp = client.get(url_for('main.edit_student', id=s_record.id))
    assert b'value="Elliot' in resp.data


def test_assign_student_grade(client, app, grade, lesson_day):
    s_name = 'Elliot'
    client.post(url_for('main.new_student'),
                       data={'name': s_name,
                             'grade': grade.id,
                             'lesson_day': lesson_day.id,
                             },
                follow_redirects=True)
    s_record = Student.query.filter_by(name=s_name).first()
    s_record.grade_id == grade.id

    # Test grade in all students
    resp = client.get(url_for('main.students'))
    assert b'6th' in resp.data


def test_assign_student_lesson_day(client, app, grade, lesson_day):
    s_name = 'Elliot'
    client.post(url_for('main.new_student'),
                       data={'name': s_name,
                             'grade': grade.id,
                             'lesson_day': lesson_day.id,
                             },
                follow_redirects=True)
    s_record = Student.query.filter_by(name=s_name).first()
    s_record.lesson_day == lesson_day

    # Test grade in all students
    resp = client.get(url_for('main.students'))
    assert b'3' in resp.data
