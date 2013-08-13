"""
A class which inherits from QueryGeneration to generate queries list of single terms
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
from QueryGeneration import QueryGeneration
from string import rsplit
from collections import Counter
from re import sub

class SingleTermQueryGeneration(QueryGeneration):
    """
    Implementation of QueryGeneration which generates single term queries
    """
    def __init__(self):
        pass

    def extractQueriesFromHtml(self, htmlContent):
        """

        :param htmlContent: the html from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #first get the text from the html
        #doc = html.document_fromstring(htmlContent)
        #text = doc.text_content()

        #parser = htmlParser(htmlContent)
        #text = parser.getText()
        #now use extractQueries from text and return the list of queries
        #return self.extractQueriesFromText(text)
        return self.extractQueriesFromText(htmlContent)

    def extractQueriesFromText(self, text):
        """
        takes a string of text from which to extract single term queries
        :type text: object
        :param text: the text from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #split into single words and store in a set so no duplicates
        #uses string.rsplit instead of str.split so a unicode object
        #from pagecaputre.getpage can be split as needed
        singleTerms = rsplit(text)

        singleTerms = self.cleanTerms(singleTerms)
        #remove '' which is generated as space is at position 1 and at end
        #http://stackoverflow.com/questions/2197451/why-are-empty-strings-returned-in-split-results
        singleTerms = filter(None, singleTerms)
        return singleTerms

    def cleanTerms(self, queryTerms):
        queryTerms=self.removePunctuation(queryTerms)
        queryTerms =self.toLower(queryTerms)
        queryTerms=self.removeStopWords(queryTerms)
        #queryTerms = self.calculateDuplicates(queryTerms)
        #cast to a set to remove duplicates then back to a list
        return list(set(queryTerms))

    def toLower(self,queryTerms):
        queryTerms = [str.lower(query) for query in queryTerms]
        return queryTerms

    def removePunctuation(self, queryTerms):
        cleaned = []
        print "cleaning up search terms, removing commas etc. at end of terms "
        for query in queryTerms:
            #get the last character
            length = str(query).__len__()
            lastChar = query[length-1:length]
            if str(lastChar).isalnum() == False:
                query = query[0:length-1]
            cleaned.append(query)

        return cleaned

    #at this stage queries is a counter object which can be treated as
    #a dictionary of unique query terms with a count of the number of occurrences
    #print queries

    def calculateDuplicates(self, queryTerms):
        terms = Counter(queryTerms)
        return terms

    def removeStopWords(self, queryTerms):
        #stopwords list from http://www.ranks.nl/resources/stopwords.html
        #can easily be switched
        #todo doesn't seem to be working
        stopList = open('stopwords.txt').readlines()
        return list(set(queryTerms) - set(stopList))

