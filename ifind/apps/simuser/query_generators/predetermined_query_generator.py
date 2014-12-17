from ifind.common.query_ranker import QueryRanker
from ifind.common.query_generation import SingleQueryGeneration
from query_generators.base_generator import BaseQueryGenerator

class PredeterminedQueryGenerator(BaseQueryGenerator):
    """
    Not really a query generator per se..self.
    but given a list of queries from a configuration file, returns the query list in the specified order.
    
    Requires the following attributes:
        stopword_file (required by all query generators, not used)
        query_file (string representing path to query file)
        user (string representing the user to focus on)
    
    The query file should be in the format
        USERID TOPIC QUERY
        Separated by spaces - first two spaces are important, all spaces after are considered part of the query.
    """
    def __init__(self, output_controller, stopword_file, query_file, user, background_file=[], topic_model=0):
        """
        Initialises the class.
        """
        super(PredeterminedQueryGenerator, self).__init__(output_controller, stopword_file, background_file=[], topic_model=0)
        self.__query_filename = query_file
        self.__user = user
    
    def generate_query_list(self, topic):
        """
        Returns the list of predetermined queries for the specified user.
        """
        queries = []
        query_file = open(self.__query_filename, 'r')
        
        for line in query_file:
            line = line.strip()
            line = line.split()
            
            query_userid = line[0]
            query_topic = line[1]
            query_terms = ' '.join(line[2:])
            
            if query_userid == self.__user and query_topic == topic.id:
                queries.append((query_terms, 0))
        
        query_file.close()
        return queries