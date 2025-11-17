"""
Authentication utilities for CookIT.

Handles user registration, authentication, and persistence.
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, List

from cookit.storage import DB_DIR, _ensure_db_dir


USERS_FILE = DB_DIR / "users.json"


@dataclass
class User:
    """Represents an application user."""

    username: str
    password_hash: str
    delivery_address: str = ""
    enabled_supermarkets: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert the user to a serializable dictionary."""
        return {
            "password_hash": self.password_hash,
            "delivery_address": self.delivery_address,
            "enabled_supermarkets": self.enabled_supermarkets,
        }

    @classmethod
    def from_dict(cls, username: str, data: dict) -> "User":
        """Create a user from stored data."""
        return cls(
            username=username,
            password_hash=data.get("password_hash", ""),
            delivery_address=data.get("delivery_address", ""),
            enabled_supermarkets=data.get("enabled_supermarkets", []),
        )


def _hash_password(password: str) -> str:
    """Return a SHA256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> Dict[str, User]:
    """Load all users from disk."""
    _ensure_db_dir()
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return {username: User.from_dict(username, data) for username, data in raw.items()}


def save_users(users: Dict[str, User]) -> None:
    """Persist all users to disk."""
    _ensure_db_dir()
    USERS_FILE.parent.mkdir(exist_ok=True)
    data = {username: user.to_dict() for username, user in users.items()}
    with open(USERS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def save_user(user: User) -> None:
    """Persist a single user record."""
    users = load_users()
    users[user.username] = user
    save_users(users)


def get_user(username: str) -> Optional[User]:
    """Retrieve a user by username."""
    users = load_users()
    return users.get(username)


def register_user(username: str, password: str) -> User:
    """
    Register a new user.

    Raises:
        ValueError: If username/password invalid or username exists.
    """
    username = username.strip()
    if not username:
        raise ValueError("Username cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")

    users = load_users()
    if username in users:
        raise ValueError("Username already exists.")

    user = User(username=username, password_hash=_hash_password(password))
    users[username] = user
    save_users(users)
    return user


def authenticate(username: str, password: str) -> Optional[User]:
    """Authenticate a user by username/password."""
    if not username or not password:
        return None
    user = get_user(username.strip())
    if user and user.password_hash == _hash_password(password):
        return user
    return None

