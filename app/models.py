from . import db
from sqlalchemy.ext.associationproxy import association_proxy


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))
    lesson_day_id = db.Column(db.Integer, db.ForeignKey('lesson_days.id'))
    sections = association_proxy('schedules', 'sections')

    def __repr__(self):
        return '<Student %r>' % self.name

    def has_grade(self):
        return self.grade is not None

    def has_lesson_day(self):
        return self.lesson_day is not None


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

    def period_span(self):
        return self.start_time.strftime('%I:%M') + "-" + self.end_time.strftime('%I:%M')


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
    student_id = db.Column(
        db.Integer, db.ForeignKey('students.id'), primary_key=True)
    section_id = db.Column(
        db.Integer, db.ForeignKey('sections.id'), primary_key=True)
    schedule_day_id = db.Column(
        db.Integer, db.ForeignKey('schedule_days.id'), primary_key=True, index=True)
    student = db.relationship("Student", backref="schedule")
    section = db.relationship("Section", backref="schedule")
    schedule_day = db.relationship("ScheduleDay", backref="schedule")

    def store_schedule(self, student, section, schedule_day):
        cur_sch = Schedule().schedule_by_student_period_day(student=student,
                                                            period=section.period,
                                                            schedule_day=schedule_day)
        if cur_sch is not None and cur_sch.section != section:
            db.session.delete(cur_sch)

        schedule = None

        if cur_sch is None or cur_sch.section != section:
            schedule = Schedule(
                student=student, section=section, schedule_day=schedule_day)
            db.session.add(schedule)

        db.session.commit()
        return schedule

    def schedule_by_student_period_day(self, student, period, schedule_day):
        sections_with_period = [
            s.id for s in Section.query.filter_by(period=period).all()]
        return Schedule.query.filter(Schedule.section_id.in_(sections_with_period)).filter_by(
            schedule_day=schedule_day, student=student).first()


class LessonDay(db.Model):
    __tablename__ = 'lesson_days'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    students = db.relationship('Student', backref='lesson_day')

    def __repr__(self):
        return '<LessonDay %r>' % self.name


class CurrentDay(db.Model):
    __tablename__ = 'current_day'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    schedule_day_id = db.Column(db.Integer, db.ForeignKey('schedule_days.id'))
    schedule_day = db.relationship('ScheduleDay')
    lessod_day_id = db.Column(db.Integer, db.ForeignKey('lesson_days.id'))
    lesson_day = db.relationship('LessonDay')

    def __repr__(self):
        return '<Current Day %r>' % self.date
