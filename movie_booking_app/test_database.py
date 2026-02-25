import unittest
import uuid
from database import register_user, login_user, create_tables

class TestDatabase(unittest.TestCase):

    def setUp(self):
        create_tables()  

    def test_register_user(self):
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        result = register_user(username, "1234")
        self.assertTrue(result)

    def test_login_user(self):
        username = f"tempuser_{uuid.uuid4().hex[:8]}"
        register_user(username, "pass")
        user = login_user(username, "pass")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], username)

    def test_empty_credentials_rejected(self):
        self.assertFalse(register_user("", "pass"))
        self.assertFalse(register_user("user", ""))
        self.assertIsNone(login_user("", "pass"))
        self.assertIsNone(login_user("user", ""))

if __name__ == "__main__":
    unittest.main()
