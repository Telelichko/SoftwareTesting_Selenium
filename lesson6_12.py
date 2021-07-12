import os
import random
import time

import rstr
import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_create_account(driver):
    test_authorization_admin_panel(driver)

    catalog_section = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]//span[contains(text(), "Catalog")]')
    catalog_section.click()

    button_add_product = driver.find_element_by_xpath('//a[contains(., "Add New Product")]')
    button_add_product.click()

    # Достаточно заполнить только информацию на вкладках General, Information и Prices
    # fill_general_info(driver)

    # fill_information_info(driver)

    tab_info = driver.find_element_by_xpath('//div[@class="tabs"]//a[contains(text(), "Information")]')
    tab_info.click()

    list_manufacturer = get_list(driver, 'Manufacturer')
    list_manufacturer.click()

    list_item_manufacturer = get_list_item(driver, 'Manufacturer', 'ACME Corp.')
    list_item_manufacturer.click()

    list_supplier = get_list(driver, 'Supplier')
    list_supplier.click()

    list_item_supplier = get_list_item(driver, 'Supplier', 'Select')
    list_item_supplier.click()

    input_keywords = get_input_by_type(driver, 'Keywords', 'text')
    input_keywords.send_keys('Keywords')

    input_short_description = get_input_by_type(driver, 'Short Description', 'text')
    input_short_description.send_keys('Short Description')

    # area_description = driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "Description")]'
    #                                      f'//div[contains(@class, "editor")]')
    # area_description.send_keys('Description')


    area_description = driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "Description")]'
                                                    f'//textarea')

    area_description.send_keys('Description')

    # fill_prices_info(driver)




    something = 1

#endregion

#region ACTIONS_METHODS_REGION

def test_authorization_admin_panel(driver):
    main_page_url = 'http://localhost/litecart/admin/'
    driver.get(main_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()

def fill_general_info(driver):
    radiobutton_status = driver.find_element_by_xpath('//div[@class="content"]//tr[contains(., "Status")]//label[contains(., "Enabled")]')
    radiobutton_status.click()

    input_name = get_input_by_type(driver, 'Name', 'text')
    input_name.send_keys('Dudu')

    input_code = get_input_by_type(driver, 'Code', 'text')
    input_code.send_keys(12345)

    checkbox_category = get_checkboxs_item(driver, 'Categories', 'Rubber Ducks')
    checkbox_category.click()

    list_categories = get_list(driver, 'Default Category')
    list_categories.click()

    list_item_category = get_list_item(driver, 'Default Category', 'Root')
    list_item_category.click()

    checkbox_product_group = get_checkboxs_item(driver, 'Product Groups', 'Unisex')
    checkbox_product_group.click()

    input_quantity = get_input_by_type(driver, 'Quantity', 'number')
    input_quantity.clear()
    input_quantity.send_keys('50')

    file_input_upload_image = get_input_by_type(driver, 'Upload Images', 'file')
    file_input_upload_image.send_keys(os.getcwd() + '\static\images\Dudu.jpg')

    #TODO: Сгенерировать через регулярное выражение или выбрать текущий день из списка
    date_input_from = get_input_by_type(driver, 'Date Valid From', 'date')
    date_input_from.click()

    #TODO: Сгенерировать через регулярное выражение или выбрать текущий день из списка
    date_input_to = get_input_by_type(driver, 'Date Valid To', 'date')
    date_input_to.click()


def get_list(driver, list_name):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

def get_list_item(driver, list_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]'
                                        f'//option[contains(text(), "{item}")]')

def get_checkboxs_item(driver, checkbox_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{checkbox_name}")]'
                                        f'//td[contains(., "{item}")]')

def get_input_by_type(driver, input_name, input_type):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{input_name}")]'
                                        f'//input[@type="{input_type}"]')

#endregion