import pytest
from selenium import webdriver
from enum import Enum
from selenium.webdriver.support import expected_conditions as ES

class Browser(Enum):
    REMOTE_CHROME = 1

@pytest.fixture()
def driver(request):
    wd = select_browser(Browser.REMOTE_CHROME, request)

    return wd

#region TESTS_METHODS_REGION

def test_check_course_page(driver):
    course_name = 'Selenium WebDriver: полное руководство'

    driver.get('https://software-testing.ru/edu/schedule/242')

    course_page_title = driver.find_element_by_xpath(f"//h2[contains(text(), '{course_name}')]")

    ES.visibility_of(course_page_title)

#endregion

#region ACTIONS_METHODS_REGION

def select_browser(browser, request):
    part_name = 'Here will be part of you User Name.'
    key = 'Here will be your Access Key'
    if browser == Browser.REMOTE_CHROME:
        wd = webdriver.Remote(
            command_executor=f'https://{part_name}_{key}@hub-cloud.browserstack.com/wd/hub',
            desired_capabilities={"browser":"chrome", "chromeOptions": { "w3c": "false" } })
    else:
        return

    wd.implicitly_wait(3)
    request.addfinalizer(wd.quit)
    return wd

#endregion