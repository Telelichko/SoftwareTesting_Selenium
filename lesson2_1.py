import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ES


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def test1(driver):
    course_name = 'Selenium WebDriver: полное руководство'

    driver.get('https://www.google.com/')

    input_search = driver.find_element_by_name('q')
    input_search.send_keys(course_name)

    input_search.send_keys(Keys.ENTER)

    course_link = driver.find_element_by_xpath(f"//a[contains(., '{course_name}')]")
    course_link.click()

    course_page_title = driver.find_element_by_xpath(f"//h2[contains(text(), '{course_name}')]")

    ES.visibility_of(course_page_title)