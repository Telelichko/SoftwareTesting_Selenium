import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
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
    test_authorization_admin_panel(driver)

    left_menu = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]')

    sections = left_menu.find_elements_by_xpath('.//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]')

    for i, item in enumerate(sections):
        item = driver.find_element_by_xpath(f'//div[contains(@id, "menu-wrapper")]//li[@id = "app-"][{i + 1}]')
        item.click()
        assert_page_title_exist(driver, item)

        subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        for j, item2 in enumerate(subsections):
            item2 = driver.find_element_by_xpath(f'//li[@id="app-" and @class="selected"]//li[contains(@id, "doc-")][{j + 1}]')

            item2.click()
            assert_page_title_exist(driver, item2)

#endregion

#region ASSERTS_METHODS_REGION

def assert_page_title_exist(driver, section):
    elements = driver.find_elements_by_xpath('//td[@id="content"]//h1')

    assert len(elements) == 1, f'Title in section "{section}" isn\'t founded.'

#endregion



