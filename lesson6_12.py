import os
import random
import time
from datetime import date, timedelta

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

    fill_tab_general(driver)

    fill_tab_information(driver)

    fill_tab_prices(driver)

    button_save = driver.find_element_by_xpath('//td[@id="content"]//button[contains(., "Save")]')
    button_save.click()

    assert_row_in_table(driver, 'Dudu Duck')

#endregion

#region ACTIONS_METHODS_REGION

def test_authorization_admin_panel(driver):
    admin_page_url = 'http://localhost/litecart/admin/'
    driver.get(admin_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()

def fill_tab_general(driver):
    radiobutton_status = driver.find_element_by_xpath('//div[@class="content"]//tr[contains(., "Status")]//label[contains(., "Enabled")]')
    radiobutton_status.click()

    input_name = get_input_by_type(driver, 'Name', 'text')
    input_name.send_keys('Dudu Duck')

    input_code = get_input_by_type(driver, 'Code', 'text')
    input_code.send_keys(random.randint(100, 999))

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

    today = date.today().strftime("%m.%d.%Y")
    day_in_future = (date.today() + timedelta(days=3)).strftime("%m.%d.%Y")

    date_input_from = get_input_by_type(driver, 'Date Valid From', 'date')
    date_input_from.send_keys(today)

    date_input_to = get_input_by_type(driver, 'Date Valid To', 'date')
    date_input_to.send_keys(day_in_future)

def fill_tab_information(driver):
    tab_info = get_tab(driver, 'Information')
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

    area_description = driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "Description")]//div[@contenteditable="true"]')
    area_description.send_keys('Description')

    input_head_title = get_input_by_type(driver, 'Head Title', 'text')
    input_head_title.send_keys('Head Title')

    input_meta_description = get_input_by_type(driver, 'Meta Description', 'text')
    input_meta_description.send_keys('Meta Description')

def fill_tab_prices(driver):
    tab_prices = get_tab(driver, 'Prices')
    tab_prices.click()

    input_purchase_price = get_input_by_type(driver, 'Purchase Price', 'number')
    input_purchase_price.clear()
    input_purchase_price.send_keys('50')

    list_purchase_price = get_list(driver, 'Purchase Price')
    list_purchase_price.click()

    list_item_category = get_list_item(driver, 'Purchase Price', 'Euros')
    list_item_category.click()

    input_price_usd = get_input_by_name_value(driver, 'gross_prices[USD]')
    input_price_usd.clear()
    input_price_usd.send_keys('40')

    input_gross_price_usd = get_input_by_name_value(driver, 'gross_prices[USD]')
    input_gross_price_usd.clear()
    input_gross_price_usd.send_keys('33')

    input_price_eur = get_input_by_name_value(driver, 'prices[EUR]')
    input_price_eur.clear()
    input_price_eur.send_keys('50')

    input_gross_price_eur = get_input_by_name_value(driver, 'gross_prices[EUR]')
    input_gross_price_eur.clear()
    input_gross_price_eur.send_keys('40')

def get_list(driver, list_name):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

def get_list_item(driver, list_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]'
                                        f'//option[contains(text(), "{item}")]')

def get_checkboxs_item(driver, checkbox_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{checkbox_name}")]'
                                        f'//td[contains(., "{item}")]/preceding-sibling::td//input')

def get_input_by_type(driver, input_name, input_type):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{input_name}")]'
                                        f'//input[@type="{input_type}"]')

def get_input_by_name_value(driver, name_value):
    return driver.find_element_by_xpath(f'//div[@class="content"]//input[@name="{name_value}"]')

def get_tab(driver, tab_name):
    return driver.find_element_by_xpath(f'//div[@class="tabs"]//a[contains(text(), "{tab_name}")]')

#endregion

#region ASSERTS_METHODS_REGION

def assert_row_in_table(driver, name):
    expected_rows = driver.find_elements_by_xpath(f'//table//td//a[text()="{name}"]')

    assert len(expected_rows) > 0, f'The row with text "{name}" didn\'t found.'

#endregion