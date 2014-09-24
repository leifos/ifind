from ifind.common.query_ranker import QueryRanker
from ifind.common.query_generation import SingleQueryGeneration
from query_generators.base_generator import BaseQueryGenerator

class TriTermQueryGenerator(BaseQueryGenerator):
    """
    Implementing Strategy 3 from Heikki's 2009 paper, generating two-term queries.
    The first two terms are drawn from the topic, with the final and third term selected from the description - in some ranked order.
    """
    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        self.__description_cutoff = 0
        
        topic_title = topic.title
        topic_description = topic.content
        topic_language_model = self._generate_topic_language_model(topic)
        
        # Generate a series of query terms from the title, and then rank the generated terms.
        title_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        title_query_list = title_generator.extract_queries_from_text(topic_title)
        title_query_list = self._rank_terms(title_query_list, topic_language_model=topic_language_model)
        
        # Produce the two-term query "stem"
        title_query_list = self.__get_title_combinations(topic_language_model, title_query_list)
        
        # Perform the same steps, but from the description of the topic.
        description_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        description_query_list = description_generator.extract_queries_from_text(topic_description)
        description_query_list = self._rank_terms(description_query_list, topic_language_model=topic_language_model)
        
        return self.__generate_permutations(topic_language_model, title_query_list, description_query_list)
    
    def _rank_terms(self, terms, **kwargs):
        """
        Ranks the query terms by their discriminatory power.
        The length of the list returned == list of initial terms supplied.
        """
        topic_language_model = kwargs.get('topic_language_model', None)
        
        ranker = QueryRanker(smoothed_language_model=topic_language_model)
        ranker.calculate_query_list_probabilities(terms)
        return ranker.get_top_queries(len(terms))
    
    def __get_title_combinations(self, topic_language_model, title_query_list):
        """
        Returns a list of two-term ranked queries, extracted from the topic title.
        If the title consists of one term...surely not!!
        """
        count = 0
        prev_term = None
        windows = []
        
        for term in title_query_list:
            if count == 0:
                prev_term = term[0]
                count = count + 1
                continue
            else:
                count = 0
                windows.append('{0} {1}'.format(prev_term, term[0]))
        
        return self._rank_terms(windows, topic_language_model=topic_language_model)
    
    def __generate_permutations(self, topic_language_model, title_query_list, description_query_list):
        """
        Returns a list of ranked permutations for each title term.
        Queries are ranked for each title term - this ensures that the sequence of w1 w2 > w1 w3 is not broken.
        """
        return_terms = []
        
        for title_term in title_query_list:
            title_terms = []
            cutoff_counter = 0
            
            for description_term in description_query_list:
                if self.__description_cutoff > 0 and cutoff_counter == self.__description_cutoff:
                    break
                
                title_terms.append('{0} {1}'.format(title_term[0], description_term[0]))
                
                cutoff_counter = cutoff_counter + 1
            
            title_terms = self._rank_terms(title_terms, topic_language_model=topic_language_model)
            return_terms = return_terms + title_terms
        
        return return_terms