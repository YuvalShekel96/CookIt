"""
Unit tests for the storage module.
"""

import shutil
import unittest

from cookit.book import Book
from cookit.dish import Dish
from cookit.ingredient import Ingredient
from cookit.shopping_list import ShoppingList
from cookit.storage import (
    DB_DIR,
    list_shopping_lists,
    load_shopping_list,
    load_supermarkets,
    load_user_book,
    load_user_shopping_list,
    save_shopping_list,
    save_supermarkets,
    save_user_book,
    save_user_shopping_list,
)
from cookit.supermarket import Supermarket


class TestStorage(unittest.TestCase):
    """Test cases for storage functions."""

    USERNAME = "testuser"

    def setUp(self):
        """Set up test fixtures."""
        if DB_DIR.exists():
            shutil.rmtree(DB_DIR)

    def tearDown(self):
        """Clean up after tests."""
        if DB_DIR.exists():
            shutil.rmtree(DB_DIR)

    def test_save_and_load_user_book(self):
        """Test saving and loading a user's book."""
        book = Book("Test Book")
        book.add_dish(Dish("Test Dish", ingredients=[Ingredient("Test Ingredient", 100.0, "g")]))

        save_user_book(self.USERNAME, book)
        loaded_book = load_user_book(self.USERNAME)

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

    def test_save_and_load_named_shopping_list(self):
        """Test saving and loading named shopping lists per user."""
        sl = ShoppingList()
        sl.add_item(Ingredient("Eggs", 6.0, "pcs"))

        save_shopping_list(sl, "test_list", self.USERNAME)
        loaded = load_shopping_list("test_list", self.USERNAME)

        self.assertIsNotNone(loaded)
        self.assertEqual(len(loaded.items), 1)
        self.assertEqual(loaded.items[0].name, "Eggs")
        self.assertIn("test_list", list_shopping_lists(self.USERNAME))

    def test_user_current_shopping_list(self):
        """Test saving/loading the current shopping list per user."""
        sl = ShoppingList()
        sl.add_item(Ingredient("Milk", 1.0, "L"))

        save_user_shopping_list(self.USERNAME, sl)
        loaded = load_user_shopping_list(self.USERNAME)

        self.assertEqual(len(loaded.items), 1)
        self.assertEqual(loaded.items[0].name, "Milk")

    def test_load_missing_user_book_returns_default(self):
        """Missing user book should return an empty book."""
        loaded = load_user_book("unknown_user")
        self.assertIsInstance(loaded, Book)
        self.assertEqual(len(loaded.dishes), 0)


if __name__ == "__main__":
    unittest.main()

