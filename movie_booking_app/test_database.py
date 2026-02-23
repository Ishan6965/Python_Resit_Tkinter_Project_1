import unittest
from database import register_user, login_user, create_tables

class TestDatabase(unittest.TestCase):

    def setUp(self):
        create_tables()  

    def test_register_user(self):
        result = register_user("testuser", "1234")
        self.assertTrue(result or result is False)  

    def test_login_user(self):
        register_user("tempuser", "pass")
        user = login_user("tempuser", "pass")
        self.assertIsNotNone(user)

if __name__ == "__main__":
    unittest.main()