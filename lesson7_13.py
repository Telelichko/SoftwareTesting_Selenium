import os
import random
from datetime import date, timedelta
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
    go_to_main_page(driver)

    element_product = driver.find_element_by_xpath('//li[contains(@class, "product")]')
    element_product.click()

    check_and_select_product_size(driver)

    button_to_cart = driver.find_element_by_xpath('//button[text()="Add To Cart"]')
    button_to_cart.click()

    something = 1


#endregion

#region ACTIONS_METHODS_REGION

def go_to_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

def check_and_select_product_size(driver):
    lists_product_size = driver.find_elements_by_xpath(f'//div[@class="content"]//tr[contains(., "Size")]//select')
    if(len(lists_product_size) == 1):
        list_size = get_list(driver, 'Size')
        list_size.click()

        lists_item_small_size = driver.find_element_by_xpath('//div[@class="information"]//select')
        lists_item_small_size.click()

def get_list(driver, list_name):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

def get_list_item(driver, list_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]'
                                        f'//option[contains(text(), "{item}")]')
#endregion
