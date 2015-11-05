from ..models import Schedule, Student, Period, Section, ScheduleDay
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import ScheduleForm, ScheduleFormItem, SchedulePeriodGroup
import pdb


@main.route('/schedule/<int:student_id>', methods=['GET'])
def edit_schedule(student_id):
    form = ScheduleForm()
    student = Student.query.get_or_404(student_id)
    period_list = list()
    schedule_day_list = ScheduleDay.query.all()

    period_group = SchedulePeriodGroup()

    for schedule_day in schedule_day_list:
        item = ScheduleFormItem()

        period_group.schedule_days.append_entry(item)

    for period in Period.query.all():

        cur_period_list = [(x.id, x.name)
                           for x in Section.query.filter_by(period=period).all()]
        period_list.append((period.number, cur_period_list))

        form.periods.append_entry(period_group)

    for i, period_select in enumerate(period_list):
        number, choices = period_select
        for j, schedule_day in enumerate(schedule_day_list):
            form.periods[i].period_num = number
            form.periods[i].schedule_days[j].section.choices = choices
            form.periods[i].schedule_days[j].student.data = student.id
            form.periods[i].schedule_days[j].schedule_day.data = schedule_day.id
    return render_template('schedule_form.html', form=form, schedule_day_list=schedule_day_list)



@main.route('/schedule/<int:student_id>', methods=['POST'])
def edit_schedule_post(student_id):
    form = ScheduleForm()
    student = Student.query.get_or_404(student_id)

    if form.validate_on_submit():
        print("Choice for period 1, schedule day 1 is " + str(form.periods[0].schedule_days[0].section.data))
        print("Student for period 1, schedule day 1 is " + str(form.periods[0].schedule_days[0].student.data))
        print("Schedule Day for period 1, schedule day 1 is " + str(form.periods[0].schedule_days[0].schedule_day.data))
        return redirect(url_for('.students'))
    return render_template('schedule_form.html', form=form, schedule_day_list=schedule_day_list)
