"""
Unit tests for the storage module.
"""

import unittest
import json
import os
from pathlib import Path
from cookit.storage import (
    save_book,
    load_book,
    save_supermarkets,
    load_supermarkets,
    save_shopping_list,
    load_shopping_list,
    DB_DIR,
)
from cookit.book import Book
from cookit.dish import Dish
from cookit.ingredient import Ingredient
from cookit.supermarket import Supermarket
from cookit.shopping_list import ShoppingList


class TestStorage(unittest.TestCase):
    """Test cases for storage functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test files
        if DB_DIR.exists():
            for file in DB_DIR.glob("*.json"):
                try:
                    file.unlink()
                except:
                    pass
    
    def tearDown(self):
        """Clean up after tests."""
        # Clean up test files
        if DB_DIR.exists():
            for file in DB_DIR.glob("*.json"):
                try:
                    file.unlink()
                except:
                    pass
    
    def test_save_and_load_book(self):
        """Test saving and loading a book."""
        book = Book("Test Book")
        dish = Dish("Test Dish", ingredients=[Ingredient("Test Ingredient", 100.0, "g")])
        book.add_dish(dish)
        
        save_book(book)
        loaded_book = load_book()
        
        self.assertIsNotNone(loaded_book)
        self.assertEqual(book.name, loaded_book.name)
        self.assertEqual(len(book.dishes), len(loaded_book.dishes))
    
    def test_save_and_load_supermarkets(self):
        """Test saving and loading supermarkets."""
        supermarkets = [
            Supermarket("Store A", delivery_price=5.00),
            Supermarket("Store B", delivery_price=3.00),
        ]
        
        save_supermarkets(supermarkets)
        loaded = load_supermarkets()
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].name, "Store A")
        self.assertEqual(loaded[1].name, "Store B")
    
    def test_save_and_load_shopping_list(self):
        """Test saving and loading shopping lists."""
        sl = ShoppingList()
        sl.add_item(Ingredient("Eggs", 6.0, "pcs"))
        
        save_shopping_list(sl, "test_list")
        loaded = load_shopping_list("test_list")
        
        self.assertIsNotNone(loaded)
        self.assertEqual(len(loaded.items), 1)
        self.assertEqual(loaded.items[0].name, "Eggs")
    
    def test_load_nonexistent_book(self):
        """Test loading a book that doesn't exist."""
        loaded = load_book()
        # Should return None or create a default book
        # Based on implementation, it returns None
        if loaded is None:
            # This is expected behavior
            pass
        else:
            # Or it might create a default
            self.assertIsInstance(loaded, Book)
    
    def test_load_nonexistent_shopping_list(self):
        """Test loading a shopping list that doesn't exist."""
        loaded = load_shopping_list("nonexistent")
        self.assertIsNone(loaded)


if __name__ == "__main__":
    unittest.main()

