__author__ = 'leif'
from ifind.search.engine import Engine
from ifind.search.response import Response


class TrecDummy(Engine):
    """
    This search engine makes no internet requests
    It serves up pre-programmed responses for testing
    For all queries, it returns the same response which is:
        a list of results with title: x, url: www.x.com, description: x x x
        where x is in ['one','two','three',...,'ten']
    """

    def __init__(self, input_file, **kwargs):
        Engine.__init__(self, **kwargs)
        self.__input_file = input_file
        
    def _create_response(self, query):
        response = Response(query.terms)
        
        f = open(self.__input_file)  # Open the results file
        
        self.query_results = {}
        
        for line in f:
            line = line.strip()
            line = line.split(',')
            
            query_terms = line[0]
            results = line[1:]
            
            self.query_results[query_terms] = results
        
        f.close()
        
        if query.terms in self.query_results:
            i = 0
            
            for x in self.query_results[query.terms]:
                i += 1
                
                response.add_result(title=x,
                                    url='http://wwww.{0}.com'.format(x),
                                    summary='{0} {0}'.format(x),
                                    rank=i,
                                    whooshid=x,
                                    docid=x)
        else:
            print "SEARCH ENGINE WARNING: TrecDummy did not match query to resultset!"
        
        return response
        
    def search(self, query):
        """Dummy search, returns the same set of results, regardless of query

        Parameters:

        * query (ifind.search.query.Query)

        Returns:

            * ifind.search.response.Response

        Raises:

            * urllib2.URLError
            * API key error

        """
        response = self._create_response(query)

        return response
