from flask import url_for


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config['TESTING']


def test_get_index(client, app):
    resp = client.get(url_for('main.index'), content_type='html/text')
    assert resp.status_code == 200
