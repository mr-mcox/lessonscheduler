from ..models import Subject
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import SubjectForm


@main.route('/subject/', methods=['GET', 'POST'])
def new_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject()
        subject.name = form.name.data
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('.subjects'))
    return render_template('subject_form.html', form=form)


@main.route('/subjects/')
def subjects():
    subjects = Subject.query.all()
    return render_template('all_subjects.html', subjects=subjects)


@main.route('/subjects/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(name=subject.name)
    if form.validate_on_submit():
        subject.name = form.name.data
        db.session.add(subject)
        flash('The subject has been updated.')
        return redirect(url_for('.subjects'))
    return render_template('subject_form.html', form=form, subject=subject)
