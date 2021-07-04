import ast
from enum import Enum

import pytest
from selenium import webdriver


class Browser(Enum):
    CHROME = 1
    FIREFOX_OLD_SCHEME = 2
    FIREFOX_NEW_SCHEME = 3
    EXPLORER = 4
    ALL = 5


@pytest.fixture()
def driver(request):
    wd = select_browser(Browser.FIREFOX_NEW_SCHEME, request)

    return wd

#region TESTS_METHODS_REGION

def test_go_to_main_page(driver):
    main_page_url = 'http://localhost/litecart/'
    driver.get(main_page_url)




def test_check_1253543577(driver):
    test_go_to_main_page(driver)

    products = driver.find_elements_by_class_name('product')

    #TODO: Проверить для индекса 6
    for i, item in enumerate(products):
        item = driver.find_element_by_xpath(f'//li[contains(@class, "product")][{i + 1}]')
        element_product_name = item.find_element_by_xpath(f'.//div[@class="name"]')
        product_name = element_product_name.text

        # TODO: акционная цена крупнее, чем обычная
        price, regular_price, campaign_price = get_prices(item, product_name)

        element_product_link = element_product_name.find_element_by_xpath('./ancestor::a[1]')
        element_product_link.click()

        item_inside = driver.find_element_by_xpath('//div[@id="box-product"]')

        element_product_name_inside = item_inside.find_element_by_class_name('title')
        product_name_inside = element_product_name_inside.text

        price_inside, regular_price_inside, campaign_price_inside = get_prices(item_inside, product_name_inside)

        assert product_name == product_name_inside, \
            f'Names of product "{product_name}" aren\'t the same ("{product_name}" != "{product_name_inside}").'

        assert price == price_inside, \
            f'The simple prices in product "{element_product_name}" aren\'t the same ("{price}" != "{price_inside}").'

        assert regular_price == regular_price_inside, \
            f'The simple prices in product "{element_product_name}" aren\'t the same ("{regular_price}" != "{regular_price_inside}").'

        assert campaign_price == campaign_price_inside, \
            f'The simple prices in product "{element_product_name.text}" aren\'t the same ("{campaign_price}" != "{campaign_price_inside}").'

        test_go_to_main_page(driver)

        something01 = 1
        # We check only one product. Without break check all.
        # break;

    something31 = 1



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
    elif browser == Browser.All:
        return
    else:
        return

    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def get_first_element_or_none(list_elements):
    if(len(list_elements) == 0):
        return None
    else:
        return list_elements[0]

def get_text_or_none(element):
    if(element == None):
        return None
    else:
        return element.text

def check_element_or_none(element):
    return element != None

def parse_element_color_to_components(element):
    color = element.value_of_css_property('color') # 51, 51, 51

    color_components = color.replace("rgb(", "").replace(")", "").split(",")
    r, g, b = int(color_components[0]), int(color_components[1]), int(color_components[2])
    return r, g, b

def get_prices(element, product_name):
    element_price = get_first_element_or_none(element.find_elements_by_class_name('price'))
    element_regular_price = get_first_element_or_none(element.find_elements_by_class_name('regular-price'))
    element_campaign_price = get_first_element_or_none(element.find_elements_by_class_name('campaign-price'))

    if element_price != None:
        assert_element_without_line(element_price)
        assert_element_grey_color(element_price)

    if element_regular_price != None:
        assert_element_crossed_out(element_regular_price)
        assert_element_small(element_regular_price)
        assert_element_grey_color(element_regular_price)

    if element_campaign_price != None:
        assert_element_without_line(element_campaign_price)
        assert_element_fatty(element_campaign_price)
        assert_element_red_color(element_campaign_price)

    if(element_price == None and element_regular_price == None and element_campaign_price == None):
        raise Exception(f'There isn\'t any price in product "{product_name}".')

    if(check_element_or_none(element_regular_price) !=  check_element_or_none(element_campaign_price)):
        raise Exception(f'There is one price instead 2 in product "{product_name}" '
                        f'(regular price = "{get_text_or_none(element_regular_price)}", campaign price = "{get_text_or_none(element_campaign_price)}").')

    price = get_text_or_none(element_price)
    regular_price = get_text_or_none(element_regular_price)
    campaign_price = get_text_or_none(element_campaign_price)

    return price, regular_price, campaign_price

#endregion



#region ASSERTS_METHODS_REGION

def assert_element_grey_color(element):
    r, g, b = parse_element_color_to_components(element)
    grey_color = r == g == b and r >= 50 and r < 150

    assert grey_color, 'The color isn\' grey.'

def assert_element_red_color(element):
    r, g, b = parse_element_color_to_components(element)
    red_color = r >= 100 and g == 0 and b == 0

    assert red_color, 'The color isn\' red.'

def assert_element_crossed_out(element):
    line_property = element.value_of_css_property('text-decoration-line')

    assert line_property == 'line-through', 'Line isn\'t crossed out.'


def assert_element_without_line(element):
    line_property = element.value_of_css_property('text-decoration-line')

    assert line_property == 'none', 'There is line on text.'

def assert_element_fatty(element):
    weight = int(element.value_of_css_property('font-weight'))

    assert weight >= 700,  'Element isn\'t fatty.'

def assert_element_small(element):
    size = int(element.value_of_css_property('font-size'))

    assert size <= 0.8,  'Element isn\'t small.'

#endregion