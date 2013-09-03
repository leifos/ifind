__author__ = 'leif'
from language_model import LanguageModel
from smoothed_doc_language_model import SmoothedModel

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



    def calculate_query_probability(self, query, l=0.5):
        """
        calculates the probability of an individual query
        :param query: the query for which to calculate the probability
        :return:score: the probability of a query given document and background
        term counts
        """
        score = 0
        query = query.split(" ")
        for term in query:
            #background_prob=self.background.get_term_probability(term)
            #doc_prob=self.document.get_term_probability(term)
            #score += l*doc_prob + (1-l)*background_prob
            calculator = SmoothedModel(self.document,self.background)
            score+=calculator.calculate_likelihood(l,term)
            #todo is rounding needed??
        return score

    def calculate_query_list_probabilities(self, query_list, l=0.5):
        """
        takes a query list and calculates the probabilities of each
        query, adds results to ranked_queries dict
        :param query_list: a list of query strings
        :return:a dictionary of queries (key) with their probability scores (value)
        """
        for query in query_list:
            score = self.calculate_query_probability(query, l)
            #print "adding query ", query
            #print "with score ", score
            self.ranked_queries[query] = score

        #order queries by probability scores
        #self.ranked_queries = OrderedDict(sorted(self.ranked_queries, key=self.ranked_queries.__getitem__,reverse=True))
        return self.ranked_queries

    def get_top_queries(self,k):
        """
        Returns top k ranked queries
        :param k: number of queries to return
        :return: list of top k queries ordered in descending order by probability
        """
        #sort ranked queries by value of probabilities from most to least likely
        #print "before sorting"
        #print self.ranked_queries.keys()
        ordered = sorted(self.ranked_queries.keys(), reverse=True)
        #print "after sorting"
        #print ordered

        if len(ordered) > k:
            return ordered[0:k]
        else:
            return ordered
