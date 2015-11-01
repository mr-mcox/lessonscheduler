from flask import url_for
from app import db
import pytest
from app.models import Grade


@pytest.fixture(autouse=True)
def setup_db(request, app):
    def reset_db():
        db.session.remove()
        db.drop_all()
        db.create_all()
    request.addfinalizer(reset_db)


def test_create_new_grade(client, app, monkeypatch):
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
