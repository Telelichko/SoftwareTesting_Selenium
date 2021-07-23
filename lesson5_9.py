import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION


def test_countries_sorted_alphabetically(driver):
    authorization_in_admin_panel(driver)

    check_countries_sorted_alphabetically(driver)

    check_zones_sorted_alphabetically(driver)

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

def check_countries_sorted_alphabetically(driver):
    go_to_countries_page(driver)

    table_countries = driver.find_element_by_xpath('//table[@class="dataTable"]')

    index_country_name = int(table_countries.find_element_by_xpath('.//tr[@class="header"]//th[text()="Name"]').get_attribute('cellIndex'))

    index_country_zone = int(table_countries.find_element_by_xpath('.//tr[@class="header"]//th[text()="Zones"]').get_attribute('cellIndex'))

    list_rows = table_countries.find_elements_by_xpath('.//tr[@class="row"]')

    list_names = []
    list_zones = []
    for row in list_rows:
        # # 1 passed in 32.29s
        # row_elements = row.find_elements_by_xpath(f'.//td')

        # 1 passed in 30.67s
        row_elements = list(row.find_elements_by_xpath(f'.//td'))

        element_name = row_elements[index_country_name].text
        list_names.append(element_name)

        text_zone = row_elements[index_country_zone].text
        list_zones.append(text_zone)

    page_title = driver.find_element_by_xpath('//h1').text
    assert_list_sorted_alphabetically(list_names, page_title)

    for i in [index for index, country in enumerate(list_zones) if country != '0']:
        country_name = go_to_page_country_by_number(driver, i + 1)
        inputs = driver.find_elements_by_xpath('//table[@id="table-zones"]//input[contains(@name, "[name]")]')

        list_inside_country_with_names = []

        for input in inputs:
            if input.get_attribute('value') == '' and input.get_attribute('type') != 'hidden':
                continue

            list_inside_country_with_names.append(input.get_attribute('value'))

        page_title = driver.find_element_by_xpath('//h1').text
        country_name = driver.find_element_by_xpath('//input[@name="name"]').get_attribute('value')

        assert_list_sorted_alphabetically(list_inside_country_with_names, f'{page_title} {country_name}')

        go_to_countries_page(driver)

def check_zones_sorted_alphabetically(driver):
    go_to_geo_zones_page(driver)

    count_rows = len(driver.find_elements_by_xpath('//table[@class="dataTable"]//tr[@class="row"]'))

    for i in range(count_rows):
        link_country = driver.find_element_by_xpath(f'//table[@class="dataTable"]/descendant::tr[@class="row"][{i + 1}]//a')
        link_country.click()

        count_zones = len(driver.find_elements_by_xpath('//table[@class="dataTable"]//select[contains(@name, "zone_code")]'))

        list_zones = []
        for i in range(count_zones):

            text_zone = driver.find_element_by_xpath(f'//table[@class="dataTable"]/descendant::select[contains(@name, "zone_code")][{i + 1}]//option[@selected]').text

            list_zones.append(text_zone)

        page_title = driver.find_element_by_xpath('//h1').text
        country_name = driver.find_element_by_xpath('//input[@name="name"]').get_attribute('value')

        assert_list_sorted_alphabetically(list_zones, f'{page_title} {country_name}')
        go_to_geo_zones_page(driver)

def go_to_countries_page(driver):
    countries_page_url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
    driver.get(countries_page_url)

def go_to_geo_zones_page(driver):
    countries_page_url = 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'
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

def assert_list_sorted_alphabetically(lists_text, page_name_for_log):
    test_passed = is_in_alphabetical_order(lists_text)

    assert test_passed, f'Countries  on page "{page_name_for_log}" ("{lists_text}") isn\'t sorted alphabetically.'

#endregion
