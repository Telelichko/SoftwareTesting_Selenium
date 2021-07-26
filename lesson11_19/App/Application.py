from selenium import webdriver
from python_tests.lesson11_19.Helpers.DomHelper import DomHelper
from python_tests.lesson11_19.Helpers.WebDriverWaitHelper import WebDriverWaitHelper
from python_tests.lesson11_19.pages.CartPage import CartPage
from python_tests.lesson11_19.pages.EditProductPage import EditProductPage
from python_tests.lesson11_19.pages.MainPage import MainPage


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.main_page = MainPage(self.driver)
        self.editProductPage = EditProductPage(self.driver)
        self.cartPage = CartPage(self.driver)
        self.domHelper = DomHelper()
        self.webDriverWaitHelper = WebDriverWaitHelper(self.driver)

    def quit(self):
        self.driver.quit()

    def driver(self):
        return self.driver

    def add_product_to_cart(self):
        self.main_page.open()
        self.main_page.get_product_in_list().click()
        self.check_and_select_small_product_size()
        count_products_in_cart = self.editProductPage.get_product_quantity().text
        self.editProductPage.get_button_to_cart().click()
        self.webDriverWaitHelper.wait_until_text_appear(self.domHelper.xpath_product_quantity, f'{int(count_products_in_cart) + 1}')

    def open_main_page(self):
        self.main_page.open()

    def check_and_select_small_product_size(self):
        is_list_exist = self.editProductPage.is_element_exist(self.domHelper.xpath_lists_product_size)
        if is_list_exist:
            self.editProductPage.get_list_size().click()
            self.editProductPage.get_lists_item_small_size().click()

    def delete_products_in_cart(self):
        self.editProductPage.get_link_cart().click()

        product_count = self.cartPage.get_product_count()

        for i in range(product_count):
            button_remove = self.cartPage.get_button_remove()
            self.webDriverWaitHelper.wait_until_element_appear(button_remove)
            button_remove.click()
            self.webDriverWaitHelper.wait_until_element_disappear(button_remove)

        self.open_main_page()