import random
from telnetlib import EC
from time import sleep

import rstr
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_create_account(driver):
    go_to_main_page(driver)

    link_registration = driver.find_element_by_link_text('New customers click here')
    link_registration.click()

    inputs = driver.find_elements_by_xpath(f'//input[not(@type="hidden") and not(@type="checkbox")]')

    password = ''
    for i, input in enumerate(inputs):
        input = driver.find_elements_by_xpath(f'//input[not(@type="hidden") and not(@type="checkbox")]')[i]
        parent_input_text = input.find_element_by_xpath('.//parent::td').text

        if 'Postcode' in parent_input_text:
            input_text = str(random.randint(10000, 99999))
        elif 'Email' in parent_input_text:
            input_text = rstr.xeger(r'[a-z][a-z0-9]{6}')
            input_text += '@mail.com'
            email = input_text
        elif 'Phone' in parent_input_text:
            input_text = '+7'
            input_text += rstr.xeger(r'[0-9]{8}')
        elif 'Password' in parent_input_text:
            if password == '':
                input_text = rstr.xeger(r'[a-z][a-z0-9]{7}')
                password = input_text
            else:
                input_text = password
        else:
            input_text = parent_input_text
            input_text += str(random.randint(100, 999))

        input.send_keys(input_text)

    item_in_list_country = driver.find_element_by_xpath('//span[contains(@class, "select2-selection__rendered")]')
    item_in_list_country.click()

    input_in_list_country = driver.find_element_by_xpath('//input[@class="select2-search__field"]')
    input_in_list_country.send_keys('United States' + Keys.ENTER)

    sleep(1)
    # # Не кликается. Вместо этого получилось сразу на элемент списка нажать
    # list_country_zone = get_list(driver, 'Zone/State/Province')
    # list_country_zone.click()

    item_in_list_country_zone = get_list_item(driver, 'Zone/State/Province', 'Colorado')
    item_in_list_country_zone.click()

    button_create = driver.find_element_by_xpath('//button[text()="Create Account"]')
    button_create.click()

    link_logout = driver.find_element_by_xpath('//a[text()="Logout"]')
    link_logout.click()

    input_email = driver.find_element_by_xpath('//input[@name="email"]')
    input_email.send_keys(email)

    input_password = driver.find_element_by_xpath('//input[@name="password"]')
    input_password.send_keys(password)

    link_login = driver.find_element_by_xpath('//button[text()="Login"]')
    link_login.click()

    link_logout = driver.find_element_by_xpath('//a[text()="Logout"]')
    link_logout.click()

#endregion

#region ACTIONS_METHODS_REGION

def go_to_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

def get_list(driver, list_name):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

def get_list_item(driver, list_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//td[contains(., "{list_name}")]'
                                        f'//option[contains(text(), "{item}")]')

#endregion

#region Experiment

def change_value_in_list_attribute(driver):
    list_country = get_list(driver, 'Country')
    # Код по изменению свойства атрибута (На примере списка Country)
    driver.execute_script('arguments[0].setAttribute("aria-hidden", "false");', list_country)
    list_country.click()

#endregion