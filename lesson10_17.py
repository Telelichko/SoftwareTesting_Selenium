import pytest
from selenium import webdriver

@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_check_logs_in_products(driver):
    authorization_in_admin_panel(driver)

    catalog_section = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]//span[contains(text(), "Catalog")]')
    catalog_section.click()

    link_product_category = driver.find_element_by_xpath('//table[@class="dataTable"]//a[not(contains(text(), "[Root]")) and not(title)]')
    link_product_category.click()

    count_products = len(driver.find_elements_by_xpath('//table[@class="dataTable"]//img/following-sibling::a'))

    products_logs = {}
    for i in range(count_products):
        link_product = driver.find_element_by_xpath(f'//table[@class="dataTable"]/descendant::img[{i + 1}]/following-sibling::a')
        link_product.click()

        logs = get_logs_on_page(driver)

        product_page_title = driver.find_element_by_xpath(f'//h1').text
        product_name = product_page_title.replace('Edit Product: ', '')
        products_logs.update({product_name: logs})

        button_cancel = driver.find_element_by_xpath('//button[contains(., "Cancel")]')
        button_cancel.click()

    is_logs_exist = len([z for z in products_logs.values() if z != []]) != 0

    assert not(is_logs_exist), f'There is some logs in products.'

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

def get_logs_on_page(driver):
    browser_logs = driver.get_log("browser")

    if browser_logs != []:
        product_page_title = driver.find_element_by_xpath(f'//h1').text
        print(f'Browser logs on page "{product_page_title}": \n')

        for l in browser_logs:
            print(f'{l} \n')

    return browser_logs

#endregion