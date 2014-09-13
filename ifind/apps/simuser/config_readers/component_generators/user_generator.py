from search_context import SearchContext
from config_readers.component_generators.base_generator import BaseComponentGenerator

class UserComponentGenerator(BaseComponentGenerator):
    """
    """
    def __init__(self, simulation_components, config_dict):
        super(UserComponentGenerator, self).__init__(config_dict)
        
        self.__simulation_components = simulation_components
        
        # Store the user's ID for easy access.
        self.id = self._config_dict['@id']
        
        # Create the user's query generator.
        self.query_generator = self._get_object_reference(config_details=self._config_dict['queryGenerator'],
                                                          package='query_generators')
        
        # Create the user's snippet classifier.
        self.snippet_classifier = self._get_object_reference(config_details=self._config_dict['textClassifiers']['snippetClassifier'],
                                                             package='text_classifiers',
                                                             components=[('topic', self.__simulation_components.topic)])
        
        # Create the uer's document classifier.
        self.document_classifier = self._get_object_reference(config_details=self._config_dict['textClassifiers']['documentClassifier'],
                                                              package='text_classifiers',
                                                              components=[('topic', self.__simulation_components.topic)])
        
        # Create the search context object.
        self.search_context = self.__generate_search_context()
        
        # Finally, create the decision maker.
        self.decision_maker = self._get_object_reference(config_details=self._config_dict['decisionMaker'],
                                                         package='decision_makers',
                                                         components=[('search_context', self.search_context)])
    
    def __generate_search_context(self):
        """
        Generate a search context object given the settings in the configuration dictionary.
        """
        topic = self.__simulation_components.topic
        search_interface = self.__simulation_components.search_interface
        
        return SearchContext(search_interface=search_interface,
                             topic=topic,
                             query_list=self.query_generator.generate_query_list(topic))