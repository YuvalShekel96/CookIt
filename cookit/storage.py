"""
Storage module for CookIT.

Provides JSON-based persistence for books, supermarkets, and shopping lists.
"""

import json
from pathlib import Path
from typing import List, Optional

from cookit.book import Book
from cookit.shopping_list import ShoppingList
from cookit.supermarket import Supermarket


# Default database directory
DB_DIR = Path("db")
USERS_DIR = DB_DIR / "users"


def _ensure_db_dir() -> None:
    """Ensure the database directory exists."""
    DB_DIR.mkdir(exist_ok=True)


def _ensure_users_dir() -> None:
    """Ensure the users subdirectory exists."""
    _ensure_db_dir()
    USERS_DIR.mkdir(exist_ok=True)


def _sanitize_value(value: str) -> str:
    """Sanitize arbitrary strings for filenames."""
    safe = "".join(c for c in value if c.isalnum() or c in (" ", "-", "_")).strip()
    return safe.replace(" ", "_")


def _sanitize_username(username: str) -> str:
    """Sanitize usernames for filenames."""
    username = username.strip()
    return _sanitize_value(username.lower() or "user")


def _user_file(username: str, suffix: str) -> Path:
    """Generate a per-user file path for a given suffix."""
    _ensure_users_dir()
    safe_username = _sanitize_username(username)
    return USERS_DIR / f"{safe_username}_{suffix}"


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


def save_shopping_list(shopping_list: ShoppingList, name: str, username: str) -> None:
    """
    Save a shopping list to JSON file.
    
    Args:
        shopping_list: ShoppingList instance to save
        name: Name identifier for the shopping list (used as filename)
    """
    _ensure_users_dir()
    safe_name = _sanitize_value(name)
    file_path = _user_file(username, f"shopping_list_{safe_name}.json")
    
    data = shopping_list.to_dict()
    data["name"] = name  # Store the original name
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_shopping_list(name: str, username: str) -> Optional[ShoppingList]:
    """
    Load a shopping list from JSON file.
    
    Args:
        name: Name identifier of the shopping list
        
    Returns:
        ShoppingList instance if file exists, None otherwise
    """
    safe_name = _sanitize_value(name)
    file_path = _user_file(username, f"shopping_list_{safe_name}.json")
    
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ShoppingList.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading shopping list: {e}")
        return None


def list_shopping_lists(username: str) -> List[str]:
    """
    List all saved shopping list names.
    
    Returns:
        List of shopping list names
    """
    if not USERS_DIR.exists():
        return []
    safe_username = _sanitize_username(username)
    shopping_lists = []
    for file_path in USERS_DIR.glob(f"{safe_username}_shopping_list_*.json"):
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


def save_user_book(username: str, book: Book) -> None:
    """Save a user's recipe book."""
    file_path = _user_file(username, "book.json")
    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(book.to_dict(), fh, indent=2, ensure_ascii=False)


def load_user_book(username: str) -> Book:
    """Load a user's recipe book (returns empty book if missing)."""
    file_path = _user_file(username, "book.json")
    if not file_path.exists():
        return Book(f"{username}'s Book")
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return Book.from_dict(data)
    except (json.JSONDecodeError, KeyError):
        return Book(f"{username}'s Book")


def save_user_shopping_list(username: str, shopping_list: ShoppingList) -> None:
    """Persist the current shopping list for a user."""
    file_path = _user_file(username, "shopping_list.json")
    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(shopping_list.to_dict(), fh, indent=2, ensure_ascii=False)


def load_user_shopping_list(username: str) -> ShoppingList:
    """Load the current shopping list for a user."""
    file_path = _user_file(username, "shopping_list.json")
    if not file_path.exists():
        return ShoppingList()
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return ShoppingList.from_dict(data)
    except (json.JSONDecodeError, KeyError):
        return ShoppingList()

