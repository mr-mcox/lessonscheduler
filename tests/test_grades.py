from flask import url_for
from app.models import Grade


def test_create_new_grade(client, app):
    grade = '6th'
    resp = client.post(url_for('main.new_grade'),
                       data={'grade': grade},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.grades', _external=True)

    # Test 6th in all grades
    resp = client.get(url_for('main.grades'))
    assert b'6th' in resp.data

    # Test that editing has value
    g_record = Grade.query.filter_by(grade=grade).first()
    resp = client.get(url_for('main.edit_grade', id=g_record.id))
    assert b'value="6th' in resp.data
