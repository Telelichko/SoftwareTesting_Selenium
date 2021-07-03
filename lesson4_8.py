import pytest
from selenium import webdriver
from enum import Enum

from selenium.common.exceptions import NoSuchElementException


class Browser(Enum):
    CHROME = 1
    FIREFOX_OLD_SCHEME = 2
    FIREFOX_NEW_SCHEME = 3
    EXPLORER = 4
    ALL = 5


@pytest.fixture()
def driver(request):
    wd = select_browser(Browser.EXPLORER, request)
    return wd

#region TESTS_METHODS_REGION

def test_authorization_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

def test_check_sections(driver):
    test_authorization_main_page(driver)

    products = driver.find_elements_by_class_name('product')

    test_passed = True
    products_without_stickers = []
    for item in products:
        product_name = item.find_element_by_class_name('name')

        product_stickers = item.find_elements_by_xpath('//div[contains(@class, "sticker")]')

        if(len(product_stickers) != 1):
            products_without_stickers.append(product_name.text)
            test_passed = False

    assert test_passed, f'{len(products)} products without stickers: {products_without_stickers}.'

#endregion

#region ACTIONS_METHODS_REGION

def select_browser(browser, request):
    if browser == Browser.CHROME:
        wd = webdriver.Chrome()
    elif browser == Browser.FIREFOX_OLD_SCHEME:
        # Needs (old) Firefox version 45
        wd = webdriver.Firefox(capabilities={"marionette": False})
    elif browser == Browser.FIREFOX_NEW_SCHEME:
        # Firefox Nightly
        # wd = webdriver.Firefox()
        wd = webdriver.Firefox(capabilities={"marionette": True})
    elif browser == Browser.EXPLORER:
        # Needs a 32 bit driver
        wd = webdriver.Ie(capabilities={"requireWindowFocus": True})
    else:
        return

    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

#endregion

#region EXPERIMENTS_REGION

def test_check_sections_runtime_estimate(driver):
    test_authorization_main_page(driver)

    products = driver.find_elements_by_class_name('product')

    test_passed = True
    products_without_stickers = []
    for item in products:
        product_name = item.find_element_by_class_name('name')

        # Crome, 11 (wrong items), 10s (wait for each test) = 115.88s (test runtime)
        # product_sticker = item.find_elements_by_class_name('sticker1')

        # Crome, 11 (wrong items), 10s (wait for each test) = 115.96s (test runtime)
        # Explorer, 11 (wrong items), 10s (wait for each test) = 122.94s (test runtime)
        product_sticker = item.find_elements_by_xpath('//div[contains(@class, "sticker1")]')


        # Crome, 11 (wrong items), 10s (wait for each test) = 115.88s (test runtime)
        # Explorer, 11 (wrong items), 10s (wait for each test) = 123.98s (test runtime)
        # product_sticker = item.find_elements_by_css_selector('div.sticker1')

        if(len(product_sticker) == 0):
            products_without_stickers.append(product_name.text)
            test_passed = False

    assert test_passed, f'Products without stickers: {products_without_stickers}.'

#endregion



