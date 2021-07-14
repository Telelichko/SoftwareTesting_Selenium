from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_add_delete_cart_products(driver):
    for i in range(3):
        add_product_to_cart(driver)

    delete_products_in_cart(driver)

#endregion

#region ACTIONS_METHODS_REGION

def go_to_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

def add_product_to_cart(driver):
    go_to_main_page(driver)

    element_product = driver.find_element_by_xpath('//li[contains(@class, "product")]')
    element_product.click()

    check_and_select_small_product_size(driver)

    count_products_in_cart = driver.find_element_by_xpath('//a[@class="content" and contains(., "Cart")]//span[@class="quantity"]').text

    button_to_cart = driver.find_element_by_xpath('//button[text()="Add To Cart"]')
    button_to_cart.click()

    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
        (By.XPATH, '//a[@class="content" and contains(., "Cart")]//span[@class="quantity"]'), f'{int(count_products_in_cart) + 1}'))

def delete_products_in_cart(driver):
    link_cart = driver.find_element_by_xpath('//a[contains(text(), "Checkout")]')
    link_cart.click()

    list_products = driver.find_elements_by_xpath('//ul[@class="items"]//li')
    product_count = len(list_products)

    for i in range(product_count):
        button_remove = driver.find_element_by_xpath('//button[text()="Remove"]')
        WebDriverWait(driver, 10).until(EC.visibility_of(button_remove))
        button_remove.click()

        WebDriverWait(driver, 10).until(EC.invisibility_of_element(button_remove))

    go_to_main_page(driver)

def check_and_select_small_product_size(driver):
    lists_product_size = driver.find_elements_by_xpath(f'//div[@class="content"]//tr[contains(., "Size")]//select')
    if(len(lists_product_size) == 1):
        list_size = get_list(driver, 'Size')
        list_size.click()

        lists_item_small_size = get_list_item(driver, 'Size', 'Small')
        lists_item_small_size.click()

def get_list(driver, list_name):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

def get_list_item(driver, list_name, item):
    return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]'
                                        f'//option[contains(text(), "{item}")]')

#endregion