__author__ = 'leif'
from ifind.seeker.list_reader import ListReader
from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import OrGroup, AndGroup
from whoosh import scoring
from whoosh.qparser import MultifieldParser
from whoosh import highlight
from whoosh import scoring
from whoosh.highlight import highlight, HtmlFormatter, ContextFragmenter

import logging

log = logging.getLogger('ifind.search.engines.whooshtrec')



class Whooshtrec(Engine):
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
            # This creates a static docIndex for ALL instance of WhooshTrec.
            # This will not work if you want indexes from multiple sources.
            # As this currently is not the case, this is a suitable fix.
            if not hasattr(Whooshtrec, 'docIndex'):
                Whooshtrec.docIndex = open_dir(whoosh_index_dir)

            log.debug("Whoosh Document index open: {0}".format(whoosh_index_dir))
            log.debug("Documents in index: {0}".format( self.docIndex.doc_count()))


            self._field = 'content'
            if 'alltext' in self.docIndex.schema:
                self._field = 'alltext'
                log.debug("Using all text field")

            if self.implicit_or:
                self.parser = QueryParser(self._field, self.docIndex.schema, group=OrGroup)
                log.debug("OR Query parser created")
            else:
                self.parser = QueryParser(self._field, self.docIndex.schema, group=AndGroup)
                log.debug("AND Query parser created")


            self.analyzer = self.docIndex.schema[self.parser.fieldname].analyzer
            # for some reason these are actually being applied.
            self.fragmenter = ContextFragmenter(maxchars=100, surround=40)
            self.fragmenter.charlimit = 100
            self.formatter = HtmlFormatter()
            self.set_model(model)

        except:
            msg = "Could not open Whoosh index at: " + whoosh_index_dir
            raise EngineConnectionException(self.name, msg)



    def set_model(self, model, pval=None):
        self.scoring_model = scoring.BM25F(B=0.75)
        engine_name = "BM25F B={0}".format(0.75)
        # Use the BM25F scoring module (B=0.75 is default for Whoosh)

        if model == 0:
            engine_name = "TFIDF"
            self.scoring_model = scoring.TF_IDF()  # Use the TFIDF scoring module
        if model == 2:
            c = 10.0
            if pval:
                c = pval
            engine_name = "PL2 c={0}".format(c)
            self.scoring_model = scoring.PL2(c=c)  # Use PL2
        if model == 1:
            B = 0.75
            if pval:
                B = pval
            engine_name = "BM25F B={0}".format(B)
            self.scoring_model = scoring.BM25F(B=B) # Use BM25

        self.searcher = self.docIndex.searcher(weighting=self.scoring_model)
        log.debug("Engine Created with: {0} retrieval model".format(engine_name))


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



    def __parse_query_terms(self, query):

        if not query.top:
            query.top = 10

        if query.top < 1:
            query.top = 10

        query.terms = query.terms.strip()
        query.terms = unicode(query.terms)
        query.parsed_terms = self.parser.parse(query.terms)


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

        response = None
        page = query.skip + 1
        pagelen = query.top

        log.debug("Query Issued: {0} Page: {1} Page Length: {2}".format(query.parsed_terms, page, pagelen))
        results = self.searcher.search_page(query.parsed_terms, page, pagelen=pagelen)
        results.fragmenter = self.fragmenter
        results.formatter = self.formatter

        setattr(results, 'actual_page', page)

        response = self._parse_whoosh_response(query, results, self._field, self.formatter, self.fragmenter)

        return response

    @staticmethod
    def _parse_whoosh_response(query, results, field, formatter, fragmenter):
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

            if title == '':
                title = "Untitled"

            rank = ((int(results.pagenum)-1) * results.pagelen) + r

            url = "/treconomics/" + str(result.docnum)

            summary = result.highlights(field)
            content = result[field]

            trecid = result["docid"]
            trecid = trecid.strip()

            source = result["source"]

            response.add_result(title=title,
                                url=url,
                                summary=summary,
                                docid=trecid,
                                source=source,
                                rank=rank,
                                whooshid=result.docnum,
                                score=result.score,
                                content=content)

        response.result_total = len(results)

        # Add the total number of pages from the results object as an attribute of our response object.
        # We also add the total number of results shown on the page.
        setattr(response, 'total_pages', results.pagecount)
        setattr(response, 'results_on_page', results.pagelen)
        setattr(response, 'actual_page', results.actual_page)
        return response

