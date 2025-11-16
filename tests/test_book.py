"""
Unit tests for the Book class.
"""

import unittest
from cookit.book import Book
from cookit.dish import Dish
from cookit.ingredient import Ingredient


class TestBook(unittest.TestCase):
    """Test cases for Book class."""
    
    def test_book_creation(self):
        """Test basic book creation."""
        book = Book("My Recipes")
        self.assertEqual(book.name, "My Recipes")
        self.assertEqual(len(book.dishes), 0)
    
    def test_add_dish(self):
        """Test adding dishes to book."""
        book = Book("Cookbook")
        dish = Dish("Pasta")
        book.add_dish(dish)
        self.assertEqual(len(book.dishes), 1)
    
    def test_remove_dish(self):
        """Test removing dishes from book."""
        book = Book("Cookbook")
        dish1 = Dish("Pasta")
        dish2 = Dish("Salad")
        book.add_dish(dish1)
        book.add_dish(dish2)
        
        self.assertTrue(book.remove_dish(dish1))
        self.assertEqual(len(book.dishes), 1)
        self.assertFalse(book.remove_dish(dish1))  # Already removed
    
    def test_find_dish(self):
        """Test finding dishes by name."""
        book = Book("Cookbook")
        dish = Dish("Spaghetti Carbonara")
        book.add_dish(dish)
        
        found = book.find_dish("Spaghetti Carbonara")
        self.assertEqual(found, dish)
        
        found_lower = book.find_dish("spaghetti carbonara")
        self.assertEqual(found_lower, dish)  # Case-insensitive
        
        not_found = book.find_dish("Pizza")
        self.assertIsNone(not_found)
    
    def test_get_all_ingredients(self):
        """Test getting all ingredients from all dishes."""
        book = Book("Cookbook")
        dish1 = Dish("Pasta", ingredients=[Ingredient("Pasta", 500.0, "g")])
        dish2 = Dish("Salad", ingredients=[Ingredient("Lettuce", 200.0, "g")])
        book.add_dish(dish1)
        book.add_dish(dish2)
        
        all_ingredients = book.get_all_ingredients()
        self.assertEqual(len(all_ingredients), 2)
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        book = Book("My Recipes")
        dish = Dish("Pasta", ingredients=[Ingredient("Pasta", 500.0, "g")])
        book.add_dish(dish)
        
        data = book.to_dict()
        book2 = Book.from_dict(data)
        
        self.assertEqual(book.name, book2.name)
        self.assertEqual(len(book.dishes), len(book2.dishes))


if __name__ == "__main__":
    unittest.main()

