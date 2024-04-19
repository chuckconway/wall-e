import unittest

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MyTestCase(unittest.TestCase):
    def test_something(self):
        password = "Folsom_800"
        hashed_password = pwd_context.hash(password)

        print(hashed_password)


if __name__ == '__main__':
    unittest.main()
