from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required
from app.models import Grade


class StudentForm(Form):
    name = StringField('Name', validators=[Required()])
    grade = SelectField('Grade', coerce=int)
    submit = SubmitField('Add/Modify')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.grade.choices = [(g.id, g.grade) for g in Grade.query.all()]


class GradeForm(Form):
    grade = StringField('Grade', validators=[Required()])
    submit = SubmitField('Add/Modify')

class SubjectForm(Form):
    name = StringField('Subject', validators=[Required()])
    submit = SubmitField('Add/Modify')

class TeacherForm(Form):
    name = StringField('Teacher', validators=[Required()])
    submit = SubmitField('Add/Modify')
