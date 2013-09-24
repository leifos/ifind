"""
An abstract class to generate queries list
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
ONLY_ALPHAS = False #bool to distinguish if only considering alphanumeric terms
AVOID_STOP = False #bool to distinguish if avoiding terms on the stop list
#MIN_LENGTH = 1 # the minimum length of a term, if =1 then no min length

from string import rsplit
from collections import Counter
from re import sub
from nltk import clean_html, regexp_tokenize
from pipeline import TermPipeline

class QueryGeneration(object):
    """
    Abstract class to represent structure for a query generator
    """

    def __init__(self, stopwordfile = None, minlen = 3, maxsize = 250):
        """
        constructor for QueryGeneration
        """
        self.min_len = minlen
        self.max_size = maxsize
        self.stop_filename = stopwordfile

    def extract_queries_from_html(self, html):
        """
        :param url: the html from which the queries are to be constructed
        :return: list of queries
        """
        content = clean_html(html)
        content = ' '.join(content.split())
        return self.extract_queries_from_text(content)

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """
        query_list = self.clean_text(text)
        return query_list

    def clean_text(self, text):
        """ normalizes the text
        :param text: a string of text, to be cleaned.
        :return: a list of terms (i.e. tokenized)
        """
        text = text.lower()
        text = text.split()
        cleaned = []

        for term in text:
            cleaner_pipeline = TermPipeline(term, minlength=self.min_len, stopfile=self.stop_filename)
            clean_result = cleaner_pipeline.perform_checks()
            if clean_result:
                cleaned.append(clean_result)
        #still need to deal with character encoding issues
        l = len(cleaned)
        if l > self.max_size:
            return cleaned[0:self.max_size]
        else:
            return cleaned

    def get_doc_term_counts(self, query_list):
        """
        for use in query ranker, for each term calculate number of occurrences
        in the document,
        :return dict of term, occurrence pairs
        """
        count_dict = {}
        for term in query_list:
            if term in count_dict:
                count_dict[term]+=1
            else:
                count_dict[term]=1
        return count_dict


class SingleQueryGeneration(QueryGeneration):

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """
        term_list = self.clean_text(text)
        self.query_count = {}

        for query in term_list:
            if query in self.query_count:
                self.query_count[query] = self.query_count[query] + 1
            else:
                self.query_count[query] = 1
        query_list = []
        for key in self.query_count:
            query_list.append(key)

        return query_list


class BiTermQueryGeneration(QueryGeneration):

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """
        term_list = self.clean_text(text)

        self.query_count = {}

        prev_term = term_list[0]

        term_list= term_list[1:len(term_list)]

        for term in term_list:
            query = prev_term + ' ' + term
            if query in self.query_count:
                self.query_count[query] = self.query_count[query] + 1
            else:
                self.query_count[query] = 1

            prev_term = term

        query_list = []
        for key in self.query_count:
            query_list.append(key)

        return query_list


class TriTermQueryGeneration(QueryGeneration):

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """
        term_list = self.clean_text(text)

        self.query_count = {}

        prev_prev_term = term_list[0]
        prev_term = term_list[1]

        term_list= term_list[2:len(term_list)]

        for term in term_list:
            query = prev_prev_term + ' ' +prev_term + ' ' + term
            if query in self.query_count:
                self.query_count[query] = self.query_count[query] + 1
            else:
                self.query_count[query] = 1

            prev_prev_term = prev_term
            prev_term = term


        query_list = []
        for key in self.query_count:
            query_list.append(key)

        return query_list
