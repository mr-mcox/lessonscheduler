from ..models import Schedule
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import ScheduleForm


@main.route('/schedule/', methods=['GET', 'POST'])
def new_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule()
        schedule.name = form.name.data
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('.schedules'))
    return render_template('schedule_form.html', form=form)


@main.route('/schedules/')
def schedules():
    schedules = Schedule.query.all()
    return render_template('all_schedules.html', schedules=schedules)


@main.route('/schedules/<int:id>', methods=['GET', 'POST'])
def edit_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    form = ScheduleForm(name=schedule.name)
    if form.validate_on_submit():
        schedule.name = form.name.data
        db.session.add(schedule)
        db.session.commit()
        flash('The schedule has been updated.')
        return redirect(url_for('.schedules'))
    return render_template('schedule_form.html', form=form, schedule=schedule)
