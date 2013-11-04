__author__ = 'leif'
import os
import sys
import logging
import logging.config
import logging.handlers
from ifind.common.rotation_ordering import PermutatedRotationOrdering
from django.conf import settings
#from ifind.common.suggestion_trie import SuggestionTrie

work_dir = os.getcwd()
my_whoosh_doc_index_dir = settings.INDEX_PATH
my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file =  os.path.join(work_dir, "data/TREC2005.qrels.txt")

print "Work DIR: " + work_dir
print "QRELS File: " + qrels_file
print "my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir

# Setup an instance of the suggestion trie to ensure everything required is present.
'''
SuggestionTrie.initialise_files(
    index_path=my_whoosh_doc_index_dir,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat")
)
'''

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log' ) )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with /treconomics/startexperiment/

exp_work_flows = [
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/pretaskquestions/1/','/treconomics/ajax_search/1/','/treconomics/posttask/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttask/2/','/treconomics/logout/']
]

class ExperimentSetup(object):

    def __init__(self, workflow, timeout=660, topics=['999', '347', '344'], rpp=10, engine=1, interface=1, description='', popup_width=None, popup_height=None, delay_results=0, enable_ajax_suggestions=False):
        self.timeout = timeout
        self.topics = topics
        self.rpp = rpp
        self.interface = interface
        self.engine = engine
        self.description = description
        self.workflow = workflow
        self.pro = PermutatedRotationOrdering()
        self.n = self.pro.number_of_orderings(self.topics)

        # Two additional instance variables to control the width and height of the experiment popup box.
        self.popup_width = popup_width
        self.popup_height = popup_height

        # Instance variable to allow you to delay results from appearing.
        # Specify an integer or float value. The value specifies the number of seconds the delay should last for.
        # If 0, there is no delay.
        self.delay_results = delay_results

        # Do you want to use AJAX suggestions if the AJAX search interface is used?
        self.enable_ajax_suggestions = enable_ajax_suggestions

    def _get_check_i(self, i):
        return i % self.n

    def get_rotations(self, i):
        """ get the ith rotation from the topics
        :param i:
        :return: returns the list of topic numbers
        """
        ith = self._get_check_i(i)
        return self.pro.get_ordering(self.topics, ith)

    def get_rotation_topic(self, i, t):
        """ get the ith rotation and the tth topic
        :param i: integer
        :param t: integer
        :return: returns the topic number
        """
        ith = self._get_check_i(i)
        rotations = self.pro.get_ordering(self.topics, ith)
        return rotations[t]

    def get_interface(self, i=0):
        return self.interface

    def __str__(self):
        return self.description

exp0 = ExperimentSetup(workflow=exp_work_flows[4], interface=0, description='structured condition')
exp1 = ExperimentSetup(workflow=exp_work_flows[4], interface=1, description='structured condition', delay_results=3, enable_ajax_suggestions=True)
exp2 = ExperimentSetup(workflow=exp_work_flows[4], description='standard condition')
exp3 = ExperimentSetup(workflow=exp_work_flows[4], interface=2, description='suggestion condition')
exp4 = ExperimentSetup(workflow=exp_work_flows[4], topics=['344', '347', ], rpp=10, interface=1, description='structured condition')
exp5 = ExperimentSetup(workflow=exp_work_flows[4], topics=['344', '347', ], rpp=10, interface=0, description='standard condition')

# these correspond to conditions
experiment_setups = [exp0, exp1, exp2, exp3, exp4, exp5]
