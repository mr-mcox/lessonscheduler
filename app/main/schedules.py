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
        period_list.append((period, cur_period_list))

        form.periods.append_entry(period_group)

    for i, period_select in enumerate(period_list):
        period, choices = period_select
        for j, schedule_day in enumerate(schedule_day_list):
            form.periods[i].period_num = period.number
            form.periods[i].schedule_days[j].section.choices = choices
            form.periods[i].schedule_days[j].student.data = student.id
            form.periods[i].schedule_days[
                j].schedule_day.data = schedule_day.id

            cur_sch = Schedule().schedule_by_student_period_day(student=student,
                                                                period=period,
                                                                schedule_day=schedule_day)
            if cur_sch is not None:
                section = cur_sch.section
                form.periods[i].schedule_days[j].section.data = section.id

    return render_template('schedule_form.html', form=form, schedule_day_list=schedule_day_list)


@main.route('/schedule/<int:student_id>', methods=['POST'])
def edit_schedule_post(student_id):
    form = ScheduleForm()
    student = Student.query.get_or_404(student_id)

    if form.validate_on_submit():
        for preriod_obj in form.periods:
            # period = Period.query.get_or_404(preriod_obj.period_num.data)
            for sched_obj in preriod_obj.schedule_days:
                student = Student.query.get_or_404(sched_obj.student.data)
                section = Section.query.get_or_404(sched_obj.section.data)
                schedule_day = ScheduleDay.query.get_or_404(
                    sched_obj.schedule_day.data)

                Schedule().store_schedule(
                    student=student,
                    section=section,
                    schedule_day=schedule_day,
                )
        return redirect(url_for('.students'))
    return render_template('schedule_form.html', form=form,
                           schedule_day_list=schedule_day_list)

@main.route('/schedule/view/<int:student_id>')
def view_schedule(student_id):
    periods = Period.query.all()
    student = Student.query.get_or_404(student_id)
    schedule_days = ScheduleDay.query.all()

    
    all_sections = list()

    for period in periods:
        period_group = list()
        for schedule_day in schedule_days:
            
                sch = Schedule().schedule_by_student_period_day(student=student,
                                                        period=period,
                                                        schedule_day=schedule_day)
                period_group.append(sch.section)

        all_sections.append(period_group)

    return render_template('student_schedule.html', student=student,
                            schedule_days=schedule_days, all_sections=all_sections)



