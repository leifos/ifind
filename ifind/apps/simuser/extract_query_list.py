__author__ = 'leif'


import os
#from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
#from ifind.common.language_model import LanguageModel
#from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
#from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker

from ifind.search.query import Query
from search_context import SearchContext
from search_interface import WhooshInterface, Document, Topic

from query_producer import QueryProducer
import random



#def read_in_background(vocab_file):
#    vocab = {}
#    f  = open(vocab_file,'r')
#    for line in f:
#        tc = line.split(',')
#        vocab[tc[0]]=int(tc[1])
#
#    backgroundLM = LanguageModel(term_dict=vocab)
#
#    return backgroundLM

#backgroundLM = read_in_background(bg_file)
#smoothedTopicLM = BayesLanguageModel(topicLM,backgroundLM,beta=100)


class ExpLog(object):

    def __init__(self, limit=300):
        self.qc = 10
        self.dc = 20
        self.sc = 3
        self.rpc = 5
        self.total_time = 0
        self.limit = limit


    def log_query(self):
        self.total_time += self.qc
        self.report('Q')

    def log_assess(self):
        self.total_time += self.dc
        self.report('D')

    def log_snippet(self):
        self.total_time += self.sc
        self.report('S')

    def log_result_page(self):
        self.total_time += self.rpc
        self.report('R')

    def is_finished(self):
        return (self.total_time < self.limit)


    def report(self,action):
        print self.limit, self.total_time, action







class BaseUser(object):

    def __init__(self, search_interface, query_producer, tlog, topic=None):
        """
            args: Topic, SearchInterface, QueryProducer
        """

        self.si = search_interface
        self.qp = query_producer
        self.sc = None
        self.log = tlog

        if topic:
            self.start_topic(topic)


    def get_actions_performed(self):
        return self.sc.actions


    def start_topic(self, topic):
        self.topic = topic
        query_list = self.qp.produce_query_list(topic)
        self.sc = SearchContext(query_list)


    def decide_action(self):
        last_action = self.sc.get_last_action()
        # if there is no last action, it is the start, so query
        if last_action:
            # if the last action was a query, then assess
            if last_action == 'Q':
                self.do_assess()
            # else, check if 10 docs have been inspected, if not, keep assessing
            else:
                if self.sc.docs_examined >= 10:
                    self.do_query()
                else:
                    self.do_assess()
        else:
            self.do_query()


    def make_query(self, text, page=1, pagelen=100):
        q = Query(text)
        q.skip = page
        q.top = pagelen
        q.issued = False
        q.examined = 0
        q.docs_seen = []
        q.docs_rel = []
        return q


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

            response = si.issue_query(q)
            q.response = response

            self.sc.issued_query_list.append(q)
            self.sc.last_query = q
            self.log.log_result_page()
            return True
        else:
            print "out of queries"
            return False



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

        document = si.get_document(whoosh_docid)
        print "document content", document.title, document.content[0:100]
        self.sc.examined_doc_list.append(document.docid)



work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex')

si = WhooshInterface(my_whoosh_doc_index_dir)

#action_handler = { 'Q': do_query, 'D': do_assess}

stopword_file = 'data/stopwords.txt'
bg_file = 'data/vocab.txt'
topic_file = 'topic.303'

print "hello"

t = Topic('303')
t.read_topic_from_file(topic_file)
print t

qp = QueryProducer(stopword_file)

query_list = qp.produce_query_list(t)

for q in query_list:
    print q


log = ExpLog()

bu = BaseUser(si,qp,log,t)


while log.is_finished():
    bu.decide_action()

print bu.get_actions_performed()



time_limit = 500

#print "start sim"
#while sc.time_spent  <  time_limit:

#    sc = decide_action(sc)
#    action = sc.action
#    #print action
#    action_handler[action](sc)
#
#
#print "end sim"





