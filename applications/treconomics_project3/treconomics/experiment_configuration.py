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
# when deployed this needs to match up with the hostname, and directory to where the project is

if socket.gethostname() == 'newssearch':
    work_dir = '~/ifind/applications/treconomics_project3/'

my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex/')
my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file = os.path.join(work_dir, "data/TREC2005.qrels.txt")
stopword_file = os.path.join(work_dir, "data/stopwords.txt")
data_dir = os.path.join(work_dir, "data")

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

# workflow must always start with startexperiment/

exp_work_flows = [
    ['startexperiment/', 'preexperiment/UK/',
     'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
     'pretaskquestions/1/', 'search/1/', 'mickeyposttask/1/',
     'pretaskquestions/2/', 'search/2/', 'mickeyposttask/2/',
     'pretaskquestions/3/', 'search/3/', 'mickeyposttask/3/',
     'logout/'],
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
     'anitatimeinstructions/TC/',
     'anitapretasksurvey/1/', 'search/1/', 'anitaposttask0survey/1/',
     'anitaposttask1survey/1/', 'anitaposttask2survey/1/',
     'anitaposttask3survey/1/', 'taskspacer/',
     'anitapretasksurvey/2/', 'search/2/', 'anitaposttask0survey/2/',
     'anitaposttask1survey/2/', 'anitaposttask2survey/2/',
     'anitaposttask3survey/2/', 'taskspacer/',
     'anitapretasksurvey/3/', 'search/3/', 'anitaposttask0survey/3/',
     'anitaposttask1survey/3/', 'anitaposttask2survey/3/',
     'anitaposttask3survey/3/', 'taskspacer/',
     'anitapretasksurvey/4/', 'search/4/', 'anitaposttask0survey/4/',
     'anitaposttask1survey/4/', 'anitaposttask2survey/4/',
     'anitaposttask3survey/4/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
     'anitatimeinstructions/NTC/',
     'anitapretasksurvey/1/', 'search/1/', 'anitaposttask0survey/1/',
     'anitaposttask1survey/1/', 'anitaposttask2survey/1/',
     'anitaposttask3survey/1/', 'taskspacer/',
     'anitapretasksurvey/2/', 'search/2/', 'anitaposttask0survey/2/',
     'anitaposttask1survey/2/', 'anitaposttask2survey/2/',
     'anitaposttask3survey/2/', 'taskspacer/',
     'anitapretasksurvey/3/', 'search/3/', 'anitaposttask0survey/3/',
     'anitaposttask1survey/3/', 'anitaposttask2survey/3/',
     'anitaposttask3survey/3/', 'taskspacer/',
     'anitapretasksurvey/4/', 'search/4/', 'anitaposttask0survey/4/',
     'anitaposttask1survey/4/', 'anitaposttask2survey/4/',
     'anitaposttask3survey/4/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
]

mickeys_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'demographicssurvey/UK/',
    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
    'anitapretasksurvey/1/', 'search/1/', 'mickeyposttask/1/',
    'anitapretasksurvey/2/', 'search/2/', 'mickeyposttask/2/',
    'anitapretasksurvey/3/', 'search/3/', 'mickeyposttask/3/',
    'logout/'
]

test_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
    'anitapretasksurvey/1/', 'search/1/', 'mickeyposttask/1/',
    'anitapretasksurvey/2/', 'search/2/', 'mickeyposttask/2/',
    'anitapretasksurvey/3/', 'search/3/', 'mickeyposttask/3/',
    'logout/'
]

suggestion_trie = AutocompleteTrie(
    min_occurrences=3,
    suggestion_count=8,
    include_stopwords=False,
    index_path=my_whoosh_doc_index_dir,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))

bm25 = WhooshTrecNews(
    whoosh_index_dir=my_whoosh_doc_index_dir,
    stopwords_file=stopword_file,
    model=1,
    newschema=True)

bm25.key_name = 'bm25'

exp_test = ExperimentSetup(
    workflow=mickeys_flow,
    engine=bm25,
    practice_topic='341',
    topics=['347', '367', '354'],
    rpp=10,
    practice_interface=1,
    interface=[1, 2, 3],
    rotation_type=1,
    description='standard condition bm25 test',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=1200)  # 300s = 5min; 600s = 10min; 1200s = 20min


# these correspond to conditions
experiment_setups = [exp_test]
