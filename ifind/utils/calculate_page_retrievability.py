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

def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
                                description="Calculate Retrievability of Page")
    parser.add_argument("-u", "--url", type=str,
                        help="url address")

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        return 2
    else:

        engine = EngineFactory('govuk')
        prc = PageRetrievabilityCalculator(engine)
        prc.calculateScore(args.url)
        print "Done!"
        return 0

if __name__ == '__main__':
    main()