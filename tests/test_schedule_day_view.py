from flask import url_for
import pytest
import urllib
from selenium import webdriver


@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    browser = None

    @pytest.fixture(scope='class')
    def browser(self, request):
        browser = webdriver.Firefox()

        def quit_browser():
            browser.quit()

        request.addfinalizer(quit_browser)
        return browser

    def test_server_is_up_and_running(self, app, browser):
        browser.get(url_for('main.index', _external=True))
        assert 'Lesson Scheduler' in browser.title
