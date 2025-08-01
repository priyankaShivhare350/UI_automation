from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.product1_add=(By.CSS_SELECTOR,".products:nth-child(1) li a + a")
        self.product2_add=(By.CSS_SELECTOR,".products:nth-child(2) li a + a")
        self.product3_add=(By.CSS_SELECTOR,".products:nth-child(3) li a + a")


    def add_first_product_to_cart(self):
        self.click((By.CSS_SELECTOR, ".products .product:first-child a.button"))