import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import driver
from pages.base_page import BasePage

class CartPage(BasePage):
    VIEW_CART_LINK = (By.CSS_SELECTOR, 'a.wpmenucart-contents')
    CART_ITEM_NAMES = (By.CSS_SELECTOR, 'td.product-name')
    REMOVE_BUTTONS = (By.CSS_SELECTOR, 'a.remove')
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, 'p.cart-empty')
    PRODUCT_PRICES = (By.CSS_SELECTOR, 'td.product-price span.woocommerce-Price-amount')
    SUBTOTAL = (By.CSS_SELECTOR, 'tr.cart-subtotal td span.woocommerce-Price-amount')
    TAX = (By.CSS_SELECTOR, 'tr.tax-rate td span.woocommerce-Price-amount')
    TOTAL = (By.CSS_SELECTOR, 'tr.order-total td span.woocommerce-Price-amount')
    CART_QUANTITY_ICON = (By.CSS_SELECTOR, "span.cartcontents")

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart(self):
        self.click(self.VIEW_CART_LINK)
        self.click(self.VIEW_CART_LINK)

    def get_cart_items(self):
        elements = self.get_elements(*self.CART_ITEM_NAMES)
        return [element.text for element in elements]


    def remove_all_items(self):
        while True:
            remove_buttons = self.get_elements(*self.REMOVE_BUTTONS)
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
        prices = self.get_elements(*self.PRODUCT_PRICES)
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

    def get_quantity_for_product(self, product_name):
        xpath = f"//td[@class='product-name']/a[text()='{product_name}']/../../td[@class='product-quantity']//input"
        quantity_input = self.get_element((By.XPATH, xpath))
        return int(quantity_input.get_attribute("value"))

    def get_cart_quantity(self):
        return int(self.get_text(self.CART_QUANTITY_ICON).split(" ")[0])

    def get_price_by_product_name(self, product_name):
        xpath = f"//td[@class='product-name']/a[text()='{product_name}']/../../td[@class='product-price']/span"
        element = self.get_element((By.XPATH, xpath))
        return float(element.text.replace("₹", "").replace(",", "").strip())

    def wait_for_product_to_appear_in_cart_icon(self):
        self.wait.until(
            lambda d: int(d.find_element(*self.CART_QUANTITY_ICON).text.split()[0]) > 0
        )

    def wait_for_item_removal(self, product_name, timeout=10):
        xpath = f"//td[@class='product-name']/a[text()='{product_name}']"
        self.wait.until(
            EC.invisibility_of_element_located((By.XPATH, xpath))
        )
