__author__ = 'rose'
import unittest
import logging
import sys
from structured_query_extraction import StructuredExtractor

class TestStructuredExtractor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStructuredExtractor")
        html = ' <html> <div id="header"><h1>hello world</h1>' \
               '</div><div id="content">this is important</div>' \
               '<div id="footer"> <h2>byes</h2></div> </html> '
        self.extractor = StructuredExtractor(html=html)

    def test_get_node_content(self):
        #test getting text for h1
        tag = 'h1'
        expected = 'hello world'
        result = self.extractor.get_node_content(tag)
        self.process_test_equals(expected,result)
        #test getting text within first div
        tag = 'div'
        expected = ''
        result = self.extractor.get_node_content(tag)
        self.process_test_equals(expected,result)

    def test_get_div_content(self):
        div_id="header"
        expected = 'hello world'
        result = self.extractor.get_div_content(div_id)
        self.process_test_equals(expected,result)

    def test_remove_div_content(self):
        div_id=["header"]
        expected = "this is important byes"
        result = self.extractor.remove_div_content(div_id)
        self.process_test_equals(expected,result)
        div_id=["content"]
        expected = "hello world byes"
        result = self.extractor.remove_div_content(div_id)
        self.process_test_equals(expected,result)
        #test multiple div removal
        ignore_divs = ['header','footer']
        result = self.extractor.remove_div_content(ignore_divs)
        expected = 'this is important'
        self.process_test_equals(expected, result)

    # def test_get_related_text(self):
    #     result = self.extractor.get_all_related_text()
    #     expected = {'h1':'hello world','div':'this is important','h2':'byes'}
    #     self.assertDictEqual(result,expected)


    def process_test_equals(self, expected, result):
        msg = 'expected  but got ', expected,result
        self.assertItemsEqual(expected, result, msg)

    # def test_create_biterm_queries(self):
    #     result = self.extractor.create_biterm_queries()
    #     expected = ['hello world', 'this important']
    #     self.process_test_equals(expected,result)

    def test_read_html(self):
        self.extractor.read_html()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestStructuredExtractor").setLevel(logging.DEBUG)
    unittest.main(exit=False)