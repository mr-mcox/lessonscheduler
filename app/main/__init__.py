from flask import Blueprint

main = Blueprint('main', __name__)

from . import students, welcome, grades, subjects, teachers, schedule_days, periods, sections, schedules, lesson_days
from ..models import LessonDay

@main.app_context_processor
def inject_lesson_days():
    return dict(all_lesson_days=LessonDay.query.order_by('name').all())