from flask import url_for
from app.models import CurrentDay, ScheduleDay, LessonDay
import pytest

@pytest.fixture
def schedule_day1(db):
    schedule_day1 = ScheduleDay(name='A')
    db.session.add(schedule_day1)
    db.session.commit()
    return schedule_day1

@pytest.fixture
def lesson_day1(db):
    lesson_day1 = LessonDay(name='A')
    db.session.add(lesson_day1)
    db.session.commit()
    return lesson_day1

def test_current_day_setup(schedule_day1, lesson_day1, client):
    resp = client.post(url_for('main.setup_current_day'),
                       data={'lesson_day': lesson_day1.id, 'schedule_day': schedule_day1.id},
                       follow_redirects=False)

    obj = CurrentDay.query.first()
    assert obj.lesson_day == lesson_day1
    assert obj.schedule_day == schedule_day1