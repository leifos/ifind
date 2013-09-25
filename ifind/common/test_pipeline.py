#!/usr/bin/python
# -*- coding: latin-1 -*-
__author__ = 'rose'
from pipeline import PunctuationTermProcessor, AlphaTermProcessor, StopwordTermProcessor
from pipeline import LengthTermProcessor, TermPipeline, TermProcessor, SpecialCharProcessor
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
        self.sctp = SpecialCharProcessor()



        self.pipeline = TermPipeline()
        self.pipeline.add_processor(self.sctp)
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

        def test_process():
            #test removal of punctuation, numbers, special characters
            #other cases are tested in test_query_gen where the clean
            #method which uses the pipeline process method is tested
            term = 'hello WORlD. my name  is Python111!!! ü'
            expected = 'hello world my name is python '
            result = self.pipeline.process(term)
            self.assertEquals(expected,result)

        def test_processors_config_order():
            #todo this is to see the impact of adding processors in
            #different orders
            pass

class TestLengthTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestLengthTermProcessor")
        self.term = 'hi'
        self.minlen=3
        self.ltp= LengthTermProcessor()

    def test_set_minlen(self):
        #check -ve num returns current min len
        min_len = self.ltp.min_len
        self.ltp.set_min_length(-1)
        result = self.ltp.min_len
        self.assertEquals(result,min_len)
        #check 0 returns current min_len

        self.ltp.set_min_length(0)
        result = self.ltp.min_len
        self.assertEquals(result,min_len)

        #now check >0
        self.ltp.set_min_length(4)
        result = self.ltp.min_len
        self.assertEquals(result,4)

    def test_check(self):
        result = self.ltp.process('a')
        self.assertEquals(result,None)

class TestPunctTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestPunctuationTermProcessor")
        self.ptp = PunctuationTermProcessor()

    def test_check(self):
        #check removing ' ' ' the '
        result = self.ptp.process(' the ')
        self.assertEquals(result, 'the')
        #check removing . at end 'hello.'

        result = self.ptp.process('hello.')
        self.assertEquals(result, 'hello')
        #check removing ! and %
        result = self.ptp.process('!good%')
        self.assertEquals(result, 'good')

class TestStopwordTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestStopwordTermProcessor")
        self.stp = StopwordTermProcessor(stopwordfile='stopwords_test.txt')

    def test_check(self):
        #test return None for term in list
        in_list= 'myself'
        result = self.stp.process(in_list)
        self.assertEquals(result, None)

        #test return None for term in list
        in_list= 'against'
        result = self.stp.process(in_list)
        self.assertEquals(result, None)
        #test return term for term not in list

        non_list='sport'
        result = self.stp.process(non_list)
        self.assertEquals(result, non_list)


class TestAlphaTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestAlphaTermProcessor")
        self.atp = AlphaTermProcessor()

    def test_check(self):

        result = self.atp.process('<h>')
        self.assertEquals(result, None)
        #check neg numbers

        result = self.atp.process('-5')
        self.assertEquals(result, None)

        #check pos numbers
        result = self.atp.process('5')
        self.assertEquals(result, None)
        #check punct
        result = self.atp.process('hello.')
        self.assertEquals(result, None)

class TestSpecialCharTermProcessor(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("TestSpecialCharTermProcessor")
        self.sctm = SpecialCharProcessor()

    def test_check(self):
        #check inclusion of special character is removed
        expected='hi'
        result = self.sctm.process('±hi')
        self.assertEquals(expected,result)
        #check spaces aren't removed
        expected='hi hello'
        result = self.sctm.process(expected)
        self.assertEquals(expected,result)
        #check special char and spaces
        testline = 'ähello my friend'
        expected = 'hello my friend'
        result = self.sctm.process(testline)
        self.assertEquals(expected, result)





if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestTermPipeline").setLevel(logging.DEBUG)
    unittest.main(exit=False)