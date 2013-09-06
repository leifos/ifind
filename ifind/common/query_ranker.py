__author__ = 'leif'
from language_model import LanguageModel
from smoothed_language_model import SmoothedLanguageModel
import math

class QueryRanker(object):

    def __init__(self, smoothed_language_model):
        """
        takes in name of file with term, occurrences pairs crawled from website
        and uses this to calculate probabilities for each query which is sorted
        in descending order and the top k queries returned
        :param docLM: ifind.common.SmoothedLanguagemodel

        :param k: integer indicating the number of queries to be returned
        :return:a subset of k queries which have the highest probability
        of retrieving the document
        """
        self.lm = smoothed_language_model
        self.ranked_queries = {}

    def calculate_query_probability(self, query):
        """
        calculates the probability of an individual query
        :param query: a string of terms
        :return:score: the probability of a query given the language model (lm)
        """
        score = 0.0
        query = query.split(" ")
        for term in query:
            score = score + self._calculate_term_score(term)
        return score

    def _calculate_term_score(self, term):
        return math.log(self.lm.get_term_prob(term),2)

    def calculate_query_list_probabilities(self, query_list):
        """
        takes a query list and calculates the probabilities of each
        query, adds results to ranked_queries dict
        :param query_list: a list of query strings
        :return:a dictionary of queries (key) with their probability scores (value)
        """
        self.ranked_queries = {}
        for query in query_list:
            score = self.calculate_query_probability(query)
            #print "adding query ", query
            #print "with score ", score
            self.ranked_queries[query] = score

        #order queries by probability scores
        #self.ranked_queries = OrderedDict(sorted(self.ranked_queries, key=self.ranked_queries.__getitem__,reverse=True))
        return self.ranked_queries

    def get_top_queries(self, k):
        """
        Returns top k ranked queries
        :param k: number of queries to return
        :return: list of top k queries ordered in descending order by probability
        """
        import operator
        sorted_x = sorted(self.ranked_queries.iteritems(), key=operator.itemgetter(1), reverse=True)

        #ordered = sorted(self.ranked_queries.keys(), reverse=True)
        if len(sorted_x) > k:
            return sorted_x[0:k]
        else:
            return sorted_x

class OddsRatioQueryRanker(QueryRanker):

    def _calculate_term_score(self, term):

        ptd = self.lm.get_term_prob(term)
        pt =  self.lm.colLM.get_term_prob(term)
        if pt == 0.0:
            pt = 0.0000001
        return math.log( ptd/pt, 2)