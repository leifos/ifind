__author__ = 'rose'
import ConfigParser, os
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
"""
This class is an experiment configuration parser for the page calculator
It reads a config file called experiments.ini and parses the configuration
It then constructs an appropriate query extractor and executes the queries
to calculate the retrievability of the page
"""


class ExpConfigurationParser(object):
    def __init__(self):
        self.engine = None
        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        self.config.read('experiments.ini')
        self.get_config()
        self.set_engine()
        self.read_html()
        self.query_list = self.get_queries()
        self.process_queries()

    def get_config(self):
        self.url = self.config.get('experiment','url')
        self.engine_name = self.config.get('experiment','engine')
        self.key = self.config.get('experiment','key')
        self.domain = self.config.get('experiment','domain')
        self.cutoff = self.config.get('experiment','cutoff')
        self.maxqueries = self.config.getint('experiment','maxqueries')
        self.stopwordfile = self.config.get('experiment','stopfile')
        self.cache = self.config.getboolean('experiment','cache')
        self.query_type = self.config.get('experiment','query_type')
        self.doc_portion_percent = self.config.getint('experiment','doc_portion_perc')
        self.doc_portion_count = self.config.get('experiment', 'doc_portion_count')
        self.selection_type = self.config.get('experiment', 'selection_type')
        self.rank_type = self.config.get('experiment', 'rank_type')
        self.crawl_file = self.config.get('experiment', 'crawl_file')
        self.divs = self.config.get('experiment','divs')

    def set_engine(self):
        cache = None
        if self.cache:
            self.cache = 'engine'

        if self.key:
            self.engine = EngineFactory(engine=self.engine_name, api_key=self.key, throttle=0.1, cache=cache)
        else:
            self.engine = EngineFactory(engine=self.engine_name, cache=cache, throttle=0.1)

        if self.domain:
            self.engine.site = self.domain

    def read_html(self):
        print "Fetching page: %s" % self.url
        pc = PageCapture(self.url)
        self.page_html = pc.get_page_sourcecode()
        print "Page loaded"
        self.page_text = ''
        self.page_text = self.page_html

    def get_queries(self):
        query_list =[]
        if self.selection_type == 'position':
            query_list = self.get_position_queries()
        elif self.selection_type == 'rank':
            query_list = self.get_ranked_queries()
        elif self.selection_type == 'position_ranked':
            text = self.get_position_text()
            query_list = self.get_ranked_queries(text)
        return query_list

    def set_divs(self):
        #todo splitting by letter, not by space or comma
        if self.divs:
            self.divs = self.divs.split()

    def get_position_queries(self):
        pce = PositionContentExtractor()
        pce.process_html_page(self.page_html)
        #now set the text of the pce to be the text from the divs with given ids
        self.set_divs()
        pce.set_all_content(self.divs,"div")
        #now check if to limit by words
        text =''
        if self.doc_portion_count:
            if self.is_integer(self.doc_portion_count):
                words = int(self.doc_portion_count)
                text = pce.get_subtext(num_words=words)
        elif self.doc_portion_percent:
            if self.is_integer(self.doc_portion_percent):
                percentage = int(self.doc_portion_percent)
                text = pce.get_subtext(percentage=percentage)
        else:
            text = pce.get_subtext()
        #print "text is ", text
        query_gen = None
        query_list = []
        if self.stopwordfile:
            query_gen = BiTermQueryGeneration(minlen=3, stopwordfile=self.stopwordfile)
        else:
            query_gen = BiTermQueryGeneration(minlen=3)
        query_list = query_gen.extract_queries_from_text(text)
        print query_list
        return query_list

    def get_ranked_queries(self, text=''):
        """
        loads the background document model and generates the ranked queries
        :return: the queries in a list
        """
        if not text:
            text = self.page_html
        if self.crawl_file:
            doc_extractor = SingleQueryGeneration(minlen=3,stopwordfile=self.stopwordfile)
            query_generator = BiTermQueryGeneration(minlen=3, stopwordfile=self.stopwordfile)
            print "Loading background distribution"
            colLM = LanguageModel(file=self.crawl_file)
            print "Background loaded, number of terms: ", colLM.get_num_terms()
            #doc_extractor.extract_queries_from_html(self.page_html)
            doc_extractor.extract_queries_from_html(text)
            doc_term_counts = doc_extractor.query_count
            print "Number of terms in document: %d" % (len(doc_term_counts))
            docLM = LanguageModel(term_dict=doc_term_counts)
            slm = BayesLanguageModel(docLM=docLM, colLM=colLM, beta=500)
            query_list = query_generator.extract_queries_from_html(text)

        print "Queries generated: ", len(query_list)
        qr = OddsRatioQueryRanker(smoothed_language_model=slm)
        scored_queries = qr.calculate_query_list_probabilities(query_list)
        queries = qr.get_top_queries(self.mq)
        query_list = []
        for query in queries:
            query_list.append(query[0])
        return query_list

    def process_queries(self):
        prc = None
        if self.cutoff:
            prc = PageRetrievabilityCalculator(engine=self.engine, max_queries=self.maxqueries)
        else:
            prc = PageRetrievabilityCalculator(engine=self.engine, max_queries=self.maxqueries)
        prc.score_page(self.url, self.query_list)

        print "\nRetrievability Scores for cumulative pce=20"
        prc.calculate_page_retrievability(c=20)
        #prc.report()
        print prc.output_summary_report()
        "\n individual query results"
        print prc.output_query_report()
        print "\nRetrievability Scores for gravity beta=1.0"


        prc.calculate_page_retrievability(c=20, beta=1.0)
        #prc.report()
        print prc.output_summary_report()

    def write_output_files(self):
        """
        a method which writes the output files, summary and  
        :return:None
        """

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

parser = ExpConfigurationParser()







