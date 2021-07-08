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

    for i, input in enumerate(inputs):
        input = driver.find_elements_by_xpath(f'//input[not(@type="hidden") and not(@type="checkbox")]')[i]
        parent_input_text = input.find_element_by_xpath('.//parent::td').text

        if 'Postcode' in parent_input_text:
            input_text = '012345'
        elif 'Email' in parent_input_text:
            input_text = rstr.xeger(r'[a-z][a-z0-9]{6}')
            input_text += '@mail.com'
        elif 'Phone' in parent_input_text:
            input_text = '799999999'
        elif 'Password' in parent_input_text:
            input_text = 'Password'
        else:
            input_text = parent_input_text
            input_text += str(random.randint(100, 999))

        input.send_keys(input_text)

    button_create = driver.find_element_by_xpath('//button[text()="Create Account"]')
    button_create.click()

    # TODO: Добавить пункты 2-3
    # 2) выход (logout), потому что после успешной регистрации автоматически происходит вход,
    # 3) повторный вход в только что созданную учётную запись,
    # 4) и ещё раз выход.


    something = 1

