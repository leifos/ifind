__author__ = 'leif'

from query_generation import QueryGeneration, SingleQueryGeneration, BiTermQueryGeneration
import unittest
import logging
import sys


class TestQueryGeneration(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestQueryGeneration")
        self.qg = QueryGeneration(minlen = 4)

    def test_extract_queries_from_text(self):
        self.logger.debug("Test Extract Queries")
        text = 'the good hello!'
        expected = ['good','hello']
        actual = self.qg.extract_queries_from_text(text)
        self.assertItemsEqual(expected, actual)

    def test_extract_queries_from_html(self):
        self.logger.debug("Test Extract Queries from HTML")
        html = '<HTML><b>Test</b> <h1>Extract</h2> Queries</HTML>'
        expected = ['test','extract', 'queries']
        actual = self.qg.extract_queries_from_html(html)
        self.assertItemsEqual(expected, actual)


class TestSingleQueryGeneration(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestQueryGeneration")
        self.qg = SingleQueryGeneration(minlen = 4)

    def test_extract_queries_from_html(self):
        self.logger.debug("Extraction of Single (non) duplicate queries")
        html = '<HTML><b>Test</b> <h1>Extract</h2> Queries <b>Test</b> <h1>Extract</h2></HTML>'
        expected = ['test','extract', 'queries']
        actual = self.qg.extract_queries_from_html(html)
        self.assertItemsEqual(expected, actual)

        counts = {'test':2, 'extract': 2, 'queries':1}
        self.assertItemsEqual(self.qg.query_count, counts)


class TestBiTermQueryGeneration(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestQueryGeneration")
        self.qg = BiTermQueryGeneration(minlen = 4)

    def test_extract_queries_from_html(self):
        self.logger.debug("Extraction of BiTerm (non) duplicate queries")
        html = '<HTML><b>Test</b> <h1>Extract</h2> Queries <b>Test</b> <h1>Extract</h2></HTML>'
        expected = ['test extract','extract queries', 'queries test']
        actual = self.qg.extract_queries_from_html(html)
        self.assertItemsEqual(expected, actual)

        counts = {'test extract':2, 'extract queries': 1, 'queries test':1}
        self.assertItemsEqual(self.qg.query_count, counts)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestQueryGeneration").setLevel(logging.DEBUG)
    unittest.main(exit=False)