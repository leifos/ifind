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
import string
"""
This class is an experiment configuration parser for the page calculator
It reads a config file called experiments.ini and parses the configuration
It then constructs an appropriate query extractor and executes the queries
to calculate the retrievability of the page
"""


class ExpConfigurationParser(object):
    def __init__(self, config_file_dir):
        self.directory = config_file_dir
        #each config file directory has three config files in it, one for each search engine
        #create a list of the full path for each config file for the current directory
        self.config_files = [self.directory + "experiment_bing.ini", self.directory + "experiment_sitebing.ini", self.directory + "experiment_govuk.ini"]
        #need to set the optional values to none here to avoid errors when checking if they exist later
        self.reset()

        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        for config_file in self.config_files:
            self.current_config_file = config_file#copy current config file so it can be used in writing out results file
            self.config.read(config_file)
            self.get_config()
            self.set_engine()
            self.read_html()
            self.query_list = self.get_queries()
            self.process_queries()
            self.reset()

    def reset(self):
        """this method sets/resets optional values for a config so there's no interference between
        configs"""
        self.engine = None
        self.cache = None
        self.domain = None
        self.cutoff = None
        self.maxqueries = None
        self.doc_portion_count = None
        self.doc_portion_percent = None
        self.crawl_file = None
        self.divs = None
        self.key = None

    def get_config(self):
        self.url = self.config.get('experiment','url')
        self.engine_name = self.config.get('experiment','engine')
        if self.engine_name == 'bing' or self.engine_name== 'sitebing':
            self.key = self.config.get('experiment','key')
        if self.engine_name == 'sitebing':
            self.domain = self.config.get('experiment','domain')
        #only get the configs for cutoff queries, maxqueries, cache, doc portions if they are in the config file
        for candidate in [ 'cutoff', 'maxqueries', 'cache', 'doc_portion_percent', 'doc_portion_count']:
            if self.config.has_option('experiment',candidate):
                if candidate == 'cutoff':
                    self.cutoff = self.config.get('experiment','cutoff')
                if candidate == 'maxqueries':
                    self.maxqueries = self.config.getint('experiment','maxqueries')
                if candidate == 'cache':
                    self.cache = self.config.getboolean('experiment','cache')
                if candidate == 'doc_portion_percent':
                    self.doc_portion_percent = self.config.getint('experiment','doc_portion_perc')
                if candidate == 'doc_portion_count':
                    self.doc_portion_count = self.config.get('experiment', 'doc_portion_count')
        self.selection_type = self.config.get('experiment', 'selection_type')
        #if selection_type is ranked or position_ranked then get the crawl file
        if self.selection_type == 'ranked' or self.selection_type == 'position_ranked':
            self.crawl_file = self.config.get('experiment', 'crawl_file')
        #if selection_type is position or position_ranked get the divs
        if self.selection_type == 'position_ranked' or self.selection_type == 'position':
            self.divs = self.config.get('experiment','divs')
        self.stopwordfile = self.config.get('experiment','stopfile')
        self.query_type = self.config.get('experiment','query_type')
        #todo need to add in rank type e.g. odds
        #self.rank_type = self.config.get('experiment', 'rank_type')


    def set_engine(self):
        if self.cache:
            self.cache = 'engine'

        if self.key:
            self.engine = EngineFactory(engine=self.engine_name, api_key=self.key, throttle=0.1, cache=self.cache)
        else:
            self.engine = EngineFactory(engine=self.engine_name, cache=self.cache, throttle=0.1)

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


        prc.calculate_page_retrievability(c=20)
        #prc.report()
        summary_report = prc.output_summary_report()
        breakdown_report = prc.output_query_report()
        self.write_output_files(summary_report,breakdown_report,"cumulative")
        print "\nRetrievability Scores for cumulative pce=20 written out"

        print "\nRetrievability Scores for gravity beta=1.0"
        prc.calculate_page_retrievability(c=20, beta=1.0)
        #prc.report()
        print prc.output_summary_report()

    def write_output_files(self, summary, breakdown, scoring):
        """
        a method which writes the output files, summary and breakdown
        :return:None
        """
        summary_file = open(self.directory + "/" +self.engine_name + "_" + scoring + "_summary_report.txt","a")
        summary_file.write(summary)
        summary_file.close()

        page = self.get_page_from_url(self.url)
        print "page is ", page
        breakdown_file = open(self.directory + "/" + page + "_" + self.engine_name + "_" + scoring + "_breakdown_report.txt","w")
        breakdown_file.write(breakdown)
        breakdown_file.close()

    def get_page_from_url(self, url):
        """
        a method which takes a whole url and extracts the name of the page
        :param url:
        :return:
        """
        last_slash_pos = url.rfind("/")
        return url[last_slash_pos+1:]

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

parser = ExpConfigurationParser('/Users/rose/code/ifind/ifind/apps/calcpage/experiments/results/all/100/position/50/')







