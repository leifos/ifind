from ifind.search.engine import Engine
from ifind.search.response import Response
from ifind.search.exceptions import EngineConnectionException, QueryParamException
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import highlight

class WhooshTrecNews(Engine):
    """
    Whoosh based search engine.

    """
    def __init__(self, whoosh_index_dir='', **kwargs):
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

        try:
            self.docIndex = open_dir( whoosh_index_dir )
            print "Whoosh Document index open: ", whoosh_index_dir
            print "Documents in index: ", self.docIndex.doc_count()
            self.parser = QueryParser("content", self.docIndex.schema)
        except:
            msg= "Could not open Whoosh index at: " + whoosh_index_dir
            raise EngineConnectionException(self.name, msg)



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

        response = None
        try:
            query_terms = self.parser.parse( unicode(query.terms) )
            page = query.skip
            pagelen = query.top

            with self.docIndex.searcher() as searcher:
                invalid_page_no = True

                # If the user specifies a page number that's higher than the number of pages available,
                # this loop looks until a page number is found that contains results and uses that instead.
                # Prevents a horrible AttributeError exception later on!
                while (invalid_page_no):
                    try:
                        results = searcher.search_page(query_terms, page, pagelen)
                        invalid_page_no = False
                        setattr(results, 'actual_page', page)
                    except ValueError:
                        page = page - 1

                results.fragmenter = highlight.ContextFragmenter(maxchars=300, surround=300)
                results.formatter = highlight.HtmlFormatter()
                results.fragmenter.charlimit = 100000
                print "WhooshTRECNewsEngine found: " + str(len(results)) + " results for query: " + query.terms
                print  "Page %d of %d - PageLength of %d" % (results.pagenum, results.pagecount, results.pagelen)
                response = self._parse_whoosh_response(query, results)
        except:
            print "Error in Search Service: Whoosh TREC News search failed"

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
        print "about to parse"
        response = Response(query.terms)
        # Dmax thinks this line is incorrect.
        # I've substituted it with a line just before returning response...
        #response.result_total = results.pagecount
        print "created response"
        r = 0
        for result in results:
            r = r + 1
            title = result["title"]
            if title:
                title = title.strip()
            else:
                title = "Untitled"

            rank = ((int(results.pagenum)-1) * results.pagelen) + r

            url = "/treconomics/" + str(result.docnum) + "?rank="+str(rank)

            summary = result.highlights("content")
            docid = result["docid"]
            docid = docid.strip()
            source = result["source"]

            response.add_result(title=title, url=url, summary=summary, docid=docid, source=source)

            if len(response) == query.top:
                break

        # Dmax has added this line as a replacement for the one commented out above.
        response.result_total = len(results)

        # Add the total number of pages from the results object as an attribute of our response object.
        # We also add the total number of results shown on the page.
        setattr(response, 'total_pages', results.pagecount)
        setattr(response, 'results_on_page', results.pagelen)
        setattr(response, 'actual_page', results.actual_page)
        return response
