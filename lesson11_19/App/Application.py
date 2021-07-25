from selenium import webdriver
from python_tests.lesson11_19.pages.MainPage import MainPage


class Application:
    # driver = webdriver.Chrome()

    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.wait = self.driver.implicitly_wait(10)
        self.main_page = MainPage(self.driver)

    def quit(self):
        self.driver.quit()

    def driver(self):
        return self.driver

    def open_main_page(self):
        self.main_page.open()