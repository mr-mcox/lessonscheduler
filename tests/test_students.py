from flask import current_app
from app import create_app, db
import pytest


@pytest.fixture()
def app():
    return create_app('testing')


@pytest.fixture(scope='function', autouse=True)
def app_context(request, app):
    app_context = app.app_context()
    app_context.push()

    def reset_context():
        app_context.pop()

    request.addfinalizer(reset_context)
    return app_context


@pytest.fixture(scope='session')
def setup_db():
    db.create_all()


@pytest.fixture(scope='function')
def reset_db():
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='session')
def client():
    return current_app.test_client(use_cookies=True)

def test_app_exists():
    assert current_app is not None


def test_app_is_testing():
    assert current_app.config['TESTING']

def test_get_index(client):
    resp = client.get('/', content_type='html/text')
    assert resp.status_code == 200
