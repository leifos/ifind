__author__ = 'leif'

from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
from ifind.common.language_model import LanguageModel
from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker

from ifind.search.engine import Engine, EngineFactory
from ifind.search.query import Query

def features(sentence):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)

engine = EngineFactory(engine="dummy")

stopword_file = 'stopwords.txt'
topic_file = 'topic.303'

doc_extractor = SingleQueryGeneration(minlen=3,stopwordfile=stopword_file)
query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=stopword_file)

topic_text = ''
if topic_file:
    f = open(topic_file, 'r')
    for line in f:
        topic_text+= ' ' + line


doc_extractor.extract_queries_from_text(topic_text)
doc_term_counts = doc_extractor.query_count
docLM = LanguageModel(term_dict=doc_term_counts)

query_generator = TriTermQueryGeneration(minlen=3, stopwordfile=stopword_file)

bi_query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=stopword_file)

query_list = query_generator.extract_queries_from_text(topic_text)
bi_query_list = bi_query_generator.extract_queries_from_text(topic_text)

qlist = query_list + bi_query_list

qr = QueryRanker(smoothed_language_model=docLM)
scored_queries = qr.calculate_query_list_probabilities(qlist)
queries = qr.get_top_queries(10)


for q in queries:
    print q
raw_input("hit return to continue")


for q in queries:
    tq = Query(q[0])
    print q[0]
    response = engine.search(tq)

    for r in response:
        # does the snippet match topic?
        print r.summary

    #print response
# take query from list



# submit query to engine

# inspect snippet, decide if relevant,

# if snippet is relevant, inspect document


