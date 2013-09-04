__author__ = 'rose'
from language_model import LanguageModel

class SmoothedLanguageModel():
    """
    class to represent calculating term weighting
    """
    #TODO(leifos): most language models are going to have 1 parameter, possibly a few more.
    def __init__(self, docLM, colLM, alpha=1.0, beta=1.0, lam=0.5):
        """
        :param docLM: a LanguageModel object representing the document
        :param colLM: a LanguageModel object representing the collection
        :return:
        """
        self.docLM=docLM
        self.colLM=colLM
        self.set_alpha(alpha)
        self.set_beta(beta)
        self.set_lam(lam)

    def set_alpha(self, value):
        if value > 0:
            self.alpha = value

    def set_beta(self, value):
        if value > 0:
            self.beta = value

    def set_lam(self, value):
        """
        lambda is always between one and zero
        :param value: float between one and zero
        """
        if value < 0:
            self.lam = 0.0
        else:
            if value > 1:
                self.lam = 1.0
            else:
                self.lam = value


    #TODO(leifos): removed variable, as this can be set when the object is created.
    #TODO(leifos): default method is JM smoothing
    #TODO(leifos): change the name from get_term_probability to get-term_prob.. shorter, but also consistent with get_term_prob in Language Model
    def get_term_prob(self, term):
        """

        :param variable: is lambda by default, but could be alpha etc. for subclasses
        :return:likelihood value
        """
        collection_prob = self.colLM.get_term_prob(term)
        doc_prob = self.docLM.get_term_prob(term)
        #TODO(leifos): adding in parathenses makes sure you are computing what your really want.
        score = (self.lam * doc_prob) + ((1.0 - self.lam) * collection_prob)
        return score

class LaPlaceLanguageModel(SmoothedLanguageModel):

    def get_term_prob(self, term):
        """
        :param term:
        :return:
        """
        numerator = float(self.docLM.get_num_occurrences(term) + self.alpha)
        denominator = float(self.docLM.get_total_occurrences() + (self.colLM.get_num_terms() * self.alpha ))
        return numerator/denominator


class BayesLanguageModel(SmoothedLanguageModel):

    def get_term_prob(self, term):
        """
        :param term:
        :return:
        """
        numerator = self.docLM.get_num_occurrences(term) + (self.beta * self.colLM.get_term_prob(term))
        #denominator = self.docLM.get_num_terms() + self.beta
        denominator = self.docLM.get_total_occurrences() + self.beta
        return float(numerator)/float(denominator)

