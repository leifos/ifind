__author__ = 'leif'

import os
from ifind.search.query import Query
from search_context import SearchContext
from search_interface import WhooshInterface, Document, Topic
from decision_maker import FixedDepthDecisionMaker, RandomDecisionMaker
from text_classifier import iFindTextClassifier


class SimUser(object):

    def __init__(self, search_interface, query_producer, text_classifier, tlog, topic=None):
        """
            args: Topic, SearchInterface, QueryProducer
        """

        self.si = search_interface
        self.qp = query_producer
        self.sc = None
        self.log = tlog
        self.action_value = None
        self.dm = FixedDepthDecisionMaker(self.si, self.sc)
        self.tc = text_classifier

        if topic:
            self.start_topic(topic)

    def report(self):
        self.sc.report()


    def get_actions_performed(self):
        return self.sc.actions


    def start_topic(self, topic):
        self.topic = topic
        query_list = self.qp.produce_query_list(topic)
        self.sc = SearchContext(self.si, topic, query_list)
        self.dm.sc = self.sc
        self.tc.set_topic(topic)


    def decide_action(self):
        """ This method decides what action the user performs next.
        The work flow implemented below is as follows:

        (1) issue Query
        (2) look at SERP
        (3* Decision Point) if serp looks poor, goto (1), else goto (4)
        (4) examine Snippet
        (5* Decision Point) if snippet looks good, goto (6), else decide whether to (1) or (4)
        (6) examine document
        (7* Decision Point) if document is relevant, goto (8), else decide whether to (1) or (4)
        (8) mark document

        :return: None
        """

        def _query():
            self.do_action('SERP')

        def _serp():
            if self.action_value:
                self.do_action('SNIPPET')
            else:
                self.do_action('QUERY')

        def _snippet():
            if self.action_value:
                self.do_action('DOC')
            else:
                self.do_action(self.do_decide())

        def _assess():
            if self.action_value:
                self.do_action('MARK')
            else:
                # look at next snip, or issue another query
                self.do_action(self.do_decide())


        def _mark():
            # always true.
            # look at next snip, or issue another query
            self.do_action(self.do_decide())


        def _none():
            self.do_action('QUERY')


        last_to_next_action = {
            'QUERY': _query,
            'SERP': _serp,
            'SNIPPET': _snippet,
            'DOC': _assess,
            'MARK': _mark,
           None: _none
        }

        last_action = self.sc.get_last_action()

        last_to_next_action[last_action]()



    def issue_query(self, text, page=1, pagelen=100):
        """ Creates a Query object, issues query to the search engine, attaches response to query object
        :param text: query string
        :param page: integer
        :param pagelen: integer
        :return: ifind.search.Query
        """
        q = Query(text)
        q.skip = page
        q.top = pagelen
        response = self.si.issue_query(q)
        q.response = response

        return q

    def do_action(self, action_name):
        """ selects the method to call to perform the action,
        then logs the action in the log and the search context,
        before performing the action
        :param action_name:
        :return: None
        """
        print action_name
        action_mapping = {
            'QUERY': self.do_query,
            'SERP': self.do_serp,
            'SNIPPET': self.do_snippet,
            'DOC': self.do_assess,
            'MARK': self.do_mark_document
        }

        # Notify the log that the user has performed the action
        self.log.log_action(action_name)
        # Record in the users search context that are going to performed the action
        self.sc.set_action(action_name)
        # Perform the action,
        self.action_value = action_mapping[action_name]()


    def do_decide(self):
        """
        Decisions between looking at the next snippet, or issuing a query.
        The DecisionMaker dm is used to decide, so that different decision makers can be used.
        :return: 'SNIPPET' or 'QUERY'
        """
        if self.dm.decide():
            return 'SNIPPET'
        else:
            return 'QUERY'



    def do_query(self):
        query_text = self.sc.get_next_query()
        if query_text:
            q = self.issue_query(query_text)
            self.sc.add_issued_query(q)
            print "Issued query", query_text
            return True
        else:
            print "Out of queries"
            return False

    def do_serp(self):
        # could put a decision point in here to decide when the page is worth looking at or not.
        return True


    def do_snippet(self):
        # needs to invoker the TextClassifier to make a decision on whether the snippet is relevant or not
        # need to remember in the search context which snippet the user is now looking at
        snippet = self.sc.get_current_snippet()

        if self.sc.seen_document_before(snippet):
            # if the document has been seen before, don't examine it, i.e. return false to the decision maker
            print "Seen this doc before", snippet.docid
            #print self.sc.examined_doc_list
            return False
        else:
            # here we can check the quality of the snippet is it indicative of relevance?
            # if so, return True, else, return False (ie. don't inspect document)
            if self.tc.is_relevant(snippet):
                print "Snippet seems relevant", snippet.docid
                return True
            else:
                return False

    def do_mark_document(self):
        return True


    def do_assess(self):

        if self.sc.get_last_query():
            document = self.sc.get_current_document()
            print "examining document", document.docid
            if self.tc.is_relevant(document):
                print "found relevant", document.docid
                self.sc.relevant_doc_list.append(document.docid)
                return True
            else:
                self.sc.docs_not_relevant += 1
                return False
        else:
            return False



    def save_rel_judgements(self, filename):
        f = open(filename,"w")
        rank = 0
        for i in self.sc.relevant_doc_list:
            rank += 1
            f.write( "{0} QO {1} {2} {3} Exp {4}".format(self.topic.id, i, rank, rank, os.linesep))
        f.close()