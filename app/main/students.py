from ..models import Student, Grade
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import StudentForm


@main.route('/student/', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student()
        student.name = form.name.data
        student.grade = Grade.query.get(form.grade.data)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('.students'))
    return render_template('student_form.html', form=form)


@main.route('/students/')
def students():
    students = Student.query.all()
    return render_template('all_students.html', students=students)


@main.route('/students/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(name=student.name)
    if form.validate_on_submit():
        student.name = form.name.data
        student.grade = Grade.query.get(form.grade.data)
        db.session.add(student)
        flash('The student has been updated.')
        return redirect(url_for('.students'))
    return render_template('student_form.html', form=form, student=student)
