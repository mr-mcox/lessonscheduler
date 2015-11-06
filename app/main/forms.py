from flask.ext.wtf import Form
from wtforms import Form as NoCsrfForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField, HiddenField, FieldList, FormField
from wtforms_components import TimeField
from wtforms.validators import Required
from app.models import Grade, Subject, Period, Teacher, Section, LessonDay


class StudentForm(Form):
    name = StringField('Name', validators=[Required()])
    grade = SelectField('Grade', coerce=int)
    lesson_day = SelectField('Lesson Day', coerce=int)
    submit = SubmitField('Add/Modify')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.grade.choices = [(g.id, g.grade) for g in Grade.query.all()]
        self.lesson_day.choices = [(g.id, g.name) for g in LessonDay.query.all()]


class GradeForm(Form):
    grade = StringField('Grade', validators=[Required()])
    submit = SubmitField('Add/Modify')


class SubjectForm(Form):
    name = StringField('Subject', validators=[Required()])
    submit = SubmitField('Add/Modify')


class TeacherForm(Form):
    name = StringField('Teacher', validators=[Required()])
    submit = SubmitField('Add/Modify')


class ScheduleDayForm(Form):
    name = StringField('Schedule Day', validators=[Required()])
    submit = SubmitField('Add/Modify')

class LessonDayForm(Form):
    name = StringField('LessonDay', validators=[Required()])
    submit = SubmitField('Add/Modify')


class PeriodForm(Form):
    number = IntegerField('Number', validators=[Required()])
    start_time = TimeField('Start Time', validators=[Required()])
    end_time = TimeField('End Time', validators=[Required()])
    submit = SubmitField('Add/Modify')


class SectionForm(Form):
    name = StringField('Section Name', validators=[Required()])
    grade = SelectField('Grade', coerce=int)
    subject = SelectField('Subject', coerce=int)
    teacher = SelectField('Teacher', coerce=int)
    period = SelectField('Period', coerce=int)
    note = StringField('Room/Note')
    submit = SubmitField('Add/Modify')

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.grade.choices = [(g.id, g.grade) for g in Grade.query.all()]
        self.subject.choices = [(x.id, x.name) for x in Subject.query.all()]
        self.teacher.choices = [(x.id, x.name) for x in Teacher.query.all()]
        self.period.choices = [(x.id, x.number) for x in Period.query.all()]


class ScheduleFormItem(NoCsrfForm):
    student = HiddenField()
    schedule_day = HiddenField()
    section = SelectField("Section", coerce=int)
    
    def __init__(self, *args, **kwargs):
        super(ScheduleFormItem, self).__init__(*args, **kwargs)
        self.section.choices = [ (s.id, s.name) for s in Section.query.all()]
        # self.section.choices = [ Section.query.all()]
        print(self.section.choices)


class SchedulePeriodGroup(NoCsrfForm):
    schedule_days = FieldList(FormField(ScheduleFormItem))
    period_num = None


class ScheduleForm(Form):
    periods = FieldList(FormField(SchedulePeriodGroup))
