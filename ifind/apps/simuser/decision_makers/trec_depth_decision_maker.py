from loggers import Actions
from decision_makers.base_decision_maker import BaseDecisionMaker

class TrecDepthDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Returns True iif the depth at which a user is in a SERP is less than a predetermined value.
    """
    def __init__(self, search_context, depth):
        super(TrecDepthDecisionMaker, self).__init__(search_context)
        self.__depth = depth
        print self.__class__, self.__depth

    def decide(self):
        """
        If the user has not examined snippets up to depth .__depth, they will examine another snippet.
        Otherwise, a further query should be issued.
        """
        if self._search_context.get_current_serp_position() < self.__depth:
            return Actions.SNIPPET
        
        return Actions.QUERY