from query_generators.base_generator import BaseQueryGenerator
from ifind.common.language_model import LanguageModel
from ifind.common.query_generation import SingleQueryGeneration
from ifind.common.smoothed_language_model import BayesLanguageModel
from ifind.common.query_ranker import QueryRanker

class BiTermQueryGenerator(BaseQueryGenerator):
    """
    A simple query generator - returns a set of queries consisting of only one term.
    These can be ranked by either the frequency of the term's occurrence, or by its perceived discriminatory value.
    """
    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        self.__content_cutoff = 5
        
        topic_title = topic.title
        topic_background = topic.content
        
        topic_language_model = self._generate_topic_language_model(topic)
        
        # Generate query terms from the topic title
        title_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        title_query_list = title_generator.extract_queries_from_text(topic_title)
        
        # Generate query terms from the topic's description
        content_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        content_query_list = content_generator.extract_queries_from_text(topic_background)
        
        return self.__generate_ranked_query_permutations(topic, title_query_list, content_query_list)
    
    def __generate_ranked_query_permutations(self, topic, title_query_list, content_query_list):
        """
        Returns a list of query terms, ordered by the first term - and then the rank of the complete two-word term.
        
        """
        return_terms = []
        observed_combinations = []
        
        for title_term in title_query_list:
            title_terms = []
            
            for content_term in content_query_list:
                if (title_term, content_term) not in observed_combinations and (content_term, title_term) not in observed_combinations:
                    observed_combinations.append((title_term, content_term))
                    title_terms.append('{0} {1}'.format(title_term, content_term))
            
            topic_language_model = self._generate_topic_language_model(topic)
            
            ranker = QueryRanker(smoothed_language_model=topic_language_model)
            ranker.calculate_query_list_probabilities(title_terms)
            
            top_queries = ranker.get_top_queries(self.__content_cutoff)
            return_terms = return_terms + top_queries
        
        return return_terms
        
    def _generate_topic_language_model(self, topic):
        """
        Returns a languge model for the given topic, considering both the title and content text.
        """
        topic_text = topic.title
        topic_background = topic.content
    
        document_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        document_extractor.extract_queries_from_text(topic_text)
        document_term_counts = document_extractor.query_count
    
        document_extractor.extract_queries_from_text(topic_background)
    
        background_term_counts = document_extractor.query_count
    
        title_language_model = LanguageModel(term_dict=document_term_counts)
        background_language_model = LanguageModel(term_dict=background_term_counts)
        topic_language_model = BayesLanguageModel(title_language_model, background_language_model, beta=10)
        return topic_language_model