from flask import url_for
import pytest
import urllib


@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_server_is_up_and_running(self, app):
        res = urllib.request.urlopen(url_for('main.index', _external=True))
        assert res.code == 200
