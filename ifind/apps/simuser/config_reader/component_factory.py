import os
import sys
import inspect
import importlib
from search_interfaces import Topic
from search_context import SearchContext

class ComponentFactory(object):
    """
    A neat class which takes a well-formed configuration dictionary, and creates a series of objects based on the configuration details supplied.
    The objects are available in a dictionary which can be easily referenced to by the various components.
    """
    def __init__(self, config_dict):
        self.__config_dict = config_dict
        self.__components = {}
    
    def get_objects(self):
        """
        Returns a dictionary of objects, each of which represent a component of the simulation.
        The objects are instantiated based on the configuration parameters supplied in .__config_dict.
        """
        self.__components['topic'] = self.__generate_topic(self.__config_dict['topic'])
        self.__components['query_generator'] = self.__generate_object(self.__config_dict['queryGenerator'], 'query_generators')
        self.__components['logger'] = self.__generate_object(self.__config_dict['logger'], 'loggers')
        self.__components['snippet_classifier'] = self.__generate_object(self.__config_dict['textClassifiers']['snippetClassifier'], 'text_classifiers')
        self.__components['document_classifier'] = self.__generate_object(self.__config_dict['textClassifiers']['documentClassifier'], 'text_classifiers')
        self.__components['search_interface'] = self.__generate_object(self.__config_dict['searchInterface'], 'search_interfaces')
        self.__components['search_context'] = self.__generate_search_context()
        self.__components['decision_maker'] = self.__generate_object(self.__config_dict['decisionMaker'], 'decision_makers')
        
        return self.__components
    
    def __generate_search_context(self):
        """
        Returns a SearchContext object.
        """
        return SearchContext(search_interface=self.__components['search_interface'],
                             topic=self.__components['topic'],
                             query_list=self.__components['query_generator'].generate_query_list(self.__components['topic']))
    
    def __generate_object(self, details, package):
        """
        Generic helper method to return an instantiated object.
        """
        selected_class = details['@class']
        available_classes= self.__get_classes(package)
        attributes = self.__return_attributes(details)
        
        return self.__get_class_reference(selected_class, available_classes, attributes)
    
    def __generate_topic(self, topic_details):
        """
        Returns a Topic object, representing the topic number and description specified by the configuration dictionary.
        """
        topic = Topic(topic_details['@number'])
        topic.read_topic_from_file(topic_details['@filename'])
        
        return topic
    
    def __get_class_reference(self, selected_class, available_classes, attributes):
        """
        Attempts to return a reference to the specified class from the list of available classes.
        If the class cannot be found, then an ImportError exception is raised.
        """
        for available_class in available_classes:
            if available_class[0] == selected_class:
                kwargs = {}

                for attribute in attributes:
                    if attribute['@is_argument']:
                        if attribute['@type'] == 'component':
                            kwargs[attribute['@name']] = self.__components[attribute['@name']]
                        else:
                            kwargs[attribute['@name']] = attribute['@value']

                reference = available_class[1](**kwargs)
                
                for attribute in attributes:
                    if not attribute['@is_argument']:
                        if attribute['@type'] == 'component':
                            setattr(reference, attribute['@name'], self.__components[attribute['@name']])
                        else:
                            setattr(reference, attribute['@name'], attribute['@value'])
                
                return reference
                
        raise ImportError("Specified class '{0}' could not be found.".format(selected_class))
    
    def __get_classes(self, package):
        """
        Returns references to all classes within the specified package (directory) name.
        Uses some reflection to work out which classes exist within which package/module.
        """
        modules = []
        classes = []
        
        # List through the modules in the specified package, ignoring __init__.py, and append them to a list.
        for f in os.listdir(package):
            if f.endswith('.py') and not f.startswith('__init__'):
                modules.append('{0}.{1}'.format(package, os.path.splitext(f)[0]))
        
        module_references = []
        
        # Attempt to import each module in turn so we can access its classes
        for module in modules:
            module_references.append(importlib.import_module(module))
        
        # Now loop through each module, looking at the classes within it - and then append each class to a list of valid classes.
        for module in module_references:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    classes.append((obj.__name__, obj))
        
        return classes
    
    def __return_attributes(self, configuration_dictionary):
        """
        Returns a consistent list of attributes from the given configuration dictionary.
        """
        attributes = []
        
        if 'attribute' in configuration_dictionary:
            if type(configuration_dictionary['attribute']) == dict:
                attributes.append(configuration_dictionary['attribute'])
            else:
                attributes = configuration_dictionary['attribute']
        
        return attributes