"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""

from pagecapture import  PageCapture

class PageRetrievabilityCalculator:
    """
    Given a url calculate the retrievability scores for that page.
    """

    def __init__(self, engine):
        self.engine = engine


    def calculate_retrievability(self, url):
        """
        Generates the queries for the page, issues them to the search engine, calculates
        the scores and returns a dictionary of results
        """
        pass

    def _generateQueries(self, html, isSingle):
        """
        generates a list of single or bi term queries
        returns said list
        :param html the html from which queries will be generated
        :param boolean isSingle to denote whether to generate single or bi-terms
        """
        pass

    def _issueQueries(self):
        """
        Issues query list to the search engine
        """
        pass

    def _calculateScores(self, url):
        """
        calls getPage
        uses html to generateQueries
        issues the queries
        calculates the scores for the page and returns them
        may start as dictionary or list, but will probably extract an object
        which will be able to
        - rank queries by query_ret_score, and show top n queries
	    - rank queries by query_ret_score * query_prob, and show the top n queries
	    - show the number of queries issued, and the number of queries that were successful, and the page retrievability

        :return: dictionary or list of results
        """
        pass

    def _getPage(self, url):
        """
        Creates a PageCapture object, uses it to get_page_sourcecode
        :param url:
        :return:
        """
        pass