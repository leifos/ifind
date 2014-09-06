__author__ = 'leif'


from ifind.search.query import Query
from search_context import SearchContext
from search_interface import WhooshInterface, Document, Topic
from decision_maker import FixedDepthDecisionMaker, RandomDecisionMaker

class SimUser(object):

    def __init__(self, search_interface, query_producer, tlog, topic=None):
        """
            args: Topic, SearchInterface, QueryProducer
        """

        self.si = search_interface
        self.qp = query_producer
        self.sc = None
        self.log = tlog
        self.action_value = None
        self.dm = RandomDecisionMaker(self.si, self.sc)

        if topic:
            self.start_topic(topic)





    def get_actions_performed(self):
        return self.sc.actions


    def start_topic(self, topic):
        self.topic = topic
        query_list = self.qp.produce_query_list(topic)
        self.sc = SearchContext(query_list)
        self.dm.sc = self.sc


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
                self.do_decide()

        def _assess():
            if self.action_value:
                self.do_action('MARK')
            else:
                # look at next snip, or issue another query
                self.do_decide()


        def _mark():
            # always true.
            # look at next snip, or issue another query
            self.do_decide()

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



    def make_query(self, text, page=1, pagelen=100):
        q = Query(text)
        q.skip = page
        q.top = pagelen
        q.issued = False
        q.examined = 0
        q.docs_seen = []
        q.docs_rel = []
        return q



    def do_action(self,action_name):

        #self.sc.set_action(action_name)
        #self.log.log_action(action_name)
        action_mapping = {
            'QUERY': self.do_query,
            'SERP': self.do_serp,
            'SNIPPET': self.do_snippet,
            'DOC': self.do_assess,
            'MARK': self.do_mark_document
        }

        self.action_value = action_mapping[action_name]()



    def do_decide(self):

        if self.dm.decide():
            self.action_value = self.do_snippet()
        else:
            self.action_value = self.do_query()



    def do_query(self):
        self.sc.set_query_action()
        self.log.log_query()

        # set the query in the search context
        qc = self.sc.query_count

        if len(self.sc.query_list) > qc:
            query = self.sc.query_list[qc]
            print "query issued" , query
            self.sc.query_count += 1

            q = self.make_query(query[0],1,100)

            response = self.si.issue_query(q)
            q.response = response

            self.sc.issued_query_list.append(q)
            self.sc.last_query = q

            return True
        else:
            print "out of queries"
            return False

    def do_serp(self):
        self.log.log_result_page()
        self.sc.set_serp_action()
        return True


    def do_snippet(self):
        self.sc.set_snippet_action()
        self.log.log_snippet()
        return True


    def do_mark_document(self):
        self.sc.set_mark_action()
        pass


    def do_assess(self):
        self.sc.set_assess_action()
        self.log.log_assess()
        q= self.sc.last_query
        response = q.response
        result_list = response.results
        i = self.sc.docs_examined - 1
        # get the ith doc from the list.

        whoosh_docid = result_list[i].whooshid

        self.log.log_snippet()
        print "snippet title", result_list[i].title
        print "snippet summary", result_list[i].summary[0:50]

        document = self.si.get_document(whoosh_docid)
        print "document content", document.title, document.content[0:100]
        self.sc.examined_doc_list.append(document.docid)