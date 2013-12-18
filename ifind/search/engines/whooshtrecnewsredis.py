from operator import itemgetter

from whoosh import scoring
from whoosh.qparser import QueryParser
from whoosh.reading import TermNotFound
from whoosh.index import open_dir, EmptyIndexError
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter

from ifind.search.engine import Engine
from ifind.search.cache import RedisConn
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException

import Queue
from threading import Thread


class WhooshTrecNewsRedis(Engine):
    """
    A revised Whoosh ifind engine.
    Implemented by dmax. Uses a new way of poking the postings file by @leifos, and also some tasty Redis caching.
    """
    def __init__(self, whoosh_index_dir='', use_cache=True, cache_host='localhost', cache_port=6379, **kwargs):
        """
        Constructor for the engine.
        """
        Engine.__init__(self, **kwargs)

        self.whoosh_index_dir = whoosh_index_dir
        if not self.whoosh_index_dir:
            raise EngineConnectionException(self.name, "'whoosh_index_dir=' keyword argument not specified")

        #  Only put PL2 in for now (for more, add the model parameter to the constructor to specify!)
        self.scoring_model_identifier = 1
        self.scoring_model = scoring.PL2(c=10.0)

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

        self.use_cache = use_cache
        if self.use_cache:
            self.cache = RedisConn(host=cache_host, port=cache_port)
            self.cache.connect()

            self.page_cache_forward_look = 40  # How many additional pages to cache when required.
            self.page_cache_when = 4  # When the user is x pages away from the end of the page cache, cache more pages.

            self.page_cache_controller = PageCacheController(cache_host=self.cache.host,
                                                             cache_port=self.cache.port,
                                                             whoosh_index=self.doc_index,
                                                             scoring_model_identifier=self.scoring_model_identifier,
                                                             parser=self.parser,
                                                             analyzer=self.analyzer,
                                                             fragmenter=self.fragmenter,
                                                             formatter=self.formatter,
                                                             cache_forward_look=self.page_cache_forward_look)

    def _search(self, query):
        """
        The concrete method of the Engine's search interface method, search().
        """
        self.__parse_query_terms(query)

        page_cache_key = get_cache_key(model_identifier=self.scoring_model_identifier,
                                       fieldname=self.parser.fieldname,
                                       term=query.terms,
                                       key_type=2,
                                       page=query.skip)

        if self.use_cache and self.cache.exists(page_cache_key):  # If true, we have a page cached - so use this!
            page_results = self.cache.get(page_cache_key)
            highest_cached_page = self.__get_highest_cached_page(query)

            if highest_cached_page - query.skip < self.page_cache_when:  # Do we need to cache some more pages?
                self.__add_to_page_cacher((highest_cached_page + 1), query, page_results)

            return parse_response(reader=self.reader,
                                 fieldname=self.parser.fieldname,
                                 analyzer=self.analyzer,
                                 fragmenter=self.fragmenter,
                                 formatter=self.formatter,
                                 query=query,
                                 results=page_results,
                                 results_are_page=True)
        else:  # No page is cached, so we get the results for that page - and no doubt cache some more pages.
            return self._request(query)

    def _request(self, query):
        """
        Services a request that does not have a page cached.
        Returns an ifind Response object using information from either the Redis cache of Whoosh.
        """
        query_cache_key = get_cache_key(model_identifier=self.scoring_model_identifier,
                                        fieldname=self.parser.fieldname,
                                        term=query.terms,
                                        key_type=1)

        if self.use_cache and self.cache.exists(query_cache_key):
            sorted_results = self.cache.get(query_cache_key)
        else:
            with self.doc_index.searcher(weighting=self.scoring_model) as searcher:
                doc_scores = {}

                if isinstance(query.parsed_terms, unicode):
                    doc_term_scores = self.__get_doc_term_scores(searcher, query.parsed_terms)
                    self.__update_scores(doc_scores, doc_term_scores)
                else:
                    try:
                        for term in query.parsed_terms:
                            doc_term_scores = self.__get_doc_term_scores(searcher, term.text)
                            self.__update_scores(doc_scores, doc_term_scores)
                    except NotImplementedError:
                        pass

            sorted_results = sorted(doc_scores.iteritems(), key=itemgetter(1), reverse=True)

        # This block of code checks if additional page caching is required.
        # This will arise when no pages for the given query are cached, or the user is close to reaching the end of
        # the cached page collection for the given query.
        if self.use_cache:
            self.cache.store(query_cache_key, sorted_results)
            highest_cached_page = self.__get_highest_cached_page(query)

            if highest_cached_page == -1:  # Cache pages from page 1.
                self.__add_to_page_cacher(1, query, sorted_results)
            elif highest_cached_page - query.skip < self.page_cache_when:  # Start caching from page x
                self.__add_to_page_cacher((highest_cached_page + 1), query, sorted_results)

        return parse_response(reader=self.reader,
                              fieldname=self.parser.fieldname,
                              analyzer=self.analyzer,
                              fragmenter=self.fragmenter,
                              formatter=self.formatter,
                              query=query,
                              results=sorted_results)

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
            ignore = ['and', 'or', 'not', 'in', 'the', 'a', 'to']  # Terms to be ignored. These are not included in the tidied querystring.
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
            query.terms = unicode(query.terms)

        if not query.top:
            raise QueryParamException(self.name, "Total number of results (query.top) not specified.")

        if query.top < 1:
            raise QueryParamException(self.name, "Page length (query.top) must be at least 1.")

        tidy_terms(query)

        if len(query.terms.split()) == 1:
            query.parsed_terms = unicode(query.terms)
        else:
            query.parsed_terms = self.parser.parse(query.terms)

        query.terms = query.terms.strip()

    def __get_doc_term_scores(self, searcher, term):
        """
        Returns a dictionary object comprised of Whoosh document IDs for keys, and scores as values.
        The scores correspond to how relevant the given document is to the given term, provided as parameter query.
        Parameter term should be a unicode string. The Whoosh searcher instance should be provided as parameter searcher.
        """
        doc_term_scores = {}
        term_cache_key = get_cache_key(model_identifier=self.scoring_model_identifier,
                                       fieldname=self.parser.fieldname,
                                       term=term,
                                       key_type=0)

        if self.use_cache and self.cache.exists(term_cache_key):
            return self.cache.get(term_cache_key)  # That was simple!
        else:
            try:
                postings = searcher.postings(self.parser.fieldname, term)

                for i in postings.all_ids():
                    doc_term_scores[i] = postings.score()

            except TermNotFound:  # If the term is not found in the inverted index, do nada.
                pass

        if self.use_cache:  # If caching is enabled, cache the results. If we are here, we need to cache them!
            self.cache.store(term_cache_key, doc_term_scores)

        return doc_term_scores

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

    def __get_highest_cached_page(self, query):
        """
        For a given query, returns the highest cached page number.
        For example, if pages 1-10 for a given page are cached, 10 would be returned.

        If no pages are cached for the given query, -1 is returned.
        This method assumes that pages are cached in a linear fashion - there are no gaps where pages are not cached.

        If caching is not enabled, -1 is always returned.
        """
        if not self.use_cache:
            return -1

        wildcard_key = '{0}:page:*:{1}:{2}'.format(self.scoring_model_identifier, self.parser.fieldname, query.terms)
        matching_keys = self.cache.keys(wildcard_key)
        highest_page = -1

        if len(matching_keys) == 0:
            return -1
        else:
            for key in matching_keys:
                key = key.split(':')
                page = int(key[2])

                if page > highest_page:
                    highest_page = page

        return highest_page

    def __add_to_page_cacher(self, start_page, query, results):
        """
        Adds a page to the queue in the caching thread.
        If the thread is not started (i.e. it died because it got old), a new thread is started.
        """
        if not self.cache:
            return

        if not self.page_cache_controller.is_alive():
            try:
                self.page_cache_controller.start()
            except RuntimeError:
                self.page_cache_controller = PageCacheController(cache_host=self.cache.host,
                                                                 cache_port=self.cache.port,
                                                                 whoosh_index=self.doc_index,
                                                                 scoring_model_identifier=self.scoring_model_identifier,
                                                                 parser=self.parser,
                                                                 analyzer=self.analyzer,
                                                                 fragmenter=self.fragmenter,
                                                                 formatter=self.formatter,
                                                                 cache_forward_look=self.page_cache_forward_look)
                self.page_cache_controller.start()

        # We can only be certain here if the page caching thread is alive - so we can now add to its queue.
        self.page_cache_controller.add(start_page, query, results)


