__author__ = 'leif'
from language_model import LanguageModel


class QueryRanker(object):


    def __init__(self, background_file, doc_term_count, l=0.5):
        """
        takes in name of file with term, occurrences pairs crawled from website
        and uses this to calculate probabilities for each query which is sorted
        in descending order and the top k queries returned
        :param background_file: the file with terms and occurrences
        :param doc_term_count: the dictionary of terms with counts from the doc
        :param k: integer indicating the number of queries to be returned
        :param l : lambda, a parameter between 0 and 1 default 0.5
        :return:a subset of k queries which have the highest probability
        of retrieving the document
        """
        self.document = LanguageModel(dict=doc_term_count)
        self.background = LanguageModel(file=background_file)
        self.ranked_queries = {}



    def calculate_query_probability(self, query, l):
        """
        calculates the probability of an individual query
        :param query: the query for which to calculate the probability
        :return:score: the probability of a query given document and background
        term counts
        """
        score = 0
        for term in query:
            background_prob=self.background.get_term_probability(term)
            doc_prob=self.document.get_term_probability(term)
            score += l*doc_prob + (1-l)*background_prob
        return score

    def calculate_query_list_probabilities(self, query_list):
        """
        takes a query list and calculates the probabilities of each
        query, adds results to ranked_queries dict
        :param query_list:
        :return:
        """
        for query in query_list:
            score=self.calculate_query_probability(query)
            self.ranked_queries[query]=score

        #order queries by probability scores
        self.ranked_queries = sorted(self.ranked_queries, key=self.ranked_queries.__getitem__,reverse=True)


    def get_top_queries(self,k):
        """
        Returns top k ranked queries
        :param k: number of queries to return
        :return: dict of top k queries with probabilities
        """
        if len(self.ranked_queries) >k:
            return self.ranked_queries[0:k]
        else:
            return self.ranked_queries
