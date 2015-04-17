from loggers import Actions
from decision_makers.base_decision_maker import BaseDecisionMaker

class TotalNonrelDecisionMakerDocs(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Returns True iif the depth at which a user is in a SERP is less than a predetermined value.
    """
    def __init__(self, search_context, nonrelevant_threshold=3):
        super(TotalNonrelDecisionMakerDocs, self).__init__(search_context)
        self.__nonrelevant_threshold = nonrelevant_threshold  # The threshold; get to this point, we stop in the current SERP.

    def decide(self):
        """
        If the user's current position in the current SERP is < the maximum depth, look at the next snippet in the SERP.
        Otherwise, a new query should be issued.
        """
        counter = 0
        examined_snippets = self._search_context.get_examined_snippets()[::-1]  # Reverse list
        examined_documents = self._search_context.get_examined_documents()[::-1]  # Reverse list
        
        for snippet in examined_snippets:
            judgment = snippet.judgment
            
            if judgment == 0:
                counter = counter + 1  # Found something nonrelevant; increment counter

                if counter == self.__nonrelevant_threshold:
                    return Actions.QUERY

        # If we get here, we are okay - so we examine the next snippet.
        return Actions.SNIPPET