from flask import url_for
from app.models import Period
from datetime import datetime, time


def test_create_new_period(client, app):
    number = 1
    resp = client.post(url_for('main.new_period'),
                       data={'number': number,
                             'start_time': '11:50',
                             'end_time': '12:30',
                             },
                       follow_redirects=False)
    with app.app_context():
        assert resp.location == url_for('main.periods', _external=True)

    # Test the period in all periods
    resp = client.get(url_for('main.periods'))
    assert b'1' in resp.data
    assert b'11:50 AM' in resp.data
    assert b'12:30 PM' in resp.data

    # Test that editing has value
    g_record = Period.query.filter_by(number=number).first()
    resp = client.get(url_for('main.edit_period', id=g_record.id))
    assert b'value="1' in resp.data
