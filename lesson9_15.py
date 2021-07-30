import pytest
from selenium import webdriver
from enum import Enum
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ES

class Browser(Enum):
    CHROME = 1
    FIREFOX_OLD_SCHEME = 2
    FIREFOX_NEW_SCHEME = 3
    EXPLORER = 4
    REMOTE_CHROME = 5
    REMOTE_EXPLORER = 6

@pytest.fixture()
def driver(request):
    wd = select_browser(Browser.REMOTE_CHROME, request)

    return wd

#region TESTS_METHODS_REGION

def test_check_course_page(driver):
    course_name = 'Selenium WebDriver: полное руководство'

    driver.get('https://www.google.com/')

    input_search = driver.find_element_by_name('q')
    input_search.send_keys(course_name)

    input_search.send_keys(Keys.ENTER)

    course_link = driver.find_element_by_xpath(f"//a[contains(., '{course_name}')]")
    course_link.click()

    course_page_title = driver.find_element_by_xpath(f"//h2[contains(text(), '{course_name}')]")

    ES.visibility_of(course_page_title)

#endregion

#region ACTIONS_METHODS_REGION

def select_browser(browser, request):
    # In virtualBox: https://coderoad.ru/43610397/%D0%9D%D0%B5-%D1%83%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F-%D0%B4%D0%BE%D1%81%D1%82%D0%B8%D1%87%D1%8C-%D1%83%D0%B7%D0%BB%D0%B0-%D0%BD%D0%B0-%D0%B2%D0%B8%D1%80%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B5-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D1%81%D0%B5%D1%82%D0%BA%D0%B8-Selenium
    # Перейдите в Настройки -> Сеть
    # 1. Прилагается к должно быть 'Bridged Adapter'
    # 2. Разверните 'Advanced' -> Неразборчивый режим должен быть 'Allow All'

    url = 'Here should be your url. Like: http://XXX.XXX.XXX.XXX .'
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
    elif browser == Browser.REMOTE_CHROME:
        wd = webdriver.Remote(f'{url}:4444/wd/hub', desired_capabilities={"browserName":"chrome"})
    elif browser == Browser.REMOTE_EXPLORER:
        wd = webdriver.Remote(f'{url}:4444/wd/hub', desired_capabilities={"browserName":"internet explorer"})
    else:
        return

    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#endregion