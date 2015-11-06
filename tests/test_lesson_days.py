from flask import url_for
from app.models import LessonDay

def test_create_new_lesson_day(client, app):
    name = '3'
    resp = client.post(url_for('main.new_lesson_day'),
                       data={'name': name},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.lesson_days', _external=True)

    # Test 3 in all lesson_days
    resp = client.get(url_for('main.lesson_days'))
    assert b'3' in resp.data

    # Test that editing has value
    g_record = LessonDay.query.filter_by(name=name).first()
    resp = client.get(url_for('main.edit_lesson_day', id=g_record.id))
    assert b'value="3' in resp.data
