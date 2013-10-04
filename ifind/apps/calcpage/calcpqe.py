__author__ = 'rose'
import argparse
from ifind.common.page_retrievability_calc import PageRetrievabilityCalculator
from ifind.common.query_generation import SingleQueryGeneration, BiTermQueryGeneration, TriTermQueryGeneration
from ifind.common.language_model import LanguageModel
from ifind.common.smoothed_language_model import SmoothedLanguageModel, BayesLanguageModel
from ifind.search.engine import EngineFactory
from ifind.search.engines import ENGINE_LIST
from ifind.common.pagecapture import PageCapture
from ifind.common.query_ranker import QueryRanker, OddsRatioQueryRanker


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
                                description="Page Calculator for pages")
    parser.add_argument("-u", "--url", type=str,
                        help="url address")
    parser.add_argument("-e","--engine",type=str,
                        help="Name of search engine: " + ENGINE_LIST.__str__())
    parser.add_argument("-k","--key",type=str,
                        help="API Key for search engine (if applicable)")
    parser.add_argument("-c","--cutoff", type=int,
                        help ="The cutoff value for queries")
    parser.add_argument("-m","--maxqueries", type=int,
                        help ="The maximum number of queries per page")
    parser.add_argument("-s","--stopwordfile", type=str,
                        help ="The filename name containing stopwords")
    parser.add_argument("-b","--backgroundfile", type=str,
                        help ="The filename name containing background term counts")
    parser.add_argument("-ca", "--cache",
                  action="store_true", default=False,
                  help="use cache")


    args = parser.parse_args()

    if not args.url:
        print "Check your URL argument"
        parser.print_help()
        return 2

    cache = None
    if args.cache:
        cache = 'engine'

    if args.key:
        engine = EngineFactory(engine=args.engine, api_key=args.key, throttle=0.1, cache=cache)
    else:
        engine = EngineFactory(engine=args.engine, cache=cache, throttle=0.1)


    stopwordfile = None
    if args.stopwordfile:
        stopwordfile = args.stopwordfile

    mq = 50
    if args.maxqueries:
        mq = args.maxqueries

    backgroundfile = 'background.txt'
    if args.backgroundfile:
        backgroundfile = args.backgroundfile

    doc_extractor = SingleQueryGeneration(minlen=3,stopwordfile=stopwordfile)
    query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=stopwordfile, maxsize=mq)
    print "Loading background distribution"
    colLM = LanguageModel(file=backgroundfile)
    print "Background loaded, number of terms: ", colLM.get_num_terms()

    print "Fetching page: %s" % (args.url)
    pc = PageCapture(args.url)
    page_html = pc.get_page_sourcecode()
    print "Page loaded"
    doc_extractor.extract_queries_from_html(page_html)
    doc_term_counts = doc_extractor.query_count
    print "Number of terms in document: %d" % (len(doc_term_counts))
    docLM = LanguageModel(term_dict=doc_term_counts)
    slm = BayesLanguageModel(docLM=docLM, colLM=colLM, beta=500)
    query_list = query_generator.extract_queries_from_html(page_html)

    print "Queries generated: ", len(query_list)
    qr = OddsRatioQueryRanker(smoothed_language_model=slm)
    scored_queries = qr.calculate_query_list_probabilities(query_list)
    queries = qr.get_top_queries(mq)
    query_list = []
    for query in queries:
        query_list.append(query[0])


    prc = PageRetrievabilityCalculator(engine=engine)
    prc.score_page(args.url, query_list)

    print "\nRetrievability Scores for cumulative c=20"
    prc.calculate_page_retrievability(c=20)
    prc.report()
    print "\nRetrievability Scores for gravity beta=1.0"

    prc.calculate_page_retrievability(c=20, beta=1.0)
    prc.report()

    print "Done!"
    return 0

if __name__ == '__main__':
    main()