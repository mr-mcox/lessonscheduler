from flask import url_for
from app import db
import pytest
from app.models import Student
from app.models import Grade


@pytest.fixture(autouse=True)
def setup_db(request, app):
    def reset_db():
        db.session.remove()
        db.drop_all()
        db.create_all()
    request.addfinalizer(reset_db)


def test_create_new_student(client, app):
    grade_name = '6th'
    client.post(url_for('main.new_grade'),
                   data={'grade': grade_name},
                   follow_redirects=True)
    grade = Grade.query.filter_by(grade=grade_name).first()

    s_name = 'Elliot'
    resp = client.post(url_for('main.new_student'),
                       data={'name': s_name, 'grade': grade.id},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.students', _external=True)

    # Test Elliot in all students
    resp = client.get(url_for('main.students'))
    assert b'Elliot' in resp.data

    # Test that editing has value
    s_record = Student.query.filter_by(name=s_name).first()
    resp = client.get(url_for('main.edit_student', id=s_record.id))
    assert b'value="Elliot' in resp.data


def test_assign_student_grade(client, app):
    grade_name = '6th'
    client.post(url_for('main.new_grade'),
                   data={'grade': grade_name},
                   follow_redirects=True)
    grade = Grade.query.filter_by(grade=grade_name).first()

    s_name = 'Elliot'
    client.post(url_for('main.new_student'),
                       data={'name': s_name, 'grade':grade.id},
                       follow_redirects=True)
    s_record = Student.query.filter_by(name=s_name).first()
    s_record.grade_id == grade.id

    # Test grade in all students
    resp = client.get(url_for('main.students'))
    assert b'6th' in resp.data


