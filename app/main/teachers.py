from ..models import Teacher
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import TeacherForm


@main.route('/teacher/', methods=['GET', 'POST'])
def new_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher()
        teacher.name = form.name.data
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('.teachers'))
    return render_template('teacher_form.html', form=form)


@main.route('/teachers/')
def teachers():
    teachers = Teacher.query.all()
    return render_template('all_teachers.html', teachers=teachers)


@main.route('/teachers/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm(name=teacher.name)
    if form.validate_on_submit():
        teacher.name = form.name.data
        db.session.add(teacher)
        db.session.commit()
        flash('The teacher has been updated.')
        return redirect(url_for('.teachers'))
    return render_template('teacher_form.html', form=form, teacher=teacher)
