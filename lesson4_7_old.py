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
    wd = select_browser(Browser.CHROME, request)
    return wd

#region TESTS_METHODS_REGION

def test_authorization_admin_panel(driver):
    main_page_url = 'http://localhost/litecart/admin/'
    driver.get(main_page_url)

    input_username = driver.find_element_by_name('username')
    input_username.send_keys('admin')

    input_password = driver.find_element_by_name('password')
    input_password.send_keys('nimda')

    button_login = driver.find_element_by_name('login')
    button_login.click()


def test_check_sections(driver):
    test_authorization_admin_panel(driver)

    left_menu = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]')

    sections = left_menu.find_elements_by_xpath('.//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]')

    for i, item in enumerate(sections):
        item = left_menu.find_elements_by_xpath(f'.//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"][{i + 1}]')
        item.click()
        assert_page_title_exist(driver, item)

        subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        for j, item2 in enumerate(subsections):
            item2 = driver.find_elements_by_xpath(f'//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"][{j + 1}]')

            sleep(1)
            item2.click()
            assert_page_title_exist(driver, item2)



def test_check_sections_2(driver):
    xpath_sections = '//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]'

    # xpath_subsection =

    test_authorization_admin_panel(driver)

    sections = driver.find_elements_by_xpath(xpath_sections)

    for i, item in enumerate(sections):
        # TODO: Отладить. Берет вместе с подразделами, в случайном порядке, и долго ждет
        something = driver.find_elements_by_xpath(xpath_sections)
        item = get_element_by_xpath_and_number(driver, xpath_sections, i)

        assert_element_by_number_exist(driver, i, item, 'Section')

        subsections = item.find_elements_by_xpath('following::ul[@class="docs"][1]//span[@class="name"]')

        item.click()
        assert_page_title_exist(driver, item)


        # subsections = item.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')


        # subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        # for i_sub, item_sub in enumerate(subsections):
        #     sleep(0.5)
        #     item_sub.click()
        #     assert_page_title_exist(driver, item_sub)


# With StaleElementReferenceException in second element
def test_check_sections_with_exception(driver):
    test_authorization_admin_panel(driver)

    left_menu = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]')

    sections = left_menu.find_elements_by_xpath('.//li[@id = "app-"]//*[not(@class="docs")]//span[@class="name"]')

    for item in sections:
        item.click()
        assert_page_title_exist(driver, item)

        subsections = driver.find_elements_by_xpath('//li[@id="app-" and @class="selected"]//ul[@class="docs"]//span[@class="name"]')

        for item2 in subsections:
            sleep(1)
            item2.click()
            assert_page_title_exist(driver, item2)


# With IndexError
def test_check_subsections_wrong_numbers(driver):
    test_authorization_admin_panel(driver)

    max_subsections = 100

    for i in range(max_subsections + 1):
        sleep(1)
        subsection = driver.find_elements_by_xpath('//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//span[@class="name"]')[i]
        if(subsection == None):
            break;

        subsection.click()

        if(i == max_subsections):
            subsection_next = driver.find_elements_by_xpath('//div[contains(@id, "menu-wrapper")]//li[@id = "app-"]//span[@class="name"]')[i + 1]
            assert subsection_next == None, f'There is more than "{max_subsections}" subsections.'

