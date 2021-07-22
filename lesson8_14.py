import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

#region TESTS_METHODS_REGION

def test_open_links_countries(driver):
    test_authorization_admin_panel(driver)

    countries_section = driver.find_element_by_xpath('//div[contains(@id, "menu-wrapper")]//span[contains(text(), "Countries")]')
    countries_section.click()

    link_first_country = driver.find_element_by_xpath('//table[@class="dataTable"]//a')
    link_first_country.click()

    count_external_pages = len(driver.find_elements_by_xpath('//td[@id="content"]//table//i'))

    window_litecart = driver.current_window_handle
    list_windows_before = driver.window_handles

    for i in range(count_external_pages):
        WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_xpath('//h1[contains(., "Edit Country")]')))

        links_external_page = driver.find_elements_by_xpath(f'//td[@id="content"]//table//i')[i]
        links_external_page.click()

        WebDriverWait(driver, 10).until(lambda d: len(list_windows_before) + 1)
        list_windows_after = driver.window_handles

        for item in list_windows_after:
            if item not in list_windows_before:
                driver.switch_to.window(item)
                # Пауза для проверки работы автотеста
                sleep(0.5)
                driver.close()
                driver.switch_to.window(window_litecart)
                break

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

def there_is_window_other_than(driver, old_windows):
    new_windows = driver.window_handles
    wait = WebDriverWait(driver, 60)  # seconds
    wait.until(lambda d: len(old_windows) < len(new_windows))
    new_window = old_windows - new_windows
    return new_window

#endregion