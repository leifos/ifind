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
from nltk import clean_html

class QueryGeneration(object):
    """
    Abstract class to represent structure for a query generator
    """

    def __init__(self, stoplist_filename=None):
        """
        constructor for QueryGeneration
        """

    def _extract_queries_from_html(self, html):
        """
        :param url: the html from which the queries are to be constructed
        :return: list of queries
        """

    def extract_queries_from_text(self, text):
        """
        :param text: the text from which the queries are to be constructed
        :return: list of queries
        """

    def clean_text(self, text):

        text = text.lower()
        list(set(nltk.regexp_tokenize(text, pattern, gaps=True)) - set(nltk.corpus.stopwords.words('english')))


        cleaned = []
        for term in text:
            # lower case
            term = term.lower()
            term = self.check_length(term)
            term = self.remove_punctuation(term)

        text= self.remove_stopwords(text)
        #queryTerms = self.calculateDuplicates(queryTerms)
        #cast to a set to remove duplicates then back to a list
        return list(set(text))




    def lower(self, text):
        text = [str.lower(term) for term in text]
        return text

    def check_length(self,text, min_len=3):
        if len(term) > min_len:
            return term
        else:
            return None

    def remove_punctuation(self, text):
        cleaned = []

        for term in text:
            #get the last character
            #is there a possibility multiple punctuation at start and end?
            length = str(term).__len__()
            firstChar = term[0:1]
            if str(firstChar).isalnum():
                term = term
            else:
                #print "cutting first letter " + firstChar + " from " +term
                term = term[1:length]
                #print "term now " +term
            #get length again incase punctuation at start and end
            length = str(term).__len__()
            lastChar = term[length-1:length]
            if str(lastChar).isalnum():
                term = term
            else:
                #print "cutting last letter " + lastChar + "from " + term
                term = term[0:length-1]
                #print " is now " + term

            #now check if there's nothing left, then don't add, if there is, add it
            if term:
                cleaned.append(term)

        return cleaned

    #at this stage queries is a counter object which can be treated as
    #a dictionary of unique query terms with a count of the number of occurrences
    #print queries

    def calculate_duplicates(self, text):
        terms = Counter(text)
        return terms

    def remove_stopwords(self, text):
        #stopwords list from http://www.ranks.nl/resources/stopwords.html
        #can easily be switched
        #todo(rose) doesn't seem to be working
        #TODO(leifos): a setter should take the filename of the stopword list and read it in
        tmp = open('stopwords.txt').readlines()
        stoplist = []

        for term in tmp:
            stoplist.append(term.strip())

        return list(set(text) - set(stoplist))
