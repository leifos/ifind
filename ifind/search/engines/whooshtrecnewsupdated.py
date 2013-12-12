from operator import itemgetter

from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter

from ifind.search.engine import Engine
from ifind.search.cache import RedisConn
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException

class WhooshTrecNews(Engine):
    """
    An updated Whoosh ifind engine.
    Implementing the new way of poking the postings file by @leifos, and also some tasty Redis caching.
    """

    def __init__(self, whoosh_index_dir='', use_cache=True, **kwargs):
        """
        Constructor for the engine.
        """
        Engine.__init__(self, **kwargs)

        self.whoosh_index_dir = whoosh_index_dir
        if not self.whoosh_index_dir:
            raise EngineConnectionException(self.name, "'whoosh_index_dir=' keyword argument not specified")

        self.use_cache = use_cache
        if self.use_cache:
            self.cache = RedisConn()
            self.cache.connect()

        #  Only put PL2 in for now (for more, add the model parameter to the constructor to specify!)
        self.scoring_model_identifier = 1
        self.scoring_model = scoring.PL2(c=10.0)

        try:
            self.doc_index = open_dir(self.whoosh_index_dir)
            self.reader = self.doc_index.reader()

            self.parser = QueryParser('content', self.doc_index.schema)  # By default, we use AND grouping.
                                                                         # Use the grouping parameter and specify whoosh.qparser.OrGroup, AndGroup...

            #  Objects required for document snippet generation
            self.analyzer = self.doc_index.schema[self.parser.fieldname].analyzer
            self.fragmenter = ContextFragmenter(maxchars=200, surround=40)
            self.formatter = HtmlFormatter()
        except:
            message = "Could not open Whoosh index at '{0}'".format(self.whoosh_index_dir)
            raise EngineConnectionException(self.name, message)

    def _search(self, query):
        """
        The concrete method of the Engine's interface method, search().
        """
        if not query.top:
            raise QueryParamException(self.name, "Total number of results (query.top) not specified.")

        if query.top < 1:
            raise QueryParamException(self.name, "Page length (query.top) must be at least 1.")

        query.terms = query.terms.strip()
        return self._request(query)

    def _request(self, query):
        """
        Returns a response from either the Redis cache or Whoosh (if results are not cached).
        """
        self.__parse_query_terms(query)  # Strips unwanted terms, prepares parsed query object
        cache_key = self.__get_cache_key(unicode(query), is_term=False)  # Cache key for the query

        if self.use_cache and self.cache.exists(cache_key):
            sorted_results = self.cache.get(cache_key)
        else:
            with self.doc_index.searcher(weighting=self.scoring_model) as searcher:
                doc_scores = {}

                if isinstance(query.parsed_terms, unicode):
                    doc_term_scores = self.__get_doc_term_scores(searcher, query.parsed_terms)
                    self.__update_scores(doc_scores, doc_term_scores)
                else:
                    for term in query.parsed_terms:
                        doc_term_scores = self.__get_doc_term_scores(searcher, term.text)
                        self.__update_scores(doc_scores, doc_term_scores)

            sorted_results = sorted(doc_scores.iteritems(), key=itemgetter(1), reverse=True)

            if self.use_cache:
                self.cache.store(cache_key, sorted_results)

        return self.__parse_response(query, sorted_results)

    def __update_scores(self, doc_scores, doc_term_scores):
        """
        Updates the doc_scores dictionary with the rankings from doc_term_scores.
        The end result is doc_scores will have a cumulative total for each document for each term.
        """
        for i in doc_term_scores:
            if i in doc_scores:
                doc_scores[i] = doc_scores[i] + doc_term_scores[i]
            else:
                doc_scores[i] = doc_term_scores[i]

    def __get_doc_term_scores(self, searcher, term):
        """
        Returns a dictionary object comprised of Whoosh document IDs for keys, and scores as values.
        The scores correspond to how relevant the given document is to the given term, provided as parameter query.
        Parameter term should be a unicode string. The Whoosh searcher instance should be provided as parameter searcher.
        """
        doc_term_scores = {}
        cache_key = self.__get_cache_key(term)  # Cache key for individual terms

        if self.use_cache and self.cache.exists(cache_key):
            return self.cache.get(cache_key)  # That was simple!
        else:
            try:
                postings = searcher.postings(self.parser.fieldname, term)

                for i in postings.all_ids():
                    doc_term_scores[i] = postings.score()

            except TermNotFound:  # If the term is not found in the inverted index, do nada.
                pass

        if self.use_cache:  # If caching is enabled, cache the results. If we are here, we need to cache them!
            self.cache.store(cache_key, doc_term_scores)

        return doc_term_scores

    def __parse_query_terms(self, query):
        """
        Parses the query terms provided.
        Creates a Whoosh compound query type in query.parsed_terms if more than one term is specified.
        If only a single term is specified, a unicode string instance is used instead.
        """
        def tidy_terms(self):
            """
            Nested function to remove unwanted query terms (e.g. AND, OR, NOT) from the query.
            Also tidies the query by removing redundant whitespace and newline characters.
            """
            ignore = ['and', 'or', 'not']  # Terms to be ignored. These are not included in the tidied querystring.
                                           # Ensure the terms in the list are all lowercase!

            terms = query.terms
            terms = terms.lower()
            terms = terms.strip()
            terms = terms.split()

            query.terms = ""

            for term in terms:
                if term not in ignore:
                    query.terms = "{0} {1}".format(query.terms, term)

            query.terms = query.terms.strip()

        tidy_terms(query)

        if len(query.terms.split()) == 1:
            query.parsed_terms = unicode(query.terms)
        else:
            query.parsed_terms = self.parser.parse(query.terms)

    def __get_term_list(self, query):
        """
        Returns a list of unicode strings, each representing a term provided in the user's query.
        """
        if isinstance(query.parsed_terms, unicode):
            return [query.parsed_terms]

        return [text for fieldname, text in query.parsed_terms.all_terms() if fieldname == self.parser.fieldname]

    def __get_cache_key(self, term, is_term=True):
        """
        Returns a string representing the cache key for the given term.
        """
        if is_term:
            type_identifier = 'term'
        else:
            type_identifier = 'query'

        return "{0}:{1}:{2}:{3}".format(self.scoring_model_identifier, type_identifier, self.parser.fieldname, term)

    def __get_page(self, query, results):
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

    def __parse_response(self, query, results):
        """
        Returns an ifind Response, given a query and set of results from Whoosh/Redis.
        Takes an ifind Query object and a list of SORTED results for the given query.

        If the page requested (query.skip) is < 0
        """
        response = Response(query.terms)
        response.result_total = len(results)

        page, response.total_pages, results = self.__get_page(query, results)
        page_len = query.top

        i = 0

        for result in results:
            i = i + 1
            rank = (page - 1) * page_len + i
            whoosh_docnum = result[0]
            score = result[1]
            stored_data = self.reader.stored_fields(whoosh_docnum)

            title = stored_data['title']

            if title:
                title = title.strip()
            else:
                title = "Untitled Document"

            url = "/treconomics/{0}/".format(whoosh_docnum)
            trecid = stored_data['docid'].strip()
            source = stored_data['source'].strip()

            summary = highlight(stored_data['content'],
                            self.__get_term_list(query),
                            self.analyzer,
                            self.fragmenter,
                            self.formatter)
            summary = "{0}...".format(summary)

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

        return response