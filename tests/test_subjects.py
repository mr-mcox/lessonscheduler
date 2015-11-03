from flask import url_for
from app.models import Subject

def test_create_new_subject(client, app):
    name = 'Math'
    resp = client.post(url_for('main.new_subject'),
                       data={'name': name},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.subjects', _external=True)

    # Test Math in all subjects
    resp = client.get(url_for('main.subjects'))
    assert b'Math' in resp.data

    # Test that editing has value
    g_record = Subject.query.filter_by(name=name).first()
    resp = client.get(url_for('main.edit_subject', id=g_record.id))
    assert b'value="Math' in resp.data
