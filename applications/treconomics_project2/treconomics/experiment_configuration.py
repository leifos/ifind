__author__ = 'leif'
import os
import socket
import logging
import logging.config
import logging.handlers
from ifind.common.autocomplete_trie import AutocompleteTrie
from ifind.search.engines.whooshtrecnews import WhooshTrecNews
from experiment_setup import ExperimentSetup

work_dir = os.getcwd()
if socket.gethostname() =='newssearch':
    work_dir = '/opt/tango/ifind/applications/treconomics_project2/'
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
    ['/treconomics/startexperiment/','/treconomics/consent','/treconomics/preexperiment/AN/',
        '/treconomics/prepracticetask/0/', '/treconomics/search/0/', '/treconomics/postpracticetask/0/', '/treconomics/anitatimeinstructions/TC/',
        '/treconomics/anitapretasksurvey/1/','/treconomics/search/1/','/treconomics/anitaposttask0survey/1/','/treconomics/anitaposttask1survey/1/','/treconomics/anitaposttask2survey/1/','/treconomics/anitaposttask3survey/1/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/2/','/treconomics/search/2/','/treconomics/anitaposttask0survey/2/','/treconomics/anitaposttask1survey/2/','/treconomics/anitaposttask2survey/2/','/treconomics/anitaposttask3survey/2/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/3/','/treconomics/search/3/','/treconomics/anitaposttask0survey/3/','/treconomics/anitaposttask1survey/3/','/treconomics/anitaposttask2survey/3/','/treconomics/anitaposttask3survey/3/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/4/','/treconomics/search/4/','/treconomics/anitaposttask0survey/4/','/treconomics/anitaposttask1survey/4/','/treconomics/anitaposttask2survey/4/','/treconomics/anitaposttask3survey/4/',
        '/treconomics/anitaexit1survey/','/treconomics/anitaexit2survey/','/treconomics/anitaexit3survey/',
        '/treconomics/anitademographicssurvey/','/treconomics/logout/'],
    ['/treconomics/startexperiment/','/treconomics/consent','/treconomics/preexperiment/AN/',
        '/treconomics/prepracticetask/0/', '/treconomics/search/0/', '/treconomics/postpracticetask/0/', '/treconomics/anitatimeinstructions/NTC/',
        '/treconomics/anitapretasksurvey/1/','/treconomics/search/1/','/treconomics/anitaposttask0survey/1/','/treconomics/anitaposttask1survey/1/','/treconomics/anitaposttask2survey/1/','/treconomics/anitaposttask3survey/1/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/2/','/treconomics/search/2/','/treconomics/anitaposttask0survey/2/','/treconomics/anitaposttask1survey/2/','/treconomics/anitaposttask2survey/2/','/treconomics/anitaposttask3survey/2/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/3/','/treconomics/search/3/','/treconomics/anitaposttask0survey/3/','/treconomics/anitaposttask1survey/3/','/treconomics/anitaposttask2survey/3/','/treconomics/anitaposttask3survey/3/','/treconomics/taskspacer/',
        '/treconomics/anitapretasksurvey/4/','/treconomics/search/4/','/treconomics/anitaposttask0survey/4/','/treconomics/anitaposttask1survey/4/','/treconomics/anitaposttask2survey/4/','/treconomics/anitaposttask3survey/4/',
        '/treconomics/anitaexit1survey/','/treconomics/anitaexit2survey/','/treconomics/anitaexit3survey/',
        '/treconomics/anitademographicssurvey/','/treconomics/logout/'],
    ['/treconomics/startexperiment/','/treconomics/consent','/treconomics/preexperiment/AN/',
        '/treconomics/anitaexit1survey/','/treconomics/anitaexit2survey/','/treconomics/anitaexit3survey/',
        '/treconomics/anitademographicssurvey/','/treconomics/logout/'],
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
pl2.key_name = 'pl2'

exp_no_time_constraint_delay  = ExperimentSetup(workflow=exp_work_flows[2], engine=pl2, practice_topic='341', topics=['347', '367', '383', '435', ], rpp=10, interface=0, description='standard condition PL2 alt delay', delay_results=[0,5,0,5,0],delay_docview=[0,5,0,5,0], trie=suggestion_trie, autocomplete=True, timeout=0)
exp_time_constraint_delay = ExperimentSetup(workflow=exp_work_flows[1], engine=pl2, practice_topic='341', topics=['347', '367', '383', '435', ], rpp=10, interface=0, description='standard condition PL2 alt delays', delay_results=[0,5,0,5,0],delay_docview=[0,5,0,5,0], trie=suggestion_trie, autocomplete=True, timeout=300)
exp_test = ExperimentSetup(workflow=exp_work_flows[3], engine=pl2, practice_topic='341', topics=['347', '367', '383', '435', ], rpp=10, interface=0, description='standard condition PL2 test', delay_results=[0,0,0,0,0],delay_docview=[0,0,0,0,0], trie=suggestion_trie, autocomplete=True, timeout=300)


# these correspond to conditions
experiment_setups = [exp_no_time_constraint_delay, exp_time_constraint_delay, exp_test]
