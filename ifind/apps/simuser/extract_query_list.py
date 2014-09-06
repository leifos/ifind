__author__ = 'leif'


import os
#from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
#from ifind.common.language_model import LanguageModel
#from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
#from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker

from ifind.search.query import Query
from search_context import SearchContext
from search_interface import WhooshInterface, Document, Topic
from sim_user import SimUser

from query_producer import QueryProducer, SmarterQueryProducer
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




work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex')

si = WhooshInterface(my_whoosh_doc_index_dir)

#action_handler = { 'Q': do_query, 'D': do_assess}

stopword_file = 'data/stopwords.txt'
bg_file = 'data/vocab.txt'
topic_file = 'topic.303'


t = Topic('303')
t.read_topic_from_file(topic_file)

qp = SmarterQueryProducer(stopword_file)

query_list = qp.produce_query_list(t)

for q in query_list:
    print q


log = ExpLog(limit=500)

bu = SimUser(si,qp,log,t)

while log.is_finished():
    bu.decide_action()

al =  bu.get_actions_performed()

for a in al:
    print a




