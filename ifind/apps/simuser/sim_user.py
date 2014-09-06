__author__ = 'leif'


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


    def get_actions_performed(self):
        return self.sc.actions


    def start_topic(self, topic):
        self.topic = topic
        query_list = self.qp.produce_query_list(topic)
        self.sc = SearchContext(query_list)
        self.dm.sc = self.sc
        self.tc.set_topic(topic)


    def decide_action(self):

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
        q = Query(text)
        q.skip = page
        q.top = pagelen
        response = self.si.issue_query(q)
        q.response = response

        return q



    def do_action(self, action_name):

        #self.sc.set_action(action_name)
        #self.log.log_action(action_name)
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
        if self.dm.decide():
            return 'SNIPPET'
        else:
            return 'QUERY'



    def do_query(self):
        query_text = self.sc.get_next_query()
        if query_text:
            q = self.issue_query(query_text)
            self.sc.add_issued_query(q)
            return True
        else:
            print "Out of queries"
            return False

    def do_serp(self):

        return True


    def do_snippet(self):
        # needs to invoker the TextClassifier to make a decision on whether the snippet is relevant or not
        # need to remember in the search context which snippet the user is now looking at
        return True


    def do_mark_document(self):
        return True


    def do_assess(self):
        q = self.sc.last_query
        response = q.response
        result_list = response.results
        i = self.sc.docs_examined - 1
        # get the ith doc from the list.

        whoosh_docid = result_list[i].whooshid
        document = self.si.get_document(whoosh_docid)
        self.sc.examined_doc_list.append(document.docid)

        if self.tc.is_relevant(document):
            print "found relevant", document.docid
            self.sc.relevant_doc_list.append(document.docid)
            return True
        else:
            self.sc.docs_not_relevant += 1
            return False

        #print "document content", document.title, document.content[0:100]
