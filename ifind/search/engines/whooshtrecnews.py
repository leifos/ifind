from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import highlight
from whoosh import scoring
import redis
import pickle

FORWARD_LOOK_PAGES = 10  # How many pages do we look forward to cache?

class WhooshTrecNews(Engine):
    """
    Whoosh based search engine.

    """
    def __init__(self, whoosh_index_dir='', model=1, implicit_or=False, interleave=False, use_cache=True, **kwargs):
        """
        Whoosh engine constructor.

        Kwargs:
            See Engine.

        Usage:
            See EngineFactory.

        """
        Engine.__init__(self, **kwargs)
        self.whoosh_index_dir = whoosh_index_dir
        if not self.whoosh_index_dir:
            raise EngineConnectionException(self.name, "'whoosh_index_dir=' keyword argument not specified")

        self.use_cache = use_cache
        self.cache = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.interleave = interleave  # Should we interleave results, and how often?
        self.implicit_or = implicit_or  # Do we implicitly join terms together with ORs?
        self.scoring_model = scoring.BM25F(B=0.25)  # Use the BM25F scoring module by default, where b=0.25

        if model == 0:
            self.scoring_model = scoring.TF_IDF()  # Use the TFIDF scoring module
        if model == 2:
            self.scoring_model = scoring.PL2()  # Use PL2 with default values

        try:
            #self.docIndex = open_dir(whoosh_index_dir)

            # This creates a static docIndex for ALL instance of WhooshTrecNews.
            # This will not work if you want indexes from multiple sources.
            # As this currently is not the case, this is a suitable fix.
            if not hasattr(WhooshTrecNews, 'docIndex'):
                WhooshTrecNews.docIndex = open_dir(whoosh_index_dir)

            print "Whoosh Document index open: ", whoosh_index_dir
            print "Documents in index: ", self.docIndex.doc_count()
            self.parser = QueryParser("content", self.docIndex.schema)
        except:
            msg = "Could not open Whoosh index at: " + whoosh_index_dir
            raise EngineConnectionException(self.name, msg)

    @staticmethod
    def build_query_parts(term_list, operator):
        return_query = ''

        for term in term_list:
            if term:
                if return_query:
                    return_query += ' ' + operator + ' ' + term
                else:
                    return_query = term

        return return_query

    def _search(self, query):
        """
        Concrete method of Engine's interface method 'search'.
        Performs a search and retrieves the results as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Query Kwargs:
            top (int): specifies maximum amount of results to return, no minimum guarantee

        Returns:
            ifind Response: object encapulsating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        if not query.top:
            raise QueryParamException(self.name, "Total result amount (query.top) not specified")

        if self.implicit_or:
            query_terms = query.terms.split(' ')
            query.terms = WhooshTrecNews.build_query_parts(query_terms, 'OR')

        query.terms = query.terms.strip()

        return self._request(query)

    def get_cache_key(self, page_no, query_terms):
        """
        Returns a string representing the state of a given instance of the WhooshTrecNews class.
        Implemented for a way of determining a unique identifiable key for caching search results.
        Returns a string in the format {0}**{1}, where
            {0}: An identifier for the model used (0=TFIDF, 1=BM25F, 2=PL2)
            {1}: 1 for use of implicit ORing, 0 for no use
        """
        model_identifier = 1

        if isinstance(self.scoring_model, scoring.TF_IDF):
            model_identifier = 0
        if isinstance(self.scoring_model, scoring.PL2):
            model_identifier = 2

        if self.implicit_or:
            implicit_or_identifier = 1
        else:
            implicit_or_identifier = 0

        if not self.interleave:
            interleave_identifier = 0
        else:
            interleave_identifier = self.interleave

        no_space_terms = query_terms.replace(' ', '_')
        return "search:{0}:{1}:{2}:{3}:'{4}'".format(model_identifier, implicit_or_identifier, interleave_identifier, page_no, no_space_terms)

    def __get__results_length(self, results):
        """
        Returns the number of hits in a results object.
        For some reason, this is incorrectly reported when calling len(results).
        """
        counter = 0

        for hit in results:
            counter = counter + 1

        return counter

    def __split_results(self, query, results):
        """
        Splits results.
        """
        results_len = self.__get__results_length(results)
        return [results[i:i + query.top] for i in range(0, results_len, query.top)]

    def __interleave_results(self, results):
        """
        Interleaves results.
        """
        if not self.interleave:
            return results  # Do nothing, interleave value not set.

        split_lists = [[[], 0] for x in xrange(self.interleave)]

        for i in range(0, len(results)):
            split_lists[i % self.interleave][0].append(results[i])

        interleaved = []

        for i in range(0, self.interleave):
            interleaved += split_lists[i][0]

        return interleaved

    def get_highest_cached_page(self, query_terms):
        """
        Returns an integer representing the highest page number that has been cached for the given query terms and engine.
        This assumes that all pages up to that point have been cached - and no pages afterwards have been, either.
        That's the way it should be - people can't jump in at page 10 of results, they sequentially move through.

        ALSO ASSUMES THAT PAGE NUMBER IS THE PENULTIMATE VALUE, BEFORE THE QUERY TERMS.

        Returns -1 if no pages have been cached for the given engine and query terms.
        """
        page_identifier = -100
        cache_key = self.get_cache_key(-100, query_terms)
        cache_key = cache_key.split(':')
        generic_cache_key = ''

        for phrase in cache_key:
            if phrase == str(page_identifier):
                generic_cache_key = generic_cache_key + '*'
            else:
                generic_cache_key = generic_cache_key + phrase + ':'

        generic_cache_key = generic_cache_key[:-1]
        keys = self.cache.keys(generic_cache_key)

        highest_page = -1

        for key in keys:
            key = key.split(':')
            pageno = int(key[4])

            if pageno > highest_page:
                highest_page = pageno

        return highest_page

    def _request(self, query):
        """
        Issues a single request to Whoosh Index and returns the result as
        an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Raises:
            EngineException

        Usage:
            Private method.

        """
        #try:
        query_terms = self.parser.parse(unicode(query.terms))
        page = query.skip
        pagelen = query.top

        with self.docIndex.searcher(weighting=self.scoring_model) as searcher:
            #invalid_page_no = True

            cache_key = self.get_cache_key(page, query.terms)

            if self.use_cache and self.cache.exists(cache_key):
                return_response = self.cache.get(cache_key)
                return_response = pickle.loads(return_response)

                print "WhooshTRECNewsEngine found CACHED results"
            else:
                results = searcher.search_page(query_terms, page, pagelen=(FORWARD_LOOK_PAGES * pagelen))
                results.fragmenter = highlight.ContextFragmenter(maxchars=3000, surround=3000)
                results.formatter = highlight.HtmlFormatter()
                results.fragmenter.charlimit = 100000
                setattr(results, 'actual_page', page)

                ifind_response = self._parse_whoosh_response(query, results)
                interleaved_results = self.__interleave_results(ifind_response.results)
                split_results = self.__split_results(query, interleaved_results)

                page_counter = page
                return_response = Response(query.terms)

                for page_list in split_results:
                    response = Response(query.terms)

                    for hit in page_list:
                        response.add_result_object(hit)

                    response.pagenum = results.pagenum
                    response.total_pages = results.pagecount
                    response.results_on_page = len(page_list)
                    response.actual_page = page_counter

                    loop_cache_key = self.get_cache_key(page_counter, query.terms)

                    if self.use_cache and not self.cache.exists(loop_cache_key):
                        response_str = pickle.dumps(response)
                        self.cache.set(loop_cache_key, response_str)

                    if page_counter == page:
                        return_response = response
                        print "WhooshTRECNewsEngine found: " + str(len(results)) + " results for query: " + query.terms
                        print "Page %d of %d - PageLength of %d" % (results.pagenum, results.pagecount, results.pagelen)

                    page_counter = page_counter + 1


            """
            # If the user specifies a page number that's higher than the number of pages available,
            # this loop looks until a page number is found that contains results and uses that instead.
            # Prevents a horrible AttributeError exception later on!
            while invalid_page_no:
                try:
                    results = searcher.search_page(query_terms, page, pagelen)
                    invalid_page_no = False
                    setattr(results, 'actual_page', page)
                except ValueError:
                    page -= page

            results.fragmenter = highlight.ContextFragmenter(maxchars=300, surround=300)
            results.formatter = highlight.HtmlFormatter()
            results.fragmenter.charlimit = 100000
            print "WhooshTRECNewsEngine found: " + str(len(results)) + " results for query: " + query.terms
            print "Page %d of %d - PageLength of %d" % (results.pagenum, results.pagecount, results.pagelen)
            response = self._parse_whoosh_response(query, results)
            """
        #except:
        #    print "Error in Search Service: Whoosh TREC News search failed"

        return return_response

    @staticmethod
    def _parse_whoosh_response(query, results):
        """
        Parses Whoosh's response and returns as an ifind Response.

        Args:
            query (ifind Query): object encapsulating details of a search query.
            results : requests library response object containing search results.

        Returns:
            ifind Response: object encapsulating a search request's results.

        Usage:
            Private method.

        """

        response = Response(query.terms)
        # Dmax thinks this line is incorrect.
        # I've substituted it with a line just before returning the response...
        #response.result_total = results.pagecount

        r = 0
        for result in results:
            r = r + 1
            title = result["title"]
            if title:
                title = title.strip()
            else:
                title = "Untitled"

            rank = ((int(results.pagenum)-1) * results.pagelen) + r

            url = "/treconomics/" + str(result.docnum)

            summary = result.highlights("content")
            trecid = result["docid"]
            trecid = trecid.strip()

            #score = result["score"]
            source = result["source"]

            response.add_result(title=title,
                                url=url,
                                summary=summary,
                                docid=trecid,
                                source=source,
                                rank=rank,
                                whooshid=result.docnum,
                                score=result.score)

            #if len(response) == query.top:
            #    break

        # Dmax has added this line as a replacement for the one commented out above.
        response.result_total = len(results)

        # Add the total number of pages from the results object as an attribute of our response object.
        # We also add the total number of results shown on the page.
        setattr(response, 'total_pages', results.pagecount)
        setattr(response, 'results_on_page', results.pagelen)
        setattr(response, 'actual_page', results.actual_page)
        return response
