"""
An abstract class to generate queries list
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
ONLY_ALPHAS = False #bool to distinguish if only considering alphanumeric terms
AVOID_STOP = False #bool to distinguish if avoiding terms on the stop list
MIN_LENGTH = 1 # the minimum length of a term, if =1 then no min length

from string import rsplit
from collections import Counter
from re import sub
from nltk import clean_html, regexp_tokenize

class QueryGeneration(object):
    """
    Abstract class to represent structure for a query generator
    """

    def __init__(self, stopwordfile = None, minlen = 3):
        """
        constructor for QueryGeneration
        """
        self.min_len = minlen
        self.stoplist = []
        self.read_stopwordfile(stopwordfile)


    def read_stopwordfile(self, stopwordfile):
        if stopwordfile:
            stopwords = open('stopwords.txt').readlines()
            self.stoplist = []
            for term in stopwords:
                self.stoplist.append(term.strip())

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

        #TODO(leifos): This could be implemented better as a configurable pipeline
        text = text.lower()
        text = text.split()
        cleaned = []
        for term in text:
            # lower case
            print term
            term = self.check_length(term)
            if term:
                term = self.remove_punctuation(term)
                if term:
                    term = self.remove_stopwords(term)
                    if term:
                        term = self.is_alphanumeric(term)
                        if term:
                            cleaned.append(term)
            print term
        return cleaned


    def check_length(self, term):
        """
        :param term: takes a term
        :return: returns the term, if it meets the minimum length criteria
        """
        if len(term) >= self.min_len:
            return term
        else:
            return None

    def is_alphanumeric(self, term):
        if term.isalpha():
            return term
        else:
            return None

    def remove_punctuation(self, term):
        """remove punctation surrounding a term
        :param term:
        :return: term without punctation
        """
        #get the last character
        #is there a possibility multiple punctuation at start and end?
        length = len(term)
        firstChar = term[0:1]
        if str(firstChar).isalnum():
            term = term
        else:
            #print "cutting first letter " + firstChar + " from " +term
            term = term[1:length]
            #print "term now " +term
        #get length again incase punctuation at start and end
        length = len(term)
        lastChar = term[length-1:length]
        if str(lastChar).isalnum():
            term = term
        else:
            #print "cutting last letter " + lastChar + "from " + term
            term = term[0:length-1]
            #print " is now " + term

        #now check if there's nothing left, then don't add, if there is, add it
        if term:
            return term
        else:
            return None

    def remove_stopwords(self, term):
        #stopwords list from http://www.ranks.nl/resources/stopwords.html
        #can easily be switched
        if term in self.stoplist:
            return None
        else:
            return term


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


