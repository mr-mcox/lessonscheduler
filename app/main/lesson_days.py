from ..models import LessonDay
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import LessonDayForm

@main.route('/lesson_day/', methods=['GET', 'POST'])
def new_lesson_day():
    form = LessonDayForm()
    if form.validate_on_submit():
        lesson_day = LessonDay()
        lesson_day.name = form.name.data
        db.session.add(lesson_day)
        db.session.commit()
        return redirect(url_for('.lesson_days'))
    return render_template('lesson_day_form.html', form=form)


@main.route('/lesson_days/')
def lesson_days():
    lesson_days = LessonDay.query.order_by('name').all()
    return render_template('all_lesson_days.html', lesson_days=lesson_days)


@main.route('/lesson_days/<int:id>', methods=['GET', 'POST'])
def edit_lesson_day(id):
    lesson_day = LessonDay.query.get_or_404(id)
    form = LessonDayForm(name=lesson_day.name)
    if form.validate_on_submit():
        lesson_day.name = form.name.data
        db.session.add(lesson_day)
        flash('The lesson_day has been updated.')
        return redirect(url_for('.lesson_days'))
    return render_template('lesson_day_form.html', form=form, lesson_day=lesson_day)
