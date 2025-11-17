"""
Unit tests for the authentication module.
"""

import shutil
import unittest

from cookit.auth import authenticate, register_user
from cookit.storage import DB_DIR


class TestAuth(unittest.TestCase):
    """Tests for user authentication and registration."""

    def setUp(self):
        if DB_DIR.exists():
            shutil.rmtree(DB_DIR)

    def tearDown(self):
        if DB_DIR.exists():
            shutil.rmtree(DB_DIR)

    def test_register_and_authenticate_user(self):
        """Register a user and ensure authentication works."""
        user = register_user("alice", "password123")
        self.assertEqual(user.username, "alice")

        authenticated = authenticate("alice", "password123")
        self.assertIsNotNone(authenticated)
        self.assertEqual(authenticated.username, "alice")

    def test_duplicate_registration_fails(self):
        """Registering the same username twice should raise ValueError."""
        register_user("bob", "secret")
        with self.assertRaises(ValueError):
            register_user("bob", "another")

    def test_invalid_credentials(self):
        """Authentication should fail for wrong passwords."""
        register_user("carol", "safe")
        self.assertIsNone(authenticate("carol", "wrong"))
        self.assertIsNone(authenticate("unknown", "safe"))


if __name__ == "__main__":
    unittest.main()

