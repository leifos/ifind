"""
A utility which takes a url or a text string and calls PageRetrievability calculator
to generate the queries, execute against a search engine, and present retreivability scores
=============================
Author: rose <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1

Usage:
------
TODO

"""

import argparse
from ifind.common.page_retrievability_calc import PageRetrievabilityCalculator
from ifind.search.engine import EngineFactory
from ifind.search.engines import ENGINE_LIST

def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
                                description="Calculate Retrievability of Page")
    parser.add_argument("-u", "--url", type=str,
                        help="url address")
    parser.add_argument("-e","--engine",type=str,
                        help="Name of search engine: " + ENGINE_LIST.__str__())

    parser.add_argument("-k","--key",type=str,
                        help="API Key for search engine (if applicable)")

    parser.add_argument("-c","--cutoff", type=int,
                        help ="The cutoff value for queries")
    args = parser.parse_args()

    if not args.url:
        print "check your URL argument"
        parser.print_help()
        return 2
    if args.engine not in ENGINE_LIST:
        print "check your engine argument"
        parser.print_help()
        return 2


    if args.key:
        engine = EngineFactory(engine=args.engine, api_key=args.key)
    else:
        engine = EngineFactory(engine=args.engine)

    prc = PageRetrievabilityCalculator(engine, args.cutoff)
    #hard coding in that it's a url being passed in, not text
    #and that I want single queries generated, need to extend
    #to allow these args to be passed in
    print "Retrievability Score for %s :" % (args.url)
    print prc.score_page (args.url)
    print "Top 10 queries"
    ql = prc.top_queries(10)

    print "Done!"
    return 0

if __name__ == '__main__':
    main()