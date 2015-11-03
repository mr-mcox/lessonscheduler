from flask import url_for
from app.models import Teacher

def test_create_new_teacher(client, app):
    name = 'Math'
    resp = client.post(url_for('main.new_teacher'),
                       data={'name': name},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.teachers', _external=True)

    # Test Math in all teachers
    resp = client.get(url_for('main.teachers'))
    assert b'Math' in resp.data

    # Test that editing has value
    g_record = Teacher.query.filter_by(name=name).first()
    resp = client.get(url_for('main.edit_teacher', id=g_record.id))
    assert b'value="Math' in resp.data
