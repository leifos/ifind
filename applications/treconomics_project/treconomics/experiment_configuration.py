__author__ = 'leif'
import os
import sys
import logging
import logging.config
import logging.handlers

work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, "data/smallindex")
my_whoosh_query_index_dir = os.path.join(work_dir,"/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file =  os.path.join(work_dir, "data/TREC2005.qrels.txt")

print "Work DIR: " + work_dir
print "QRELS File: " + qrels_file
print "my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir

# workflow must always start with /treconomics/startexperiment/

exp_work_flows = [
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/demographicssurvey/','/treconomics/searchefficacysurvey/','/treconomics/pretaskquestions/1/','/treconomics/search/1/','/treconomics/posttaskquestions/1/','/treconomics/pretaskquestions/2/','/treconomics/search/2/','/treconomics/posttaskquestions/2/','/treconomics/pretaskquestions/3/','/treconomics/search/3/','/treconomics/posttaskquestions/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/US/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/nasafactorcomparesurvey/','/treconomics/performance/','/treconomics/logout/'],
['/treconomics/startexperiment/','/treconomics/preexperiment/UK/','/treconomics/search/1/','/treconomics/search/2/','/treconomics/search/3/','/treconomics/nasaloadsurvey/','/treconomics/nasaqueryloadsurvey/','/treconomics/nasanavigationloadsurvey/','/treconomics/nasaassessmentloadsurvey/','/treconomics/performance/','/treconomics/logout/']
]

# these are the rotations of topics
# We could put a method here that reads the topics from the database table, and then automatically constructs the rotations here

rotations = [ [347, 344, 435 ], [347, 435, 344], [344, 347, 435], [344, 435, 347], [435, 347, 344], [435, 344, 347]  ]

# timeout is in seconds
timeout = 660

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log' ) )
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)




class ExperimentSetup(object):

    def __init__(self, timeout = 660, topics=['347','344','435'], rpp=10, engine=1, interface=1):
        self.timeout = timeout
        self.topics = topics
        self.rpp = rpp
        self.engine = engine

exp0 = ExperimentSetup(interface=0)
exp1 = ExperimentSetup(interface=0)
exp2 = ExperimentSetup()
exp3 = ExperimentSetup(interface=2)
exp4 = ExperimentSetup(rpp=3)
exp5 = ExperimentSetup(rpp=6)


experiment_setups = [exp0,exp1,exp2,exp3,exp4,exp5]

