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
from ifind.common.PageRetrievabilityCalculator import PageRetrievabilityCalculator
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
    parser.add_argument("-s","--single",type=bool,
                        help="Whether the terms to generate are single terms, True for single terms, False for double")

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        return 2
    if args.engine not in ENGINE_LIST:
        parser.print_help()
        return 2
    if args.single not in {True,False}:
        parser.print_help()
        return 2


    engine = EngineFactory(args.engine)
    prc = PageRetrievabilityCalculator(engine)
    #hard coding in that it's a url being passed in, not text
    #and that I want single queries generated, need to extend
    #to allow these args to be passed in
    prc._calculateScores(args.url, True, args.single)
    print "Done!"
    return 0

if __name__ == '__main__':
    main()