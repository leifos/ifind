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

    # Onika starts the experiment by entering her u: test12 and p: 12
    def test_user_login(self):
        self.browser = webdriver.Safari()
        self.browser.get('http://localhost:8000/startexperiment')
        self.assertIn('test12', self.browser.find_elements_by_id())

    # She presses Login, a new page is opened!
    def test_login_button(self):
        pass

    def test_instructions_page(self):
        pass

    # She reads the instructions provided and presses Next
    # She reads the Practice Task instructions and presses Next

    # She presses Show Task
    # She closes the new window after reading the task

    # She enters relevant query terms and presses Search
    # She hovers over the first few results and selects one
    # She decides to Mark it as Relevant
    # She decides to View Saved
    # She decides to go Back to Results
    # She decides to End Task
    # She reads the short debrief and presses Next


if __name__ == '__main__':
    unittest.main()