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