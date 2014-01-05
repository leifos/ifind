
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
        parser.add_argument("-d","--domain",type=str,
                            help="domain for search engine (if applicable, i.e. engine is sitebing, default is gla.ac.uk)")
        parser.add_argument("-c","--cutoff", type=int,
                            help ="The cutoff value for queries")
        parser.add_argument("-m","--maxqueries", type=int,
                            help ="The maximum number of queries per page")
        parser.add_argument("-s","--stopwordfile", type=str,
                            help ="The filename name containing stopwords")
        parser.add_argument("-ca", "--cache",
                      action="store_true", default=False,
                      help="use cache")
        #parser.add_argument("-ex","--experiment", type=int, help=" experiment number 1 - x")
        args = parser.parse_args()

        if not args.url:
            print "Check your URL argument"
            parser.print_help()
            return 2
        else:
            self.url = args.url

        cache = None
        if args.cache:
            self.cache = 'engine'

        if args.key:
            self.engine = EngineFactory(engine=args.engine, api_key=args.key, throttle=0.1, cache=cache)
        else:
            self.engine = EngineFactory(engine=args.engine, cache=cache, throttle=0.1)

        if args.domain:
            self.engine.site = args.domain

        stopwordfile = None
        if args.stopwordfile:
            self.stopwordfile = args.stopwordfile
        else:
            self.stopwordfile = None

        self.mq = 250
        if args.maxqueries:
            self.mq = args.maxqueries

        print "Fetching page: %s" % (args.url)
        pc = PageCapture(args.url)
        self.page_html = pc.get_page_sourcecode()
        print "Page loaded"
        self.page_text = ''

        # answer = raw_input("Do you want to use a percentage of this page? Enter y or n \n")
        # if answer == 'y':
        #     percent = raw_input("What percentage do you want to use? \n")
        #     if self.is_integer(percent):
        #         self.page_text = self.reduce_page(percentage=percent)
        #     else:
        #         print "input error, will exit"
        #         sys.exit(2)
        #         #todo update so asks again, not exit
        # else:
        self.page_text = self.page_html

        query_list = []
        answer = raw_input("Do you want to use only a position based extractor? Enter y or n \n")
        if answer == 'y' or answer != 'n': #if enter is hit then assume y
            text = self.get_position_text()
            #todo at this stage this could be single, bi or tri terms
            query_gen = None
            if self.stopwordfile:
                query_gen = BiTermQueryGeneration(minlen=3, stopwordfile=self.stopwordfile)
            else:
                query_gen = BiTermQueryGeneration(minlen=3)
            query_list = query_gen.extract_queries_from_text(text)
        elif answer == 'n':
            answer = raw_input("Do you want to use only a rank based extractor? Enter y or n \n")
            if answer == 'y' or answer != 'n': #if enter is hit then assume y:
                query_list = self.get_ranked_queries()
            elif answer == 'n':
                answer = raw_input("Do you want to use a rank based extractor combined with a position extractor? Enter y or n \n")
                if answer == 'y' or answer != 'n': #if enter is hit then assume y:
                    text = self.get_position_text()
                    query_list = self.get_ranked_queries(text)
                elif answer == 'n':
                    print "sorry, that's all the options, system will exit"
                    sys.exit(0)

        print "Queries generated: ", len(query_list)
        prc = None
        if args.cutoff:
            prc = PageRetrievabilityCalculator(engine=self.engine, max_queries=self.mq)
        else:
            prc = PageRetrievabilityCalculator(engine=self.engine, max_queries=self.mq)
        prc.score_page(self.url, query_list)

        print "\nRetrievability Scores for cumulative pce=20"
        prc.calculate_page_retrievability(c=20)
        prc.report()
        print "\nRetrievability Scores for gravity beta=1.0"

        prc.calculate_page_retrievability(c=20, beta=1.0)
        prc.report()

        print "Done!"
        return 0

    def reduce_page(self, percentage):
        """
        this method reduces the whole page content to a percentage of the content
        :param percentage: the percentage of the page to be used for generating queries
        :return: the reduced page content as a string
        """
        pce = PositionContentExtractor()
        pce.process_html_page(self.page_html)
        return pce.get_subtext(percentage=percentage)

    def get_position_text(self):
        """
        This method asks the user for the div ids to include, gets the content of said divs, and then
        asks the user for a percentage of said div to use
        :return: The queries generated from the text left after above reduction
        """
        text = ''
        include_answer = raw_input("Do you want to enter divs to be included or excluded? Enter i for include, "
                                   "e for exclude")
        include = True#defaults to include
        if include_answer == 'e':
            include = False

        #todo check words and percentage are ints before convert
        divs = raw_input("enter IDs of the divs separated by spaces \n")
        ids = ['wrapper']#defaults to wrapper, overwritten if divs are entered
        if divs:
            #split string into list of IDs
            ids = divs.split()
        if include:
            #set the extractor with no divs to ignore and process the page
            pce = PositionContentExtractor()
            pce.process_html_page(self.page_html)
            #now set the text of the pce to be the text from the divs with given ids
            pce.set_all_content(ids,"div")
        else:
            pce = PositionContentExtractor(div_ids=ids)
            pce.process_html_page(self.page_html)

        limit_by_words = raw_input("enter y if you want to limit by a number of words \n")
        #defaults to no if you just hit enter
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
        return text



    def get_ranked_queries(self, text=''):
        """
        loads the background document model and generates the ranked queries
        :return: the queries in a list
        """
        if not text:
            text = self.page_html
        backgroundfile = 'background.txt'
        filename = raw_input("enter the filename of the background file, background.txt is default")
        if filename:
            backgroundfile = filename
        print "background file is ", backgroundfile

        doc_extractor = SingleQueryGeneration(minlen=3,stopwordfile=self.stopwordfile)
        query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=self.stopwordfile)
        print "Loading background distribution"
        colLM = LanguageModel(file=backgroundfile)
        print "Background loaded, number of terms: ", colLM.get_num_terms()
        #doc_extractor.extract_queries_from_html(self.page_html)
        doc_extractor.extract_queries_from_html(text)
        doc_term_counts = doc_extractor.query_count
        print "Number of terms in document: %d" % (len(doc_term_counts))
        docLM = LanguageModel(term_dict=doc_term_counts)
        slm = BayesLanguageModel(docLM=docLM, colLM=colLM, beta=500)
        #query_list = query_generator.extract_queries_from_html(self.page_html)
        query_list = query_generator.extract_queries_from_html(text)

        print "Queries generated: ", len(query_list)
        qr = OddsRatioQueryRanker(smoothed_language_model=slm)
        scored_queries = qr.calculate_query_list_probabilities(query_list)
        queries = qr.get_top_queries(self.mq)
        query_list = []
        for query in queries:
            query_list.append(query[0])
        return query_list


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
