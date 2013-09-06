"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1

requires nltk: pip install nltk
"""

from query_generation import SingleQueryGeneration
from ifind.search.query import Query
from urllib import urlopen
import time

class PageRetrievabilityCalculator:
    """ Given a url calculate the retrievability scores for that page.

    """

    def __init__(self, engine, c=50, beta=0.0):
        """
        :param engine: expects a ifind.search.engine
        :param cutoff: number of results to request from the search engine per query
        :param c: cutoff value when computing retrievability scores and when retrieving documents from search engine
        :param beta: the discount for computing gravity based retrievability scores
        :return: an initialized PageRetrievabiliyCalculator
        """
        self.engine = engine
        self.url = None
        #the dictionary of ifind.search.query.Query objects
        self.query_dict = {}
        # total retrievability for the latest url processed
        self.ret_score = 0.0
        self.beta = beta
        self.c = c


    def score_page(self, url, query_list):
        """
        Issues each query against the search engine, and tries to match that page.
        Store each query as a ifind.search.query.Query object in query_dict
        Updates the rank property of the ifind.search.query.Query object after each search
        :param url: a url string to match the results against
        :param query_list: a list of strings, each string is query
        :return: None
        """

        # check whether url is valid

        #if valid, set url
        self.url = url

        self.ret_score = 0
        self.page_retrieved = 0

        self._make_query_dict(query_list)
        for query_key in self.query_dict:
            iquery = self.query_dict[query_key]
            rank = self._process_query(iquery)
            iquery.rank = rank
            if rank > 0:
                self.page_retrieved = self.page_retrieved + 1


    def report(self):
        print "For url: %s" % (self.url)
        print "A total of %d queries were issued" % (self.engine.num_requests)
        print "Of those %d were handled by the cache" % (self.engine.num_requests_cached)
        print "The page scored: %f" % (self.ret_score)
        print "retrieved: %d query count: %d" % (self.page_retrieved, self.query_count)
        f = float(self.page_retrieved) / float(self.query_count)
        print "Percentage of query that returned the page %f " % (f)

    def stats(self):
        return {'url':self.url, 'query_count': self.query_count, 'retrieved': self.page_retrieved, 'retrievability':self.ret_score }


    def calculate_page_retrievability(self, c=None, beta=None):
        """
        :param c (int): takes a new value of the c param and sets it for use in the calculate retrievability method
        :param beta (float): take a new value of the beta param and sets it
        :return: the total retrievability score for the page (float), updates the iquery objects with the ret_score based on the current c and beta
        """

        if c:
            self.c = c
        if beta:
            self.beta = beta

        total_retrievability = 0
        for query_key in self.query_dict:
            iquery = self.query_dict[query_key]
            iquery.ret_score = self._calculate_retrievability(iquery.rank)
            total_retrievability += iquery.ret_score

        self.ret_score = total_retrievability
        return total_retrievability

    def top_queries(self, n):
        """ returns the top n queries which had the highest retrievabilty scores
        :param n: integer
        :return: returns a list of the top n ifind.search.query.Query objects

        """

        #TODO(leifos):from self.query_ret_scores sort by the highest score
        import operator

        top_query_list= sorted(self.query_dict.values(), key=operator.attrgetter('ret_score'))
        top_query_list.reverse()

        if len(top_query_list) > n:
            return top_query_list[0:n]
        else:
            return top_query_list

    def _make_query_dict(self, query_list):
        """
        generates a list of queries from plain text
        :return returns a list of queries as strings

        """
        self.query_dict = {}

        for q in query_list:
            aQ = Query(terms=q, top=self.c)
            aQ.rank = 0
            aQ.ret_score = 0.0
            self.query_dict[q] = aQ


        self.query_count = len(self.query_dict)

    def _process_query(self, query):
        """
        Issues single query to the search engine and return the rank at which the url was returned
        object
        :param: query expects an ifind.search.Query
        :return: rank of url in the search results, else 0

        """

        rank = 0

        result_list = self.engine.search(query)
        # check if url is in the results.
        i = 0
        match_url = self.url.rstrip("/")
        for result in result_list:
            i += 1
            result_url = result.url.rstrip("/")

            #TODO(leifos): may need a better matching function in case there are small differences between url
            if result_url == match_url:
                rank = i
                break

        print "%d\t%d\t%d\t%d\t%s" % (len(result_list), rank, self.engine.num_requests, self.engine.num_requests_cached, query.terms)

        return rank

    def _calculate_retrievability(self, rank, query_opp=1.0):
        """
        computes either gravity based score or cumulative
        :param rank (int): rank of the url
        :param query_opp (float): opportunity of the query
        :return: returns the retrievability value as a float,

        """

        if rank == 0:
            return 0.0
        else:
            if rank <= self.c:
                if self.beta > 0.0:
                    return query_opp * (1.0/(rank**self.beta))
                else:
                    return query_opp
            else:
                return 0.0