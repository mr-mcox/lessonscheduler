from ..models import Student, Grade, LessonDay
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
        student.lesson_day = LessonDay.query.get(form.lesson_day.data)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('.students'))
    return render_template('student_form.html', form=form)


@main.route('/students/')
def students():
    students = Student.query.join(Grade).order_by(Grade.grade, Student.name).all()
    return render_template('all_students.html', students=students)

@main.route('/students/lesson_day/<int:lesson_day_id>')
def students_for_lesson_day(lesson_day_id):
    lesson_day = LessonDay.query.get_or_404(lesson_day_id)
    students = Student.query.filter_by(lesson_day=lesson_day).join(Grade).order_by(Grade.grade, Student.name).all()
    return render_template('all_students.html', students=students)


@main.route('/students/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(name=student.name)
    if form.validate_on_submit():
        student.name = form.name.data
        student.grade = Grade.query.get(form.grade.data)
        student.lesson_day = LessonDay.query.get(form.lesson_day.data)
        db.session.add(student)
        flash('The student has been updated.')
        return redirect(url_for('.students'))
    form.grade.data = student.grade.id
    return render_template('student_form.html', form=form, student=student)
