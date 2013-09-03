__author__ = 'rose'
from language_model import LanguageModel

class SmoothedModel():
    """
    class to represent calculating term weighting
    """
    def __init__(self, doc, bk):
        """
        :param doc: a LanguageModel object representing the document
        :param bk: a LanguageModel object representing the collection
        :return:
        """
        self.docLM=doc
        self.collectionLM=bk

    def calculate_likelihood(self, variable, term):
        """

        :param variable: is lambda by default, but could be alpha etc. for subclasses
        :return:likelihood value
        """
        collection_prob=self.collectionLM.get_term_probability(term)
        doc_prob=self.docLM.get_term_probability(term)
        score = variable*doc_prob + (1-variable)*collection_prob
        return score

class LaPlaceLanguageModel(SmoothedModel):
    def calculate_likelihood(self, variable, term):
        """

        :param variable: alpha
        :param term:
        :return:
        """
        numerator = float(self.docLM.get_num_occurrences(term) + variable)
        denominator = float(self.docLM.get_total_occurrences() + self.docLM.get_num_terms())
        return numerator/denominator

class JMModel(SmoothedModel):
    def calculate_likelihood(self, variable, term):
        """

        :param variable:lambda
        :param term:
        :return:
        """
        result = float((1-variable)*self.docLM.get_term_probability + variable*self.collectionLM.get_term_probability(term))
        return result

class BayesModel(SmoothedModel):
    def calculate_likelihood(self, variable, term):
        """

        :param variable: beta
        :param term:
        :return:
        """
        numerator = float(self.docLM.get_num_occurrences(term) + variable * self.collectionLM.get_term_probability(term))
        denominator = float(self.docLM.get_num_terms + variable)
        return numerator/denominator

