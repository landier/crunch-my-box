import unittest
from grabber.email_document import Email

class EmailTestCase(unittest.TestCase):
    def test_repr(self):
        email = Email(7, "This is my subject")
        self.assertEqual("7: This is my subject", email.__repr__())

if __name__ == '__main__':
    unittest.main()
