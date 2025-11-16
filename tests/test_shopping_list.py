"""
Unit tests for the ShoppingList class.
"""

import unittest
from cookit.shopping_list import ShoppingList
from cookit.ingredient import Ingredient
from cookit.dish import Dish


class TestShoppingList(unittest.TestCase):
    """Test cases for ShoppingList class."""
    
    def test_shopping_list_creation(self):
        """Test basic shopping list creation."""
        sl = ShoppingList()
        self.assertEqual(len(sl.items), 0)
    
    def test_add_item(self):
        """Test adding items to shopping list."""
        sl = ShoppingList()
        ing = Ingredient("Tomatoes", 500.0, "g")
        sl.add_item(ing)
        self.assertEqual(len(sl.items), 1)
        self.assertEqual(sl.items[0].units_required, 500.0)
    
    def test_merge_quantities(self):
        """Test automatic merging of quantities for same ingredient."""
        sl = ShoppingList()
        ing1 = Ingredient("Flour", 500.0, "g")
        ing2 = Ingredient("Flour", 300.0, "g")
        
        sl.add_item(ing1)
        sl.add_item(ing2)
        
        self.assertEqual(len(sl.items), 1)
        self.assertEqual(sl.items[0].units_required, 800.0)
    
    def test_add_dish(self):
        """Test adding all ingredients from a dish."""
        sl = ShoppingList()
        dish = Dish("Pasta", ingredients=[
            Ingredient("Pasta", 500.0, "g"),
            Ingredient("Tomatoes", 300.0, "g")
        ])
        sl.add_dish(dish)
        self.assertEqual(len(sl.items), 2)
    
    def test_remove_dish(self):
        """Test removing ingredients from a dish."""
        sl = ShoppingList()
        dish = Dish("Pasta", ingredients=[
            Ingredient("Pasta", 500.0, "g"),
            Ingredient("Tomatoes", 300.0, "g")
        ])
        sl.add_dish(dish)
        self.assertEqual(len(sl.items), 2)
        
        sl.remove_dish(dish)
        self.assertEqual(len(sl.items), 0)
    
    def test_total_cost(self):
        """Test total cost calculation."""
        sl = ShoppingList()
        ing1 = Ingredient("Milk", 1.0, "L", price_per_unit=3.50)
        ing2 = Ingredient("Bread", 1.0, "pcs", price_per_unit=2.00)
        sl.add_item(ing1)
        sl.add_item(ing2)
        
        total = sl.total_cost()
        self.assertEqual(total, 5.50)
    
    def test_total_cost_missing_price(self):
        """Test total cost returns None when price is missing."""
        sl = ShoppingList()
        ing1 = Ingredient("Milk", 1.0, "L", price_per_unit=3.50)
        ing2 = Ingredient("Bread", 1.0, "pcs")  # No price
        sl.add_item(ing1)
        sl.add_item(ing2)
        
        total = sl.total_cost()
        self.assertIsNone(total)
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        sl = ShoppingList()
        sl.add_item(Ingredient("Eggs", 6.0, "pcs", price_per_unit=0.50))
        
        data = sl.to_dict()
        sl2 = ShoppingList.from_dict(data)
        
        self.assertEqual(len(sl.items), len(sl2.items))
        self.assertEqual(sl.items[0].name, sl2.items[0].name)


if __name__ == "__main__":
    unittest.main()

