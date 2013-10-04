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
from ifind.common.position_query_extractor import PositionQueryExtractor

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
        parser = argparse.ArgumentParser(
                                    description="Experiment specifics parser")
        if self.experiment_num == 1:
            parser.add_argument("-d", "--divs", type=str,
                            help="IDs of the divs to exclude separated by spaces")
            parser.add_argument("-w", "--words", type=int, help="the number of words to use"
                                "in generating queries")
            parser.add_argument("-p", "--percentage", type=int, help="the percentage of words"
                                                        "to use in generating queries")
            args = parser.parse_args()
            ids = []
            if args.divs:
                #split string into list of IDs
                ids = args.divs.split()

            pqe = PositionQueryExtractor(html=self.page_html, div_ids=ids)
            content = pqe.remove_div_content()
            text = ""
            if args.words:
                text = pqe.get_subtext(text=content, num_words=args.words)
            elif args.percentage:
                text = pqe.get_subtext(text=content,percentage=args.percentage)
            else:
                text = pqe.get_subtext(text=content)

            query_list = pqe.generate_queries(text)
            print "Queries generated: ", len(query_list)

            prc = PageRetrievabilityCalculator(engine=self.engine)
            prc.score_page(args.url, query_list)

            print "\nRetrievability Scores for cumulative c=20"
            prc.calculate_page_retrievability(c=20)
            prc.report()
            print "\nRetrievability Scores for gravity beta=1.0"

            prc.calculate_page_retrievability(c=20, beta=1.0)
            prc.report()




# if __name__ == '__main__':
#     runner = ExperimentRunner()
