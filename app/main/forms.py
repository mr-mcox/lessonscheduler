from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required


class StudentForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Submit')

    # def __init__(self, student=None, *args, **kwargs):
    #     super(StudentForm, self).__init__(*args, **kwargs)
    #     self.student = student
