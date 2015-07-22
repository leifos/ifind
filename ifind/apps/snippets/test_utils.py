__author__ = 'mickeypash'
import unittest
import utils
import test

# TODO consider using py.test or nose


class TestSnippetUtilities(unittest.TestCase):

    def test_remove_stopwords(self):
        snippet = 'The town in the states'
        filtered_snippet = ['town', 'states']
        self.assertItemsEqual(utils.remove_stopwords(snippet),
                              actual_seq=filtered_snippet,
                              msg='Removed stop words')


if __name__ == '__main__':
    unittest.main()