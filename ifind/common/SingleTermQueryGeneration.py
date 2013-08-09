"""
A class which inherits from QueryGeneration to generate queries list of single terms
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
from QueryGeneration import QueryGeneration
from htmlParser import htmlParser

class SingleTermQueryGeneration(QueryGeneration):
    """
    Implementation of QueryGeneration which generates single term queries
    """
    def __init__(self):
        pass

    def extractQueriesFromHtml(self, html):
        """

        :param html: the html from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #first get the text from the html
        parser = htmlParser(html)
        text = parser.getText()
        #now use extractQueries from text and return the list of queries
        return self.extractQueriesFromText(text)

    def extractQueriesFromText(self, text):
        """
        takes a string of text from which to extract single term queries
        :param text: the text from which the queries are to be generated
        :return:queries: list of queries as strings
        """
        #split into single words and store in a set so no duplicates
        singleTerms = set(str.rsplit(text, " "))
        return list(singleTerms)



