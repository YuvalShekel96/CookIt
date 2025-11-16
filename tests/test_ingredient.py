"""
Unit tests for the Ingredient class.
"""

import unittest
from cookit.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    """Test cases for Ingredient class."""
    
    def test_ingredient_creation(self):
        """Test basic ingredient creation."""
        ing = Ingredient("Tomatoes", 500.0, "g")
        self.assertEqual(ing.name, "Tomatoes")
        self.assertEqual(ing.units_required, 500.0)
        self.assertEqual(ing.unit_type, "g")
        self.assertIsNone(ing.price_per_unit)
        self.assertIsNone(ing.source_supermarket)
    
    def test_ingredient_with_price(self):
        """Test ingredient creation with price."""
        ing = Ingredient("Milk", 1.0, "L", price_per_unit=3.50, source_supermarket="Store A")
        self.assertEqual(ing.price_per_unit, 3.50)
        self.assertEqual(ing.source_supermarket, "Store A")
    
    def test_total_price(self):
        """Test total price calculation."""
        ing = Ingredient("Flour", 2.0, "kg", price_per_unit=2.50)
        self.assertEqual(ing.total_price(), 5.0)
    
    def test_total_price_no_price(self):
        """Test total price returns None when price is not set."""
        ing = Ingredient("Salt", 100.0, "g")
        self.assertIsNone(ing.total_price())
    
    def test_equality(self):
        """Test ingredient equality based on name and unit_type."""
        ing1 = Ingredient("Sugar", 500.0, "g")
        ing2 = Ingredient("Sugar", 300.0, "g")
        ing3 = Ingredient("Sugar", 500.0, "kg")
        
        self.assertEqual(ing1, ing2)  # Same name and unit_type
        self.assertNotEqual(ing1, ing3)  # Different unit_type
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        ing = Ingredient("Eggs", 6.0, "pcs", price_per_unit=0.50, source_supermarket="Store B")
        data = ing.to_dict()
        
        ing2 = Ingredient.from_dict(data)
        self.assertEqual(ing.name, ing2.name)
        self.assertEqual(ing.units_required, ing2.units_required)
        self.assertEqual(ing.unit_type, ing2.unit_type)
        self.assertEqual(ing.price_per_unit, ing2.price_per_unit)
        self.assertEqual(ing.source_supermarket, ing2.source_supermarket)


if __name__ == "__main__":
    unittest.main()

