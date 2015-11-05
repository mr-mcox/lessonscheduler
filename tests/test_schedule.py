from flask import url_for
from app.models import Teacher, Grade, Period, Subject, Section, ScheduleDay, Student, Schedule

from datetime import time


def test_schedule(client, app, db):
    grade = Grade(grade='8th')
    period1 = Period(number=1, start_time=time(10, 15), end_time=time(11, 30))
    period2 = Period(number=2, start_time=time(10, 15), end_time=time(11, 30))
    subject = Subject(name='Math')
    teacher = Teacher(name="Mrs. Cox")
    section1 = Section(name='1:section',
                       grade=grade,
                       subject=subject,
                       teacher=teacher,
                       period=period1)
    section2 = Section(name='2:section',
                       grade=grade,
                       subject=subject,
                       teacher=teacher,
                       period=period2)
    schedule_day1 = ScheduleDay(name='A')
    schedule_day2 = ScheduleDay(name='B')
    student = Student(name='Elliot', grade=grade)
    db.session.add(grade)
    db.session.add(subject)
    db.session.add(teacher)
    db.session.add(period1)
    db.session.add(period2)
    db.session.add(section1)
    db.session.add(section2)
    db.session.add(student)
    db.session.add(schedule_day1)
    db.session.add(schedule_day2)
    db.session.commit()

    schedule1 = Schedule(
        student=student, section=section1, schedule_day=schedule_day1)
    schedule2 = Schedule(
        student=student, section=section2, schedule_day=schedule_day2)
    db.session.add(schedule1)
    db.session.add(schedule2)
    db.session.commit()

    sections_with_period = [
        s.id for s in Section.query.filter_by(period=period1).all()]
    assert Schedule.query.filter(Schedule.section_id.in_(sections_with_period)).filter_by(
        schedule_day=schedule_day1, student=student).first() == schedule1

    resp = client.post(url_for('main.edit_schedule', student_id=student.id),
                       data={'student': student.id,
                             'section': section1.id,
                             'schedule_day': schedule_day1,
                             },
                       follow_redirects=False)

    resp = client.get(url_for('main.edit_schedule', student_id=student.id))
    assert b'1:section' in resp.data
