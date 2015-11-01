from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required


class StudentForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Add/Modify')

class GradeForm(Form):
    grade = StringField('Grade', validators=[Required()])
    submit = SubmitField('Add/Modify')