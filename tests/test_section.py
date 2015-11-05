from flask import url_for
from app.models import Teacher, Grade, Period, Subject, Section
from datetime import time


def test_create_new_teacher(client, app, db):
    grade = Grade(grade='8th')
    period = Period(number=1, start_time=time(10, 15), end_time=time(11, 30))
    subject = Subject(name='Math')
    teacher = Teacher(name="Mrs. Cox")
    db.session.add(grade)
    db.session.add(subject)
    db.session.add(teacher)
    db.session.add(period)
    db.session.commit()

    name = '1: Section'
    note = "Bathroom"

    resp = client.post(url_for('main.new_section'),
                       data={'name': name,
                             'note': note,
                             'grade': grade.id,
                             'subject': subject.id,
                             'period': period.id,
                             'teacher': teacher.id,
                             },
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.sections', _external=True)

    # # Test note in all sections
    resp = client.get(url_for('main.sections'))
    assert b'Bathroom' in resp.data

    # Test that editing has value
    record = Section.query.filter_by(name=name).first()
    resp = client.get(url_for('main.edit_section', id=record.id))
    assert b'value="1: Section"' in resp.data
    assert b'value="Bathroom' in resp.data
