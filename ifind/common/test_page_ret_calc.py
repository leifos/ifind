__author__ = 'rose'
from page_retrievability_calc import PageRetrievabilityCalculator
import unittest
import logging
import sys
from ifind.search.engine import EngineFactory

class TestPageRetCalc(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestPageRetCalc")
        #currently engine set to govuk, may need to change this
        self.engine = EngineFactory(engine="govuk")
        #url may need to be changed
        self.url = "https://www.gov.uk/renew-adult-passport"
        self.pg_calc= PageRetrievabilityCalculator(engine=self.engine)

    def test_populate_crawl_dict(self):
        print "hello"
        self.logger.debug("Test Populate Crawl Dict")
        from os import getcwd
        cwd="cwd:", getcwd()
        self.logger.debug(cwd)
        self.pg_calc.populate_crawl_dict('common/term_occurrences.txt')

        #check it's not null and contains the following
        #hello 10
        #world 20
        #goodbye 10
        expected = {'hello' : 10, 'world' : 20, 'goodbye':10}
        self.assertDictEqual(self.pg_calc.crawl_dict,expected)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestPageRetCalc").setLevel(logging.DEBUG)
    unittest.main(exit=False)