class PageCacheController(Thread):
    """
    A class implemented by dmax that acts as a controller for caching individual pages.
    Launched as a separate thread, contains a thread-safe Queue which is populated with page caching jobs to run.
    """
    def __init__(self,
                 cache_host,
                 cache_port,
                 whoosh_index,
                 scoring_model_identifier,
                 parser,
                 analyzer,
                 fragmenter,
                 formatter,
                 cache_forward_look):
        """
        Constructor for an instance of the PageCacheController.
        """
        super(PageCacheController, self).__init__()
        self.__queue = Queue.Queue()
        self.__ticks_before_death = 60  # How many ticks the loop should do before dying off.

        #  Whoosh setup
        self.__reader = whoosh_index.reader()
        self.__analyzer = analyzer
        self.__fragmenter = fragmenter
        self.__formatter = formatter

        #  Cache setup
        self.__cache = RedisConn(host=cache_host, port=cache_port)
        self.__cache.connect()

        # Misc.
        self.__scoring_model_identifier = scoring_model_identifier
        self.__parser = parser
        self.__cache_forward_look = cache_forward_look

    def run(self):
        """
        The main body of the thread's execution; called when the thread is started.
        """
        ticks = 0  # After a certain number of ticks of inactivity, the thread will commit suicide.

        while True:
            if ticks == self.__ticks_before_death:
                print "Page cacher has timed out; dying. Bleugh!"
                break

            try:
                item = self.__queue.get(timeout=1)
                ticks = 0

                start_page = item[0]
                query = item[1]
                results = item[2]

                for curr_page in range(start_page, (start_page + self.__cache_forward_look)):
                    query.skip = curr_page
                    page_results = get_page(query, results)  # Obtain results from the queue, not the cache.
                                                             # Even though the caching starts before this, there is
                                                             # no guarantee that the cache will be ready to service it!

                    if curr_page < page_results[1]:  # If this is not true, the page looked at is greater than
                                                     # the highest page of results; so we do not cache.
                        page_cache_key = get_cache_key(model_identifier=self.__scoring_model_identifier,
                                                       fieldname=self.__parser.fieldname,
                                                       term=query.terms,
                                                       key_type=2,
                                                       page=curr_page)

                        self.__cache.store(page_cache_key, page_results)  # Store the page.
                    else:
                        break

                print "  >>> PAGE_CACHE: Pages {0} to {1} cached for '{2}'".format(start_page, curr_page, query.terms)
            except Queue.Empty:  # This is reached when we try look for an item in the queue and find nothing.
                                 # So we're one tick closer to death...
                ticks = ticks + 1
                continue

    def add(self, start_page, query, results):
        """
        Adds an item to the queue for processing.
        """
        self.__queue.put((start_page, query, results))


def get_cache_key(model_identifier, fieldname, term, key_type=0, page=0):
    """
    Returns a string representing a cache key for the given term/query, term.
    The key returned can be varied by specifying a different value for key_type.
        When key_type == 0, the key returned is for an individual term.
        When key_type == 1, the key returned is for a full result set for a full query.
        When key_type == 2, the key returned is for a given page of results for a full query. Use the page parameter.
    """
    if key_type == 1:
        key_type_identifier = 'query'
    elif key_type == 2:
        key_type_identifier = 'page:{0}'.format(page)
    else:
        key_type_identifier = 'term'

    return "{0}:{1}:{2}:{3}".format(model_identifier, key_type_identifier, fieldname, term)


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