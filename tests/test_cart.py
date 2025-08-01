import time

import pytest
# from pages.product_page import ProductPage
# from utils import config

import pytest
from pages.cart_page import CartPage
from utils import config

@pytest.mark.cart
def test_add_single_product_to_cart(driver):
    cart_page = CartPage(driver)
    product_name = "Selenium Ruby"
    cart_page.add_product_to_cart_by_name(product_name)
    cart_page.open_cart()
    cart_items = cart_page.get_cart_items()
    assert product_name in cart_items, f"{product_name} not found in cart."

@pytest.mark.cart
def test_add_multiple_products_to_cart(driver):
    cart_page = CartPage(driver)
    products = ["Selenium Ruby", "Thinking in HTML"]
    for product in products:
        time.sleep(5)
        cart_page.add_product_to_cart_by_name(product)
    cart_page.open_cart()
    cart_items = cart_page.get_cart_items()
    assert len(cart_items) == len(products), f"Expected {len(products)} items, but found {len(cart_items)}"
    for product in products:
        assert product in cart_items, f"{product} not found in cart"
    print(f"All products successfully added to cart: {cart_items}")
@pytest.mark.cart
def test_remove_one_of_multiple_products(driver):
    cart_page = CartPage(driver)
    time.sleep(5)
    cart_page.add_product_to_cart_by_name("Selenium Ruby")
    time.sleep(5)
    cart_page.add_product_to_cart_by_name("Thinking in HTML")
    cart_page.open_cart()
    cart_page.remove_item_by_name("Thinking in HTML")
    time.sleep(5)
    items = cart_page.get_cart_items()
    assert ("Selenium Ruby" in items)
    assert ("Thinking in HTML" not in items)

@pytest.mark.cart
def test_remove_all_products(driver):
    driver.get(config.BASE_URL)
    cart_page = CartPage(driver)
    time.sleep(5)
    cart_page.add_product_to_cart_by_name("Selenium Ruby")
    time.sleep(5)
    cart_page.add_product_to_cart_by_name("Thinking in HTML")
    cart_page.open_cart()
    time.sleep(5)
    cart_page.remove_all_items()
    time.sleep(5)
    assert cart_page.is_cart_empty(), "Cart is not empty after removing all items"

def test_add_multiple_quantities_same_product(driver):
    driver.get(config.BASE_URL)
    cart_page = CartPage(driver)
    product = "Selenium Ruby"
    for _ in range(3):
        cart_page.add_product_to_cart_by_name(product)
    cart_page.open_cart()
    cart_items = cart_page.get_cart_items()
    assert cart_items.count(product) >= 1, f"{product} not found in cart"
