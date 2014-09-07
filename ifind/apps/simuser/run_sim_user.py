__author__ = 'leif'

import os
#from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
#from ifind.common.language_model import LanguageModel
#from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
#from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker

from ifind.search.query import Query
from search_context import SearchContext
from search_interface import WhooshInterface, Document, Topic
from text_classifier import iFindTextClassifier
from sim_user import SimUser

from query_producer import QueryProducer, SmarterQueryProducer
import random
from exp_log import ExpLog

work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex')

si = WhooshInterface(my_whoosh_doc_index_dir)

#action_handler = { 'Q': do_query, 'D': do_assess}

stopword_file = 'data/stopwords.txt'
bg_file = 'data/vocab.txt'
topic_file = 'topic.307'


t = Topic('307')
t.read_topic_from_file(topic_file)

qp = SmarterQueryProducer(stopword_file)

query_list = qp.produce_query_list(t)

for q in query_list:
    print q


log = ExpLog(limit=750)

tc = iFindTextClassifier(stopword_file, bg_file)
tc.threshold = -0.20

bu = SimUser(si, qp, tc, log, t)

while log.is_finished():
    bu.decide_action()

al =  bu.get_actions_performed()

bu.report()

bu.save_rel_judgements('test.out')
