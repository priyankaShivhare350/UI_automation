import time
import pytest
from pages.cart_page import CartPage
from utils import config

@pytest.mark.cart
class TestCartPage:
     def test_add_single_product_to_cart(self,driver):
        cart_page = CartPage(driver)
        product_name = "Selenium Ruby"
        cart_page.add_product_to_cart_by_name(product_name)
        cart_page.open_cart()
        cart_items = cart_page.get_cart_items()
        assert product_name in cart_items, f"{product_name} not found in cart."
    
     def test_add_multiple_products_to_cart(self,driver):
        cart_page = CartPage(driver)
        products = ["Selenium Ruby", "Thinking in HTML"]
        for product in products:
            cart_page.add_product_to_cart_by_name(product)
            cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) == len(products), f"Expected {len(products)} items, but found {len(cart_items)}"
        for product in products:
            assert product in cart_items, f"{product} not found in cart"
    
     def test_remove_one_of_multiple_products(self,driver):
        cart_page = CartPage(driver)
        cart_page.add_product_to_cart_by_name("Selenium Ruby")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.add_product_to_cart_by_name("Thinking in HTML")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_page.remove_item_by_name("Thinking in HTML")
        cart_page.wait_for_item_removal("Thinking in HTML")
        items = cart_page.get_cart_items()
        assert "Selenium Ruby" in items
        assert "Thinking in HTML" not in items
    
     def test_remove_all_products(self,driver):
        cart_page = CartPage(driver)
        cart_page.add_product_to_cart_by_name("Selenium Ruby")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.add_product_to_cart_by_name("Thinking in HTML")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_page.remove_all_items()
        assert cart_page.is_cart_empty(), "Cart is not empty after removing all items"
     def test_add_multiple_quantities_same_product(self,driver):
        cart_page = CartPage(driver)
        product = "Selenium Ruby"
        for _ in range(3):
            cart_page.add_product_to_cart_by_name(product)
            cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_items = cart_page.get_cart_items()
        assert cart_items.count(product) >= 1, f"{product} not found in cart"
        quantity = cart_page.get_quantity_for_product(product)
        assert quantity == 3, f"Expected quantity 3 but got {quantity} for {product}"
    
     def test_cart_icon_updated_quantity(self,driver):
        cart_page = CartPage(driver)
        cart_page.add_product_to_cart_by_name("Selenium Ruby")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        quantity_icon = cart_page.get_cart_quantity()
        assert quantity_icon > 0, "Cart icon did not update with quantity"
    
     def test_price_calculation_per_quantity(self,driver):
        cart_page = CartPage(driver)
        product = "Selenium Ruby"
    
        # Add product once
        cart_page.add_product_to_cart_by_name(product)
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
    
        unit_price = cart_page.get_price_by_product_name(product)
        quantity = cart_page.get_quantity_for_product(product)
        cart_totals = cart_page.get_cart_totals()
        subtotal = float(cart_totals['subtotal'].replace("\u20b9", "").replace(",", "").strip())
    
        assert quantity == 1, f"Expected quantity 1, got {quantity}"
        assert subtotal == unit_price, f"Expected subtotal {unit_price}, got {subtotal}"
    
        # Add product two more times (total 3)
        driver.get(config.BASE_URL)
        for _ in range(2):
            cart_page.add_product_to_cart_by_name(product)
            cart_page.wait_for_product_to_appear_in_cart_icon()
        time.sleep(5)
        cart_page.open_cart()
        quantity = cart_page.get_quantity_for_product(product)
        cart_totals = cart_page.get_cart_totals()
        subtotal = float(cart_totals['subtotal'].replace("\u20b9", "").replace(",", "").strip())
        expected_subtotal = unit_price * 3
        assert quantity == 3, f"Expected quantity 3, got {quantity}"
        assert subtotal == expected_subtotal, f"Expected subtotal {expected_subtotal}, got {subtotal}"
    
     def test_delete_product_from_cart_then_go_back(self,driver):
        cart_page = CartPage(driver)
        cart_page.add_product_to_cart_by_name("Selenium Ruby")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_page.remove_item_by_name("Selenium Ruby")
        driver.back()
        cart_items = cart_page.get_cart_items()
        assert "Selenium Ruby" not in cart_items
    
     def test_remove_from_already_empty_cart(self,driver):
        cart_page = CartPage(driver)
        cart_page.open_cart()
        cart_page.remove_all_items()
        try:
            cart_page.remove_all_items()
            assert True
        except:
            pytest.fail("Removing from an already empty cart caused an error")
    
     def test_browser_back_after_removal(self,driver):
        cart_page = CartPage(driver)
        cart_page.add_product_to_cart_by_name("Selenium Ruby")
        cart_page.wait_for_product_to_appear_in_cart_icon()
        cart_page.open_cart()
        cart_page.remove_item_by_name("Selenium Ruby")
        driver.back()
        cart_items = cart_page.get_cart_items()
        assert "Selenium Ruby" not in cart_items
