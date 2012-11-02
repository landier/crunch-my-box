import unittest
from mail.service.grabber import Grabber

class GrabberTestCase(unittest.TestCase):
    def test_something(self):
        grabber = Grabber()
        self.assertIsNotNone(grabber)

if __name__ == '__main__':
    unittest.main()
