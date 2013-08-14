"""
A class which inherits from QueryGeneration to generate queries list of single terms
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
from querygeneration import QueryGeneration
from string import rsplit
from collections import Counter
from re import sub
from nltk import clean_html

class SingleTermQueryGeneration(QueryGeneration):
    """
    Implementation of QueryGeneration which generates single term queries
    """
    def __init__(self):
        pass

    def extract_queries_from_html(self, html):
        """

        :param htmlContent: the html from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #first get the text from the html
        #make sure only single white spaces remain

        content = clean_html(html)
        content = ' '.join(content.split())

        return self.extract_queries_from_text(content)


    def extract_queries_from_text(self, text):
        """
        takes a string of text from which to extract single term queries
        :type text: object
        :param text: the text from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #split into single words and store in a set so no duplicates
        #uses string.rsplit instead of str.split so a unicode object
        #from pagecaputre.getpage can be split as needed
        single_terms = rsplit(text)

        single_terms = self.clean_text(single_terms)
        #remove '' which is generated as space is at position 1 and at end
        #http://stackoverflow.com/questions/2197451/why-are-empty-strings-returned-in-split-results
        single_terms = filter(None, single_terms)
        return single_terms

    def clean_text(self, text):
        text = self.remove_punctuation(text)
        text =self.lower(text)
        text = self.min_length(text)
        text=self.remove_stopwords(text)
        #queryTerms = self.calculateDuplicates(queryTerms)
        #cast to a set to remove duplicates then back to a list
        return list(set(text))

    def lower(self, text):
        text = [str.lower(term) for term in text]
        return text

    def min_length(self,text, min_len=3):
        new_text = []
        for term in text:
            if len(term) > min_len:
                new_text.append(term)
        return new_text

    def remove_punctuation(self, text):
        cleaned = []
        print "cleaning up search terms, removing punctuation from first and last positions etc. at end of terms "

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

