from selenium.webdriver.support.wait import WebDriverWait
from python_tests.lesson11_19.Helpers.DomHelper import DomHelper


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.domHelper = DomHelper()

    def open(self):
        self.driver.get("http://localhost/litecart/")
        return self

    def get_product_in_list(self):
        return self.driver.find_element_by_xpath(self.domHelper.xpath_product_in_list)