from ..models import ScheduleDay
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import ScheduleDayForm


@main.route('/schedule_day/', methods=['GET', 'POST'])
def new_schedule_day():
    form = ScheduleDayForm()
    if form.validate_on_submit():
        schedule_day = ScheduleDay()
        schedule_day.name = form.name.data
        db.session.add(schedule_day)
        db.session.commit()
        return redirect(url_for('.schedule_days'))
    return render_template('schedule_day_form.html', form=form)


@main.route('/schedule_days/')
def schedule_days():
    schedule_days = ScheduleDay.query.all()
    return render_template('all_schedule_days.html', schedule_days=schedule_days)


@main.route('/schedule_days/<int:id>', methods=['GET', 'POST'])
def edit_schedule_day(id):
    schedule_day = ScheduleDay.query.get_or_404(id)
    form = ScheduleDayForm(name=schedule_day.name)
    if form.validate_on_submit():
        schedule_day.name = form.name.data
        db.session.add(schedule_day)
        db.session.commit()
        flash('The schedule_day has been updated.')
        return redirect(url_for('.schedule_days'))
    return render_template('schedule_day_form.html', form=form, schedule_day=schedule_day)
