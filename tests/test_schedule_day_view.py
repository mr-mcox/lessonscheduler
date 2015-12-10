from flask import url_for
import pytest
from selenium import webdriver


@pytest.mark.usefixtures('live_server')
@pytest.mark.selenium
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

    def test_filter_sections_by_day(self, app, browser):
        # Emily goes to home page
        browser.get(url_for('main.index', _external=True))
        # Emily clicks on setup menu
        setup_menu = browser.find_element_by_name("Setup Button")
        setup_menu.click()
        # Emily clicks on setup day
        setup_day = browser.find_element_by_name("Setup Today")
        setup_day.click()
        # Emily chooses schedule day A
        # Emily clicks the setup button
        # Emily clicks on students
        # Emily selects lesson day 1
        # The only classes shown are for schedule day A
        # Emily clicks on setup menu
        # Emily clicks on setup day
        # Emily chooses schedule day B
        # Emily clicks the setup button
        # Emily clicks on students
        # Emily selects lesson day 1
        # The only classes shown are for schedule day B
