__author__ = 'leif'

from simulator import User, StartScreen, ResultScreen, DocScreen
import unittest
import logging
import sys


class TestUser(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestUser")
        self.user = User()


    def test_screen(self):

        query = self.user.select_next_action(StartScreen())
        self.assertItemsEqual(query, (1, 'hello'))

        query = self.user.select_next_action(StartScreen())
        self.assertItemsEqual(query, (1, 'goodbye'))



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestUser").setLevel(logging.DEBUG)
    unittest.main(exit=False)