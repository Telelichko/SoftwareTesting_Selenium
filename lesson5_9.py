import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Firefox(capabilities={"marionette": True})
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION


def test_countries_sorted_alphabetically(driver):
    authorization_in_admin_panel(driver)
    go_to_countries_page(driver)

    table_countries = driver.find_element_by_xpath('//table[@class="dataTable"]')

    index_country_name = int(table_countries.find_element_by_xpath('.//tr[@class="header"]//th[text()="Name"]').get_attribute('cellIndex'))

    index_country_zone = int(table_countries.find_element_by_xpath('.//tr[@class="header"]//th[text()="Zones"]').get_attribute('cellIndex'))

    list_rows = table_countries.find_elements_by_xpath('.//tr[@class="row"]')

    list_names = []
    list_zones = []
    for row in list_rows:
        element_name = row.find_element_by_xpath(f'.//td[{index_country_name + 1}]')
        list_names.append(element_name.text)

        text_zone = row.find_element_by_xpath(f'.//td[{index_country_zone + 1}]').text
        list_zones.append(text_zone)

    assert_countries_sorted_alphabetically(list_names, 'Countries')

    for i in [index for index, country in enumerate(list_zones) if country != '0']:
        country_name = go_to_page_country_by_number(driver, i + 1)
        inputs = driver.find_elements_by_xpath('//table[@id="table-zones"]//input[contains(@name, "[name]")]')

        list_inside_country_with_names = []

        for input in inputs:
            if input.get_attribute('value') == '' and input.get_attribute('type') != 'hidden':
                continue;

            list_inside_country_with_names.append(input.get_attribute('value'))

        assert_countries_sorted_alphabetically(list_names, f'Edit Country "{country_name}"')

        go_to_countries_page(driver)

#endregion

#region ACTIONS_METHODS_REGION

def authorization_in_admin_panel(driver):
    main_page_url = 'http://localhost/litecart/admin/'
    driver.get(main_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()

def go_to_countries_page(driver):
    countries_page_url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
    driver.get(countries_page_url)

def is_in_alphabetical_order(list_words):
    for i in range(len(list_words) - 1):
        if list_words[i] > list_words[i + 1]:
            return False
    return True

def go_to_page_country_by_number(driver, number):
    link_country = driver.find_element_by_xpath(f'//table[@class="dataTable"]//tr[@class="row"][{number}]//a[contains(@href, "edit_country")]')
    country_name =  link_country.text
    link_country.click()

    return country_name

#endregion

#region ASSERTS_METHODS_REGION

def assert_countries_sorted_alphabetically(countries_names, page_name_for_log):
    test_passed = is_in_alphabetical_order(countries_names)

    assert test_passed, f'Countries  on page "{page_name_for_log}" ("{countries_names}") isn\'t sorted alphabetically.'

#endregion
