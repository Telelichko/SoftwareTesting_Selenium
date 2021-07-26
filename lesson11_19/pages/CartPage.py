from python_tests.lesson11_19.Helpers.DomHelper import DomHelper


class CartPage():

    def __init__(self, driver):
        self.driver = driver
        self.domHelper = DomHelper()

    def get_button_remove(self):
        return self.driver.find_element_by_xpath(self.domHelper.xpath_button_remove)

    def get_product_count(self):
        return len(self.driver.find_elements_by_xpath(self.domHelper.xpath_list_products))