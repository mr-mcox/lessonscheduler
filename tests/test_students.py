from flask import current_app
from app import create_app, db
import pytest


@pytest.fixture()
def app():
    print("Created app")
    return create_app('testing')


@pytest.fixture(scope='function', autouse=True)
def app_context(request, app):
    app_context = app.app_context()
    app_context.push()

    def reset_context():
        app_context.pop()

    request.addfinalizer(reset_context)
    print("Created context")
    return app_context


@pytest.fixture(scope='session')
def setup_db():
    db.create_all()


@pytest.fixture(scope='function')
def reset_db():
    db.session.remove()
    db.drop_all()


def test_app_exists():
    assert current_app is not None


def test_app_is_testing():
    assert current_app.config['TESTING']
