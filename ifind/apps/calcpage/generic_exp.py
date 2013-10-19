
#!/usr/bin/env python
# -*- coding: latin-1 -*-
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
from ifind.common.position_content_extractor import PositionContentExtractor
import sys

class ExperimentRunner(object):

    def __init__(self):
        self.setup()

    def setup(self):
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
        parser.add_argument("-ca", "--cache",
                      action="store_true", default=False,
                      help="use cache")
        #todo to get a number of experiments and add description to help
        parser.add_argument("-ex","--experiment", type=int, help=" experiment number 1 - x")


        args = parser.parse_args()

        if not args.url:
            print "Check your URL argument"
            parser.print_help()
            return 2
        else:
            self.url = args.url

        if not args.experiment:
            print "check your experiment number"
            parser.print_help()
            return 2
        else:
            self.experiment_num = args.experiment

        cache = None
        if args.cache:
            self.cache = 'engine'

        if args.key:
            self.engine = EngineFactory(engine=args.engine, api_key=args.key, throttle=0.1, cache=cache)
        else:
            self.engine = EngineFactory(engine=args.engine, cache=cache, throttle=0.1)


        stopwordfile = None
        if args.stopwordfile:
            self.stopwordfile = args.stopwordfile
        else:
            self.stopwordfile = None

        self.mq = 50
        if args.maxqueries:
            self.mq = args.maxqueries

        print "Fetching page: %s" % (args.url)
        pc = PageCapture(args.url)
        self.page_html = pc.get_page_sourcecode()
        print "Page loaded"

        self.run_experiment()

        print "Done!"
        return 0


    def run_experiment(self):
    #a function to extract queries from page

        if self.experiment_num == 1:
            self.exp_1()
        if self.experiment_num == 2:
            self.exp_2()

    def exp_1(self):
        text = ''
        divs = raw_input("enter IDs of the divs to exclude separated by spaces \n")
        ids = []
        if divs:
            #split string into list of IDs
            ids = divs.split()

        pce = PositionContentExtractor(div_ids=ids)
        pce.process_html_page(self.page_html)

        limit_by_words = raw_input("enter y if you want to limit by a number of words \n")
        yes_vals = ["y",'Y',"Yes",'yes']
        if limit_by_words in yes_vals:
            while True:
                words = raw_input("enter the number of words to use"
                                  "in generating queries \n")
                if self.is_integer(words):
                    words = int(words)
                    text = pce.get_subtext(num_words=words)
                    break
        else:
            limit_by_percent = raw_input("enter y if you want to limit by a percentage of words \n")
            if limit_by_percent in yes_vals:
                while True:
                    percentage = raw_input("the percentage of words to use in generating queries \n")
                    if self.is_integer(percentage):
                        percentage = int(percentage)
                        text = pce.get_subtext(percentage=percentage)
                        break
            else:
                text = pce.get_subtext()


        #todo at this stage this could be single, bi or tri terms
        query_gen = None
        if self.stopwordfile:
            query_gen = BiTermQueryGeneration(stopwordfile=self.stopwordfile)
        else:
            query_gen = BiTermQueryGeneration()

        query_list = query_gen.extract_queries_from_text(text)
        print "Queries generated: ", len(query_list)

        prc = PageRetrievabilityCalculator(engine=self.engine)
        prc.score_page(self.url, query_list)

        print "\nRetrievability Scores for cumulative pce=20"
        prc.calculate_page_retrievability(c=20)
        prc.report()
        print "\nRetrievability Scores for gravity beta=1.0"

        prc.calculate_page_retrievability(c=20, beta=1.0)
        prc.report()

    def exp_2(self):
        """
        performs experiment 2 where divs are not excluded, but included
        :return: None
        """
        text = ''
        #todo check words and percentage are ints before convert
        divs = raw_input("enter IDs of the divs to INCLUDE separated by spaces \n")
        ids = []
        if divs:
            #split string into list of IDs
            ids = divs.split()

        #set the extractor with no divs to ignore and process the page
        pce = PositionContentExtractor()
        pce.process_html_page(self.page_html)
        #now set the text of the pce to be the text from the divs with given ids
        pce.set_all_content(ids,"div")

        limit_by_words = raw_input("enter y if you want to limit by a number of words \n")
        yes_vals = ["y",'Y',"Yes",'yes']
        if limit_by_words in yes_vals:
            while True:
                words = raw_input("enter the number of words to use"
                                  "in generating queries \n")
                if self.is_integer(words):
                    words = int(words)
                    text = pce.get_subtext(num_words=words)
                    break
        else:
            limit_by_percent = raw_input("enter y if you want to limit by a percentage of words \n")
            if limit_by_percent in yes_vals:
                while True:
                    percentage = raw_input("the percentage of words to use in generating queries \n")
                    if self.is_integer(percentage):
                        percentage = int(percentage)
                        text = pce.get_subtext(percentage=percentage)
                        break
            else:
                text = pce.get_subtext()


        #todo at this stage this could be single, bi or tri terms
        query_gen = None
        if self.stopwordfile:
            query_gen = BiTermQueryGeneration(stopwordfile=self.stopwordfile)
        else:
            query_gen = BiTermQueryGeneration()
        query_list = query_gen.extract_queries_from_text(text)
        print "Queries generated: ", len(query_list)

        prc = PageRetrievabilityCalculator(engine=self.engine)
        prc.score_page(self.url, query_list)

        print "\nRetrievability Scores for cumulative pce=20"
        prc.calculate_page_retrievability(c=20)
        prc.report()
        print "\nRetrievability Scores for gravity beta=1.0"

        prc.calculate_page_retrievability(c=20, beta=1.0)
        prc.report()



    def is_integer(self, value):
        """
        checks a given value is an integer, returns true or false
        :param value:
        :return:
        """
        try:
            int(value)
            return True
        except ValueError:
            return False



def main(args):
    runner = ExperimentRunner()

if __name__ == '__main__':
    main(sys.argv)
