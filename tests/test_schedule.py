from flask import url_for
from app.models import Teacher, Grade, Period, Subject, Section, ScheduleDay, Student, Schedule
from datetime import time
# from app.main.schedules import store_schedule
import pytest


@pytest.fixture
def grade(db):
    grade = Grade(grade='8th')
    db.session.add(grade)
    db.session.commit()
    return grade


@pytest.fixture
def student(db, grade):
    student = Student(name='Elliot', grade=grade)
    db.session.add(student)
    db.session.commit()
    return student


@pytest.fixture
def schedule_day1(db):
    schedule_day1 = ScheduleDay(name='A')
    db.session.add(schedule_day1)
    db.session.commit()
    return schedule_day1


@pytest.fixture
def schedule_day2(db):
    schedule_day2 = ScheduleDay(name='B')
    db.session.add(schedule_day2)
    db.session.commit()
    return schedule_day2


@pytest.fixture
def period1(db):
    period1 = Period(number=1, start_time=time(10, 15), end_time=time(11, 30))
    db.session.add(period1)
    db.session.commit()
    return period1


@pytest.fixture
def period2(db):
    period2 = Period(number=2, start_time=time(10, 15), end_time=time(11, 30))
    db.session.add(period2)
    db.session.commit()
    return period2


@pytest.fixture
def section1(db, grade, period1):
    subject = Subject(name='Math')
    teacher = Teacher(name="Mrs. Cox")
    section1 = Section(name='1:section',
                       grade=grade,
                       subject=subject,
                       teacher=teacher,
                       period=period1)
    db.session.add(subject)
    db.session.add(teacher)
    db.session.add(section1)
    db.session.commit()
    return section1


@pytest.fixture
def section1B(db, grade, period1):
    subject = Subject(name='Science')
    teacher = Teacher(name="Mr. Pryor")
    section = Section(name='AP - 2',
                      grade=grade,
                      subject=subject,
                      teacher=teacher,
                      period=period1)
    db.session.add(subject)
    db.session.add(teacher)
    db.session.add(section)
    db.session.commit()
    return section


@pytest.fixture
def section2(db, grade, period2):
    subject = Subject(name='Math')
    teacher = Teacher(name="Mrs. Cox")
    section2 = Section(name='2:section',
                       grade=grade,
                       subject=subject,
                       teacher=teacher,
                       period=period2)
    db.session.add(subject)
    db.session.add(teacher)
    db.session.add(section2)
    db.session.commit()
    return section2


def test_edit_schedule(client, app, student, section1, period1, schedule_day1):
    resp = client.get(url_for('main.edit_schedule', student_id=student.id))
    assert b'1:section' in resp.data


def test_store_schedule(client, app, db, grade, student, schedule_day1, section1, period1):

    Schedule().store_schedule(student=student,
                              section=section1,
                              schedule_day=schedule_day1)

    sections_with_period = [
        s.id for s in Section.query.filter_by(period=period1).all()]
    assert Schedule.query.filter(Schedule.section_id.in_(sections_with_period)).filter_by(
        schedule_day=schedule_day1, student=student).first() is not None


def test_schedule_by_student_period_day(section1,
                                        student,
                                        period1,
                                        schedule_day1):

    sch1 = Schedule().store_schedule(student=student,
                                     section=section1,
                                     schedule_day=schedule_day1)
    res = Schedule().schedule_by_student_period_day(student=student,
                                                    period=period1,
                                                    schedule_day=schedule_day1)
    assert res == sch1


def test_edit_removes_old_schedule_at_same_time(section1, section1B, student, schedule_day1):
    Schedule().store_schedule(student=student,
                              section=section1,
                              schedule_day=schedule_day1)
    assert len(Schedule.query.all()) == 1
    Schedule().store_schedule(student=student,
                              section=section1B,
                              schedule_day=schedule_day1)
    assert len(Schedule.query.all()) == 1

def test_do_not_store_duplicates(section1, student, schedule_day1):
    Schedule().store_schedule(student=student,
                              section=section1,
                              schedule_day=schedule_day1)
    assert len(Schedule.query.all()) == 1
    Schedule().store_schedule(student=student,
                              section=section1,
                              schedule_day=schedule_day1)
    assert len(Schedule.query.all()) == 1
