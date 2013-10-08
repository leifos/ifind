__author__ = 'rose'
import unittest
import logging
import sys
from position_content_extractor import PositionContentExtractor
from pagecapture import PageCapture

class TestPositionExtractor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStructuredExtractor")
        html = ' <html> <div id="header"><h1>hello world</h1>' \
               '</div><div id="content"><p>this is important</p>' \
               '<p> study computing it is fun</p></div>' \
               '<div id="footer"> <h2>byes</h2></div> </html> '
        div_ids=[]
        self.extractor = PositionContentExtractor(div_ids=div_ids)
        self.extractor.process_html_page(html)

    def test_remove_div_content(self):

        div_id=["header"]
        self.extractor.set_div_ids(div_id)
        expected = "this is important study computing it is fun byes"

        self.process_test_equals(expected, self.extractor.text)

        div_id=["content"]
        expected = "hello world byes"
        self.extractor.set_div_ids(div_id)

        self.process_test_equals(expected, self.extractor.text)
        #test multiple div removal
        ignore_divs = ['header','footer']
        self.extractor.set_div_ids(ignore_divs)

        expected = 'this is important study computing it is fun'
        self.process_test_equals(expected, self.extractor.text)

    def test_get_subtext(self):
        self.extractor.text = "this is a sentence which has some words in it"
        result = self.extractor.get_subtext(num_words=2)
        expected = "this is"
        self.process_test_equals(expected,result)
        #test greater than length returns whole text
        result = self.extractor.get_subtext(num_words=12)
        self.process_test_equals(self.extractor.text, result)


    def process_test_equals(self, expected, result):
        msg = 'Expected but got: ', expected, result
        self.assertItemsEqual(expected, result, msg)



class WebTestPositionExtractor(unittest.TestCase):

    def setUp(self):
        """
        Setting up test on offensive page
        """
        self.logger = logging.getLogger("TestStructuredExtractor")
        pc = PageCapture('https://www.gov.uk/vehicles-you-can-drive')
        html = pc.get_page_sourcecode()

        #from BeautifulSoup import BeautifulSoup
        #soup = BeautifulSoup(html)
        #texts = soup.findAll(text=True)
        #print texts


    def test_extract_from_bad_page(self):
        #text = self.extractor.get_subtext()

        #self.assertGreater(len(text),0)
        pass


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestPositionExtractor").setLevel(logging.DEBUG)
    unittest.main(exit=False)

