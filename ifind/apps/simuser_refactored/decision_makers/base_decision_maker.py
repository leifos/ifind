import abc

class BaseDecisionMaker(object):
    """
    
    """
    def __init__(self, search_context):
        self._search_context = search_context
    
    @abc.abstractmethod
    def decide(self):
        """
        Abstract method - must be implemented by an inheriting class.
        A returned value of True indicates that the user intends to examine a snippet.
        Otherwise, False indicates that the next query should be issued.
        """
        pass