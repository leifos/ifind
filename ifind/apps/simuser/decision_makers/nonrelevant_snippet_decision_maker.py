from loggers import Actions
from decision_makers.base_decision_maker import BaseDecisionMaker
from ifind.seeker.trec_qrel_handler import TrecQrelHandler

class NonRelevantSnippetDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Returns True iif the depth at which a user is in a SERP is less than a predetermined value.
    """
    def __init__(self, search_context, qrel_file, nonrelevant_limit=3):
        super(NonRelevantSnippetDecisionMaker, self).__init__(search_context)
        
        self.__counter = 0  # Counts the number of nonrelevant documents seen.
        self.__nonrelevant_limit = nonrelevant_limit  # Sets the number of nonrelevant documents seen in the SERP before giving up.
        self.__qrels = TrecQrelHandler(qrel_file)  # Our QREL handler - raises an exception if the specified file cannot be found.
    
    def decide(self):
        """
        If the user's current position in the current SERP is < the maximum depth, look at the next snippet in the SERP.
        Otherwise, a new query should be issued.
        """
        topic_no = self._search_context.get_topic().id
        snippet_doc_id = self._search_context.get_current_snippet().doc_id
        judgment = self.__qrels.get_value(topic_no, snippet_doc_id)
        
        # Reached the threshold; these results suck! Apparently.
        if self.__counter == self.__nonrelevant_limit:
            self.__counter = 0
            return Actions.QUERY
        
        if judgment > 0:
            self.__counter = 0  # Reset the counter; we found something relevant!
        else:
            self.__counter = self.__counter + 1 # This must be a nonrelevant document; one closer to giving up.
        
        return Actions.SNIPPET