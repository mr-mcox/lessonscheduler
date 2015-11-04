from flask import Blueprint

main = Blueprint('main', __name__)

from . import students, welcome, grades, subjects, teachers, schedule_days, periods, sections