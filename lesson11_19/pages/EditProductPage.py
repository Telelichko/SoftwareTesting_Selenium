from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from python_tests.lesson11_19.Helpers.DomHelper import DomHelper


class EditProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.domHelper = DomHelper()

    def get_list_size(self):
        return self.domHelper.get_list(self.driver, 'Size')

    def get_lists_item_small_size(self):
        return self.domHelper.get_list_item(self.driver, 'Size', 'Small')

    def get_product_quantity(self):
        return self.driver.find_element_by_xpath(self.domHelper.xpath_product_quantity)

    def get_button_to_cart(self):
        return self.driver.find_element_by_xpath(self.domHelper.xpath_button_to_cart)

    def get_link_cart(self):
        return self.driver.find_element_by_xpath(self.domHelper.xpath_link_cart)

    def is_element_exist(self, xpath):
        elements = self.driver.find_elements_by_xpath(xpath)

        if len(elements) > 0:
            return True

        return False

    def wait_until_text_appear(self, xpath, expected_text):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), expected_text))