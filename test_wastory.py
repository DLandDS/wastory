import unittest
from unittest import TestCase


class Test(TestCase):
    def test_video1(self):
        from wastory import main
        self.assertTrue(main("example.mp4"))


if __name__ == '__main__':
    unittest.main()
