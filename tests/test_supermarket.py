"""
Unit tests for the Supermarket class.
"""

import unittest
from cookit.supermarket import Supermarket
from cookit.shopping_list import ShoppingList
from cookit.ingredient import Ingredient


class TestSupermarket(unittest.TestCase):
    """Test cases for Supermarket class."""
    
    def test_supermarket_creation(self):
        """Test basic supermarket creation."""
        sm = Supermarket("Store A")
        self.assertEqual(sm.name, "Store A")
        self.assertEqual(sm.delivery_price, 0.0)
        self.assertEqual(sm.website_url, "")
        self.assertEqual(len(sm.price_catalog), 0)
    
    def test_set_price(self):
        """Test setting prices in catalog."""
        sm = Supermarket("Store A")
        sm.set_price("Milk", 3.50)
        self.assertEqual(sm.get_price("Milk"), 3.50)
    
    def test_get_price(self):
        """Test getting prices from catalog."""
        sm = Supermarket("Store A")
        sm.set_price("Bread", 2.00)
        self.assertEqual(sm.get_price("Bread"), 2.00)
        self.assertIsNone(sm.get_price("Unknown Item"))
    
    def test_total_cost(self):
        """Test calculating total cost for shopping list."""
        sm = Supermarket("Store A", delivery_price=5.00)
        sm.set_price("Milk", 3.50)
        sm.set_price("Bread", 2.00)
        
        sl = ShoppingList()
        sl.add_item(Ingredient("Milk", 1.0, "L"))
        sl.add_item(Ingredient("Bread", 1.0, "pcs"))
        
        total = sm.total_cost(sl)
        self.assertEqual(total, 10.50)  # 3.50 + 2.00 + 5.00
    
    def test_total_cost_missing_price(self):
        """Test total cost returns None when item price is missing."""
        sm = Supermarket("Store A")
        sm.set_price("Milk", 3.50)
        # Bread price not set
        
        sl = ShoppingList()
        sl.add_item(Ingredient("Milk", 1.0, "L"))
        sl.add_item(Ingredient("Bread", 1.0, "pcs"))
        
        total = sm.total_cost(sl)
        self.assertIsNone(total)
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        sm = Supermarket("Store A", delivery_price=5.00, website_url="https://store.com")
        sm.set_price("Milk", 3.50)
        
        data = sm.to_dict()
        sm2 = Supermarket.from_dict(data)
        
        self.assertEqual(sm.name, sm2.name)
        self.assertEqual(sm.delivery_price, sm2.delivery_price)
        self.assertEqual(sm.website_url, sm2.website_url)
        self.assertEqual(sm.price_catalog, sm2.price_catalog)


if __name__ == "__main__":
    unittest.main()

