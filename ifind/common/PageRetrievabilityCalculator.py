"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""

class PageRetrievabilityCalculator:
    """
    Given a url calculate the retrievability scores for that page.
    """

    def __init__(self, url, engine):
        self.url = url
        self.engine = engine


    def calculate_retrievability(self):
        """
        Generates the queries for the page, issues them to the search engine, calculates
        the scores and returns a dictionary of results
        """
        pass

    def generateQueries(self):
        """
        generates a list of single and bi term queries
        returns said list
        """
        pass



    def generateSingleQueries(self):
        """
        generates a list of single term queries and returns it
        """
        pass

    def generateBiQueries(self):
        """
        Generates a list of bi-term queries and returns it.
        """
        pass


    def issueQueries(self):
        """
        Issues query list to the search engine
        """
        pass

    def calculateScores(self):
        """
        calculates the scores for the page and returns them
        may start as dictionary or list, but will probably extract an object
        which will be able to
        - rank queries by query_ret_score, and show top n queries
	    - rank queries by query_ret_score * query_prob, and show the top n queries
	    - show the number of queries issued, and the number of queries that were successful, and the page retrievability

        :return: dictionary or list of results
        """
        pass