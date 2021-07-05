import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_authorization_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)

def test_check_stickers_count(driver):
    test_authorization_main_page(driver)

    products = driver.find_elements_by_class_name('product')

    test_passed = True
    products_with_stickers_other_1 = []
    for item in products:
        product_name = item.find_element_by_class_name('name')

        product_stickers = item.find_elements_by_xpath('.//div[contains(@class, "sticker")]')

        if(len(product_stickers) != 1):
            products_with_stickers_other_1.append(product_name.text)
            test_passed = False

    assert test_passed, f'{len(products)} products without or more than one stickers: {products_with_stickers_other_1}.'

#endregion



