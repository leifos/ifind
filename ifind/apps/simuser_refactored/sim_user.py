import os
from loggers import Actions

class SimulatedUser(object):
    """
    
    """
    def __init__(self, search_context, decision_maker, logger, document_classifier, snippet_classifier):
        """
        """
        self.__search_context = search_context
        self.__decision_maker = decision_maker
        self.__logger = logger
        self.__document_classifier = document_classifier
        self.__snippet_classifier = snippet_classifier
        
        self.__action_value = None  # Response from the appropriate action method - True or False?
    
    def decide_action(self):
        """
        This method is central to the whole simulation - it decides which action the user should perform next.
        The workflow implemented below is as follows. Steps with asterisks are DECISION POINTS.
        
        (1)  User issues query
        (2)  User looks at the SERP
        (3*) If the SERP looks poor, goto (1) else goto (4)
        
        (4)  Examine a snippet
        (5*) If the snippet looks at least somewhat relevant, goto (6) else decide whether to goto (1) or (4)
        
        (6)  Examine document
        (7*) If the document looks to be relevant to the provided topic, goto (8), else decide whether to goto (1) or (4)
        
        (8)  Mark the document
        (9*) Decide whether to goto (1) or (4)
        
        This method returns no value.
        """
        def after_query():
            self.__do_action(Actions.SERP)
        
        def after_serp():
            if self.__action_value:
                self.__do_action(Actions.SNIPPET)
            else:
                self.__do_action(Actions.QUERY)
        
        def after_snippet():
            if self.__action_value:
                self.__do_action(Actions.DOC)
            else:
                self.__do_action(self.__do_decide())
        
        def after_assess_document():
            if self.__action_value:
                self.__do_action(Actions.MARK)
            else:
                self.__do_action(self.__do_decide())
        
        def after_mark():
            """
            This condition will always be True; we won't get here unless the document has been successfully marked!
            After the document has been marked, the user must decide whether (s)he wants to look at the subsequent snippet, or issue another query.
            """
            self.__do_action(self.__do_decide())
        
        def after_none():
            """
            If no action has been supplied from before, then we must be at the start of the search session.
            Therefore, we begin by querying.
            """
            self.__do_action(Actions.QUERY)
        
        last_to_next_action_mapping = {
            Actions.QUERY  : after_query,
            Actions.SERP   : after_serp,
            Actions.SNIPPET: after_snippet,
            Actions.DOC    : after_assess_document,
            Actions.MARK   : after_mark,
            None           : after_none
        }
        
        last_action = self.__search_context.get_last_action()
        last_to_next_action_mapping[last_action]()
    
    def __do_action(self, action):
        """
        Selects the appropriate method to call to execute the requested action, then logs the interaction in the log and search context.
        This method returns None.
        """
        action_mapping = {
            Actions.QUERY  : self.__do_query,
            Actions.SERP   : self.__do_serp,
            Actions.SNIPPET: self.__do_snippet,
            Actions.DOC    : self.__do_assess_document,
            Actions.MARK   : self.__do_mark_document
        }
        
        # Log - first telling the logger of the action, and then the search context.
        self.__logger.log_action(action)
        self.__search_context.set_action(action)
        
        # Now call the appropriate method to perform the action.
        self.__action_value = action_mapping[action]()
    
    def __do_query(self):
        """
        Called when the simulated user wishes to issue another query.
        This works by calling the search context for the subsequent query text, and is then issued to the search interface by the search context on behalf of the user.
        If no further queries are available, the logger is told of this - and the simulation will then stop at the next iteration.
        """
        query_text = self.__search_context.get_next_query()
        
        if query_text:
            print "Issued query '{0}'".format(query_text)
            self.__search_context.add_issued_query(query_text)  # Can also supply page number and page lengths here/
            return True
        
        print "Out of queries"
        # Tells the logger that there are no remaining queries; the logger will then stop the simulation.
        self.__logger.queries_exhausted()
        return False
    
    def __do_serp(self):
        """
        Called when the simulated user wishes to examine a SERP - the "initial glance" - after issuing a query.
        At present, the user will always move to examine the first snippet of the SERP - but a decision can be included here to do otherwise.
        """
        return True
    
    def __do_snippet(self):
        """
        Called when the user needs to make the decision whether to examine a snippet or not.
        The logic within this method supports previous observations of the same document, and whether the text within the snippet appears to be relevant.
        """
        snippet = self.__search_context.get_current_snippet()
        
        if self.__search_context.get_document_observation_count(snippet) > 0:
            # This document has been previously seen; so we ignore it. But the higher the count, cumulated credibility could force us to examine it?
            print "Seen this document before", snippet.doc_id
            self.__search_context.increment_serp_position()
            return False
        else:
            # This snippet has not been previously seen; check quality of snippet. Does it show some form of relevance?
            # If so, we return True - and if not, we return False, which moves the simulator to the next step.
            if self.__snippet_classifier.is_relevant(snippet):
                print "Snippet seems relevant, go look at it", snippet.doc_id
                return True
            else:
                self.__search_context.increment_serp_position()
                return False
    
    def __do_assess_document(self):
        """
        Called when a document is to be assessed.
        """
        if self.__search_context.get_last_query():
            document = self.__search_context.get_current_document()
            print "Examining document", document.doc_id
            
            if self.__document_classifier.is_relevant(document):
                print "Document considered relevant", document.doc_id
                self.__search_context.add_relevant_document(document)
                self.__search_context.increment_serp_position()
                return True
            else:
                self.__search_context.add_irrelevant_document(document)
                self.__search_context.increment_serp_position()
                return False
        
        return False
    
    def __do_mark_document(self):
        """
        The outcome of marking a document as relevant. At this stage, the user has decided that the document is relevant; hence True can be the only result.
        """
        return True
    
    def __do_decide(self):
        """
        Method which returns whether a further snippet should be examined, or the next query should be issued.
        This is the "decision making" logic - and makes use of the predefined DecisionMaker instance to work this out (with the search context available to it).
        The method also determines if we have reached the end of the SERP - if we have, the only action available to the user is to query (at the moment).
        """
        
        print self.__search_context.reached_end_of_serp()
        
        
        if self.__search_context.reached_end_of_serp():
            return Actions.QUERY
        
        if self.__decision_maker.decide():
            return Actions.SNIPPET
        
        return Actions.QUERY
    
    def save_relevance_judgments(self, output_filename):
        """
        Saves relevance judgments to the filename specified by parameter output_filename.
        """
        f = open(output_filename, 'w')
        topic = self.__search_context.get_topic()
        rank = 0
        
        for document in self.__search_context.get_relevant_documents():
            rank = rank + 1
            f.write("{0} Q0 {1} {2} {3} Exp{4}".format(topic.id, document.doc_id, rank, rank, os.linesep))
        
        f.close()