__author__ = 'david'

# Simple module to evaluate the performance of a given search engine over a given collection.
# Return precision metrics (e.g. p@1, p@5, rprec) for a given set of queries.

import os
import sys
import time
from ifind.search.query import Query
from ifind.search.engines.whooshtrecnewsredis import WhooshTrecNewsRedis
from ifind.seeker.trec_qrel_handler import TrecQrelHandler

# Specify variable engine as an instance of the engine you wish to use.
doc_index_dir = os.path.join(os.getcwd(), 'fullindex')
engine = WhooshTrecNewsRedis(whoosh_index_dir=doc_index_dir, use_cache=False)
#engine = WhooshTrecNewsRedis(whoosh_index_dir=doc_index_dir, use_cache=False, results_limit=False)

def print_usage():
    print "Usage: engine_perf.py <queries_file> <output_file>"
    print "   <queries_file>: Input file of queries. In format <TOPIC>-<QID> <TERMS><LINEBREAK>"
    print "   <qrels_file>:   Location to the QRELS file."
    print "   <output_file>:  Location of file for writing output. Includes column headers."

def calculate_precision(qrels, results, topic_num, k):
    """
    Returns a float representing the precision @ k for a given topic, topic_num, and set of results, results.
    """
    def get_no_relevant():
        i = 0
        rels_found = 0

        for r in results:
            i = i + 1
            val = qrels.get_value(topic_num, r.docid)
            if val > 0:
                rels_found = rels_found + 1
        return [rels_found, i]

    results = results.results[0:k]
    no_relevant = get_no_relevant()[0]
    return no_relevant / float(k)

def get_perf(queries_file, qrels_file, output_file):
    '''
    Goes and works out the performance for each query.
    '''
    qf = open(queries_file, 'r')
    of = open(output_file, 'w')

    qrels = TrecQrelHandler(qrels_file)

    for line in qf:
        line = line.strip()
        line = line.split()

        qid = line[0]
        topic = line[0].split('-')[0]
        query = ' '.join(line[1:])

        print "Query '{0}'".format(query)
        time_start = time.time()

        q = Query(query, top=100)
        q_results = engine.search(q)

        p_at_1 = calculate_precision(qrels, q_results, topic, 1)
        p_at_2 = calculate_precision(qrels, q_results, topic, 2)
        p_at_3 = calculate_precision(qrels, q_results, topic, 3)
        p_at_4 = calculate_precision(qrels, q_results, topic, 4)
        p_at_5 = calculate_precision(qrels, q_results, topic, 5)
        p_at_10 = calculate_precision(qrels, q_results, topic, 10)
        p_at_15 = calculate_precision(qrels, q_results, topic, 15)
        p_at_20 = calculate_precision(qrels, q_results, topic, 20)
        p_at_30 = calculate_precision(qrels, q_results, topic, 30)

        time_end = time.time()
        time_elapsed = time_end - time_start

        of.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}{11}".format(
            qid,
            time_elapsed,
            p_at_1,
            p_at_2,
            p_at_3,
            p_at_4,
            p_at_5,
            p_at_10,
            p_at_15,
            p_at_20,
            p_at_30,
            os.linesep
        ))

        print "{0:.3f} seconds".format(time_elapsed)
        print

    qf.close()
    of.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)
    else:
        results = get_perf(sys.argv[1], sys.argv[2], sys.argv[3])