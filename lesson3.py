import pytest
from selenium import webdriver
from enum import Enum

class Browser(Enum):
    CHROME = 1
    FIREFOX_OLD_SCHEME = 2
    FIREFOX_NEW_SCHEME = 3
    EXPLORER = 4
    ALL = 5


@pytest.fixture()
def driver(request):
    wd = select_browser(Browser.FIREFOX_NEW_SCHEME, request)

    return wd

def test_authorization_admin_panel(driver):
    main_page_url = 'http://localhost/litecart/admin/'
    driver.get(main_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()


def select_browser(browser, request):
    if browser == Browser.CHROME:
        wd = webdriver.Chrome()
    elif browser == Browser.FIREFOX_OLD_SCHEME:
        # Needs (old) Firefox version 45
        wd = webdriver.Firefox(capabilities={"marionette": False})
    elif browser == Browser.FIREFOX_NEW_SCHEME:
        # Firefox Nightly
        # wd = webdriver.Firefox()
        wd = webdriver.Firefox(capabilities={"marionette": True})
    elif browser == Browser.EXPLORER:
        # Needs a 32 bit driver
        wd = webdriver.Ie(capabilities={"requireWindowFocus": True})
    elif browser == Browser.All:
        return
    else:
        return

    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd



