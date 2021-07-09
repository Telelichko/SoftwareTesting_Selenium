import random
import rstr
import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def test_create_account(driver):
    main_page_url = 'http://localhost/litecart/'

    driver.get(main_page_url)

    link_registration = driver.find_element_by_link_text('New customers click here')
    link_registration.click()

    inputs = driver.find_elements_by_xpath(f'//input[not(@type="hidden") and not(@type="checkbox")]')

    password = ''
    for i, input in enumerate(inputs):
        input = driver.find_elements_by_xpath(f'//input[not(@type="hidden") and not(@type="checkbox")]')[i]
        parent_input_text = input.find_element_by_xpath('.//parent::td').text

        if 'Postcode' in parent_input_text:
            input_text = '012345'
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