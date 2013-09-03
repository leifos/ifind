__author__ = 'rose'

from query_ranker import QueryRanker
import unittest
import logging
import sys

class TestQueryRanker(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestQueryRanker")
        self.ranker = QueryRanker()

    def test_populate_crawl_dict(self):
        self.logger.debug("Test Populate Crawl Dict")
        self.ranker.populate_crawl_dict('term_occurrences.txt')

        #check it's not null and contains the following
        #hello 10
        #world 20
        #goodbye 10
        expected = {'hello' : 10, 'world' : 20, 'goodbye':10}
        self.assertDictEqual(self.ranker.crawl_dict,expected)

    def test_get_times_in_crawlfile(self):
        self.logger.debug("Test Get Times in Crawl File")
        self.ranker.populate_crawl_dict('term_occurrences.txt')
        hello_count=self.ranker.get_times_in_crawlfile('hello')
        hello_expected=10
        self.assertEquals(hello_count,hello_expected)

    def test_get_total_crawl_occurrences(self):
        self.logger.debug("Test Get Total Crawl Occurrences")
        self.ranker.populate_crawl_dict('term_occurrences.txt')
        expected_total=40
        actual_total=self.ranker.get_total_crawl_occurrences()
        self.assertEquals(expected_total,actual_total)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestQueryRanker").setLevel(logging.DEBUG)
    unittest.main(exit=False)

