import unittest
from app.models import User


class UserTest(unittest.TestCase):
    """Test case for user model"""

    def setUp(self):
        """Set up for user model instance"""
        self.user = User(username="smith", password="hello")

    def test_password_setter(self):
        """ Test password_setter test case to check password hashing and if the hashed password exists"""

        self.assertTrue(self.user.hashed_password is not None)

    def test_access_password(self):
        """ Test access password test case for checking if it raises AttributeError when trying to access the password"""
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
        """Test password verification to check if the hashed password can be verified"""
        self.assertTrue(self.user.verify_password('hello'))


# if __name__ == '__main__':
#     unittest.main()
