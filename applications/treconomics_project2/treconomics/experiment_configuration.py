__author__ = 'leif'
import os
import logging
import logging.config
import logging.handlers
from ifind.common.autocomplete_trie import AutocompleteTrie
from ifind.search.engines.whooshtrecnews import WhooshTrecNews
from experiment_setup import ExperimentSetup

work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex')
my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file = os.path.join(work_dir, "data/TREC2005.qrels.txt")
stopword_file = os.path.join(work_dir, "data/stopwords.txt")

print "Work DIR: " + work_dir
print "QRELS File: " + qrels_file
print "my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir
print "Stopword file: " + stopword_file

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with /treconomics/startexperiment/

exp_work_flows = [
    ['/treconomics/startexperiment/','/treconomics/preexperiment/UK/',
        '/treconomics/prepracticetask/0/', '/treconomics/search/0/','/treconomics/postpracticetask/0/',
        '/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/',
        '/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/',
        '/treconomics/logout/'],
    ['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/anitademographicssurvey/',
        '/treconomics/prepracticetask/0/', '/treconomics/search/0/',
        '/treconomics/anitapretasksurvey/1/','/treconomics/search/1/','/treconomics/anitaposttask1survey/1/','/treconomics/anitaposttask2survey/1/','/treconomics/anitaposttask3survey/1/',
        '/treconomics/anitapretasksurvey/2/','/treconomics/search/2/','/treconomics/anitaposttask1survey/2/','/treconomics/anitaposttask2survey/2/','/treconomics/anitaposttask3survey/2/',
        '/treconomics/logout/'],
]


suggestion_trie = AutocompleteTrie(
                    min_occurrences=3,
                    suggestion_count=8,
                    include_stopwords=False,
                    index_path=my_whoosh_doc_index_dir,
                    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
                    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
                    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))


pl2 = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir, stopwords_file=stopword_file, model=2)

exp_fast_high = ExperimentSetup(workflow=exp_work_flows[1], engine=pl2, practice_topic='367', topics=['347', '435', ], rpp=10, interface=0, description='standard condition PL2 no delay', trie=suggestion_trie, autocomplete=True, timeout=1200)
exp_slow_high = ExperimentSetup(workflow=exp_work_flows[1], engine=pl2, practice_topic='367', topics=['347', '435', ], rpp=10, interface=0, description='standard condition PL2 increasing delays', delay_results=[0,5,10], trie=suggestion_trie, autocomplete=True, timeout=1200)


# these correspond to conditions
experiment_setups = [exp_fast_high, exp_slow_high]
