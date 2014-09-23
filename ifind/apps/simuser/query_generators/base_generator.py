import abc
from ifind.common.query_ranker import QueryRanker
from ifind.common.language_model import LanguageModel
from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration

class BaseQueryGenerator(object):
    """
    
    """
    def __init__(self, stopword_file, background_file=[]):  # TODO(dmax): stopwords_file to be a list!
        """
        
        """
        self._stopword_file = stopword_file
        self._background_file = background_file
    
    def _generate_topic_language_model(self, topic):
        """
        Given a Topic object, returns a language model representation for the given topic.
        Override this method in inheriting classes to generate and return different language models.
        """
        topic_text = topic.content
        
        document_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        document_extractor.extract_queries_from_text(topic_text)
        document_term_counts = document_extractor.query_count
        
        # The langauge model we return is simply a representtaion of the number of times terms occur within the topic text.
        topic_language_model = LanguageModel(term_dict=document_term_counts)
        return topic_language_model
    
    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        topic_text = topic.content
        topic_lang_model = self._generate_topic_language_model(topic)
        
        bi_query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        tri_query_generator = TriTermQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        
        tri_query_list = tri_query_generator.extract_queries_from_text(topic_text)
        bi_query_list = bi_query_generator.extract_queries_from_text(topic_text)
        
        query_list = tri_query_list + bi_query_list
        
        query_ranker = QueryRanker(smoothed_language_model=topic_lang_model)
        query_ranker.calculate_query_list_probabilities(query_list)
        return query_ranker.get_top_queries(100)
    
    @abc.abstractmethod
    def _rank_terms(self, terms, **kwargs):
        """
        Given a list of query terms (list of strings) as parameter terms, returns a list of those queries - ranked in some way.
        Additional parameters may be passed (if required for a given implementation) through kwargs.
        """
        pass