from ..models import Grade
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import GradeForm

@main.route('/grade/', methods=['GET', 'POST'])
def new_grade():
    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade()
        grade.grade = form.grade.data
        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('.grades'))
    return render_template('grade_form.html', form=form)


@main.route('/grades/')
def grades():
    grades = Grade.query.all()
    return render_template('all_grades.html', grades=grades)


@main.route('/grades/<int:id>', methods=['GET', 'POST'])
def edit_grade(id):
    grade = Grade.query.get_or_404(id)
    form = GradeForm(grade=grade.grade)
    if form.validate_on_submit():
        grade.grade = form.grade.data
        db.session.add(grade)
        flash('The grade has been updated.')
        return redirect(url_for('.grades'))
    return render_template('grade_form.html', form=form, grade=grade)
