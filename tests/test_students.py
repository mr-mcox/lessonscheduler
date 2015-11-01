from flask import url_for
from app import db
import pytest
import json
from app.models import Student
from app.main.forms import StudentForm


@pytest.fixture(autouse=True)
def setup_db(request, app):
    def reset_db():
        db.session.remove()
        db.drop_all()
    request.addfinalizer(reset_db)
    db.create_all()


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config['TESTING']


def test_get_index(client, app):
    resp = client.get(url_for('main.index'), content_type='html/text')
    assert resp.status_code == 200


def test_create_new_student(client, app, monkeypatch):
    s_name = 'Elliot'
    resp = client.post(url_for('main.new_student'),
                       data={'name': s_name},
                       follow_redirects=False)

    with app.app_context():
        assert resp.location == url_for('main.students', _external=True)

    # Test Elliot in all students
    resp = client.get(url_for('main.students'))
    assert b'Elliot' in resp.data

    # Test that editing has value
    s_record = Student.query.filter_by(name=s_name).first()
    resp = client.get(url_for('main.edit_student', id=s_record.id))
    assert b'value="Elliot' in resp.data
