__author__ = 'leif'

from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
from ifind.common.language_model import LanguageModel
from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker


class QueryProducer(object):


    def __init__(self, stopword_file, background_file=[]):

        self.stopword_file = stopword_file
        self.background_file = background_file


    def produce_query_list(self, topic):

        topic_text = topic.content
        topicLM = self.make_topic_lm(topic)
        bi_query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=self.stopword_file)
        tri_query_generator = TriTermQueryGeneration(minlen=3, stopwordfile=self.stopword_file)
        tri_query_list = tri_query_generator.extract_queries_from_text(topic_text)
        bi_query_list = bi_query_generator.extract_queries_from_text(topic_text)

        query_list = tri_query_list + bi_query_list

        qr = QueryRanker(smoothed_language_model=topicLM)
        qr.calculate_query_list_probabilities(query_list)
        queries = qr.get_top_queries(20)
        return queries


    def make_topic_lm(self, topic ):
        topic_text = topic.content
        doc_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self.stopword_file)
        doc_extractor.extract_queries_from_text(topic_text)
        doc_term_counts = doc_extractor.query_count
        topicLM = LanguageModel(term_dict=doc_term_counts)

        return topicLM




class SmarterQueryProducer(QueryProducer):

    def make_topic_lm(self, topic):

        topic_text = topic.title
        topic_bg = topic.content
        doc_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self.stopword_file)
        doc_extractor.extract_queries_from_text(topic_text)
        doc_term_counts = doc_extractor.query_count

        doc_extractor.extract_queries_from_text(topic_bg)

        bg_term_counts = doc_extractor.query_count

        titleLM = LanguageModel(term_dict=doc_term_counts)

        bgLM = LanguageModel(term_dict=bg_term_counts)

        topicLM = BayesLanguageModel(titleLM, bgLM,beta=10)

        return topicLM