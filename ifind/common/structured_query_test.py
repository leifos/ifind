__author__ = 'rose'
import unittest
import logging
import sys
from structured_query_extraction import StructuredExtractor

class TestStructuredExtractor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStructuredExtractor")
        html = '<html> <h1>hello world</h1> <h2>byes</h2> </html>'
        self.extractor = StructuredExtractor(html=html)

    def test_get_content(self):
        tag = 'h1'
        expected = '<h1>hello world</h1>'
        result = self.extractor.get_content(tag)
        msg = 'expected  but got ' , expected,result
        self.assertItemsEqual(expected, result, msg)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestStructuredExtractor").setLevel(logging.DEBUG)
    unittest.main(exit=False)