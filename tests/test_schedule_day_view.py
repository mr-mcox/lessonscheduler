from flask import url_for
import pytest
from selenium import webdriver
from app.models import Teacher, Grade, Period, Subject, Section, ScheduleDay, Student, Schedule, LessonDay
from datetime import time
import time as ptime
from selenium.webdriver.support.ui import Select


@pytest.fixture
def grade(db):
    grade = Grade(grade='8th')
    db.session.add(grade)
    db.session.commit()
    return grade

@pytest.fixture
def lesson_day(db):
    lesson_day = LessonDay(name='6th')
    db.session.add(lesson_day)
    db.session.commit()
    return lesson_day


@pytest.fixture
def student(db, grade, lesson_day):
    student = Student(name='Elliot', grade=grade, lesson_day=lesson_day)
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
def section1(db, grade, period1):
    subject = Subject(name='Math')
    teacher = Teacher(name="Mrs. Cox")
    section1 = Section(name='Mrs. Cox Math',
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
    section = Section(name='Mr. Pryor Science',
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
def student_schedule(client, app, db, grade, student, schedule_day1, schedule_day2, section1, section1B, period1):

    Schedule().store_schedule(student=student,
                              section=section1,
                              schedule_day=schedule_day1)
    Schedule().store_schedule(student=student,
                              section=section1B,
                              schedule_day=schedule_day2)


@pytest.mark.usefixtures('live_server')
@pytest.mark.selenium
class TestLiveServer:

    browser = None

    @pytest.fixture(scope='class')
    def browser(self, request):
        browser = webdriver.Firefox()

        def quit_browser():
            browser.quit()

        request.addfinalizer(quit_browser)
        return browser

    def test_server_is_up_and_running(self, app, browser):
        browser.get(url_for('main.index', _external=True))
        assert 'Lesson Scheduler' in browser.title

    def test_filter_sections_by_day(self, app, browser, student_schedule):
        # There are two schedule days (A and B) one lesson day with one student

        # Emily goes to home page
        browser.get(url_for('main.index', _external=True))
        # Emily clicks on setup menu
        browser.find_element_by_link_text("Setup").click()
        # Emily clicks on setup day
        browser.find_element_by_link_text("Setup Today").click()
        # Emily chooses schedule day A
        day_menu = Select(browser.find_element_by_name("schedule_day"))
        day_menu.select_by_visible_text("A")
        # Emily clicks the setup button
        browser.find_element_by_name("submit").click()
        # Emily clicks on students
        browser.find_element_by_name("Student menu").click()
        # Emily selects all students
        browser.find_element_by_link_text("All Students").click()
        #Emily clicks into Elliot
        browser.find_element_by_link_text("Elliot").click()
        # The only classes shown are for schedule day A
        assert "Mrs. Cox"  in browser.page_source
        assert "Mr. Pryor" not in browser.page_source
        # Emily clicks on setup menu
        # Emily clicks on setup day
        # Emily chooses schedule day B
        # Emily clicks the setup button
        # Emily clicks on students
        # Emily selects lesson day 1
        # The only classes shown are for schedule day B
