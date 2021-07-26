class DomHelper:

    #region Xpath_For_MainPage

    xpath_product_in_list = '//li[contains(@class, "product")]'

    #endregion

    #region Xpath_For_EditProductPage

    xpath_lists_product_size = '//div[@class="content"]//tr[contains(., "Size")]//select'

    xpath_product_quantity = '//a[@class="content" and contains(., "Cart")]//span[@class="quantity"]'

    xpath_link_cart = '//a[contains(text(), "Checkout")]'

    xpath_button_to_cart = '//button[text()="Add To Cart"]'

    #endregion

    #region Xpath_For_CartPage

    xpath_list_products = '//ul[@class="items"]//li'

    xpath_button_remove = '//button[text()="Remove"]'

    #endregion

    def get_list(self, driver, list_name):
        return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]//select')

    def get_list_item(self, driver, list_name, item):
        return driver.find_element_by_xpath(f'//div[@class="content"]//tr[contains(., "{list_name}")]'
                                            f'//option[contains(text(), "{item}")]')