from ..models import Schedule, Student, Period
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import ScheduleForm
import pdb


@main.route('/schedule/<int:student_id>', methods=['GET', 'POST'])
def edit_schedule(student_id):
    form = ScheduleForm(student=Student.query.get_or_404(student_id))
    # pdb.set_trace()
    if form.validate_on_submit():
        schedule = Schedule()
        schedule.name = form.name.data
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('.schedules'))
    return render_template('schedule_form.html', form=form, periods=Period.query.all())


# @main.route('/schedules/')
# def schedules():
#     schedules = Schedule.query.all()
#     return render_template('all_schedules.html', schedules=schedules)


# @main.route('/schedules/<int:id>', methods=['GET', 'POST'])
# def edit_schedule(id):
#     schedule = Schedule.query.get_or_404(id)
#     form = ScheduleForm(name=schedule.name)
#     if form.validate_on_submit():
#         schedule.name = form.name.data
#         db.session.add(schedule)
#         flash('The schedule has been updated.')
#         return redirect(url_for('.schedules'))
#     return render_template('schedule_form.html', form=form, schedule=schedule)
