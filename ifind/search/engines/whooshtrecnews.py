from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.seeker.list_reader import ListReader
from ifind.search.exceptions import EngineConnectionException, QueryParamException
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import highlight
from whoosh import scoring
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter


FORWARD_LOOK_PAGES = 10  # How many pages do we look forward to cache?

class WhooshTrecNews(Engine):
    """
    Whoosh based search engine.

    """
    def __init__(self, whoosh_index_dir='', stopwords_file='', model=1, implicit_or=False, **kwargs):
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


        self.stopwords_file = stopwords_file
        if self.stopwords_file:
            self.stopwords = ListReader(self.stopwords_file)  # Open the stopwords file, read into a ListReader



        self.implicit_or=implicit_or

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

            self.analyzer = self.docIndex.schema[self.parser.fieldname].analyzer
            self.fragmenter = ContextFragmenter(maxchars=200, surround=40)
            self.fragmenter.charlimit = 10000
            self.formatter = HtmlFormatter()
            self.set_model(model)

        except:
            msg = "Could not open Whoosh index at: " + whoosh_index_dir
            raise EngineConnectionException(self.name, msg)



    def set_model(self, model, pval=None):
        self.scoring_model = scoring.BM25F(B=0.75)  # Use the BM25F scoring module (B=0.75 is default for Whoosh)
        if model == 0:
            self.scoring_model = scoring.TF_IDF()  # Use the TFIDF scoring module
        if model == 2:
            c = 10.0
            if pval:
                c = pval
            self.scoring_model = scoring.PL2()  # Use PL2 with default values
        if model == 1:
            B = 0.75
            if pval:
                B = pval
            self.scoring_model = scoring.BM25F(B=B) # BM25

        print self.scoring_model
        self.searcher = self.docIndex.searcher(weighting=self.scoring_model)



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
        self.__parse_query_terms(query)

        return self._request(query)

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

        page = query.skip
        pagelen = query.top
        response = None
        print query.parsed_terms
        #results = self.searcher.search(query.parsed_terms, page, pagelen=pagelen,limit=10)
        results = self.searcher.search_page(query.parsed_terms, page, pagelen=pagelen)
        results.fragmenter = self.fragmenter
        results.formatter = self.formatter

        setattr(results, 'actual_page', page)

        response = self._parse_whoosh_response(query, results)

        return response

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

        response.result_total = len(results)

        # Add the total number of pages from the results object as an attribute of our response object.
        # We also add the total number of results shown on the page.
        setattr(response, 'total_pages', results.pagecount)
        setattr(response, 'results_on_page', results.pagelen)
        setattr(response, 'actual_page', results.actual_page)
        return response

    def __parse_query_terms(self, query):
        """
        Using the stopwords list provided, parses the query object and prepares it for being sent to the engine.
        """

        if not query.top:
            query.top = 10

        if query.top < 1:
            query.top = 10

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

        if self.implicit_or:
            query_terms = query.terms.split(' ')
            query.terms = WhooshTrecNews.build_query_parts(query_terms, 'OR')


        #if len(query.terms.split()) == 1:
        #    query.parsed_terms = unicode(query.terms)
        #else:
        query.parsed_terms = self.parser.parse(query.terms)