
from smoothed_doc_language_model import SmoothedModel
import unittest
import logging
import sys

class TestSmoothedDocLanguageModel(unittest.TestCase):

    def setUp(self):
        self.model=SmoothedModel

    def test_calculate_likelihood(self):
        pass

    def test_calculate_laplace_likelihood(self):
        pass

    def test_calculate_JM_likelihood(self):
        pass

    def test_calculate_bayes_likelihood(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestSmoothedModel").setLevel(logging.DEBUG)
    unittest.main(exit=False)


