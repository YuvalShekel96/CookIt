"""
Unit tests for the Dish class.
"""

import unittest
from cookit.dish import Dish
from cookit.ingredient import Ingredient


class TestDish(unittest.TestCase):
    """Test cases for Dish class."""
    
    def test_dish_creation(self):
        """Test basic dish creation."""
        dish = Dish("Pasta")
        self.assertEqual(dish.name, "Pasta")
        self.assertEqual(len(dish.ingredients), 0)
        self.assertIsNone(dish.type)
        self.assertEqual(len(dish.labels), 0)
        self.assertEqual(len(dish.steps), 0)
    
    def test_dish_with_all_fields(self):
        """Test dish creation with all fields."""
        ingredients = [Ingredient("Pasta", 500.0, "g")]
        dish = Dish(
            "Spaghetti",
            ingredients=ingredients,
            dish_type="Main Course",
            labels=["Italian", "Quick"],
            steps=["Boil water", "Cook pasta"]
        )
        self.assertEqual(dish.name, "Spaghetti")
        self.assertEqual(len(dish.ingredients), 1)
        self.assertEqual(dish.type, "Main Course")
        self.assertEqual(len(dish.labels), 2)
        self.assertEqual(len(dish.steps), 2)
    
    def test_add_ingredient(self):
        """Test adding ingredients."""
        dish = Dish("Salad")
        ing = Ingredient("Lettuce", 200.0, "g")
        dish.add_ingredient(ing)
        self.assertEqual(len(dish.ingredients), 1)
        self.assertEqual(dish.ingredients[0], ing)
    
    def test_remove_ingredient(self):
        """Test removing ingredients."""
        dish = Dish("Soup")
        ing1 = Ingredient("Tomatoes", 300.0, "g")
        ing2 = Ingredient("Onions", 100.0, "g")
        dish.add_ingredient(ing1)
        dish.add_ingredient(ing2)
        
        self.assertTrue(dish.remove_ingredient(ing1))
        self.assertEqual(len(dish.ingredients), 1)
        self.assertFalse(dish.remove_ingredient(ing1))  # Already removed
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        dish = Dish(
            "Pizza",
            ingredients=[Ingredient("Flour", 500.0, "g")],
            dish_type="Main Course",
            labels=["Italian"],
            steps=["Make dough", "Add toppings"]
        )
        data = dish.to_dict()
        
        dish2 = Dish.from_dict(data)
        self.assertEqual(dish.name, dish2.name)
        self.assertEqual(dish.type, dish2.type)
        self.assertEqual(dish.labels, dish2.labels)
        self.assertEqual(dish.steps, dish2.steps)
        self.assertEqual(len(dish.ingredients), len(dish2.ingredients))


if __name__ == "__main__":
    unittest.main()

