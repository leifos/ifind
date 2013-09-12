__author__ = 'rose'
from pipeline import PunctuationTermProcessor, AlphaTermProcessor, StopwordTermProcessor
from pipeline import LengthTermProcessor, TermPipeline, TermProcessor
import unittest
import logging
import sys

class TestTermPipeline(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestTermPipeline")

        self.ltp = LengthTermProcessor()
        self.tp = TermProcessor()
        self.stp = StopwordTermProcessor(stopwordfile='stopwords_test.txt')
        self.ptp = PunctuationTermProcessor()
        self.atp = AlphaTermProcessor()


        self.pipeline = TermPipeline()
        self.pipeline.add_processor(self.tp)
        self.pipeline.add_processor(self.ltp)
        self.pipeline.add_processor(self.ptp)
        self.pipeline.add_processor(self.stp)
        self.pipeline.add_processor(self.atp)


    def test_read_stopfile(self):
        expected = ['accessibility', 'information', 'site', 'skip',
                    'main', 'content', 'a', 'about', 'above', 'after',
                    'again', 'against', 'all', 'am', 'an', 'and', 'any',
                    'are', "aren't", 'as', 'at', 'be', 'because', 'been',
                    'before', 'being', 'below', 'between', 'both', 'but',
                    'by', "can't", 'cannot', 'could', "couldn't", 'did',
                    "didn't", 'do', 'does', "doesn't", 'doing', "don't",
                    'down', 'during', 'each', 'few', 'for', 'from',
                    'further', 'had', "hadn't", 'has', "hasn't", 'have',
                    "haven't", 'having', 'he', "he'd", "he'll", "he's",
                    'her', 'here', "here's", 'hers', 'herself', 'him',
                    'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
                    "i'm", "i've", 'if', 'in', 'into', 'is', "isn't",
                    'it', "it's", 'its', 'itself', "let's", 'me', 'more',
                    'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not',
                    'of', 'off', 'on', 'once', 'only', 'or', 'other',
                    'ought', 'our', 'ours', 'ourselves', 'out', 'over',
                    'own', 'same', "shan't", 'she', "she'd", "she'll",
                    "she's", 'should', "shouldn't", 'so', 'some', 'such',
                    'than', 'that', "that's", 'the', 'their', 'theirs',
                    'them', 'themselves', 'then', 'there', "there's",
                    'these', 'they', "they'd", "they'll", "they're",
                    "they've", 'this', 'those', 'through', 'to', 'too',
                    'under', 'until', 'up', 'us', 'very', 'was', "wasn't",
                    'we', "we'd", "we'll", "we're", "we've", 'were',
                    "weren't", 'what', "what's", 'when', "when's", 'where',
                    "where's", 'which', 'while', 'who', "who's", 'whom',
                    'why', "why's", 'with', "won't", 'would', "wouldn't",
                    'you', "you'd", "you'll", "you're", "you've", 'your',
                    'yours', 'yourself', 'yourselves']
        self.assertEquals(expected,self.stp.stoplist)

class TestLengthTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestLengthTermProcessor")
        self.term = 'hi'
        self.minlen=3
        self.length_proc= LengthTermProcessor()

    def test_set_minlen(self):
        #check -ve num returns current min len
        min_len = self.length_proc.min_len
        self.length_proc.set_min_length(-1)
        result = self.length_proc.min_len
        self.assertEquals(result,min_len)
        #check 0 returns current min_len

        self.length_proc.set_min_length(0)
        result = self.length_proc.min_len
        self.assertEquals(result,min_len)

        #now check >0
        self.length_proc.set_min_length(4)
        result = self.length_proc.min_len
        self.assertEquals(result,4)

class TestPunctTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestPunctuationTermProcessor")
        self.punct_proc = PunctuationTermProcessor()

    def test_check(self):
        #check removing ' ' ' the '
        result = self.punct_proc.process(' the ')
        self.assertEquals(result, 'the')
        #check removing . at end 'hello.'

        result = self.punct_proc.process('hello.')
        self.assertEquals(result, 'hello')
        #check removing ! and %
        result = self.punct_proc.process('!good%')
        self.assertEquals(result, 'good')

class TestStopwordTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStopwordTermProcessor")
        self.stop_processor = StopwordTermProcessor(stopwordfile='stopwords_test.txt')

    def test_check(self):
        #test return None for term in list
        in_list= 'myself'
        result = self.stop_processor.process(in_list)
        self.assertEquals(result, None)

        #test return None for term in list
        in_list= 'against'
        result = self.stop_processor.process(in_list)
        self.assertEquals(result, None)
        #test return term for term not in list

        non_list='sport'
        result = self.stop_processor.process(non_list)
        self.assertEquals(result, non_list)


class TestAlphaTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestAlphaTermProcessor")
        self.alpha_processor = AlphaTermProcessor()

    def test_check(self):

        result = self.alpha_processor.process('<h>')
        self.assertEquals(result, None)
        #check neg numbers

        result = self.alpha_processor.process('-5')
        self.assertEquals(result, None)

        #check pos numbers
        result = self.alpha_processor.process('5')
        self.assertEquals(result, None)
        #check punct
        result = self.alpha_processor.process('hello.')
        self.assertEquals(result, None)



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestTermPipeline").setLevel(logging.DEBUG)
    unittest.main(exit=False)