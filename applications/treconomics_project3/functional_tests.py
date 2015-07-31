__author__ = 'mickeypash'
import unittest
from selenium import webdriver


class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.close()

    def test_home_page(self):
        self.browser = webdriver.Safari()
        self.browser.get('http://localhost:8000')
        self.assertIn('NewsSearch', self.browser.title)
        print 'Test passes'


if __name__ == '__main__':
    unittest.main()