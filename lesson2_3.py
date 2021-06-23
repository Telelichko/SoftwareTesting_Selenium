import random

import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

# Preconditions: Create new customer with email - store@gmail.com,  password - admin
def test_authorization(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

    input_email = driver.find_element_by_name('email')
    input_email.send_keys('store@gmail.com')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('admin')

    button_login = driver.find_element_by_name('login')
    button_login.click()

# Test failed
def test_create_account(driver):
    main_page_url = 'http://localhost/litecart/'

    driver.get(main_page_url)

    link_registration = driver.find_element_by_link_text('New customers click here')
    link_registration.click()

    inputs = driver.find_elements_by_tag_name('input')

    for input in inputs:
        parent_input_text = input.find_element_by_xpath('//parent::td[1]').text

        if parent_input_text == 'Postcode':
            input_text = '012345'
        elif parent_input_text == 'Email':
            input_text = 'mail@mail.com'
        elif parent_input_text == 'Phone':
            input_text = '799999999'
        elif 'Password' in parent_input_text:
            input_text = 'Password'
        else:
            # TODO: !!! 1 проблема - "ElementNotInteractableException: Message: element not interactable" -
            # TODO: Поле ввода под "Tax ID" не предназначено для взаимодействий !!!
            input_text = parent_input_text

        # TODO: !!! 2 проблема - Как быть с полем для "CAPTCHA" ???


        input_text += str(random.randint(100, 999))
        input.send_keys(input_text)

