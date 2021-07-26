from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class WebDriverWaitHelper:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_until_text_appear(self, xpath, expected_text):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), expected_text))

    def wait_until_element_appear(self, element):
        self.wait.until(EC.visibility_of(element))

    def wait_until_element_disappear(self, element):
        self.wait.until(EC.invisibility_of_element(element))