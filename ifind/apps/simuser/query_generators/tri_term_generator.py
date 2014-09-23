from query_generators.base_generator import BaseQueryGenerator
from ifind.common.language_model import LanguageModel
from ifind.common.query_generation import SingleQueryGeneration
from ifind.common.smoothed_language_model import BayesLanguageModel
from ifind.common.query_ranker import QueryRanker

class TriTermQueryGenerator(BaseQueryGenerator):
    """
    Following query strategy 3 from Heikki's 2009 paper.
    Three query terms, the first selected from the topic title, the following two selected from the topic description using a sliding window approach.
    """
    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        self.__title_terms = 2
        self.__windows = 3
        
        topic_title = topic.title
        topic_background = topic.content
        
        topic_language_model = self._generate_topic_language_model(topic)
        
        # Generate query terms from the topic title
        title_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        title_query_list = title_generator.extract_queries_from_text(topic_title)
        
        # Generate query terms from the topic's description
        content_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        content_query_list = content_generator.extract_queries_from_text(topic_background)
        
        return self.__generate_query_terms(topic_language_model, title_query_list, content_query_list)
    
    def __generate_query_terms(self, topic_language_model, title_query_list, content_query_list):
        """
        Using a sliding window approach, generates a series of queries based on the title and content terms.
        Before the queries are generated, the individual terms are ranked.
        """
        if self.__title_terms > len(title_query_list):
            self.__title_terms = len(title_query_list)
        
        if self.__windows > (len(content_query_list) / 2):
            self.__windows = len(content_query_list) / 2
        
        generated_terms = []
        
        # Rank the title query terms
        title_ranker = QueryRanker(smoothed_language_model=topic_language_model)
        title_ranker.calculate_query_list_probabilities(title_query_list)
        title_query_list = title_ranker.get_top_queries(len(title_query_list))
        
        # Rank the content (description) title terms
        content_ranker = QueryRanker(smoothed_language_model=topic_language_model)
        content_ranker.calculate_query_list_probabilities(content_query_list)
        content_query_list = content_ranker.get_top_queries(len(content_query_list))
        
        window_position = 0
        
        # Looping through the number of title terms we want to use...
        for i in range(0, self.__title_terms):
            title_term = title_query_list[i]
            
            # Then the number of windows which we want to produce.
            for i in range(0, self.__windows):
                windowed_terms = content_query_list[i*2:((i*2)+2)]
                query = title_term[0]
                
                for term in windowed_terms:
                    query = "{0} {1}".format(query, term[0])
                
                generated_terms.append(query)
                window_position = window_position + 1
        
        return generated_terms
    
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