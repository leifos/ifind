from search_interfaces import Topic
from config_readers.user_config_reader import UserConfigReader
from config_readers.component_generators.base_generator import BaseComponentGenerator

class SimulationComponentGenerator(BaseComponentGenerator):
    """
    A component generator for Simulations. Extends the BaseComponentGenerator.
    Includes a reference to a UserComponentGenerator, containing all user-relevant components.
    """
    def __init__(self, simulation_id, config_dict):
        """
        Instantiates all the necessary components for the given configuration dictionary.
        """
        super(SimulationComponentGenerator, self).__init__(config_dict)
        
        # What is the simulation's ID?
        self.simulation_id = simulation_id
        
        # Generate a Topic object.
        self.topic = self.__generate_topic()
        
        # Generate the logger object for the simulation.
        self.logger = self._get_object_reference(config_details=self._config_dict['logger'],
                                                 package='loggers')
        
        # Generate the search interface to be used.
        self.search_interface = self._get_object_reference(config_details=self._config_dict['searchInterface'],
                                                           package='search_interfaces')
        
        # Create the user object - by loading the specified file into a UserConfigReader, then obtaining its components.
        user_config_file = self._config_dict['user']['@configurationFile']
        self.user = UserConfigReader(user_config_file).get_component_generator(self)
    
    def __generate_topic(self):
        """
        Generates a topic object based on the settings in the configuration dictionary provided.
        """
        config = self._config_dict['topic']
        
        topic = Topic(config['@id'])
        topic.read_topic_from_file(config['@filename'])
        
        return topic