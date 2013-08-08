"""
A class which inherits from QueryGeneration to generate queries list of biterms
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""
from QueryGeneration import QueryGeneration

class BiTermQueryGeneration(QueryGeneration):
    """
    Implementation of QueryGeneration which generates single term queries
    """
    def __init__(self):
        pass

    def extractQueriesFromHtml(self, html):
        pass

    def extractQueriesFromText(self, text):
        pass