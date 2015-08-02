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
    work_dir = '/opt/tango/ifind/applications/treconomics_project3/'

my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/test100index/')
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
event_logger.setLevel(logging.WARNING)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with /treconomics/startexperiment/

exp_work_flows = [
    ['/treconomics/startexperiment/', '/treconomics/preexperiment/UK/',
     '/treconomics/prepracticetask/0/', '/treconomics/search/0/', '/treconomics/postpracticetask/0/',
     '/treconomics/pretaskquestions/1/', '/treconomics/search/1/', '/treconomics/posttaskquestions/1/',
     '/treconomics/pretaskquestions/2/', '/treconomics/search/2/', '/treconomics/posttaskquestions/2/',
     '/treconomics/pretaskquestions/3/', '/treconomics/search/3/', '/treconomics/posttaskquestions/3/',
     '/treconomics/logout/'],
    ['/treconomics/startexperiment/', '/treconomics/consent', '/treconomics/preexperiment/AN/',
     '/treconomics/prepracticetask/0/', '/treconomics/search/0/', '/treconomics/postpracticetask/0/',
     '/treconomics/anitatimeinstructions/TC/',
     '/treconomics/anitapretasksurvey/1/', '/treconomics/search/1/', '/treconomics/anitaposttask0survey/1/',
     '/treconomics/anitaposttask1survey/1/', '/treconomics/anitaposttask2survey/1/',
     '/treconomics/anitaposttask3survey/1/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/2/', '/treconomics/search/2/', '/treconomics/anitaposttask0survey/2/',
     '/treconomics/anitaposttask1survey/2/', '/treconomics/anitaposttask2survey/2/',
     '/treconomics/anitaposttask3survey/2/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/3/', '/treconomics/search/3/', '/treconomics/anitaposttask0survey/3/',
     '/treconomics/anitaposttask1survey/3/', '/treconomics/anitaposttask2survey/3/',
     '/treconomics/anitaposttask3survey/3/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/4/', '/treconomics/search/4/', '/treconomics/anitaposttask0survey/4/',
     '/treconomics/anitaposttask1survey/4/', '/treconomics/anitaposttask2survey/4/',
     '/treconomics/anitaposttask3survey/4/',
     '/treconomics/anitaexit1survey/', '/treconomics/anitaexit2survey/', '/treconomics/anitaexit3survey/',
     '/treconomics/anitademographicssurvey/', '/treconomics/logout/'],
    ['/treconomics/startexperiment/', '/treconomics/consent', '/treconomics/preexperiment/AN/',
     '/treconomics/prepracticetask/0/', '/treconomics/search/0/', '/treconomics/postpracticetask/0/',
     '/treconomics/anitatimeinstructions/NTC/',
     '/treconomics/anitapretasksurvey/1/', '/treconomics/search/1/', '/treconomics/anitaposttask0survey/1/',
     '/treconomics/anitaposttask1survey/1/', '/treconomics/anitaposttask2survey/1/',
     '/treconomics/anitaposttask3survey/1/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/2/', '/treconomics/search/2/', '/treconomics/anitaposttask0survey/2/',
     '/treconomics/anitaposttask1survey/2/', '/treconomics/anitaposttask2survey/2/',
     '/treconomics/anitaposttask3survey/2/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/3/', '/treconomics/search/3/', '/treconomics/anitaposttask0survey/3/',
     '/treconomics/anitaposttask1survey/3/', '/treconomics/anitaposttask2survey/3/',
     '/treconomics/anitaposttask3survey/3/', '/treconomics/taskspacer/',
     '/treconomics/anitapretasksurvey/4/', '/treconomics/search/4/', '/treconomics/anitaposttask0survey/4/',
     '/treconomics/anitaposttask1survey/4/', '/treconomics/anitaposttask2survey/4/',
     '/treconomics/anitaposttask3survey/4/',
     '/treconomics/anitaexit1survey/', '/treconomics/anitaexit2survey/', '/treconomics/anitaexit3survey/',
     '/treconomics/anitademographicssurvey/', '/treconomics/logout/'],
    ['/treconomics/startexperiment/', '/treconomics/consent', '/treconomics/preexperiment/AN/',
     '/treconomics/anitaexit1survey/', '/treconomics/anitaexit2survey/', '/treconomics/anitaexit3survey/',
     '/treconomics/anitademographicssurvey/', '/treconomics/logout/'],
]

suggestion_trie = AutocompleteTrie(
    min_occurrences=3,
    suggestion_count=8,
    include_stopwords=False,
    index_path=my_whoosh_doc_index_dir,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))

bm25 = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir, stopwords_file=stopword_file, model=1, newschema=True)
bm25.key_name = 'bm25'

exp_test = ExperimentSetup(workflow=exp_work_flows[0],
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
                           timeout=300)


# these correspond to conditions
experiment_setups = [exp_test]
