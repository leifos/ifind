__author__ = 'leif'

from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
from ifind.common.language_model import LanguageModel
from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
import math

class TextClassifier(object):


    def __init__(self, stopword_file=[], background_file=[]):
        """
        :param search_interface.topic:
        :param stopword_file:
        :param background_file:
        :return:
        """
        self.stopword_file = stopword_file
        self.background_file = background_file
        if self.background_file:
            self.read_in_background(self.background_file)

    def set_topic(self, topic):
        self.topic = topic

    def read_in_background(self, vocab_file):
        vocab = {}
        f  = open(vocab_file,'r')
        for line in f:
            tc = line.split(',')
            vocab[tc[0]]=int(tc[1])

        self.backgroundLM = LanguageModel(term_dict=vocab)

#backgroundLM = read_in_background(bg_file)
#smoothedTopicLM = BayesLanguageModel(topicLM,backgroundLM,beta=100)



    def is_relevant(self, document):
        """

        :param search_interface.document
        :return:
        """
        return True


class iFindTextClassifier(TextClassifier):

    def __init__(self, stopword_file=[], background_file=[]):
        TextClassifier.__init__(self, stopword_file, background_file)
        self.topicLM = None
        self.threshold = -0.20


    def set_topic(self, topic):
        self.topic = topic
        self.make_topic_lm()


    def make_topic_lm(self):
        topic_text = self.topic.content + self.topic.title

        doc_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self.stopword_file)
        doc_extractor.extract_queries_from_text(topic_text)
        doc_term_counts = doc_extractor.query_count
        lm = LanguageModel(term_dict=doc_term_counts)
        self.topicLM = SmoothedLanguageModel(lm,self.backgroundLM,100)
        print "making topic", self.topicLM.docLM.total_occurrences


    def is_relevant(self, document):
        #print "computing relevance", document.docid

        score = 0.0
        count = 0.0
        for t in document.title.split(' '):
            score = score + self._get_term_score(t)
            count += 1.0

        for t in document.content.split(' '):
            score = score + self._get_term_score(t)
            count += 1.0


        if  (score/count) > self.threshold:
            return True
        else:
            return False


    def _get_term_score(self, term):

        ptd = self.topicLM.get_term_prob(term)
        pt = self.backgroundLM.get_term_prob(term)
        if pt == 0.0:
            return 0.0
        else:
            return math.log( ptd/pt, 2)