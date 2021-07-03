import threading
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.support import wait
from waiting import wait


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Ie(capabilities={"requireWindowFocus": True})
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_authorization_admin_panel(driver):
    main_page_url = 'http://localhost/litecart/admin/'
    driver.get(main_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()


def test_check_sections(driver):
    xpath_sections = '//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]'

    # xpath_subsection =

    test_authorization_admin_panel(driver)

    sections = driver.find_elements_by_xpath(xpath_sections)

    for i, item in enumerate(sections):
        # TODO: Отладить. Берет вместе с подразделами, в случайном порядке, и долго ждет
        something = driver.find_elements_by_xpath(xpath_sections)
        item = get_element_by_xpath_and_number(driver, xpath_sections, i)

        assert_element_by_number_exist(driver, i, item, 'Section')

        subsections = item.find_elements_by_xpath('following::ul[@class="docs"][1]//span[@class="name"]')

        item.click()
        assert_page_title_exist(driver, item)


        # subsections = item.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')


        # subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        # for i_sub, item_sub in enumerate(subsections):
        #     sleep(0.5)
        #     item_sub.click()
        #     assert_page_title_exist(driver, item_sub)


# With StaleElementReferenceException in second element
def test_check_sections_with_exception(driver):
    test_authorization_admin_panel(driver)

    left_menu = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]')

    sections = left_menu.find_elements_by_xpath('//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]')

    for item in sections:
        item.click()
        assert_page_title_exist(driver, item)

        subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        for item2 in subsections:
            sleep(1)
            item2.click()
            assert_page_title_exist(driver, item2)


# With IndexError
def test_check_subsections_wrong_numbers(driver):
    test_authorization_admin_panel(driver)

    max_subsections = 100

    for i in range(max_subsections + 1):
        sleep(1)
        subsection = driver.find_elements_by_xpath('//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//span[@class="name"]')[i]
        if(subsection == None):
            break;

        subsection.click()

        if(i == max_subsections):
            subsection_next = driver.find_elements_by_xpath('//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//span[@class="name"]')[i + 1]
            assert subsection_next == None, f'There is more than "{max_subsections}" subsections.'

#endregion

#region ACTIONS_METHODS_REGION

def get_element_by_xpath_and_number(driver, xpath_sections, number):
    try:
        something = driver.find_elements_by_xpath(xpath_sections)
        return driver.find_elements_by_xpath(xpath_sections)[number - 1]
    except IndexError:
        return None


#endregion

#region ASSERTS_METHODS_REGION

def assert_page_title_exist(driver, section):
    elements = driver.find_elements_by_xpath('//td[@id="content"]//h1')

    assert len(elements) == 1, f'Title in section "{section}" isn\'t founded.'

def assert_element_by_number_exist(driver, index, element, element_type_for_log):
    assert element != None, f'{element_type_for_log} by number "{index + 1}" isn\'t founded.'

#endregion



