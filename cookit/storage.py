"""
Storage module for CookIT.

Provides JSON-based persistence for books, supermarkets, and shopping lists.
"""

import json
import os
from pathlib import Path
from typing import List, Optional
from cookit.book import Book
from cookit.supermarket import Supermarket
from cookit.shopping_list import ShoppingList


# Default database directory
DB_DIR = Path("db")


def _ensure_db_dir() -> None:
    """Ensure the database directory exists."""
    DB_DIR.mkdir(exist_ok=True)


def save_book(book: Book) -> None:
    """
    Save a book to JSON file.
    
    Args:
        book: Book instance to save
    """
    _ensure_db_dir()
    file_path = DB_DIR / "book.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(book.to_dict(), f, indent=2, ensure_ascii=False)


def load_book() -> Optional[Book]:
    """
    Load a book from JSON file.
    
    Returns:
        Book instance if file exists, None otherwise
    """
    file_path = DB_DIR / "book.json"
    
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Book.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading book: {e}")
        return None


def save_supermarkets(supermarkets: List[Supermarket]) -> None:
    """
    Save a list of supermarkets to JSON file.
    
    Args:
        supermarkets: List of Supermarket instances to save
    """
    _ensure_db_dir()
    file_path = DB_DIR / "supermarkets.json"
    
    data = [supermarket.to_dict() for supermarket in supermarkets]
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_supermarkets() -> List[Supermarket]:
    """
    Load supermarkets from JSON file.
    
    Returns:
        List of Supermarket instances (empty list if file doesn't exist)
    """
    file_path = DB_DIR / "supermarkets.json"
    
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Supermarket.from_dict(sm_data) for sm_data in data]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading supermarkets: {e}")
        return []


def save_shopping_list(shopping_list: ShoppingList, name: str) -> None:
    """
    Save a shopping list to JSON file.
    
    Args:
        shopping_list: ShoppingList instance to save
        name: Name identifier for the shopping list (used as filename)
    """
    _ensure_db_dir()
    # Sanitize name for filename
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_name = safe_name.replace(" ", "_")
    
    file_path = DB_DIR / f"shopping_list_{safe_name}.json"
    
    data = shopping_list.to_dict()
    data["name"] = name  # Store the original name
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_shopping_list(name: str) -> Optional[ShoppingList]:
    """
    Load a shopping list from JSON file.
    
    Args:
        name: Name identifier of the shopping list
        
    Returns:
        ShoppingList instance if file exists, None otherwise
    """
    # Sanitize name for filename
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_name = safe_name.replace(" ", "_")
    
    file_path = DB_DIR / f"shopping_list_{safe_name}.json"
    
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ShoppingList.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading shopping list: {e}")
        return None


def list_shopping_lists() -> List[str]:
    """
    List all saved shopping list names.
    
    Returns:
        List of shopping list names
    """
    if not DB_DIR.exists():
        return []
    
    shopping_lists = []
    for file_path in DB_DIR.glob("shopping_list_*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "name" in data:
                    shopping_lists.append(data["name"])
                else:
                    # Fallback: extract name from filename
                    name = file_path.stem.replace("shopping_list_", "")
                    shopping_lists.append(name)
        except (json.JSONDecodeError, KeyError):
            continue
    
    return shopping_lists

