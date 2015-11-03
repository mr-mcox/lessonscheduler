from ..models import Period
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import PeriodForm
import pdb

@main.route('/period/', methods=['GET', 'POST'])
def new_period():
    form = PeriodForm()
    if form.validate_on_submit():
        period = Period()
        period.number = form.number.data
        period.start_time = form.start_time.data
        period.end_time = form.end_time.data
        db.session.add(period)
        db.session.commit()
        return redirect(url_for('.periods'))
    return render_template('period_form.html', form=form)


@main.route('/periods/')
def periods():
    periods = Period.query.all()
    return render_template('all_periods.html', periods=periods)


@main.route('/periods/<int:id>', methods=['GET', 'POST'])
def edit_period(id):
    period = Period.query.get_or_404(id)
    form = PeriodForm(
        number=period.number,
        start_time=period.start_time,
        end_time=period.end_time)
    if form.validate_on_submit():
        period.number = form.number.data
        period.start_time = form.start_time.data
        period.end_time = form.end_time.data
        db.session.add(period)
        flash('The period has been updated.')
        return redirect(url_for('.periods'))
    return render_template('period_form.html', form=form, period=period)
