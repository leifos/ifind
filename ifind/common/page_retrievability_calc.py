"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1

requires nltk: pip install nltk
"""

from single_term_query_gen import SingleTermQueryGeneration
from ifind.search.query import Query
from urllib import urlopen
import time

class PageRetrievabilityCalculator:
    """ Given a url calculate the retrievability scores for that page.

    """

    def __init__(self, engine, cutoff=10, generator=None):
        self.engine = engine
        self.cutoff= cutoff
        #query, retrievability score pairs for all queries issued
        self.query_ret_scores = {}
        #query, rank pairs for all queries issued against self.engine
        self.query_rank = {}
        self.url = None
        #the list of queries
        self.query_list = {}

        if generator:
            self.generator = generator
        else:
            # default to a single term generator
            self.generator = SingleTermQueryGeneration()


    def set_query_generator(self, generator):
        """ sets generator, not really needed
        :param generator: Expects a ifind.common.QueryGeneration
        :return: None

        """
        self.generator = generator

    def score_page(self, url):
        """
        :param url:
        :return:

        """

        # check whether url is valid

        #if valid, set url
        self.url = url
        # now generate queries that will be used
        self.query_list = self._generate_queries()

        for query in self.query_list:
            time.sleep(0.2)
            rank = self._process_query(query)
            self.query_rank[query] = rank

        return self.calculate_page_retrievability()

    def calculate_page_retrievability(self):
        self.query_ret_scores = {}
        total_retrievability = 0
        for query in self.query_rank:
            self.query_ret_scores[query] = self._calculate_retrievability(self.query_rank[query])
            total_retrievability += self.query_ret_scores[query]

        return total_retrievability


    def top_queries(self, n):
        """
        :param n: integer
        :return: returns a list of the top n queries

        """

        #TODO(leifos):from self.query_ret_scores sort by the highest score


        top_query_list =['to be implemented']
        return top_query_list

    def _generate_queries(self):
        """
        generates a list of single or bi term queries from plain text or html
        returns said list
        :return returns a list of queries as strings

        """

        #use the generator to create the queries for the text, store
        #the result in a list

        html = urlopen(self.url).read()
        ####TODO (rose) ask user for stopfile name
        queries = self.generator.extract_queries_from_html(html, stopfile_name='stopwords.txt')

        #create list of query objects so queries can be issued
        #against engines
        query_list = []
        for query in queries:
            currQuery = Query(query, self.cutoff)
            query_list.append(currQuery)
        #return the queries object list
        return query_list


    def _process_query(self, query):
        """
        Issues single query to the search engine and return the rank at which the url was returned
        object
        :param: query expects an ifind.search.Query
        :return: rank of url in the search results, else 0

        """
        rank = 0

        print "issuing query : %s" % (query.terms)
        result_list = self.engine._search(query)
        # check if url is in the results.
        i = 0
        print "no of results : %d" % (len(result_list))
        for result in result_list:
            i += 1
            #TODO(leifos): may need a better matching function in case there are small differences between url
            if result.url == self.url:
                rank = i
                print "Found %s" % (self.url)
                break

        return rank

    def _calculate_retrievability(self, rank, query_opp=1):
        """
        :param rank: rank of the url
        :param query_opp: opportunity of the query
        :return: returns the retrievability value for a given rank

        """
        #TODO(leifos): use a class to enable different retrievability functions to be used.

        if rank == 0:
            return 0.0
        else:
            return query_opp * (1.0/rank)
