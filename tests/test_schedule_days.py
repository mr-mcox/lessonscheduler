from flask import url_for
from app.models import ScheduleDay

def test_create_new_schedule_day(client, app):
    name = 'Math'
    resp = client.post(url_for('main.new_schedule_day'),
                       data={'name': name},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.schedule_days', _external=True)

    # Test Math in all schedule_days
    resp = client.get(url_for('main.schedule_days'))
    assert b'Math' in resp.data

    # Test that editing has value
    g_record = ScheduleDay.query.filter_by(name=name).first()
    resp = client.get(url_for('main.edit_schedule_day', id=g_record.id))
    assert b'value="Math' in resp.data
