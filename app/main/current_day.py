from ..models import CurrentDay, ScheduleDay, LessonDay
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import CurrentDayForm

@main.route('/current_day/', methods=['GET', 'POST'])
def setup_current_day():
    form = CurrentDayForm()
    if form.validate_on_submit():
        today = CurrentDay()
        today.date = form.date.data
        today.schedule_day = ScheduleDay.query.get_or_404(form.schedule_day.data)
        today.lesson_day = LessonDay.query.get_or_404(form.lesson_day.data)
        db.session.add(today)
        db.session.commit()
        return redirect(url_for('.students'))
    return render_template('current_day_form.html', form=form)