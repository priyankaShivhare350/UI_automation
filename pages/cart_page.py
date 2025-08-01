import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

from conftest import driver
from pages.base_page import BasePage

class CartPage(BasePage):
    # Locators
    VIEW_CART_LINK = (By.CSS_SELECTOR, 'a.wpmenucart-contents')
    CART_ITEM_NAMES = (By.CSS_SELECTOR, 'td.product-name')
    REMOVE_BUTTONS = (By.CSS_SELECTOR, 'a.remove')
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, 'p.cart-empty')
    PRODUCT_PRICES = (By.CSS_SELECTOR, 'td.product-price span.woocommerce-Price-amount')
    SUBTOTAL = (By.CSS_SELECTOR, 'tr.cart-subtotal td span.woocommerce-Price-amount')
    TAX = (By.CSS_SELECTOR, 'tr.tax-rate td span.woocommerce-Price-amount')
    TOTAL = (By.CSS_SELECTOR, 'tr.order-total td span.woocommerce-Price-amount')

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart(self):
        self.click(self.VIEW_CART_LINK)
        self.click(self.VIEW_CART_LINK)

    def get_cart_items(self):
        elements = self.driver.find_elements(*self.CART_ITEM_NAMES)
        return [element.text for element in elements]


    def remove_all_items(self):
        while True:
            remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
            if not remove_buttons:
                break
            try:
                remove_buttons[0].click()
                time.sleep(1)  # Optional: wait for DOM to update
            except StaleElementReferenceException:
                continue


    def is_cart_empty(self):
        return self.is_element_displayed(self.EMPTY_CART_MESSAGE)

    def add_product_to_cart_by_name(self, product_name):
        product_xpath = f"//h3[text()='{product_name}']/../..//a[text()='Add to basket']"
        product_locator = (By.XPATH, product_xpath)
        self.scroll_into_view(product_locator)
        self.click(product_locator)

    def remove_item_by_name(self, product_name):
        item_xpath = f"//td[@class='product-name']/a[text()='{product_name}']/../../td[@class='product-remove']/a"
        item_locator = (By.XPATH, item_xpath)
        self.click(item_locator)
        # self.wait_for_element_invisible((By.CSS_SELECTOR, 'div.woocommerce-message'))

    def get_product_prices(self):
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [price.text for price in prices]

    def get_cart_totals(self):
        subtotal = self.get_text(self.SUBTOTAL)
        tax = self.get_text(self.TAX)
        total = self.get_text(self.TOTAL)
        return {
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }
