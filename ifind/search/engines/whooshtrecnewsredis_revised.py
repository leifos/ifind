__author__ = 'david'

from operator import itemgetter

from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound
from whoosh.index import open_dir, EmptyIndexError
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter

from ifind.seeker.list_reader import ListReader
from ifind.search.engine import Engine
from ifind.search.cache import RedisConn
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException

import os
import time

class WhooshTrecNewsRedis(Engine):
    """
    A revised Whoosh ifind engine.
    Implemented by dmax. Uses a new way of poking the postings file by @leifos, and also some tasty Redis caching.
    """
    def __init__(self, whoosh_index_dir='', stopwords_file='', cache_host='localhost', cache_port=6379, **kwargs):
        Engine.__init__(self, **kwargs)

        self.whoosh_index_dir = whoosh_index_dir
        if not self.whoosh_index_dir:
            raise EngineConnectionException(self.name, "'whoosh_index_dir=' keyword argument not specified")

        self.stopwords_file = stopwords_file
        if self.stopwords_file:
            self.stopwords = ListReader(self.stopwords_file)  # Open the stopwords file, read into a ListReader
        else:
            raise EngineConnectionException(self.name, "'stopwords_file=' keyword argument not specified")

        self.scoring_model_identifier = 1
        self.scoring_model = scoring.PL2(c=10.0)
        
        self.__verbose = False

        try:
            self.doc_index = open_dir(self.whoosh_index_dir)
            self.reader = self.doc_index.reader()
            self.parser = QueryParser('content', self.doc_index.schema)  # By default, we use AND grouping.
                                                                         # Use the grouping parameter and specify whoosh.qparser.OrGroup, etc...

            #  Objects required for document snippet generation
            self.analyzer = self.doc_index.schema[self.parser.fieldname].analyzer
            self.fragmenter = ContextFragmenter(maxchars=200, surround=40)
            self.formatter = HtmlFormatter()
        except EmptyIndexError:
            message = "Could not open Whoosh index at '{0}'".format(self.whoosh_index_dir)
            raise EngineConnectionException(self.name, message)
        except OSError:
            message = "Could not open Whoosh index at '{0}' - directory does not exist".format(self.whoosh_index_dir)
            raise EngineConnectionException(self.name, message)

        # Attempt to connect to the specified Redis cache.
        self.cache = RedisConn(host=cache_host, port=cache_port)
        self.cache.connect()

    def _search(self, query):
        """
        The concrete search method.
        """
        self.__parse_query_terms(query)

        with self.doc_index.searcher(weighting=self.scoring_model) as searcher:
            doc_scores = {}

            if isinstance(query.parsed_terms, unicode):
                t = time.time()
                doc_term_scores = self.__get_doc_term_scores(searcher, query.parsed_terms)
                t = time.time() - t
                
                if self.__verbose:
                    print "  > Retrieve results for '{0}': {1}".format(query.parsed_terms, t)

                t = time.time()
                self.__update_scores(doc_scores, doc_term_scores)
                t = time.time() - t
                
                if self.__verbose:
                    print "  >> Time to update scores: {0}".format(t)
            else:
                try:
                    for term in query.parsed_terms:
                        t = time.time()
                        doc_term_scores = self.__get_doc_term_scores(searcher, term.text)
                        t = time.time() - t
                        
                        if self.__verbose:
                            print "  > Retrieve results for '{0}': {1}".format(term, t)

                        t = time.time()
                        self.__update_scores(doc_scores, doc_term_scores)
                        t = time.time() - t
                        
                        if self.__verbose:
                            print "  >> Time to update scores: {0}".format(t)
                except NotImplementedError:
                    pass

        t = time.time()
        sorted_results = sorted(doc_scores.iteritems(), key=itemgetter(1), reverse=True)
        t = time.time() - t
        
        if self.__verbose:
            print "  > Time to sort results: {0}".format(t)

        return parse_response(reader=self.reader,
                              fieldname=self.parser.fieldname,
                              analyzer=self.analyzer,
                              fragmenter=self.fragmenter,
                              formatter=self.formatter,
                              query=query,
                              results=sorted_results)

    def __get_doc_term_scores(self, searcher, term):
        """
        Returns a dictionary object comprised of Whoosh document IDs for keys, and scores as values.
        The scores correspond to how relevant the given document is to the given term, provided as parameter query.
        Parameter term should be a unicode string. The Whoosh searcher instance should be provided as parameter searcher.
        """
        doc_term_scores = {}
        term_cache_key = get_cache_key(model_identifier=self.scoring_model_identifier,
                                       fieldname=self.parser.fieldname,
                                       term=term)

        if self.cache.exists(term_cache_key):
            if self.__verbose:
                print "  >> Results are cached"
            return self.cache.get(term_cache_key)  # Easy peasy, return the object from the cache.
        else:
            if self.__verbose:
                print "  >> Results not cached"
            try:
                postings = searcher.postings(self.parser.fieldname, term)

                for i in postings.all_ids():  # THIS IS SLOW, LEIF HAS AN ALGORITHM TO SPEED THIS UP?
                    doc_term_scores[i] = postings.score()
            except TermNotFound:
                pass

            self.cache.store(term_cache_key, doc_term_scores)

        return doc_term_scores

    def __parse_query_terms(self, query):
        """
        Using the stopwords list provided, parses the query object and prepares it for being sent to the engine.
        """

        if not query.top:
            raise QueryParamException(self.name, "Total number of results (query.top) not specified.")

        if query.top < 1:
            raise QueryParamException(self.name, "Page length (query.top) must be at least 1.")

        # Tidy up the querystring. Split it into individual terms so we can process them.
        terms = query.terms
        terms = terms.lower()
        terms = terms.strip()
        terms = terms.split()  # Chop!

        query.terms = ""  # Reset the query's terms string to a blank string - we will rebuild it.

        for term in terms:
            if term not in self.stopwords:
                query.terms = "{0} {1}".format(query.terms, term)

        query.terms = query.terms.strip()
        query.terms = unicode(query.terms)

        if len(query.terms.split()) == 1:
            query.parsed_terms = unicode(query.terms)
        else:
            query.parsed_terms = self.parser.parse(query.terms)

    def __update_scores(self, doc_scores, doc_term_scores):
        """
        Updates the doc_scores dictionary with the rankings from doc_term_scores.
        It's a cumulative function - meaning that doc_scores will have a cumulative total for each document for each term.
        """
        for i in doc_term_scores:
            if i in doc_scores:
                doc_scores[i] = doc_scores[i] + doc_term_scores[i]
            else:
                doc_scores[i] = doc_term_scores[i]

def get_cache_key(model_identifier, fieldname, term):
    """
    Returns a string representing a cache key for the given query term, fieldname and model identifier combination.
    """
    return "{0}:term:{1}:{2}".format(model_identifier, fieldname, term)

def get_page(query, results):
    """
    Given a Query object and a set of results, returns the page number that has been requested.
    Also includes the corresponding set of results for the requested page.
    Note that if the page number if out of acceptable range, the last page of available results is returned.
    If the page number requested is negative, the first page of results is returned.
    """
    page = query.skip
    page_len = query.top

    results = [results[i: i + page_len] for i in range(0, len(results), page_len)]
    total_pages = len(results)

    if len(results) == 0:
        return 1, 0, []

    try:
        if page < 1:  # Valid Python to have negative indices for lists!
            results = results[0]
            page = 1
        else:
            results = results[page - 1]
    except IndexError:
        if page < 1:  # If the requested page is out of range in a negative direction
            results = results[0]
            page = 1
        else:  # If the requested page is out of range in a positive direction
            results = results[len(results) - 1]
            page = len(results)

    return page, total_pages, results

def parse_response(reader, fieldname, analyzer, fragmenter, formatter, query, results, results_are_page=False):
    """
    Returns an ifind Response, given a query and set of results from Whoosh/Redis.
    Takes an ifind Query object and a list of SORTED results for the given query.

    If the page requested (query.skip) is < 0, page 1 is returned.
    If the page requested is greater than the number of available pages, the last page is returned.
    """
    def get_term_list():
        if isinstance(query.parsed_terms, unicode):
            return [query.parsed_terms]

        return [text for term_fieldname, text in query.parsed_terms.all_terms() if fieldname == fieldname]

    t = time.time()
    response = Response(query.terms)
    response.results_total = len(results)


    if results_are_page:
        page = results[0]
        response.total_pages = results[1]
        results = results[2]
    else:
        page, response.total_pages, results = get_page(query, results)

    page_len = query.top

    i = 0

    for result in results:
        i = i + 1
        rank = (page - 1) * page_len + i
        whoosh_docnum = result[0]
        score = result[1]
        stored_data = reader.stored_fields(whoosh_docnum)

        title = stored_data['title']

        if title:
            title = title.strip()
        else:
            title = "Untitled Document"

        url = "/treconomics/{0}/".format(whoosh_docnum)
        trecid = stored_data['docid'].strip()
        source = stored_data['source'].strip()

        summary = highlight(stored_data['content'],
                        get_term_list(),
                        analyzer,
                        fragmenter,
                        formatter)
        summary = "{0}...".format(''.join([unicode_char if ord(unicode_char) < 128 else '' for unicode_char in summary]))

        response.add_result(title=title,
                            url=url,
                            summary=summary,
                            docid=trecid,
                            source=source,
                            rank=rank,
                            whooshid=whoosh_docnum,
                            score=score)

    # The following two lines are for compatibility purposes with the existing codebase.
    # Would really like to take these out.
    setattr(response, 'results_on_page', len(results))
    setattr(response, 'actual_page', page)
    t = time.time() - t
    #print "  > Processing results time: {0}".format(t)
    return response