def test_check_sections_3(driver):
    test_authorization_admin_panel(driver)

    go_to_subsection(driver, 'Appearence', 'Template')
    assert_page_title(driver, 'Template')

    go_to_subsection(driver, 'Appearence', 'Logotype')
    assert_page_title(driver, 'Logotype')

    go_to_subsection(driver, 'Catalog', 'Catalog')
    assert_page_title(driver, 'Catalog')

    go_to_subsection(driver, 'Catalog', 'Product Groups')
    assert_page_title(driver, 'Product Groups')

    go_to_subsection(driver, 'Catalog', 'Option Groups')
    assert_page_title(driver, 'Option Groups')

    go_to_subsection(driver, 'Catalog', 'Manufacturers')
    assert_page_title(driver, 'Manufacturers')

    go_to_subsection(driver, 'Catalog', 'Suppliers')
    assert_page_title(driver, 'Suppliers')

    go_to_subsection(driver, 'Catalog', 'Delivery Statuses')
    assert_page_title(driver, 'Delivery Statuses')

    go_to_subsection(driver, 'Catalog', 'Sold Out Statuses')
    assert_page_title(driver, 'Sold Out Statuses')

    go_to_subsection(driver, 'Catalog', 'Quantity Units')
    assert_page_title(driver, 'Quantity Units')

    go_to_subsection(driver, 'Catalog', 'CSV Import/Export')
    assert_page_title(driver, 'CSV Import/Export')

    go_to_section(driver, 'Countries')
    assert_page_title(driver, 'Countries')

    go_to_section(driver, 'Currencies')
    assert_page_title(driver, 'Currencies')

    go_to_subsection(driver, 'Customers', 'Customers')
    assert_page_title(driver, 'Customers')

    go_to_subsection(driver, 'Customers', 'CSV Import/Export')
    assert_page_title(driver, 'CSV Import/Export')

    go_to_subsection(driver, 'Customers', 'Newsletter')
    assert_page_title(driver, 'Newsletter')

    go_to_section(driver, 'Geo Zones')
    assert_page_title(driver, 'Geo Zones')

    go_to_subsection(driver, 'Languages', 'Languages')
    assert_page_title(driver, 'Languages')

    go_to_subsection(driver, 'Languages', 'Storage Encoding')
    assert_page_title(driver, 'Storage Encoding')

    go_to_subsection(driver, 'Modules', 'Background Jobs')
    assert_page_title(driver, 'Job Modules')

    go_to_subsection(driver, 'Modules', 'Customer')
    assert_page_title(driver, 'Customer Modules')

    go_to_subsection(driver, 'Modules', 'Shipping')
    assert_page_title(driver, 'Shipping Modules')

    go_to_subsection(driver, 'Modules', 'Payment')
    assert_page_title(driver, 'Payment Modules')

    go_to_subsection(driver, 'Modules', 'Order Total')
    assert_page_title(driver, 'Order Total Modules')

    go_to_subsection(driver, 'Modules', 'Order Success')
    assert_page_title(driver, 'Order Success Modules')

    go_to_subsection(driver, 'Modules', 'Order Action')
    assert_page_title(driver, 'Order Action Modules')

    go_to_subsection(driver, 'Orders', 'Orders')
    assert_page_title(driver, 'Orders')

    go_to_subsection(driver, 'Orders', 'Order Statuses')
    assert_page_title(driver, 'Order Statuses')

    go_to_section(driver, 'Pages')
    assert_page_title(driver, 'Pages')

    go_to_subsection(driver, 'Reports', 'Monthly Sales')
    assert_page_title(driver, 'Monthly Sales')

    go_to_subsection(driver, 'Reports', 'Most Sold Products')
    assert_page_title(driver, 'Most Sold Products')

    go_to_subsection(driver, 'Reports', 'Most Shopping Customers')
    assert_page_title(driver, 'Most Shopping Customers')

    go_to_subsection(driver, 'Settings', 'Store Info')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Defaults')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'General')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Listings')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Images')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Checkout')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Advanced')
    assert_page_title(driver, 'Settings')

    go_to_subsection(driver, 'Settings', 'Security')
    assert_page_title(driver, 'Settings')

    go_to_section(driver, 'Slides')
    assert_page_title(driver, 'Slides')

    go_to_subsection(driver, 'Tax', 'Tax Classes')
    assert_page_title(driver, 'Tax Classes')

    go_to_subsection(driver, 'Tax', 'Tax Rates')
    assert_page_title(driver, 'Tax Rates')

    go_to_subsection(driver, 'Translations', 'Search Translations')
    assert_page_title(driver, 'Search Translations')

    go_to_subsection(driver, 'Translations', 'Scan Files')
    assert_page_title(driver, 'Scan Files For Translations')

    go_to_subsection(driver, 'Translations', 'CSV Import/Export')
    assert_page_title(driver, 'CSV Import/Export')

    go_to_section(driver, 'Users')
    assert_page_title(driver, 'Users')

    go_to_subsection(driver, 'vQmods', 'vQmods')
    assert_page_title(driver, 'vQmods')

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

    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def go_to_section(driver, text_section):
    try:
        button_section = driver.find_element_by_xpath(f'//span[text()="{text_section}"]')
        button_section.click()
    except NoSuchElementException:
        print(f'\n Button of section with name {text_section} isn\'t exist.')

def go_to_subsection(driver, text_section, text_subsection):
    try:
        button_section = driver.find_element_by_xpath(f'//span[text()="{text_section}"]')
        button_section.click()
    except NoSuchElementException:
        print(f'\n Button of section with name "{text_section}" isn\'t exist.')

    try:
        button_subsection = driver.find_element_by_xpath(f'//span[text()="{text_subsection}"]')
        button_subsection.click()
    except NoSuchElementException:
        print(f'\n Button of subsection with name "{text_subsection}" isn\'t exist.')
#endregion

#region ASSERTS_METHODS_REGION

def assert_page_title(driver, page_title):
    elements = driver.find_elements_by_tag_name(f'h1')

    necessary_elements = list(filter(lambda x: x.text == page_title, elements))

    assert len(necessary_elements) > 0, f'Title "{page_title}" isn\'t founded on page. There is "{elements[0].text}" title.'

    # Variant 1
    # elements = driver.find_elements_by_xpath(f'//h1[contains(text(),"{page_title}")]')
    # assert len(elements) == 1, f'Title "{page_title}" isn\'t founded on page.'

#endregion



