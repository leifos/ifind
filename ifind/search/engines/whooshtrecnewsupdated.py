from operator import itemgetter

from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound

from ifind.search.engine import Engine
from ifind.search.cache import RedisConn
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
            self.parser = QueryParser('content', self.doc_index.schema)  # By default, we use AND grouping.
                                                                         # Use the grouping parameter and specify whoosh.qparser.OrGroup, AndGroup...
        except:
            message = "Could not open Whoosh index at '{0}'".format(self.whoosh_index_dir)
            raise EngineConnectionException(self.name, message)

    def _search(self, query):
        """
        The concrete method of the Engine's interface method, search().
        """
        if not query.top:
            raise QueryParamException(self.name, "Total number of results (query.top) not specified!")

        query.terms = query.terms.strip()
        return self._request(query)

    def _request(self, query):
        """
        Returns a response from either the Redis cache or Whoosh (if results are not cached).
        """
        self.__parse_query_terms(query)  # Strips unwanted terms, prepares parsed query object

        with self.doc_index.searcher(weighting=self.scoring_model) as searcher:
            doc_scores = {}

            if isinstance(query.parsed_terms, unicode):
                doc_term_scores = self.__get_doc_term_scores(searcher, query.parsed_terms)
                self.__update_scores(doc_scores, doc_term_scores)
            else:
                for term in query.parsed_terms:
                    doc_term_scores = self.__get_doc_term_scores(searcher, term.text)
                    self.__update_scores(doc_scores, doc_term_scores)

        results = sorted(doc_scores.iteritems(), key=itemgetter(1), reverse=True)

        # TODO: get results for a particular page (using query.top and query.skip)
        # TODO: turn the results list into a fully fledged ifind Response object in __parse_response
        # TODO: tidy up the use of page/actual_page in the rest of the codebase
        # TODO: additional todos in the todo list on my desk

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
        cache_key = self.__get_cache_key(term)

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

        if len(query.terms) == 1:
            query.parsed_terms = unicode(query.terms)

        query.parsed_terms = self.parser.parse(query.terms)

    def __get_cache_key(self, term):
        """
        Returns a string representing the cache key for the given term.
        """
        return "{0}:{1}:{2}".format(self.scoring_model_identifier, self.parser.fieldname, term)

    @staticmethod
    def __parse_response(query, results):
        """
        Returns an ifind Response, given a query and set of results from Whoosh/Redis.
        """
        pass