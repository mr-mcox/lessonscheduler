from ..models import Section, Grade, Subject, Teacher, Period
from . import main
from flask import render_template, url_for, flash, redirect
from .. import db
from .forms import SectionForm


@main.route('/section/', methods=['GET', 'POST'])
def new_section():
    form = SectionForm()
    if form.validate_on_submit():
        section = Section()
        section.name = form.name.data
        section.grade = Grade.query.get(form.grade.data)
        section.subject = Subject.query.get(form.subject.data)
        section.teacher = Teacher.query.get(form.teacher.data)
        section.period = Period.query.get(form.period.data)
        section.note = form.note.data
        db.session.add(section)
        db.session.commit()
        return redirect(url_for('.sections'))
    return render_template('section_form.html', form=form)


@main.route('/sections/')
def sections():
    sections = Section.query.all()
    return render_template('all_sections.html', sections=sections)


@main.route('/sections/<int:id>', methods=['GET', 'POST'])
def edit_section(id):
    section = Section.query.get_or_404(id)
    form = SectionForm(name=section.name)
    if form.validate_on_submit():
        section.name = form.name.data
        section.grade = Grade.query.get(form.grade.data)
        section.subject = Subject.query.get(form.subject.data)
        section.teacher = Teacher.query.get(form.teacher.data)
        section.period = Period.query.get(form.period.data)
        section.note = form.note.data
        db.session.add(section)
        flash('The section has been updated.')
        return redirect(url_for('.sections'))
    form.grade.data = section.grade.id
    form.subject.data = section.subject.id
    form.teacher.data = section.teacher.id
    form.period.data = section.period.id
    form.note.data = section.note
    return render_template('section_form.html', form=form, section=section)
