from sim_user import SimulatedUser
from search_interfaces import Topic
from search_context import SearchContext
from loggers.fixed_cost_logger import FixedCostLogger
from text_classifiers.ifind_classifier import IFindTextClassifier
from query_generators.smarter_generator import SmarterQueryGenerator
from search_interfaces.whoosh_interface import WhooshSearchInterface
from decision_makers.random_decision_maker import RandomDecisionMaker
from decision_makers.fixed_depth_decision_maker import FixedDepthDecisionMaker

#  Input files (configuration reader?)
stopwords = 'data/stopwords.txt'
background_vocab = 'data/vocab.txt'
topic_file = 'data/topic.307'
whoosh_index_dir = 'data/fullindex'

#  Read in the specified topic (refactor so that the Topic class takes a filename?)
topic = Topic('307')
topic.read_topic_from_file(topic_file)

#  Instantiate the query producer (could the stopwords list be an actual list, not just a filename?)
query_generator = SmarterQueryGenerator(stopwords)
query_list = query_generator.generate_query_list(topic)
#for q in query_list:
#    print q

#  Set up the logger
logger = FixedCostLogger(time_limit=200)
# from loggers import Actions  # provides a set list of actions which we can log.

# Set up the text classifier
text_classifier = IFindTextClassifier(topic, stopwords, background_vocab)
text_classifier.threshold = -0.15

# Set up additional simulation components
search_interface = WhooshSearchInterface(whoosh_index_dir)
search_context = SearchContext(search_interface=search_interface,
                               topic=topic,
                               query_list=query_list)

decision_maker = FixedDepthDecisionMaker(search_context)

# Instantiate the simulated user
user = SimulatedUser(search_context=search_context,
                     decision_maker=decision_maker,
                     logger=logger,
                     document_classifier=text_classifier,
                     snippet_classifier=text_classifier)

# Run the simulation
while not logger.is_finished():
    user.decide_action()

# Report relevance judgments
user.save_relevance_judgments('test.out')