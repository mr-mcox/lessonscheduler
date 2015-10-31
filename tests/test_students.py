from flask import url_for
from app import db
import pytest
import json


# @pytest.fixture()
# def app():
#     # print("Starting app")
#     return create_app('testing')


# @pytest.fixture(scope='function', autouse=True)
# @pytest.fixture()
# def app_context(request, app):
#     # print("Starting app_context")
#     app_context = app.app_context()
#     app_context.push()

#     def reset_context():
#         app_context.pop()

#     request.addfinalizer(reset_context)
#     return app_context


@pytest.fixture()
def setup_db(app):
    # print("Starting setup_db")
    db.drop_all()
    db.create_all()


# @pytest.fixture(scope='function')
@pytest.fixture()
def reset_db():
    db.session.remove()
    db.drop_all()


# @pytest.fixture()
# def client(app, app_context, setup_db):
#     # print("Starting client")
#     return app.test_client(use_cookies=True)


def get_api_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config['TESTING']


def test_get_index(client, app):
    resp = client.get(url_for('main.index'), content_type='html/text')
    assert resp.status_code == 200


def test_create_new_student(client, app):
    rv = client.post(url_for('main.new_student'),
                     data=json.dumps({'name': 'Elliot'}),
                     headers=get_api_headers(),
                     follow_redirects=True)
    # with app.test_request_context('/'):
    #     the_url = url_for('main.edit_student')
    #     assert rv.location == url_for('main.edit_student')
    assert b'Elliot' in rv.data
    # resp = json.loads(rv.data.decode('utf-8'))
    # assert resp['name'] == 'Elliot'

    # response = client.get(
    #     url_for('main.students'),
    #     headers=get_api_headers())
    # assert response.status_code == 200
    # json_response = json.loads(response.data.decode('utf-8'))
    # assert json_response.get('students') is not None
    # assert len(json_response.get('students')) == 1

    # rv = client.put(url,
    #                 data=json.dumps({'name': 'Elliot Stabler'}),
    #                 headers=get_api_headers())
    # assert rv.status_code == 200
    # resp = json.loads(rv.data.decode('utf-8'))
    # assert resp['name'] == 'Elliot Stabler'
